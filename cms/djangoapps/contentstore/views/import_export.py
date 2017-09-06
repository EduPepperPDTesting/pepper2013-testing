"""
These views handle all actions in Studio related to import and exporting of
courses
"""
import logging
import os
import tarfile
import shutil
import re
from tempfile import mkdtemp
from path import path
from contextlib import contextmanager

from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django_future.csrf import ensure_csrf_cookie
from django.core.urlresolvers import reverse
from django.core.servers.basehttp import FileWrapper
from django.core.files.temp import NamedTemporaryFile
from django.views.decorators.http import require_http_methods

from mitxmako.shortcuts import render_to_response
from auth.authz import create_all_course_groups

from xmodule.modulestore.xml_importer import import_from_xml
from xmodule.contentstore.django import contentstore
from xmodule.modulestore.xml_exporter import export_to_xml
from xmodule.modulestore.django import modulestore
from xmodule.modulestore import Location
from xmodule.exceptions import SerializationError

from .access import get_location_and_verify_access
from util.json_request import JsonResponse
import time
from pymongo import MongoClient
import json
from sshtunnel import SSHTunnelForwarder
from xmodule.course_module import CourseDescriptor
import MySQLdb
from django.contrib.auth.models import User
from collections import OrderedDict
from django import db
from django.db import connection
from multiprocessing import Process, Queue, Pipe
from async_task.models import AsyncTask
from datetime import datetime, timedelta
from pytz import UTC



__all__ = ['import_course', 'generate_export_course', 'export_course', 'sync_course', 'dest_course_exists']

log = logging.getLogger(__name__)


# Regex to capture Content-Range header ranges.
CONTENT_RE = re.compile(r"(?P<start>\d{1,11})-(?P<stop>\d{1,11})/(?P<end>\d{1,11})")


@ensure_csrf_cookie
@require_http_methods(("GET", "POST", "PUT"))
@login_required
def import_course(request, org, course, name):
    """
    This method will handle a POST request to upload and import a .tar.gz file
    into a specified course
    """
    location = get_location_and_verify_access(request, org, course, name)

    @contextmanager
    def wfile(filename, dirname):
        """
        A with-context that creates `filename` on entry and removes it on exit.
        `filename` is truncted on creation. Additionally removes dirname on
        exit.
        """
        open("file", "w").close()
        try:
            yield filename
        finally:
            os.remove(filename)
            shutil.rmtree(dirname)

    if request.method == 'POST':

        data_root = path(settings.GITHUB_REPO_ROOT)
        course_subdir = "{0}-{1}-{2}".format(org, course, name)
        course_dir = data_root / course_subdir

        filename = request.FILES['course-data'].name
        if not filename.endswith('.tar.gz'):
            return JsonResponse(
                {'ErrMsg': 'We only support uploading a .tar.gz file.'},
                status=415
            )
        temp_filepath = course_dir / filename

        if not course_dir.isdir():
            os.mkdir(course_dir)

        logging.debug('importing course to {0}'.format(temp_filepath))

        # Get upload chunks byte ranges
        try:
            matches = CONTENT_RE.search(request.META["HTTP_CONTENT_RANGE"])
            content_range = matches.groupdict()
        except KeyError:    # Single chunk 
            # no Content-Range header, so make one that will work
            content_range = {'start': 0, 'stop': 1, 'end': 2}

        # stream out the uploaded files in chunks to disk
        if int(content_range['start']) == 0:
            mode = "wb+"
        else:
            mode = "ab+"
            size = os.path.getsize(temp_filepath)
            # Check to make sure we haven't missed a chunk
            # This shouldn't happen, even if different instances are handling
            # the same session, but it's always better to catch errors earlier.
            if size < int(content_range['start']):
                log.warning(
                    "Reported range %s does not match size downloaded so far %s",
                    content_range['start'],
                    size
                )
                return JsonResponse(
                    {'ErrMsg': 'File upload corrupted. Please try again'},
                    status=409
                )
            # The last request sometimes comes twice. This happens because
            # nginx sends a 499 error code when the response takes too long.
            elif size > int(content_range['stop']) and size == int(content_range['end']):
                return JsonResponse({'ImportStatus': 1})

        with open(temp_filepath, mode) as temp_file:
            for chunk in request.FILES['course-data'].chunks():
                temp_file.write(chunk)

        size = os.path.getsize(temp_filepath)

        if int(content_range['stop']) != int(content_range['end']) - 1:
            # More chunks coming
            return JsonResponse({
                "files": [{
                    "name": filename,
                    "size": size,
                    "deleteUrl": "",
                    "deleteType": "",
                    "url": reverse('import_course', kwargs={
                        'org': location.org,
                        'course': location.course,
                        'name': location.name
                    }),
                    "thumbnailUrl": ""
                }]
            })

        else:   # This was the last chunk.

            # 'Lock' with status info.
            status_file = data_root / (course + filename + ".lock")

            # Do everything from now on in a with-context, to be sure we've
            # properly cleaned up.
            with wfile(status_file, course_dir):

                with open(status_file, 'w+') as sf:
                    sf.write("Extracting")

                tar_file = tarfile.open(temp_filepath)
                tar_file.extractall(course_dir + '/')

                with open(status_file, 'w+') as sf:
                    sf.write("Verifying")

                # find the 'course.xml' file
                dirpath = None

                def get_all_files(directory):
                    """
                    For each file in the directory, yield a 2-tuple of (file-name,
                    directory-path)
                    """
                    for dirpath, _dirnames, filenames in os.walk(directory):
                        for filename in filenames:
                            yield (filename, dirpath)

                def get_dir_for_fname(directory, filename):
                    """
                    Returns the dirpath for the first file found in the directory
                    with the given name.  If there is no file in the directory with
                    the specified name, return None.
                    """
                    for fname, dirpath in get_all_files(directory):
                        if fname == filename:
                            return dirpath
                    return None

                fname = "course.xml"

                dirpath = get_dir_for_fname(course_dir, fname)

                if not dirpath:
                    return JsonResponse(
                        {'ErrMsg': 'Could not find the course.xml file in the package.'},
                        status=415
                    )

                logging.debug('found course.xml at {0}'.format(dirpath))

                if dirpath != course_dir:
                    for fname in os.listdir(dirpath):
                        shutil.move(dirpath / fname, course_dir)

                _module_store, course_items = import_from_xml(
                    modulestore('direct'),
                    settings.GITHUB_REPO_ROOT,
                    [course_subdir],
                    load_error_modules=False,
                    static_content_store=contentstore(),
                    target_location_namespace=location,
                    draft_store=modulestore()
                )

                logging.debug('new course at {0}'.format(course_items[0].location))

                with open(status_file, 'w') as sf:
                    sf.write("Updating course")

                create_all_course_groups(request.user, course_items[0].location)
                logging.debug('created all course groups at {0}'.format(course_items[0].location))

            return JsonResponse({'Status': 'OK'})
    else:
        course_module = modulestore().get_item(location)

        return render_to_response('import.html', {
            'context_course': course_module,
            'successful_import_redirect_url': reverse('course_index', kwargs={
                'org': location.org,
                'course': location.course,
                'name': location.name,
            })
        })


@ensure_csrf_cookie
@login_required
def generate_export_course(request, org, course, name, filename):
    """
    This method will serialize out a course to a .tar.gz file which contains a
    XML-based representation of the course
    """
    location = get_location_and_verify_access(request, org, course, name)
    course_module = modulestore().get_instance(location.course_id, location)
    loc = Location(location)
    export_file = NamedTemporaryFile(prefix=filename + '.', suffix=".tar.gz")
    root_dir = path(mkdtemp())
    try:
        export_to_xml(modulestore('direct'), contentstore(), loc, root_dir, name, modulestore())
    except SerializationError, e:
        logging.exception('There was an error exporting course {0}. {1}'.format(course_module.location, unicode(e)))
        unit = None
        failed_item = None
        parent = None
        try:
            failed_item = modulestore().get_instance(course_module.location.course_id, e.location)
            parent_locs = modulestore().get_parent_locations(failed_item.location, course_module.location.course_id)

            if len(parent_locs) > 0:
                parent = modulestore().get_item(parent_locs[0])
                if parent.location.category == 'vertical':
                    unit = parent
        except:
            # if we have a nested exception, then we'll show the more generic error message
            pass

        return render_to_response('export.html', {
            'context_course': course_module,
            'successful_import_redirect_url': '',
            'in_err': True,
            'raw_err_msg': str(e),
            'failed_module': failed_item,
            'unit': unit,
            'edit_unit_url': reverse('edit_unit', kwargs={
                'location': parent.location
            }) if parent else '',
            'course_home_url': reverse('course_index', kwargs={
                'org': org,
                'course': course,
                'name': name
            })
        })
    except Exception, e:
        logging.exception('There was an error exporting course {0}. {1}'.format(course_module.location, unicode(e)))
        return render_to_response('export.html', {
            'context_course': course_module,
            'successful_import_redirect_url': '',
            'in_err': True,
            'unit': None,
            'raw_err_msg': str(e),
            'course_home_url': reverse('course_index', kwargs={
                'org': org,
                'course': course,
                'name': name
            })
        })

    logging.debug('tar file being generated at {0}'.format(export_file.name))
    fname=export_file.name.split(".")
    file_name=fname[0]+'.'+time.strftime('%Y%m%d%H%I%M%S',time.localtime(time.time()))+'.tar.gz'
    os.rename(export_file.name,file_name)
    tar_file = tarfile.open(name=file_name, mode='w:gz')
    tar_file.add(root_dir / name, arcname=name)
    tar_file.close()

    # remove temp dir
    shutil.rmtree(root_dir / name)

    wrapper = FileWrapper(export_file)
    response = HttpResponse(wrapper, content_type='application/x-tgz')
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(file_name)
    response['Content-Length'] = os.path.getsize(file_name)
    return response


@ensure_csrf_cookie
@login_required
def export_course(request, org, course, name):
    """
    This method serves up the 'Export Course' page
    """
    location = get_location_and_verify_access(request, org, course, name)

    course_module = modulestore().get_item(location)

    return render_to_response('export.html', {
        'context_course': course_module,
        'successful_import_redirect_url': ''
    })


def remove_course(id_org, id_course, conn=None):
    if conn is None:
        opt = settings.MODULESTORE['default']['OPTIONS']
        conn = MongoClient(opt['host'], opt['port'])

    def remove_docs(db_name, collection_name, cond):
        db = conn[db_name]
        collection = db[collection_name]
        collection.remove(cond)

    remove_docs("xmodule", "modulestore", {"_id.org": id_org, "_id.course": id_course})
    remove_docs("xcontent", "fs.files", {"_id.org": id_org, "_id.course": id_course})
    remove_docs("xcontent", "fs.chunks", {"files_id.org": id_org, "files_id.course": id_course})


def copy_course(task, id_org, id_course, _from, _to):
    def copy_docs(db_name, collection_name, cond):
        from_db = _from[db_name]
        to_db = _to[db_name]

        from_collection = from_db[collection_name]
        to_collection = to_db[collection_name]

        # to_collection.remove(cond)
        cursor = from_collection.find(cond)
        
        num_done = 0.0
        num_total = cursor.count()
        
        for doc in cursor:
            d = doc['_id']
            
            if "__getitem__" in dir(d) and (d.get("category") == "asset" or d.get("category") == "thumbnail"):
                doc['_id'] = OrderedDict([("category", d['category']),
                                          ("name", d['name']),
                                          ("course", d['course']),
                                          ("tag", d['tag']),
                                          ("org", d['org']),
                                          ("revision", d['revision'])])
            elif "__getitem__" in dir(d):
                doc['_id'] = OrderedDict([("tag", d['tag']),
                                          ("org", d['org']),
                                          ("course", d['course']),
                                          ("category", d['category']),
                                          ("name", d['name']),
                                          ("revision", d['revision'])])

            to_collection.save(doc)
            num_done = num_done + 1
            rate = (num_done / num_total if num_total > 0 else 0) * 100
            update_task(task, "progress", "sync course(%s.%s) progress: %0.2f%%" %
                        (db_name, collection_name, rate))

    copy_docs("xmodule", "modulestore", {"_id.org": id_org, "_id.course": id_course})
    copy_docs("xcontent", "fs.files", {"_id.org": id_org, "_id.course": id_course})
    copy_docs("xcontent", "fs.chunks", {"files_id.org": id_org, "files_id.course": id_course})


def postpone(function):
    def decorator(*args, **kwargs):
        p = Process(target=function, args=args, kwargs=kwargs)
        p.daemon = True
        p.start()
    return decorator


def update_task(task, status, message):
    task.update_time = datetime.now(UTC)
    task.status = status
    task.last_message = message
    task.save()
    db.transaction.commit()


@postpone
def do_sync_course(task, org, course, name, d, user):
    """
    Sync Course to Another Server
    """

    # course_location = "i4x://%s/%s/course/%s" % (org, course, name)
    # course_obj = modulestore().get_instance(course_id, CourseDescriptor.id_to_location(course_id))
    try:
        update_task(task, "progress", "grant course permission")
        
        # ** connect dest server
        remote_server = SSHTunnelForwarder(
            d['host'],
            ssh_port=d['ssh_port'],
            ssh_username=d['ssh_username'],
            ssh_password=d['ssh_password'],
            remote_bind_address=('127.0.0.1', d['mysql_port'])
        )
        remote_server.start()
        
        # ** connect mysql on dest server
        remote_mysql = MySQLdb.connect(
            host="127.0.0.1",
            user=d["mysql_username"],
            passwd=d["mysql_password"],
            db=d["mysql_db"],
            port=remote_server.local_bind_port)
        remote_cursor = remote_mysql.cursor(MySQLdb.cursors.DictCursor)

        # ** connect mysql on local server
        mysql_options = settings.DATABASES.get("read")
        
        local_mysql = MySQLdb.connect(
            host=mysql_options["HOST"],
            port=int(mysql_options["PORT"]),
            db=mysql_options["NAME"],
            user=mysql_options["USER"],
            passwd=mysql_options["PASSWORD"],
            charset="utf8")
        local_cursor = local_mysql.cursor(MySQLdb.cursors.DictCursor)

        def get_or_create(table, **kwargs):
            st = []
            for k, v in kwargs.items():
                st.append("%s='%s'" % (k, v))
            remote_cursor.execute("select id from %s where %s;" % (table, " and ".join(st)))
            result = remote_cursor.fetchone()
            if result is None:
                remote_cursor.execute("insert into %s set %s;" % (table, ", ".join(st)))
                return remote_cursor.lastrowid
            else:
                return result["id"]
            
        def get_group_id(org, course, name, role):
            group_name = "%s_%s/%s/%s" % (role, org, course, name)
            return get_or_create("auth_group", name=group_name)
 
        def update_user_group(user_id, org, course, name, role):
            group_id = get_group_id(org, course, name, role)
            return get_or_create("auth_user_groups", user_id=user_id, group_id=group_id)
  
        def update_user_enrollment(user_id, org, course, name):
            course_id = "%s/%s/%s" % (org, course, name)
            remote_cursor.execute("select * from student_courseenrollment where user_id=%s and course_id='%s'" % (user_id, course_id))
            result = remote_cursor.fetchone()
            if result is None:
                remote_cursor.execute("insert into student_courseenrollment set user_id='%s', course_id='%s', \
                created=now(), is_active=1, mode='honor'" % (user_id, course_id))

        def grant_user_roles(user_id, org, course, name):
            """
            Grant all of the course roles to the user
            """
            course_id = "%s/%s/%s" % (org, course, name)
            local_cursor.execute("select * from django_comment_client_role where course_id='%s';" % (course_id))
            for role in local_cursor.fetchall():
                #** copy role
                role_id = get_or_create("django_comment_client_role", course_id=course_id, name=role["name"])
                
                #** grant (all) new copied roles
                get_or_create("django_comment_client_role_users", role_id=role_id, user_id=user_id)

                #** copy role permissions
                local_cursor.execute("select * from django_comment_client_permission_roles where role_id='%s';" % (role["id"]))
                for perm in local_cursor.fetchall():
                    get_or_create("django_comment_client_permission_roles", permission_id=perm["permission_id"], role_id=role_id)
            
        # ** create course group for the user
        remote_cursor.execute("select * from auth_user where email='%s'" % user.email)
        user = remote_cursor.fetchone()
        if user is None:
            # *** user(owner) must already exists on the dest server
            raise User.DoesNotExist
        else:
            update_user_group(user['id'], org, course, name, "instructor")
            update_user_group(user['id'], org, course, name, "staff")
            update_user_enrollment(user['id'], org, course, name)
            grant_user_roles(user['id'], org, course, name)

        remote_mysql.commit()
        remote_mysql.close()
        remote_server.stop()

        update_task(task, "progress", "course sync started")

        # ** connect to mongo on dest server
        remote_server = SSHTunnelForwarder(
            d['host'],
            ssh_port=d['ssh_port'],
            ssh_username=d['ssh_username'],
            ssh_password=d['ssh_password'],
            remote_bind_address=('127.0.0.1', d['mongo_port']),
            # local_bind_address=('0.0.0.0', 27018)
        )
        remote_server.start()

        remote_mongo = MongoClient('127.0.0.1', remote_server.local_bind_port)
        # remote_mongo.admin.authenticate(d['user'], d['password'])

        opt = settings.MODULESTORE['default']['OPTIONS']
        local = MongoClient(opt['host'], opt['port'])
        # local.admin.authenticate(opt['user'], opt['password'])

        # ** sync course to dest server
        copy_course(task, org, course, local, remote_mongo)

        remote_mongo.close()
        remote_server.stop()

        update_task(task, "finished", "sync finished")
    except Exception as e:
        # import sys, traceback
        # exc_type, exc_value, exc_traceback = sys.exc_info()
        # update_task(task, "error", "task error: %s %s %s" % (e, exc_traceback.tb_lineno, exc_traceback.tb_frame.f_code.co_filename))
        update_task(task, "error", "task error: %s" % (e))
    finally:
        task.save()
        db.transaction.commit()


@login_required
def sync_course(request):
    org = request.POST.get("id_org", "")
    course = request.POST.get("id_course", "")
    name = request.POST.get("id_name", "")

    dest_id = int(request.POST.get("dest", ""))
    d = settings.COURSE_SYNC_DEST[dest_id]

    task = AsyncTask()
    task.type = "sync course"
    task.create_user = request.user
    task.create_time = datetime.now(UTC)
    task.update_time = task.create_time
    task.title = "remotely export course %s/%s/%s to %s" % (org, course, name, d.get("name"))
    task.last_message = "task started"
    task.status = "started"
    task.save()
    db.transaction.commit()

    connection.close()

    do_sync_course(task, org, course, name, d, request.user)
    return HttpResponse(json.dumps({'success': True, 'taskId': task.id}), content_type="application/json")


@login_required
def dest_course_exists(request):
    org = request.POST.get("id_org", "")
    course = request.POST.get("id_course", "")
    name = request.POST.get("id_name", "")
    dest_id = int(request.POST.get("dest", ""))
    d = settings.COURSE_SYNC_DEST[dest_id]
    error = None
    exists = False
    try:
        server = SSHTunnelForwarder(
            d['host'],
            ssh_port=d['ssh_port'],
            ssh_username=d['ssh_username'],
            ssh_password=d['ssh_password'],
            remote_bind_address=('127.0.0.1', d['mongo_port']),
        )
        server.start()

        dest = MongoClient('127.0.0.1', server.local_bind_port)
        exists = dest["xmodule"]["modulestore"].find({"_id.category": "course", "_id.org": org, "_id.course": course, "_id.name": name}).count() > 0

        dest.close()
        server.stop()

    except Exception as e:
        error = e

    return HttpResponse(json.dumps({'success': error is None, 'exists': exists, "error": str(error)}), content_type="application/json")

    

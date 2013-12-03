from mitxmako.shortcuts import render_to_response, render_to_string
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django_future.csrf import ensure_csrf_cookie
from mitxmako.shortcuts import render_to_response

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, Http404

import student.views
import branding
import courseware.views
from mitxmako.shortcuts import marketing_link
from util.cache import cache_if_anonymous
import json

from student.models import Contract,UserProfile,Registration


def create(request):
    return render_to_response('contract.html', {"contracts":Contract.objects.all(),"contract_from":True})

def modify(request,contract_id=''):
    from student.models import Contract

    contract={}
    if contract_id:
        c=Contract.objects.get(id=contract_id)
        contract['id']=c.id
        contract['name']=c.name
        contract['district_id']=c.district_id
        contract['term_months']=c.term_months
        contract['licenses']=c.licenses
    
    return render_to_response('contract.html',
                              {"contracts":Contract.objects.all(),
                               "contract":contract,
                               "contract_from":True})

def import_user(request):
    contract={}

    return render_to_response('contract.html', {"contracts":Contract.objects.all(),
 
                                                "import_from":True
                                                })

def index(request):
    return render_to_response('contract.html', {"contracts":Contract.objects.all()})

def submit(request):
    if not request.user.is_authenticated:
        raise Http404
    
    contract_id = request.POST['contract_id']
    name = request.POST['name']
    district_id = request.POST['district_id']
    term_months = request.POST['term_months']
    licenses = request.POST['licenses']

    try:
        c=Contract()
        c.id=contract_id
        c.name=name
        c.district_id=district_id
        c.term_months=term_months
        c.licenses=licenses
        c.status='ALLOW'
        c.save()

    except Exception:
        transaction.rollback()
        return HttpResponse(json.dumps({'success': False,'error':'ddddd'}))

    return HttpResponse(json.dumps({'success': True}))


from django import forms
import csv  

# class UploadFileForm(forms.Form):
#   title = forms.CharField(max_length=50)
#   file = forms.FileField()
  
def import_user_submit(request):
    # http://www.cnblogs.com/yijun-boxing/archive/2011/04/18/2020155.html
    
    CONTRACT_CVS_COL_CONTRACT_ID=0
    CONTRACT_CVS_COL_DISTRICT_ID=1
    CONTRACT_CVS_COL_EMAIL=2
    CONTRACT_CVS_COL_USERNAME=3
    CONTRACT_CVS_COUNT_COL=4
    
    message={}
    n=0
    if request.method == 'POST':
        f=request.FILES['file']
        dialect = csv.Sniffer().sniff(f.read(1024), delimiters=";,")
        f.seek(0)
        r=csv.reader(f,dialect)
        try:
            for i,line in enumerate(r):
                n=n+1

                contract_id=line[CONTRACT_CVS_COL_CONTRACT_ID]
                district_id=line[CONTRACT_CVS_COL_DISTRICT_ID]
                email=line[CONTRACT_CVS_COL_EMAIL]
                username=line[CONTRACT_CVS_COL_USERNAME]

                for value in line:
                    if len(value.strip())==0:
                        raise Exception("Catch csv line with empty fields line")
                

                if len(line) != CONTRACT_CVS_COUNT_COL:
                    raise Exception("Catch csv line of wrong fields count")

                user = User(username=username, email=email, is_active=True)
                user.set_password(username)
                registration = Registration()

                try:
                    user.save()
                except IntegrityError:
                    if len(User.objects.filter(username=username)) > 0:
                        raise Exception("An account with the Public Username '{username}' already exists.".format(username=username))
                       
                    if len(User.objects.filter(email=email)) > 0:
                        raise Exception("An account with the Email '{email}' already exists.".format(email=email))

                registration.register(user)
    
                profile=UserProfile(user=user)
                profile.contract_id=contract_id
                profile.district_id=district_id
                profile.email=email
                profile.username=username
                profile.save()

                reg = Registration.objects.get(user=user)
                d = {'name': profile.name, 'key': reg.activation_key}

                subject = render_to_string('emails/activation_email_subject.txt', d)
                subject = ''.join(subject.splitlines())
                message = render_to_string('emails/activation_email.txt', d)


                try:
                    _res = user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
                except:
                    log.warning('Unable to send reactivation email', exc_info=True)
                    return HttpResponse(json.dumps({'success': False, 'error': _('Unable to send reactivation email')}))                
                
                
            message={'success': True, "message":"Success! %s users imported." % (n)}
        except Exception as e:
            transaction.rollback()
            message={'success': False,'message':'Import error: %s, At cvs line: %s' % (e,n)}
            
        # title = forms.CharField(max_length=50)
        # file = forms.FileField()
        
    return HttpResponse(json.dumps(message))


def submit_contract(request):
    if not request.user.is_authenticated:
        raise Http404
    
    contract_id = request.POST['contract_id']
    name = request.POST['name']
    district_id = request.POST['district_id']
    term_months = request.POST['term_months']
    licenses = request.POST['licenses']

    try:
        from student.models import Contract
        c=Contract()
        if len(contract_id):
            c.id=contract_id
        c.name=name
        c.district_id=district_id
        c.term_months=term_months
        c.licenses=licenses
        c.status='ALLOW'
        c.save()

  

    except Exception as e:
        transaction.rollback()
        return HttpResponse(json.dumps({'success': False,'error': "%s" % e}))

    return HttpResponse(json.dumps({'success': True}))


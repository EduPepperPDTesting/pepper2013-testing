import cgi
import json
import logging
from copy import deepcopy
from collections import OrderedDict

from lxml import etree
from pkg_resources import resource_string

from xmodule.x_module import XModule, XModuleDescriptor
from xmodule.stringify import stringify_children
from xmodule.mako_module import MakoModuleDescriptor
from xmodule.editing_module import EditingDescriptor
from xmodule.xml_module import XmlDescriptor
from xblock.fields import Scope, String, Integer, Dict, Boolean, List
from xmodule.contentstore.content import StaticContent
from xmodule.modulestore.mongo import draft
from xmodule.modulestore.exceptions import ItemNotFoundError, InvalidLocationError
from xmodule.modulestore import Location
import json


log = logging.getLogger(__name__)

class PollCompareFields(object):
	display_name = String(help="Display name for this module", scope=Scope.settings)
	# student_answers = Dict(help="All answers for for poll for student", scope=Scope.user_state)
	# student_polls = Dict(help="All poll informations for student ever submited", scope=Scope.user_state)
	# capa_ids = List(help="All referenced poll ids for this poll compare page", scope=Scope.user_state)
	data = String(help="Html contents to display for this module", default=u"", scope=Scope.content)
	# data = String(Help="Html contents to display for this module", default=u"", scope=Scope.content)
	poll_compare_count = Integer(help="",default=0,scope=Scope.user_state)
	compares = List(help="",scope=Scope.user_state)
	# compare:{"from":"","to":""}

class PollCompareModule(PollCompareFields, XModule):
	_tag_name = 'poll_compare'
	_child_tag_name = 'compare'
	_child_tag_name_answers = 'answers'

	js = {
		'coffee': [resource_string(__name__, 'js/src/javascript_loader.coffee'),
				   resource_string(__name__, 'js/src/collapsible.coffee')],
		'js': [resource_string(__name__, 'js/src/poll_compare/logme.js'),
			   resource_string(__name__, 'js/src/poll_compare/poll_compare.js'),
			   resource_string(__name__, 'js/src/poll_compare/poll_compare_main.js')]
	}
	css = {'scss':[resource_string(__name__,'css/poll_compare/display.scss')]}

	js_module_name = "PollCompare"

	def handle_ajax(self, dispatch, data):
		return json.dumps({'error': 'Unknown Command123!'})

	def get_html(self):
		if self.data is not None:
			compares = self.definition_from_xml_string(self.data)
			poll_compares,answers = self.dump_poll_compare(compares)
		params = {
			'element_id':self.location.html_id(),
			'element_class':self.location.category,
			'ajax_url':self.system.ajax_url,
			'poll_compares':poll_compares,
			'answers':answers
		}

		self.content = self.system.render_template('poll_compare.html', params)
		return self.content

	def dump_poll(self):
		return null

	def definition_from_xml_string(self,data):
		try:
			xml_object = etree.fromstring(data)
			if len(xml_object.xpath(self._child_tag_name)) == 0:
				raise ValueError("poll_compare definition must include at least one 'compare' tag")
			xml_object_copy = deepcopy(xml_object)
			compares = []
			for element_compare in xml_object_copy.findall(self._child_tag_name):
				from_loc = element_compare.get('from_loc', None)
				to_loc   = element_compare.get('to_loc', None)
				compare_id = element_compare.get('compare_id', None)
				display_name = element_compare.get("display_name", None)
				if from_loc:
					if to_loc:
						compares.append({
							'compare_id': compare_id,
							'from_loc': from_loc,
							'to_loc': to_loc,
							'student_answers': {'from_loc':None,'to_loc':None},
							'display_name': display_name
						})
				xml_object_copy.remove(element_compare)

			for answers in xml_object_copy.findall(self._child_tag_name_answers):
				answer_attr={}
				if answers is not None:
					for k in answers.attrib:
						answer_attr[k]=answers.get(k, None)
					'''
            		answer_1 = answers.get('answer1', None)
            		answer_2 = answers.get('answer2', None)
            		answer_3 = answers.get('answer3', None)
            		answer_4 = answers.get('answer4', None)
            		answer_5 = answers.get('answer5', None)
            		'''
            		compares.append({'answers':answer_attr})			

			return compares
		except etree.XMLSyntaxError as err:
			pass

	def dump_poll_compare(self,compares):
		"""
		Dump poll_compares
		"""
		if compares is None:
			compares = {}

		# compares_to_json = {}
		compares_to_json = OrderedDict()
		answers_to_display = OrderedDict()

		for compare_element in compares:
			tmp_item = {}
			if compare_element.get('from_loc',None) is not None:
				tmp_item['from_loc'] = compare_element['from_loc']
				tmp_item['to_loc'] = compare_element['to_loc']
				tmp_item['display_name'] = compare_element['display_name']
				tmp_item['student_answers'] = compare_element['student_answers']
				compares_to_json["{0}".format(compare_element['compare_id'])] = tmp_item
			else:
				answers = None
				answers = compare_element.get('answers',None)
				if answers is not None:
					tmp_item = {}
					for key in answers:
						tmp_item[key] = answers[key]
					answers_to_display['answers'] = tmp_item
				else:
					tmp_item = {}
					'''
					tmp_item['answer1'] = "answer1"
					tmp_item['answer2'] = "answer2"
					tmp_item['answer3'] = "answer3"
					tmp_item['answer4'] = "answer4"
					tmp_item['answer5'] = "answer5"
					'''
					for key in answers:
						tmp_item[key] = key
					answers_to_display['answers'] = tmp_item
		if len(answers_to_display)>0:
			_answers = sorted(answers_to_display.get('answers',None).iteritems(),key=lambda k:k[0],reverse=False)
			_json = json.dumps(compares_to_json, sort_keys=True, indent=2)
		else:
			_answers=answers_to_display
			_json=compares_to_json
		return _json,_answers


class PollCompareDescriptor(PollCompareFields, XmlDescriptor, EditingDescriptor):
	_tag_name = 'poll_compare'
	_child_tag_name = 'compare'
	mako_template = 'widgets/poll_compare-edit.html'
	module_class = PollCompareModule

	js = {
		'coffee': [resource_string(__name__, 'js/src/poll_compare/edit.coffee')]
	}
	css = {
		'scss': [resource_string(__name__,'css/editor/edit.scss'),
				 resource_string(__name__,'css/poll_compare/edit.scss')]
	}

	js_module_name = "POLLCompareEditingDescriptor"
	filename_extension = "xml"
	template_dir_name = "poll_compare"

	@classmethod
	def load_definition(cls, xml_object, system, location):
		'''Load a descriptor from the specified xml_object:

		If there is a filename attribute, load it as a string, and
		log a warning if it is not parseable by etree.HTMLParser.

		If there is not a filename attribute, the definition is the body
		of the xml_object, without the root tag (do not want <html> in the
		middle of a page)
		'''
		filename = xml_object.get('filename')
		if filename is None:
			definition_xml = deepcopy(xml_object)
			cls.clean_metadata_from_xml(definition_xml)
			return {'data': stringify_children(definition_xml)}, []
		else:
			# html is special.  cls.filename_extension is 'xml', but
			# if 'filename' is in the definition, that means to load
			# from .html
			# 'filename' in html pointers is a relative path
			# (not same as 'html/blah.html' when the pointer is in a directory itself)
			pointer_path = "{category}/{url_path}".format(
				category='poll_compare',
				url_path=name_to_pathname(location.name)
			)
			base = path(pointer_path).dirname()
			# log.debug("base = {0}, base.dirname={1}, filename={2}".format(base, base.dirname(), filename))
			filepath = "{base}/{name}.html".format(base=base, name=filename)
			# log.debug("looking for html file for {0} at {1}".format(location, filepath))

			# VS[compat]
			# TODO (cpennington): If the file doesn't exist at the right path,
			# give the class a chance to fix it up. The file will be written out
			# again in the correct format.  This should go away once the CMS is
			# online and has imported all current (fall 2012) courses from xml
			if not system.resources_fs.exists(filepath):
				candidates = cls.backcompat_paths(filepath)
				# log.debug("candidates = {0}".format(candidates))
				for candidate in candidates:
					if system.resources_fs.exists(candidate):
						filepath = candidate
						break

			try:
				with system.resources_fs.open(filepath) as file:
					html = file.read().decode('utf-8')
					# Log a warning if we can't parse the file, but don't error
					# if not check_html(html) and len(html) > 0:
					#     msg = "Couldn't parse html in {0}, content = {1}".format(filepath, html)
					#     log.warning(msg)
					#     system.error_tracker("Warning: " + msg)

					definition = {'data': html}

					# TODO (ichuang): remove this after migration
					# for Fall 2012 LMS migration: keep filename (and unmangled filename)
					definition['filename'] = [filepath, filename]

					return definition, []

			except (ResourceNotFoundError) as err:
				msg = 'Unable to load file contents at path {0}: {1} '.format(
					filepath, err)
				# add more info and re-raise
				raise Exception(msg), None, sys.exc_info()[2]


	@classmethod
	def backcompat_paths(cls, path):
		if path.endswith('.html.xml'):
			path = path[:-9] + '.html'  # backcompat--look for html instead of xml
		if path.endswith('.html.html'):
			path = path[:-5]  # some people like to include .html in filenames..
		candidates = []
		while os.sep in path:
			candidates.append(path)
			_, _, path = path.partition(os.sep)

		# also look for .html versions instead of .xml
		nc = []
		for candidate in candidates:
			if candidate.endswith('.xml'):
				nc.append(candidate[:-4] + '.html')
		return candidates + nc


	def get_context(self):
		_context = EditingDescriptor.get_context(self)
		_context.update({'test':self.data})
		if self.data == u'':
			template_data='<poll_compare><compare compare_id="compare_1" from_loc="i4x://[org]/[course]/[category]/[url_name]" to_loc="i4x://[org]/[course]/[category]/[url_name]" display_name="test1"></compare><compare compare_id="compare_2" from_loc="i4x://[org]/[course]/[category]/[url_name]" to_loc="i4x://[org]/[course]/[category]/[url_name]" display_name="test2"></compare></poll_compare>'
			_context.update({'test':template_data})
		_context.update({'base_asset_url': StaticContent.get_base_url_path_for_course_assets(self.location) + '/'})
		return _context

 	def definition_to_xml(self, resource_fs):
 		if self.data is None:
 			return None
 		xml_object = etree.fromstring(self.data)
 		# xml_object.set('display_name', self.display_name)
 		return xml_object
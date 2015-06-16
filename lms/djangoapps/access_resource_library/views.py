from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django_future.csrf import ensure_csrf_cookie
from mitxmako.shortcuts import render_to_response
from student.models import ResourceLibrary,StaticContent
from collections import deque
from django.contrib.auth.decorators import login_required

def index_bak(request):

	def custom_compare_key(item):
		category_order = item.category.display_order * 10000
		subclass_order = (item.subclass.display_order if item.subclass is not None else 1) * 100
		display_order  = item.display_order
		return category_order + subclass_order + display_order

	resources_librarys = list(ResourceLibrary.objects.prefetch_related())

	resources_librarys.sort(key = lambda x: custom_compare_key(x), reverse=False)
	result = {}
	for resource_library in resources_librarys:
		category = resource_library.category
		subclass = resource_library.subclass if resource_library.subclass is not None else None
		subclass_sites = subclass.sites.get_query_set() if subclass else None

		tmp_item = {}
		tmp_dict = {}
		tmp_sub_items = {}
		tmp_cat_items = {}

		category_key = 'id_{}_{}order_{}'.format(category.id,category.display,category.display_order)
		category_displayorder = category.display_order
		
		subclass_key = 'id_{}_{}order_{}'.format(subclass.id,subclass.display,subclass.display_order) if subclass is not None else 'nosubclass'
		subclass_name = subclass.display if subclass is not None else 'nosubclass'
		subclass_displayorder = subclass.display_order if subclass else 0

		tmp_item['display'] = resource_library.display
		tmp_item['link'] = resource_library.link			

		if result.get(category_key, None) is None:		
			tmp_sub_items['display'] = subclass_name
			tmp_sub_items['display_order'] = subclass_displayorder
			tmp_sub_items['items'] = deque()
			tmp_sub_items['items'].append(tmp_item)
			if subclass_sites:
				tmp_sub_items['sites'] = deque()
				for site in subclass_sites:
					tmp_sit_items = dict()
					tmp_sit_items['display'] = site.display
					tmp_sit_items['link'] = site.link
					tmp_sit_items['display_order'] = site.display_order
					tmp_sub_items['sites'].append(tmp_sit_items)	
			tmp_dict[subclass_key] = tmp_sub_items
			tmp_cat_items['display'] = category.display
			tmp_cat_items['display_order'] = category.display_order
			tmp_cat_items['items'] = tmp_dict
			result[category_key] = tmp_cat_items
		else:
			if result[category_key]['items'].get(subclass_key, None) is None:
				tmp_sub_items['display'] = subclass_name
				tmp_sub_items['display_order'] = subclass_displayorder
				tmp_sub_items['items'] = deque()
				tmp_sub_items['items'].append(tmp_item)
				if subclass_sites:
					if tmp_sub_items.get('sites', None) is None:
						tmp_sub_items['sites'] = deque()
					for site in subclass_sites:
						tmp_sit_items = dict()
						tmp_sit_items['display'] = site.display
						tmp_sit_items['display_order'] = site.display_order
						tmp_sit_items['link'] = site.link
						tmp_sub_items['sites'].append(tmp_sit_items)
				result[category_key]['items'][subclass_key] = tmp_sub_items
			else:
				result[category_key]['items'][subclass_key]['items'].append(tmp_item)
	resources = result

	return render_to_response('access_resource_library.html', {'resources': result})

@login_required
def index(request):
	static_content = StaticContent.objects.get(name="Resource Library")
	static_html_content = static_content.content if static_content else 'sorry for maintain...'
	return render_to_response('access_resource_library_.html',{'static_content':static_html_content})

@login_required
def index_list(request):
	return render_to_response('access_resource_library_list.html')

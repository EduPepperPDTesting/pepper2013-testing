from django.conf import settings
from django.conf.urls import patterns, include, url
from ratelimitbackend import admin
from django.conf.urls.static import static

import django.contrib.auth.views

# Uncomment the next two lines to enable the admin:
if settings.DEBUG or settings.MITX_FEATURES.get('ENABLE_DJANGO_ADMIN_SITE'):
    admin.autodiscover()

urlpatterns = (
    '',  # nopep8

    # url(r'^$', 'idp.views.tnl_domain_add', name="tnl_domain_add"),

####### Ancestor
    # === shopping begin ===
    url(r'^shopping/$', 'shopping.views.course_list', name="shopping_course_list"),
    url(r'^shopping/enroll/post$', 'shopping.views.enroll_post', name="shopping_enroll_post"),
    url(r'^shopping/(?P<course_id>[^/]+/[^/]+/[^/]+)/course_info/$', 'shopping.views.course_info', name="shopping_course_info"),
    url(r'^shopping/valid_discount_code/$', 'shopping.views.valid_discount_code', name="shopping_valid_discount_code"),
    # === shopping end ===
    
    url(r'^student/drop_districts$', 'student.views.drop_districts', name="student_drop_districts"),
    url(r'^student/drop_states$', 'student.views.drop_states', name="student_drop_states"),
    url(r'^student/drop_schools$', 'student.views.drop_schools', name="student_drop_schools"),
    
    # === notification config begin ===
    url(r'^confignotification/$', 'communities.notification.configuration', name="communities_notification_index"),
    url(r'^communities/notification/groups$', 'communities.notification.groups', name="communities_notification_groups"),
    url(r'^communities/notification/all_groups$', 'communities.notification.all_groups', name="communities_notification_all_groups"),
    url(r'^communities/notification/types$', 'communities.notification.types', name="communities_notification_types"),
    url(r'^communities/notification/groups/save$', 'communities.notification.save_group', name="communities_notification_save_group"),
    url(r'^communities/notification/types/save$', 'communities.notification.save_type', name="communities_notification_save_type"),

    url(r'^communities/notification/groups/delete$', 'communities.notification.delete_group', name="communities_notification_delete_group"),
    url(r'^communities/notification/types/delete$', 'communities.notification.delete_type', name="communities_notification_delete_type"),

    url(r'^communities/notification/groups/edit$', 'communities.notification.edit_group', name="communities_notification_edit_group"),
    url(r'^communities/notification/types/edit$', 'communities.notification.edit_type', name="communities_notification_edit_type"),

    url(r'^communities/notification/config$', 'communities.notification.config', name="communities_notification_config"),
    url(r'^communities/notification/config_other$', 'communities.notification.config_other', name="communities_notification_config_other"),
    url(r'^communities/notification/configs/save$', 'communities.notification.save_config', name="communities_notification_save_config"),
        url(r'^communities/notification/configs/saveother$', 'communities.notification.save_other_config', name="communities_notification_save_other_config"),
    # === notification config end ===
    
    # === sso begin ===
    # easyiep
    url(r'^sso/$', 'sso.sp.genericsso', name="sso"),
    url(r'^register_easyiep/(?P<activation_key>[^/]*)/$', 'sso.sp.register_user_easyiep', name="register_user_easyiep"),
    url(r'^activate_easyiep_account$', 'sso.sp.activate_account', name="activate_easyiep_account"),

    url(r'^genericsso/$', 'sso.sp.genericsso'),
    url(r'^sso/activate_account/$', 'sso.sp.activate_account', name="activate_sso_account"),
    # edit idp
    url(r'^sso/idp_metadata/edit/$', 'sso.idp_metadata.edit', name="sso_idp_metadata_edit"),
    url(r'^sso/idp_metadata/all_json/$', 'sso.idp_metadata.all_json', name="sso_idp_metadata_all_json"),
    url(r'^sso/idp_metadata/save/$', 'sso.idp_metadata.save', name="sso_idp_metadata_save"),
    # edit sp
    url(r'^sso/sp_metadata/edit/$', 'sso.sp_metadata.edit', name="sso_sp_metadata_edit"),
    url(r'^sso/sp_metadata/all_json/$', 'sso.sp_metadata.all_json', name="sso_sp_metadata_all_json"),
    url(r'^sso/sp_metadata/save/$', 'sso.sp_metadata.save', name="sso_sp_metadata_save"),
    url(r'^sso/sp_metadata/download/saml_federation_metadata$',
        'sso.sp_metadata.download_saml_federation_metadata', name="sso_download_saml_federation_metadata"),
    url(r'^register_sso_user/(?P<activation_key>[^/]*)/$', 'sso.sp.register_sso', name="register_sso_user"),
    url(r'^sso/idp/auth/$', 'sso.idp.auth'),

    url(r'^sso/course_assignments$', 'sso.idp_metadata.course_assignment', name="sso_course_assignment"),
    url(r'^sso/course_assignments/list$', 'sso.idp_metadata.course_assignment_list', name="sso_course_assignment_list"),
    url(r'^sso/course_assignments/save$', 'sso.idp_metadata.course_assignment_save', name="sso_course_assignment_save"),
    url(r'^sso/course_assignments/delete$', 'sso.idp_metadata.course_assignment_delete', name="sso_course_assignment_delete"),
    # === sso end ===

    # === pepreg begin ==
    url(r'^pepreg/$', 'administration.pepreg.index', name='pepreg'),

    url(r'^pepreg/rows$', 'administration.pepreg.rows', name="pepreg_rows"),
    url(r'^pepreg/save_training$', 'administration.pepreg.save_training', name="pepreg_save_training"),
    url(r'^pepreg/delete_training$', 'administration.pepreg.delete_training', name="pepreg_delete_training"),
    url(r'^pepreg/training_json$', 'administration.pepreg.training_json', name="pepreg_training_json"),
    url(r'^pepreg/getCalendarInfo$', 'administration.pepreg.getCalendarInfo', name="pepreg_training_calendar_json"),
    url(r'^pepreg/getCalendarMonth$', 'administration.pepreg.getCalendarMonth', name="pepreg_training_calendar_getmonth"),
    url(r'^pepreg/register$', 'administration.pepreg.register', name="pepreg_register"),
    url(r'^pepreg/set_student_attended$', 'administration.pepreg.set_student_attended', name="pepreg_set_student_attended"),
    url(r'^pepreg/set_student_validated$', 'administration.pepreg.set_student_validated', name="pepreg_set_student_validated"),
    url(r'^pepreg/student_list$', 'administration.pepreg.student_list', name="pepreg_student_list"),
    url(r'^pepreg/delete_student$', 'administration.pepreg.delete_student', name="pepreg_delete_student"),
    url(r'^pepreg/map/$', 'administration.pepreg.show_map', name="pepreg_map"),
    url(r'^pepreg/download_students_excel/$', 'administration.pepreg.download_students_excel', name="pepreg_download_students_excel"),
    url(r'^pepreg/download_students_pdf/$', 'administration.pepreg.download_students_pdf', name="pepreg_download_students_pdf"),
    url(r'^pepreg/(?P<training_id>[a-zA-Z0-9_]+)$', 'training.views.training_registration', name="training_registration"),
    #url(r'^pepreg/training_registration/$', 'training.views.training_registration', name="training_registration"),
    url(r'^pepreg/(?P<training_id>[a-zA-Z0-9_]+)/join/$', 'training.views.training_join', name='training_join'),
    url(r'^pepreg/(?P<training_id>[a-zA-Z0-9_]+)/leave/$', 'training.views.training_leave', name='training_leave'),
    url(r'^pepreg/(?P<training_id>[a-zA-Z0-9_]+)/tables/get_add_user_rows/$', 'training.views.get_add_user_rows', name="training_get_add_user_rows"),
    url(r'^pepreg/(?P<training_id>[a-zA-Z0-9_]+)/tables/get_remove_user_rows/$', 'training.views.get_remove_user_rows', name="training_get_remove_user_rows"),
    # === pepreg end ==

    # === Portfolio Settings begin ==
    url(r'^portfolio_settings/$', 'portfolio_settings.portfolio.index', name='portfolio_settings'),
    # === Portfolio Settings end ==

    url(r'^pepper-utilities/drop/states', 'pepper_utilities.views.drop_states', name='pepper_utilities_drop_states'),
    url(r'^pepper-utilities/drop/districts', 'pepper_utilities.views.drop_districts', name='pepper_utilities_drop_districts'),
    url(r'^pepper-utilities/drop/schools', 'pepper_utilities.views.drop_schools', name='pepper_utilities_drop_schools'),
    url(r'^pepper-utilities/drop/cohorts', 'pepper_utilities.views.drop_cohorts', name='pepper_utilities_drop_cohorts'),
    url(r'^pepper-utilities/user/email-completion', 'pepper_utilities.views.user_email_completion', name='pepper_utilities_user_email_completion'),
    url(r'^pepper-utilities/user/email-exists', 'pepper_utilities.views.user_email_exists', name='pepper_utilities_user_email_exists'),

    url(r'^permissions$', 'permissions.views.permissions_view', name='permissions_view'),
    url(r'^permissions/groups/permissions/list$', 'permissions.views.group_permissions_list', name='permissions_group_permissions_list'),
    url(r'^permissions/groups/permissions/add$', 'permissions.views.group_permission_add', name='permissions_group_permission_add'),
    url(r'^permissions/groups/permissions/delete$', 'permissions.views.group_permission_delete', name='permissions_group_permission_delete'),
    url(r'^permissions/groups/members/list$', 'permissions.views.group_member_list', name='permissions_group_members_list'),
    url(r'^permissions/groups/members/add$', 'permissions.views.group_member_add', name='permissions_group_member_add'),
    url(r'^permissions/groups/members/delete$', 'permissions.views.group_member_delete', name='permissions_group_member_delete'),
    url(r'^permissions/groups/check$', 'permissions.views.group_check', name='permissions_group_check'),
    url(r'^permissions/groups/add$', 'permissions.views.group_add', name='permissions_group_add'),
    url(r'^permissions/groups/delete$', 'permissions.views.group_delete', name='permissions_group_delete'),
    url(r'^permissions/groups/list$', 'permissions.views.group_list', name='permissions_group_list'),
    url(r'^permissions/permissions/check$', 'permissions.views.permission_check', name='permissions_permission_check'),
    url(r'^permissions/permissions/add$', 'permissions.views.permission_add', name='permissions_permission_add'),
    url(r'^permissions/permissions/delete$', 'permissions.views.permission_delete', name='permissions_permission_delete'),
    url(r'^permissions/permissions/list$', 'permissions.views.permissions_list', name='permissions_permissions_list'),

    url(r'^reporting$', 'reporting.views.reports_view', name='reporting_reports'),
    url(r'^reporting/categories/save$', 'reporting.views.category_save', name='reporting_category_save'),
    url(r'^reporting/categories/delete$', 'reporting.views.category_delete', name='reporting_category_delete'),
    url(r'^reporting/order/save$', 'reporting.views.order_save', name='reporting_order_save'),
    url(r'^reporting/report/delete$', 'reporting.views.report_delete', name='reporting_report_delete'),
    url(r'^reporting/report/(?P<report_id>[0-9a-z]+)$', 'reporting.views.report_view', name='reporting_report'),
    url(r'^reporting/report/(?P<report_id>[0-9a-z]+)/edit$', 'reporting.views.report_edit', name='reporting_report_edit'),
    url(r'^reporting/report/(?P<report_id>[0-9a-z]+)/save$', 'reporting.views.report_save', name='reporting_report_save'),
    url(r'^reporting/views/edit$', 'reporting.views.views_edit', name='reporting_views_edit'),
    url(r'^reporting/views/edit/update$', 'reporting.views.views_edit_update', name='reporting_views_edit_update'),
    url(r'^reporting/views/add$', 'reporting.views.view_add', name='reporting_view_add'),
    url(r'^reporting/views/delete$', 'reporting.views.views_delete', name='reporting_views_delete'),
    url(r'^reporting/views/data$', 'reporting.views.view_data', name='reporting_view_data'),
    url(r'^reporting/views/list$', 'reporting.views.views_list', name='reporting_views_list'),
    url(r'^reporting/views/relationships/add$', 'reporting.views.relationship_add', name='reporting_relationship_add'),
    url(r'^reporting/views/relationships/delete$', 'reporting.views.relationships_delete', name='reporting_relationships_delete'),
    url(r'^reporting/views/relationships/data$', 'reporting.views.relationship_data', name='reporting_relationship_data'),
    url(r'^reporting/views/related$', 'reporting.views.related_views', name='reporting_related_views'),
    url(r'^reporting/views/columns$', 'reporting.views.view_columns', name='reporting_view_columns'),
    url(r'^reporting/report/get_rows$', 'reporting.views.report_get_rows', name='reporting_report_get_rows'),
    url(r'^reporting/report/get_progress/(?P<report_id>[0-9a-z]+)$', 'reporting.views.report_get_progress', name='reporting_report_get_progress'),
    url(r'^reporting/report/(?P<report_id>[0-9a-z]+)/download_excel$', 'reporting.views.report_download_excel', name="report_download_excel"),
    url(r'^reporting/report/(?P<report_id>[0-9a-z]+)/report_get_custom_filters$', 'reporting.views.report_get_custom_filters', name="report_get_custom_filters"),

    url(r'^usage_report/$', 'administration.usage_report.main', name="usage_report"),
    url(r'^usage_report/get_result$', 'administration.usage_report.get_user_login_info', name="get_user_login_info"),
    url(r'^usage_report/drop_states$', 'administration.usage_report.drop_states', name="usage_report_drop_states"),
    url(r'^usage_report/drop_districts$', 'administration.usage_report.drop_districts', name="usage_report_drop_districts"),
    url(r'^usage_report/drop_schools$', 'administration.usage_report.drop_schools', name="usage_report_drop_schools"),
    url(r'^usage_report/download_excel/$', 'administration.usage_report.usage_report_download_excel', name="usage_report_download_excel"),

    #@begin:Add for Dashboard Posts
    #@date:2016-12-29
    url(r'^dashboard/post/get$', 'student.newdashboard.get_posts', name='dashboard_get_posts'),
    url(r'^dashboard/post/like$', 'student.newdashboard.submit_new_like', name='dashboard_submit_new_like'),
    url(r'^dashboard/delete/post', 'student.newdashboard.delete_post', name='dashboard_delete_post'),
    url(r'^dashboard/delete/comment', 'student.newdashboard.delete_comment', name='dashboard_delete_comment'),
    url(r'^dashboard/post/comment', 'student.newdashboard.submit_new_comment', name='dashboard_submit_new_comment'),
    url(r'^dashboard/post/lookup', 'student.newdashboard.lookup_name', name='dashboard_lookup_name'),
    url(r'^dashboard/post/showlikes', 'student.newdashboard.get_full_likes', name='dashboard_get_full_likes'),
    url(r'^dashboard/post/new$', 'student.newdashboard.submit_new_post', name='dashboard_submit_new_post'),
    #@end
    #@begin:Add for Dashboard My Activity
    #@date:2016-12-29
    url(r'^dashboard/my_activity/get$', 'student.newdashboard.get_my_activities', name='get_my_activities'),
    #@end

    url(r'^tnl/domain/add$', 'tnl_integration.views.tnl_domain_add', name="tnl_domain_add"),
    url(r'^tnl/domain/delete$', 'tnl_integration.views.tnl_domain_delete', name="tnl_domain_delete"),
    url(r'^tnl/district/add$', 'tnl_integration.views.tnl_district_add', name="tnl_district_add"),
    url(r'^tnl/district/delete$', 'tnl_integration.views.tnl_district_delete', name="tnl_district_delete"),
    url(r'^tnl/course/add$', 'tnl_integration.views.tnl_course_add', name="tnl_course_add"),
    url(r'^tnl/course/delete$', 'tnl_integration.views.tnl_course_delete', name="tnl_course_delete"),
    url(r'^tnl/drop-courses$', 'tnl_integration.views.tnl_drop_courses', name="tnl_drop_courses"),
    url(r'^tnl/drop-districts$', 'tnl_integration.views.tnl_drop_districts', name="tnl_drop_districts"),
    url(r'^tnl/drop-domains$', 'tnl_integration.views.tnl_drop_domains', name="tnl_drop_domains"),
    url(r'^tnl/domain/data$', 'tnl_integration.views.tnl_domain_data', name='tnl_domain_data'),
    url(r'^tnl/tables$', 'tnl_integration.views.tnl_tables', name='tnl_tables'),

    url(r'^student/drop_districts$', 'student.views.drop_districts', name="student_drop_districts"),
    url(r'^student/drop_states$', 'student.views.drop_states', name="student_drop_states"),
    url(r'^student/drop_schools$', 'student.views.drop_schools', name="student_drop_schools"),

    url(r'^study_time/$', 'study_time.views.create_report', name="create_report"),
    url(r'^record_time/$', 'study_time.views.record_time', name="record_time"),
    url(r'^record_time/course_time_load$', 'study_time.views.get_course_time', name="get_course_time"),
    url(r'^record_time/course_time_save$', 'study_time.views.save_course_time', name="save_course_time"),

    url(r'^record_time/external_time_load$', 'study_time.views.get_external_time', name="get_external_time"),
    url(r'^record_time/external_time_save$', 'study_time.views.save_external_time', name="save_external_time"),
    url(r'^record_time/external_time_del$', 'study_time.views.del_external_time', name="del_external_time"),

    url(r'^study_time/get_info_range$', 'study_time.views.get_study_time_range', name="get_study_time_range"),
    url(r'^configuration/$', 'administration.configuration.main', name="configuration"),
    url(r'^configuration/drop_association_type$', 'administration.configuration.drop_association_type', name="drop_association_type"),
    url(r'^configuration/drop_association$', 'administration.configuration.drop_association', name="drop_association"),
    url(r'^configuration/drop_publish_association$', 'administration.configuration.drop_publish_association', name="drop_publish_association"),
    url(r'^configuration/certificate/table$', 'administration.configuration.certificate_table', name="configuration_certificate_table"),
    url(r'^configuration/certificate/delete$', 'administration.configuration.certificate_delete', name="configuration_certificate_delete"),
    url(r'^configuration/certificate/save$', 'administration.configuration.certificate_save', name="configuration_certificate_save"),
    url(r'^configuration/certificate/load_data$', 'administration.configuration.certificate_loadData', name="configuration_certificate_loadData"),
    url(r'^configuration/end_of_year_roll_over/roll_over$', 'administration.configuration.roll_over', name="configuration_roll_over"),
    url(r'^configuration/tnl$', 'tnl_integration.views.tnl_configuration', name='tnl_configuration'),

    url(r'^user-info$', 'administration.configuration.get_user_info', name="get_user_info"),

    url(r'^pepconn/add_to_cohort/submit$', 'administration.pepconn.add_to_cohort', name="pepconn_cohort_add_submit"),
    url(r'^pepconn/remove_from_cohort/submit$', 'administration.pepconn.remove_from_cohort', name="pepconn_cohort_remove_submit"),

    url(r'^custom/save$', 'administration.pepconn.save_custom_email', name="pepconn_save_custom_email"),
    url(r'^custom/get$', 'administration.pepconn.get_custom_email', name="pepconn_get_custom_email"),
    url(r'^custom/get-list$', 'administration.pepconn.get_custom_email_list', name="pepconn_get_custom_email_list"),
    url(r'^custom/delete$', 'administration.pepconn.delete_custom_email', name="pepconn_delete_custom_email"),

    url(r'^organization/$', 'organization.organization.main', name="organizational_configuration"),

    url(r'^pepconn/add_to_sso/submit$', 'administration.pepconn.add_to_sso', name="pepconn_sso_add_submit"),

    url(r'^pepconn/$', 'administration.pepconn.main', name="pepconn"),
    url(r'^pepconn/import_user/submit/$', 'administration.pepconn.import_user_submit', name="pepconn_import_user_submit"),
    url(r'^pepconn/import_user/progress/$', 'administration.pepconn.import_user_progress', name="pepconn_import_user_progress"),
    url(r'^pepconn/import_user/tasks$', 'administration.pepconn.import_user_tasks', name="pepconn_import_user_tasks"),
    url(r'^pepconn/tasks/close$', 'administration.pepconn.task_close', name="pepconn_task_close"),

    url(r'^pepconn/cohort/submit/$', 'administration.pepconn.cohort_submit', name="pepconn_cohort_submit"),
    url(r'^pepconn/import_district/single_submit/$', 'administration.pepconn.single_district_submit', name="pepconn_single_district_submit"),
    url(r'^pepconn/import_school/single_submit/$', 'administration.pepconn.single_school_submit', name="pepconn_single_school_submit"),
    url(r'^pepconn/import_user/single_submit/$', 'administration.pepconn.single_user_submit', name="pepconn_single_user_submit"),

    url(r'^pepconn/import_district/submit/$', 'administration.pepconn.import_district_submit', name="pepconn_import_district_submit"),
    url(r'^pepconn/import_district/progress/$', 'administration.pepconn.import_district_progress', name="pepconn_import_district_progress"),
    url(r'^pepconn/import_district/tasks/$', 'administration.pepconn.import_district_tasks', name="pepconn_import_district_tasks"),

    url(r'^pepconn/import_school/submit/$', 'administration.pepconn.import_school_submit', name="pepconn_import_school_submit"),
    url(r'^pepconn/import_school/progress/$', 'administration.pepconn.import_school_progress', name="pepconn_import_school_progress"),
    url(r'^pepconn/import_school/tasks/$', 'administration.pepconn.import_school_tasks', name="pepconn_import_school_tasks"),

    url(r'^pepconn/edit_district/get_info/$', 'administration.pepconn.district_get_info', name="pepconn_district_get_info"),
    url(r'^pepconn/edit_district/request/$', 'administration.pepconn.district_edit_info', name="pepconn_district_edit_info"),

    url(r'^pepconn/edit_school/get_info/$', 'administration.pepconn.school_get_info', name="pepconn_school_get_info"),
    url(r'^pepconn/edit_school/edit_info/$', 'administration.pepconn.school_edit_info', name="pepconn_school_edit_info"),

    url(r'^pepconn/edit_cohort/get_info/$', 'administration.pepconn.cohort_get_info', name="pepconn_cohort_get_info"),
    url(r'^pepconn/edit_cohort/edit_info/$', 'administration.pepconn.cohort_edit_info', name="pepconn_cohort_edit_info"),

    url(r'^pepconn/edit_user/get_info/$', 'administration.pepconn.user_get_info', name="pepconn_user_get_info"),
    url(r'^pepconn/edit_user/edit_info/$', 'administration.pepconn.user_edit_info', name="pepconn_user_edit_info"),

    url(r'^pepconn/drop_districts$', 'administration.pepconn.drop_districts', name="pepconn_drop_districts"),
    url(r'^pepconn/drop_states$', 'administration.pepconn.drop_states', name="pepconn_drop_states"),
    url(r'^pepconn/drop_schools$', 'administration.pepconn.drop_schools', name="pepconn_drop_schools"),
    url(r'^pepconn/drop_cohorts$', 'administration.pepconn.drop_cohorts', name="pepconn_drop_cohorts"),

    url(r'^pepconn/favorite_filter_load$', 'administration.pepconn.favorite_filter_load', name="pepconn_favorite_filter_load"),
    url(r'^pepconn/favorite_filter_save$', 'administration.pepconn.favorite_filter_save', name="pepconn_favorite_filter_save"),
    url(r'^pepconn/favorite_filter_delete$', 'administration.pepconn.favorite_filter_delete', name="pepconn_favorite_filter_delete"),

    url(r'^pepconn/registration/table$', 'administration.pepconn.registration_table', name="pepconn_registration_table"),
    url(r'^pepconn/registration/send_email$', 'administration.pepconn.registration_send_email', name="pepconn_registration_send_email"),
    url(r'^pepconn/registration/email_progress$', 'administration.pepconn.registration_email_progress', name="pepconn_registration_email_progress"),
    url(r'^pepconn/registration/invite_count/$', 'administration.pepconn.registration_invite_count', name="pepconn_registration_invite_count"),
    url(r'^pepconn/registration/delete_users/$', 'administration.pepconn.registration_delete_users', name="pepconn_registration_delete_users"),
    url(r'^pepconn/registration/download_csv/$', 'administration.pepconn.registration_download_csv', name="pepconn_registration_download_csv"),
    url(r'^pepconn/registration/download_excel/$', 'administration.pepconn.registration_download_excel', name="pepconn_registration_download_excel"),
    url(r'^pepconn/registration/modify_user_status/$', 'administration.pepconn.registration_modify_user_status', name="pepconn_registration_modify_user_status"),

    url(r'^pepconn/tables/get_user_rows/$', 'administration.pepconn.get_user_rows', name="pepconn_get_user_rows"),
    url(r'^pepconn/tables/get_district_rows/$', 'administration.pepconn.get_district_rows', name="pepconn_get_district_rows"),
    url(r'^pepconn/tables/get_school_rows/$', 'administration.pepconn.get_school_rows', name="pepconn_get_school_rows"),
    url(r'^pepconn/tables/get_cohort_rows/$', 'administration.pepconn.get_cohort_rows', name="pepconn_get_cohort_rows"),

    url(r'^time_report/$', 'administration.time_report.main', name="time_report"),
    url(r'^time_report/drop_districts$', 'administration.time_report.drop_districts', name="time_report_drop_districts"),
    url(r'^time_report/drop_states$', 'administration.time_report.drop_states', name="time_report_drop_states"),
    url(r'^time_report/drop_schools$', 'administration.time_report.drop_schools', name="time_report_drop_schools"),
    url(r'^time_report/time_table$', 'administration.time_report.time_table', name="time_report_time_table"),
    url(r'^time_report/download_excel/$', 'administration.time_report.time_report_download_excel', name="time_report_download_excel"),
    url(r'^time_report/time_table/progress/$', 'administration.time_report.time_table_progress', name="time_report_time_table_progress"),
    url(r'^time_report/time_table/get_result$', 'administration.time_report.get_time_table_result', name="time_report_get_time_table_result"),
    url(r'^time_report/drop_courses$', 'administration.time_report.drop_courses', name="time_report_drop_courses"),
    url(r'^time_report/drop_enroll_courses$', 'administration.time_report.drop_enroll_courses', name="time_report_drop_enroll_courses"),
    url(r'^time_report/adjustment_time_save$', 'administration.time_report.save_adjustment_time', name="time_report_adjustment_time_save"),
    url(r'^time_report/adjustment_time_load$', 'administration.time_report.load_adjustment_time', name="time_report_adjustment_time_load"),
    url(r'^time_report/single_user_time_load$', 'administration.time_report.load_single_user_time', name="time_report_single_user_time_load"),
    url(r'^time_report/enrollment_courses_load$', 'administration.time_report.load_enrollment_courses', name="time_report_enrollment_courses_load"),
    url(r'^time_report/adjustment_log_load$', 'administration.time_report.load_adjustment_log', name="time_report_adjustment_log_load"),
    url(r'^time_report/import_adjustment_time/submit/$', 'administration.time_report.import_adjustment_time_submit', name="time_report_import_adjustment_time_submit"),

    url(r'^alert_message/$', 'administration.alert_message.main', name="alert_message"),#20160411 add
    url(r'^alert_message_post/$', 'administration.alert_message.alert_message_post', name="alert_message_post"),#20160411 add

    url(r'^more_courses_available/$', 'student.views.more_courses_available', name="more_courses_available"),
    url(r'^reg_kits/$', 'reg_kits.views.district', name="reg_kits"),
    url(r'^reg_kits/course_permission/$', 'reg_kits.views.course_permission', name="course_permission"),
    url(r'^reg_kits/course_permission_save/$', 'reg_kits.views.course_permission_save', name="course_permission_save"),
    url(r'^reg_kits/download_course_permission_csv/$', 'reg_kits.views.download_course_permission_csv', name="download_course_permission_csv"),
    url(r'^reg_kits/download_course_permission_excel/$', 'reg_kits.views.download_course_permission_excel', name="download_course_permission_excel"),

    url(r'^request_course_access$', 'student.views.request_course_access_ajax', name="request_course_access"),

    url(r'^reg_kits/drop_districts$', 'reg_kits.views.drop_districts', name="drop_districts"),
    url(r'^reg_kits/drop_states$', 'reg_kits.views.drop_states', name="drop_states"),
    url(r'^reg_kits/drop_schools$', 'reg_kits.views.drop_schools', name="drop_schools"),
    url(r'^reg_kits/drop_cohorts$', 'reg_kits.views.drop_cohorts', name="drop_cohorts"),

    url(r'^reg_kits/district/$', 'reg_kits.views.district', name="district"),
    url(r'^reg_kits/district/form/$', 'reg_kits.views.district_form', name="district_form"),
    url(r'^reg_kits/district/form/(?P<district_id>\d+)$', 'reg_kits.views.district_form', name="district_form"),
    url(r'^reg_kits/district/delete/$', 'reg_kits.views.district_delete', name="district_delete"),
    url(r'^reg_kits/district/submit/$', 'reg_kits.views.district_submit', name="district_submit"),

    url(r'^reg_kits/transaction/$', 'reg_kits.views.transaction', name="transaction"),
    url(r'^reg_kits/transaction/form$', 'reg_kits.views.transaction_form', name="transaction_form"),
    url(r'^reg_kits/transaction/form/h(?P<transaction_id>\d+)$', 'reg_kits.views.transaction_form', name="transaction_modify"),
    url(r'^reg_kits/transaction/submit$', 'reg_kits.views.transaction_submit', name="transaction_submit"),
    url(r'^reg_kits/transaction/delete/$', 'reg_kits.views.transaction_delete', name="transaction_delete"),

    url(r'^reg_kits/cohort/$', 'reg_kits.views.cohort', name="cohort"),
    url(r'^reg_kits/cohort/form/$', 'reg_kits.views.cohort_form', name="cohort_form"),
    url(r'^reg_kits/cohort/form/(?P<cohort_id>\d+)$', 'reg_kits.views.cohort_form', name="cohort_form"),
    url(r'^reg_kits/cohort/delete/$', 'reg_kits.views.cohort_delete', name="cohort_delete"),
    url(r'^reg_kits/cohort/submit/$', 'reg_kits.views.cohort_submit', name="cohort_submit"),

    url(r'^reg_kits/school/$', 'reg_kits.views.school', name="school"),
    url(r'^reg_kits/school/form/$', 'reg_kits.views.school_form', name="school_form"),
    url(r'^reg_kits/school/form/(?P<school_id>\d+)$', 'reg_kits.views.school_form', name="school_form"),
    url(r'^reg_kits/school/delete/$', 'reg_kits.views.school_delete', name="school_delete"),
    url(r'^reg_kits/school/submit/$', 'reg_kits.views.school_submit', name="school_submit"),

    url(r'^reg_kits/school/import_school_submit/$', 'reg_kits.views.import_school_submit', name="import_school_submit"),
    url(r'^reg_kits/district/import_district_submit/$', 'reg_kits.views.import_district_submit', name="import_district_submit"),
    url(r'^reg_kits/cohort/import_cohort_submit/$', 'reg_kits.views.import_cohort_submit', name="import_cohort_submit"),

    url(r'^reg_kits/user/$', 'reg_kits.views.user', name="user"),
    url(r'^reg_kits/user/form/$', 'reg_kits.views.user_form', name="user_form"),
    url(r'^reg_kits/user/form/(?P<user_id>\d+)$', 'reg_kits.views.user_form', name="user_form"),
    url(r'^reg_kits/user/delete/$', 'reg_kits.views.user_delete', name="user_delete"),
    url(r'^reg_kits/user/submit/$', 'reg_kits.views.user_submit', name="user_submit"),
    url(r'^reg_kits/user/send_invite_email/$', 'reg_kits.views.send_invite_email', name="send_invite_email"),
    url(r'^reg_kits/user/modify_status$', 'reg_kits.views.user_modify_status', name="user_modify_status"),

    url(r'^reg_kits/import_user_submit/$', 'reg_kits.views.import_user_submit', name="import_user_submit"),

    url(r'^reg_kits/download_user_csv/$', 'reg_kits.views.download_user_csv', name="download_user_csv"),
    url(r'^reg_kits/download_user_excel/$', 'reg_kits.views.download_user_excel', name="download_user_excel"),

    url(r'^reg_kits/download_school_csv/$', 'reg_kits.views.download_school_csv', name="download_school_csv"),
    url(r'^reg_kits/download_school_excel/$', 'reg_kits.views.download_school_excel', name="download_school_excel"),

    url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/people/$', 'people.views.people', name="people"),
    url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/my_people/$', 'people.views.my_people', name="my_people"),

    # url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/chat/$', 'chat.views.index', name="chat"),

    url(r'^research_pedagogy$', 'branding.views.intro_research', name="intro_research"),
    url(r'^our_team$', 'branding.views.intro_ourteam', name="intro_ourteam"),
    url(r'^what_is_pepper$', 'branding.views.what_is', name="what_is"),

    url(r'^people/$', 'people.views.people', name="people"),
    url(r'^my_people/$', 'people.views.my_people', name="my_people"),
    url(r'^add_people/$', 'people.views.add_people', name="add_people"),
    url(r'^remove_people/$', 'people.views.del_people', name="del_people"),

    url(r'^resource_library_global$', 'access_resource_library.views.index_list', name="access_resource_library_list"),
    url(r'^resource_library_global/states/$', 'access_resource_library.views.states', name="^resource_library_global_states"),
    url(r'^resource_library_global/districts/$', 'access_resource_library.views.districts', name="^resource_library_global_districts"),
    url(r'^course_libraries$', 'access_resource_library.views.index', name="access_resource_library"),
    url(r'^resource_library_global/resources/$', 'access_resource_library.views.resources', name="resource_library_global_resources"),
    url(r'^resource_library_global/generic_resources/$', 'access_resource_library.views.generic_resources', name="resource_library_global_generic_resources"),

    url(r'^communities/$', 'communities.views.communities', name="communities"),

    url(r'^community/(?P<community_id>[a-zA-Z0-9_]+)$', 'communities.views.community', name='community_view'),
    url(r'^community/(?P<community_id>[a-zA-Z0-9_]+)/discussion-list$', 'communities.views.discussion_list', name='community_discussion_list'),
    url(r'^community/discussion/(?P<discussion_id>[0-9]+)$', 'communities.views.discussion', name='community_discussion_view'),
    url(r'^community/discussion/new/add$', 'communities.views.discussion_add', name='community_discussion_add'),
    url(r'^community/discussion/edit$', 'communities.views.discussion_edit', name='community_discussion_edit'),
    url(r'^community/reply/edit$', 'communities.views.reply_edit', name='community_reply_edit'),
    url(r'^community/discussion/(?P<discussion_id>[0-9]+)/reply$', 'communities.views.discussion_reply', name='community_discussion_reply'),
    url(r'^community/discussion/(?P<discussion_id>[0-9]+)/delete$', 'communities.views.discussion_delete', name='community_discussion_delete'),
    url(r'^community/discussion/(?P<reply_id>[0-9]+)/reply-delete$', 'communities.views.discussion_reply_delete', name='community_discussion_reply_delete'),

    url(r'^community/post/showlikes', 'communities.views.get_full_likes', name='community_get_full_likes'),
    url(r'^community/post/check$', 'communities.views.check_content_priority', name='community_check_content_priority'),
    url(r'^community/post/like$', 'communities.views.submit_new_like', name='community_submit_new_like'),
    url(r'^community/post/new$', 'communities.views.submit_new_post', name='community_submit_new_post'),
    url(r'^community/post/get$', 'communities.views.get_posts', name='community_get_posts'),
    url(r'^community/discussion/get$', 'communities.views.get_discussions', name='community_get_discussions'),
    url(r'^community/post/comment', 'communities.views.submit_new_comment', name='community_submit_new_comment'),
    url(r'^community/post/lookup', 'communities.views.lookup_name', name='community_lookup_name'),
    url(r'^community/ask/expert', 'communities.views.email_expert', name='community_ask_an_expert'),
    url(r'^community/delete/comment', 'communities.views.delete_comment', name='community_delete_comment'),
    url(r'^community/delete/post', 'communities.views.delete_post', name='community_delete_post'),
    # @author:scott
    # @date:2017-02-27
    url(r'^community/top/post', 'communities.views.top_post', name='community_top_post'),
    # @end
    url(r'^communities/add$', 'communities.views.community_edit', name='community_add'),
    url(r'^communities/process$', 'communities.views.community_edit_process', name='community_edit_process'),
    url(r'^communities/check-user$', 'communities.views.community_check_user', name='community_check_user'),
    url(r'^community/(?P<community_id>[a-zA-Z0-9_]+)/edit$', 'communities.views.community_edit', name='community_edit'),
    url(r'^community/(?P<community_id>[a-zA-Z0-9_]+)/delete$', 'communities.views.community_delete', name='community_delete'),
    url(r'^community/(?P<community_id>[a-zA-Z0-9_]+)/join/$', 'communities.views.community_join', name='community_join'),
    url(r'^community/(?P<community_id>[a-zA-Z0-9_]+)/leave/$', 'communities.views.community_leave', name='community_leave'),
    url(r'^community/(?P<community_id>[a-zA-Z0-9_]+)/manage_member/$', 'communities.views.community_manage_member', name='community_mange_member'),
    url(r'^community/(?P<community_id>[a-zA-Z0-9_]+)/tables/get_add_user_rows/$', 'communities.views.get_add_user_rows', name="community_get_add_user_rows"),
    url(r'^community/(?P<community_id>[a-zA-Z0-9_]+)/tables/get_remove_user_rows/$', 'communities.views.get_remove_user_rows', name="community_get_remove_user_rows"),

    url(r'^polls/(?P<poll_type>[a-zA-Z0-9_]+)/(?P<poll_id>[0-9]+)$', 'polls.views.poll_view', name='poll_view'),
    url(r'^polls/form/(?P<poll_type>[a-zA-Z0-9_]+)$', 'polls.views.poll_form_view', name='poll_form_view'),
    url(r'^polls/save/(?P<poll_type>[a-zA-Z0-9_]+)$', 'polls.views.poll_form_submit', name='poll_form_submit'),
    url(r'^polls/vote$', 'polls.views.poll_vote', name='poll_vote'),

    url(r'^contact_us_submit/$', 'branding.views.contact_us_submit', name="contact_us_submit"),
    url(r'^contact_us_modal_submit/$', 'branding.views.contact_us_modal_submit', name="contact_us_modal_submit"),

    url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^\/]+)/portfolio/my_discussions/(?P<user_id>[^/]+)$',
             'portfolio.views.my_discussions', name="portfolio_my_discussions"),

    #url(r'^download_certificate/$', 'student.views.download_certificate', name="download_certificate"),
    url(r'^latest_news/$', 'student.views.latest_news', name="latest_news"),
    url(r'^access_resource_library/$', 'access_resource_library.views.index', name="access_resource_library"),
    # certificate view
    url(r'^update_certificate$', 'certificates.views.update_certificate'),
    url(r'^certificate_preview$', 'certificates.views.certificate_preview', name="certificate_preview"),
    url(r'^(?P<course_id>[^/]+/[^/]+/[^/]+)/(?P<completed_time>[^/]+)/download_certificate$', 'certificates.views.download_certificate', name="download_certificate"),
    url(r'^course_credits$', 'certificates.views.course_credits', name="course_credits"),

    url(r'^download_certificate_demo$', 'certificates.views.download_certificate_demo'),
    url(r'^$', 'branding.views.index', name="root"),   # Main marketing page, or redirect to courseware
    url(r'^dashboard$', 'student.views.dashboard', name="dashboard"),
    url(r'^dashboard/get_pepper_stats$', 'student.views.get_pepper_stats', name="get_pepper_stats"),
    url(r'^newdashboard$', 'student.newdashboard.newdashboard', name="newdashboard"),
    url(r'^my_courses$', 'student.newdashboard.my_courses', name="my_courses"),


    url(r'^upload_photo$', 'student.views.upload_photo', name="upload_photo"),

    url(r'^user_photo/$', 'student.views.user_photo', name="user_photo"),
    url(r'^user_photo/(?P<user_id>\d+)$', 'student.views.user_photo', name="user_photo"),

    url(r'^dashboard/(?P<user_id>\d+)$', 'student.views.dashboard', name="dashboard"),
    url(r'^login$', 'student.views.signin_user', name="signin_user"),

    url(r'^user_information$', 'student.newdashboard.user_information', name="user_information"),
    url(r'^user_information/(?P<user_id>\d+)$', 'student.newdashboard.user_information', name="user_information"),

    url(r'^interactive_update/get_info$', 'notifications.views.get_interactive_update', name="get_interactive_update"),
    url(r'^interactive_update/get_range_info$', 'notifications.views.get_interactive_update_range', name="get_interactive_update_range"),
    url(r'^interactive_update/save_info$', 'notifications.views.save_interactive_update', name="save_interactive_update"),
    url(r'^interactive_update/set_info$', 'notifications.views.set_interactive_update', name="set_interactive_update"),
    url(r'^interactive_update/del_info$', 'notifications.views.del_interactive_update', name="del_interactive_update"),
    url(r'^message_board/get_info$', 'notifications.views.get_message', name="get_message"),
    url(r'^message_board/save_info$', 'notifications.views.save_message', name="save_message"),
    url(r'^message_board/upload_image$', 'notifications.views.upload_image', name="upload_message_image"),
    url(r'^my_chunks$', 'my_chunks.views.mychunks', name="mychunks"),
    url(r'^my_chunks/get_info_range$', 'my_chunks.views.get_mychunks_range', name="get_mychunks_range"),
    url(r'^my_chunks/get_info$', 'my_chunks.views.get_mychunk', name="get_mychunk"),
    url(r'^my_chunks/save_info$', 'my_chunks.views.save_mychunk', name="save_mychunk"),
    url(r'^my_chunks/del_info$', 'my_chunks.views.del_mychunk', name="del_mychunk"),
    url(r'^my_chunks/set_rate$', 'my_chunks.views.set_rate', name="set_rate"),
    url(r'^my_chunks/get_integrate_rate$', 'my_chunks.views.get_integrate_rate', name="get_integrate_rate"),
    url(r'^register/$', 'student.views.register_user', name="register_user"),
    url(r'^register/(?P<activation_key>[^/]*)/$', 'student.views.register_user', name="register_user"),

    url(r'^admin_dashboard$', 'dashboard.views.dashboard'),
    url(r'^change_email$', 'student.views.change_email_request', name="change_email"),
    url(r'^email_confirm/(?P<key>[^/]*)$', 'student.views.confirm_email_change'),

    url(r'^change_percent_lunch$', 'student.views.change_percent_lunch', name="change_percent_lunch"),
    url(r'^change_percent_iep$', 'student.views.change_percent_iep', name="change_percent_iep"),
    url(r'^change_percent_eng_learner$', 'student.views.change_percent_eng_learner', name="change_percent_eng_learner"),

    url(r'^change_name$', 'student.views.change_name_request', name="change_name"),
    url(r'^change_skype_name$', 'student.views.change_skype_name', name="change_skype_name"),
    url(r'^change_school$', 'student.views.change_school_request', name="change_school"),
    url(r'^change_change_grade_level$', 'student.views.change_grade_level_request', name="change_grade_level"),
    url(r'^change_major_subject_area$', 'student.views.change_major_subject_area_request', name="change_major_subject_area"),
    url(r'^change_bio$', 'student.views.change_bio_request', name="change_bio"),

    url(r'^change_years_in_education$', 'student.views.change_years_in_education_request', name="change_years_in_education"),

    url(r'^accept_name_change$', 'student.views.accept_name_change'),
    url(r'^reject_name_change$', 'student.views.reject_name_change'),
    url(r'^pending_name_changes$', 'student.views.pending_name_changes'),
    url(r'^event$', 'track.views.user_track'),
    url(r'^t/(?P<template>[^/]*)$', 'static_template_view.views.index'),   # TODO: Is this used anymore? What is STATIC_GRAB?
    url(r'^accounts/login$', 'student.views.accounts_login', name="accounts_login"),
    url(r'^login_ajax$', 'student.views.login_user', name="login"),
    url(r'^login_ajax/(?P<error>[^/]*)$', 'student.views.login_user'),
    url(r'^logout$', 'student.views.logout_user', name='logout'),
    url(r'^create_account$', 'student.views.create_account', name='create_account'),
    url(r'^activate/(?P<key>[^/]*)$', 'student.views.activate_account', name="activate"),
    url(r'^begin_exam_registration/(?P<course_id>[^/]+/[^/]+/[^/]+)$', 'student.views.begin_exam_registration', name="begin_exam_registration"),
    url(r'^create_exam_registration$', 'student.views.create_exam_registration'),
    url(r'^password_reset/$', 'student.views.password_reset', name='password_reset'),
    ## Obsolete Django views for password resets
    ## TODO: Replace with Mako-ized views
    url(r'^password_change/$', django.contrib.auth.views.password_change,
        name='auth_password_change'),
    url(r'^password_change_done/$', django.contrib.auth.views.password_change_done,
        name='auth_password_change_done'),
    url(r'^password_reset_confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'student.views.password_reset_confirm_wrapper',
        name='auth_password_reset_confirm'),
    url(r'^password_reset_complete/$', django.contrib.auth.views.password_reset_complete,
        name='auth_password_reset_complete'),
    url(r'^password_reset_done/$', django.contrib.auth.views.password_reset_done,
        name='auth_password_reset_done'),
    url(r'^heartbeat$', include('heartbeat.urls')),
    url(r'^user_api/', include('user_api.urls')),
)
js_info_dict = {
    'domain': 'djangojs',
    'packages': ('lms',),
}
urlpatterns += (
    # Serve catalog of localized strings to be rendered by Javascript
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
)
#Semi-static views (these need to be rendered and have the login bar, but don't change)
urlpatterns += (
    url(r'^404$', 'static_template_view.views.render',
        {'template': '404.html'}, name="404"),
)
# Semi-static views only used by edX, not by themes
if not settings.MITX_FEATURES["USE_CUSTOM_THEME"]:
    urlpatterns += (
        url(r'^jobs$', 'static_template_view.views.render',
            {'template': 'jobs.html'}, name="jobs"),
        url(r'^press$', 'student.views.press', name="press"),
        url(r'^media-kit$', 'static_template_view.views.render',
            {'template': 'media-kit.html'}, name="media-kit"),
        url(r'^faq$', 'static_template_view.views.render',
            {'template': 'faq.html'}, name="faq_edx"),
        url(r'^help$', 'static_template_view.views.render',
            {'template': 'help.html'}, name="help_edx"),
        # TODO: (bridger) The copyright has been removed until it is updated for edX
        # url(r'^copyright$', 'static_template_view.views.render',
        #     {'template': 'copyright.html'}, name="copyright"),
        #Press releases
        url(r'^press/([_a-zA-Z0-9-]+)$', 'static_template_view.views.render_press_release', name='press_release'),
        # Favicon
        (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/images/favicon.ico'}),
        url(r'^submit_feedback$', 'util.views.submit_feedback'),
        url(r'^notifications$', 'notifications.views.notifications', name="notifications"),

    )
# Only enable URLs for those marketing links actually enabled in the
# settings. Disable URLs by marking them as None.
for key, value in settings.MKTG_URL_LINK_MAP.items():
    # Skip disabled URLs
    if value is None:
        continue
    # These urls are enabled separately
    if key == "ROOT" or key == "COURSES" or key == "FAQ":
        continue
    # Make the assumptions that the templates are all in the same dir
    # and that they all match the name of the key (plus extension)
    template = "%s.html" % key.lower()
    # To allow theme templates to inherit from default templates,
    # prepend a standard prefix
    if settings.MITX_FEATURES["USE_CUSTOM_THEME"]:
        template = "theme-" + template
    # Make the assumption that the URL we want is the lowercased
    # version of the map key
    urlpatterns += (url(r'^%s' % key.lower(),
                        'static_template_view.views.render',
                        {'template': template}, name=value),)
if settings.PERFSTATS:
    urlpatterns += (url(r'^reprofile$', 'perfstats.views.end_profile'),)
# Multicourse wiki (Note: wiki urls must be above the courseware ones because of
# the custom tab catch-all)
if settings.WIKI_ENABLED:
    from wiki.urls import get_pattern as wiki_pattern
    from django_notify.urls import get_pattern as notify_pattern
    # Note that some of these urls are repeated in course_wiki.course_nav. Make sure to update
    # them together.
    urlpatterns += (
        # First we include views from course_wiki that we use to override the default views.
        # They come first in the urlpatterns so they get resolved first
        url('^wiki/create-root/$', 'course_wiki.views.root_create', name='root_create'),
        url(r'^wiki/', include(wiki_pattern())),
        url(r'^notify/', include(notify_pattern())),
        # These urls are for viewing the wiki in the context of a course. They should
        # never be returned by a reverse() so they come after the other url patterns
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/course_wiki/?$',
            'course_wiki.views.course_wiki_redirect', name="course_wiki"),
        url(r'^courses/(?:[^/]+/[^/]+/[^/]+)/wiki/', include(wiki_pattern())),
    )
if settings.COURSEWARE_ENABLED:
    urlpatterns += (
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/jump_to/(?P<location>.*)$',
            'courseware.views.jump_to', name="jump_to"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/jump_to_id/(?P<module_id>.*)$',
            'courseware.views.jump_to_id', name="jump_to_id"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/modx/(?P<location>.*?)/(?P<dispatch>[^/]*)$',
            'courseware.module_render.modx_dispatch',
            name='modx_dispatch'),
        # Software Licenses
        # TODO: for now, this is the endpoint of an ajax replay
        # service that retrieve and assigns license numbers for
        # software assigned to a course. The numbers have to be loaded
        # into the database.
        url(r'^software-licenses$', 'licenses.views.user_software_license', name="user_software_license"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/xqueue/(?P<userid>[^/]*)/(?P<mod_id>.*?)/(?P<dispatch>[^/]*)$',
            'courseware.module_render.xqueue_callback',
            name='xqueue_callback'),
        url(r'^change_setting$', 'student.views.change_setting',
            name='change_setting'),
        # TODO: These views need to be updated before they work
        url(r'^calculate$', 'util.views.calculate'),
        # TODO: We should probably remove the circuit package. I believe it was only used in the old way of saving wiki circuits for the wiki
        # url(r'^edit_circuit/(?P<circuit>[^/]*)$', 'circuit.views.edit_circuit'),
        # url(r'^save_circuit/(?P<circuit>[^/]*)$', 'circuit.views.save_circuit'),
        url(r'^courses/?$', 'branding.views.courses', name="courses"),
        url(r'^nccourses/?$', 'branding.views.newgroup_courses', name="newgroup_courses"),
        url(r'^nccourses-list$', 'courseware.views.dpicourse_list', name="nccourse_list"),
        url(r'^courses-list$', 'courseware.views.course_list', name="course_list"),
        url(r'^courses/states$', 'courseware.views.states', name="courses_states"),
        url(r'^courses/districts$', 'courseware.views.districts', name="courses_districts"),
        url(r'^courses/leadership$', 'courseware.views.collections', name="courses_collections"),
        url(r'^what_is$', 'branding.views.what_is', name="what_is"),
        url(r'^demo1$', 'branding.views.demo1', name="demo1"),
        url(r'^demo2$', 'branding.views.demo2', name="demo2"),
        url(r'^demo3$', 'branding.views.demo3', name="demo3"),
        url(r'^demo4$', 'branding.views.demo4', name="demo4"),
        url(r'^districts$', 'branding.views.districts', name="districts"),
        url(r'^contact$', 'branding.views.contact', name="contact_us"),
        url(r'^intro$', 'branding.views.intro', name="intro"),
        url(r'^intro_research$', 'branding.views.intro_research', name="intro_research"),
        url(r'^intro_ourteam$', 'branding.views.intro_ourteam', name="intro_ourteam"),
        url(r'^intro_faq$', 'branding.views.intro_faq', name="intro_faq"),
        url(r'^change_enrollment$',
            'student.views.change_enrollment', name="change_enrollment"),
        url(r'^change_email_settings$', 'student.views.change_email_settings', name="change_email_settings"),
        #About the course
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/about$',
            'courseware.views.course_about', name="about_course"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/cabout$',
            'courseware.views.cabout', name="cabout"),
        #View for mktg site (kept for backwards compatibility TODO - remove before merge to master)
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/mktg-about$',
            'courseware.views.mktg_course_about', name="mktg_about_course"),
        #View for mktg site
        url(r'^mktg/(?P<course_id>.*)$',
            'courseware.views.mktg_course_about', name="mktg_about_course"),
        #Inside the course
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/$',
            'courseware.views.course_info', name="course_root"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/info$',
            'courseware.views.course_info', name="info"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/syllabus$',
            'courseware.views.syllabus', name="syllabus"),   # TODO arjun remove when custom tabs in place, see courseware/courses.py
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/book/(?P<book_index>\d+)/$',
            'staticbook.views.index', name="book"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/book/(?P<book_index>\d+)/(?P<page>\d+)$',
            'staticbook.views.index', name="book"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/pdfbook/(?P<book_index>\d+)/$',
            'staticbook.views.pdf_index', name="pdf_book"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/pdfbook/(?P<book_index>\d+)/(?P<page>\d+)$',
            'staticbook.views.pdf_index', name="pdf_book"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/pdfbook/(?P<book_index>\d+)/chapter/(?P<chapter>\d+)/$',
            'staticbook.views.pdf_index', name="pdf_book"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/pdfbook/(?P<book_index>\d+)/chapter/(?P<chapter>\d+)/(?P<page>\d+)$',
            'staticbook.views.pdf_index', name="pdf_book"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/htmlbook/(?P<book_index>\d+)/$',
            'staticbook.views.html_index', name="html_book"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/htmlbook/(?P<book_index>\d+)/chapter/(?P<chapter>\d+)/$',
            'staticbook.views.html_index', name="html_book"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/courseware/?$',
            'courseware.views.index', name="courseware"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/courseware/(?P<chapter>[^/]*)/$',
            'courseware.views.index', name="courseware_chapter"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/courseware/(?P<chapter>[^/]*)/(?P<section>[^/]*)/$',
            'courseware.views.index', name="courseware_section"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/courseware/(?P<chapter>[^/]*)/(?P<section>[^/]*)/(?P<position>[^/]*)/?$',
            'courseware.views.index', name="courseware_position"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/progress$',
            'courseware.views.progress', name="progress"),
        url(r'^courseware/drop_districts$', 'courseware.views.drop_districts', name="courseware_drop_districts"),#20160324 add
        # Takes optional student_id for instructor use--shows profile as that student sees it.
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/progress/(?P<student_id>[^/]*)/$',
            'courseware.views.progress', name="student_progress"),
        # For the instructor
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/instructor$',
            'instructor.views.legacy.instructor_dashboard', name="instructor_dashboard"),

        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/portfolio/about_me$',
            'portfolio.views.about_me', name="portfolio_about_me"),

        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/portfolio/about_me/(?P<user_id>[^/]+)$',
            'portfolio.views.about_me', name="portfolio_about_me"),

        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/portfolio/my_coursework/(?P<user_id>[^/]+)$',
            'portfolio.views.journal_and_reflections', name="portfolio_journal_and_reflections"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/portfolio/my_coursework/(?P<user_id>[^/]+)/(?P<chapter_id>[^/]+)$',
            'portfolio.views.journal_and_reflections', name="portfolio_journal_and_reflections"),

        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/portfolio/uploads$',
            'portfolio.views.uploads', name="portfolio_uploads"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/resource_library$',
            'courseware.views.resource_library', name="resource_library"),
        # see ENABLE_INSTRUCTOR_BETA_DASHBOARD section for more urls
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/gradebook$',
            'instructor.views.legacy.gradebook', name='gradebook'),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/grade_summary$',
            'instructor.views.legacy.grade_summary', name='grade_summary'),

        url(r'^instructor/dashboard/progress/(?P<course_id>[^/]+/[^/]+/[^/]+)/(?P<username>[^/]*)$',
             'instructor.views.instructor_dashboard.student_course_progress', name="view_student_process"),

        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/staff_grading$',
            'open_ended_grading.views.staff_grading', name='staff_grading'),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/staff_grading/get_next$',
            'open_ended_grading.staff_grading_service.get_next', name='staff_grading_get_next'),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/staff_grading/save_grade$',
            'open_ended_grading.staff_grading_service.save_grade', name='staff_grading_save_grade'),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/staff_grading/save_grade$',
            'open_ended_grading.staff_grading_service.save_grade', name='staff_grading_save_grade'),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/staff_grading/get_problem_list$',
            'open_ended_grading.staff_grading_service.get_problem_list', name='staff_grading_get_problem_list'),
        # Open Ended problem list
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/open_ended_problems$',
            'open_ended_grading.views.student_problem_list', name='open_ended_problems'),
        # Open Ended flagged problem list
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/open_ended_flagged_problems$',
            'open_ended_grading.views.flagged_problem_list', name='open_ended_flagged_problems'),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/open_ended_flagged_problems/take_action_on_flags$',
            'open_ended_grading.views.take_action_on_flags', name='open_ended_flagged_problems_take_action'),
        # Cohorts management
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/cohorts$',
            'course_groups.views.list_cohorts', name="cohorts"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/cohorts/add$',
            'course_groups.views.add_cohort',
            name="add_cohort"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/cohorts/(?P<cohort_id>[0-9]+)$',
            'course_groups.views.users_in_cohort',
            name="list_cohort"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/cohorts/(?P<cohort_id>[0-9]+)/add$',
            'course_groups.views.add_users_to_cohort',
            name="add_to_cohort"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/cohorts/(?P<cohort_id>[0-9]+)/delete$',
            'course_groups.views.remove_user_from_cohort',
            name="remove_from_cohort"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/cohorts/debug$',
            'course_groups.views.debug_cohort_mgmt',
            name="debug_cohort_mgmt"),
        # Open Ended Notifications
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/open_ended_notifications$',
            'open_ended_grading.views.combined_notifications', name='open_ended_notifications'),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/peer_grading$',
            'open_ended_grading.views.peer_grading', name='peer_grading'),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/notes$', 'notes.views.notes', name='notes'),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/notes/', include('notes.urls')),
    )
    # allow course staff to change to student view of courseware
    if settings.MITX_FEATURES.get('ENABLE_MASQUERADE'):
        urlpatterns += (
            url(r'^masquerade/(?P<marg>.*)$', 'courseware.masquerade.handle_ajax', name="masquerade-switch"),
        )
    # discussion forums live within courseware, so courseware must be enabled first
    if settings.MITX_FEATURES.get('ENABLE_DISCUSSION_SERVICE'):
        urlpatterns += (
            url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/news$',
                'courseware.views.news', name="news"),
            url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/discussion/',
                include('django_comment_client.urls')),
            url(r'^notification_prefs/enable/', 'notification_prefs.views.ajax_enable'),
            url(r'^notification_prefs/disable/', 'notification_prefs.views.ajax_disable'),
            url(r'^notification_prefs/status/', 'notification_prefs.views.ajax_status'),
            url(r'^notification_prefs/unsubscribe/(?P<token>[a-zA-Z0-9-_=]+)/', 'notification_prefs.views.unsubscribe'),
        )
    urlpatterns += (
        # This MUST be the last view in the courseware--it's a catch-all for custom tabs.
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/(?P<tab_slug>[^/]+)/$',
        'courseware.views.static_tab', name="static_tab"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/(?P<tab_slug>[^/]+)/(?P<is_global>global)/$',
        'courseware.views.static_tab', name="static_tab"),
    )
    if settings.MITX_FEATURES.get('ENABLE_STUDENT_HISTORY_VIEW'):
        urlpatterns += (
            url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/submission_history/(?P<student_username>[^/]*)/(?P<location>.*?)$',
                'courseware.views.submission_history',
                name='submission_history'),
        )
if settings.COURSEWARE_ENABLED and settings.MITX_FEATURES.get('ENABLE_INSTRUCTOR_BETA_DASHBOARD'):
    urlpatterns += (
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/instructor_dashboard$',
            'instructor.views.instructor_dashboard.instructor_dashboard_2', name="instructor_dashboard_2"),
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/instructor_dashboard/api/',
            include('instructor.views.api_urls'))
    )

if settings.DEBUG or settings.MITX_FEATURES.get('ENABLE_DJANGO_ADMIN_SITE'):
    ## Jasmine and admin
    urlpatterns += (url(r'^prod_admin/', include(admin.site.urls)),)

if not settings.DEBUG:
    admin.autodiscover()
    urlpatterns += (url(r'^prod_admin/', include(admin.site.urls)),)

if settings.MITX_FEATURES.get('AUTH_USE_OPENID'):
    urlpatterns += (
        url(r'^openid/login/$', 'django_openid_auth.views.login_begin', name='openid-login'),
        url(r'^openid/complete/$', 'external_auth.views.openid_login_complete', name='openid-complete'),
        url(r'^openid/logo.gif$', 'django_openid_auth.views.logo', name='openid-logo'),
    )
if settings.MITX_FEATURES.get('AUTH_USE_SHIB'):
    urlpatterns += (
        url(r'^shib-login/$', 'external_auth.views.shib_login', name='shib-login'),
    )
if settings.MITX_FEATURES.get('AUTH_USE_CAS'):
    urlpatterns += (
        url(r'^cas-auth/login/$', 'external_auth.views.cas_login', name="cas-login"),
        url(r'^cas-auth/logout/$', 'django_cas.views.logout', {'next_page': '/'}, name="cas-logout"),
    )
if settings.MITX_FEATURES.get('RESTRICT_ENROLL_BY_REG_METHOD'):
    urlpatterns += (
        url(r'^course_specific_login/(?P<course_id>[^/]+/[^/]+/[^/]+)/$',
            'external_auth.views.course_specific_login', name='course-specific-login'),
        url(r'^course_specific_register/(?P<course_id>[^/]+/[^/]+/[^/]+)/$',
            'external_auth.views.course_specific_register', name='course-specific-register'),
    )
# Shopping cart
urlpatterns += (
    url(r'^shoppingcart/', include('shoppingcart.urls')),
)
if settings.MITX_FEATURES.get('AUTH_USE_OPENID_PROVIDER'):
    urlpatterns += (
        url(r'^openid/provider/login/$', 'external_auth.views.provider_login', name='openid-provider-login'),
        url(r'^openid/provider/login/(?:.+)$', 'external_auth.views.provider_identity', name='openid-provider-login-identity'),
        url(r'^openid/provider/identity/$', 'external_auth.views.provider_identity', name='openid-provider-identity'),
        url(r'^openid/provider/xrds/$', 'external_auth.views.provider_xrds', name='openid-provider-xrds')
    )
if settings.MITX_FEATURES.get('ENABLE_PEARSON_LOGIN', False):
    urlpatterns += url(r'^testcenter/login$', 'external_auth.views.test_center_login'),
if settings.MITX_FEATURES.get('ENABLE_LMS_MIGRATION'):
    urlpatterns += (
        url(r'^migrate/modules$', 'lms_migration.migrate.manage_modulestores'),
        url(r'^migrate/reload/(?P<reload_dir>[^/]+)$', 'lms_migration.migrate.manage_modulestores'),
        url(r'^migrate/reload/(?P<reload_dir>[^/]+)/(?P<commit_id>[^/]+)$', 'lms_migration.migrate.manage_modulestores'),
        url(r'^gitreload$', 'lms_migration.migrate.gitreload'),
        url(r'^gitreload/(?P<reload_dir>[^/]+)$', 'lms_migration.migrate.gitreload'),
    )
if settings.MITX_FEATURES.get('ENABLE_SQL_TRACKING_LOGS'):
    urlpatterns += (
        url(r'^event_logs$', 'track.views.view_tracking_log'),
        url(r'^event_logs/(?P<args>.+)$', 'track.views.view_tracking_log'),
    )
if settings.MITX_FEATURES.get('ENABLE_SERVICE_STATUS'):
    urlpatterns += (
        url(r'^status/', include('service_status.urls')),
    )
if settings.MITX_FEATURES.get('ENABLE_INSTRUCTOR_BACKGROUND_TASKS'):
    urlpatterns += (
        url(r'^instructor_task_status/$', 'instructor_task.views.instructor_task_status', name='instructor_task_status'),
    )
if settings.MITX_FEATURES.get('RUN_AS_ANALYTICS_SERVER_ENABLED'):
    urlpatterns += (
        url(r'^edinsights_service/', include('edinsights.core.urls')),
    )
    import edinsights.core.registry
# FoldIt views
urlpatterns += (
    # The path is hardcoded into their app...
    url(r'^comm/foldit_ops', 'foldit.views.foldit_ops', name="foldit_ops"),
)
if settings.MITX_FEATURES.get('ENABLE_DEBUG_RUN_PYTHON'):
    urlpatterns += (
        url(r'^debug/run_python', 'debug.views.run_python'),
    )
# Crowdsourced hinting instructor manager.
if settings.MITX_FEATURES.get('ENABLE_HINTER_INSTRUCTOR_VIEW'):
    urlpatterns += (
        url(r'^courses/(?P<course_id>[^/]+/[^/]+/[^/]+)/hint_manager$',
            'instructor.hint_manager.hint_manager', name="hint_manager"),
    )
# enable automatic login
if settings.MITX_FEATURES.get('AUTOMATIC_AUTH_FOR_TESTING'):
    urlpatterns += (
        url(r'^auto_auth$', 'student.views.auto_auth'),
    )
urlpatterns = patterns(*urlpatterns)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#Custom error pages
handler404 = 'static_template_view.views.render_404'
handler500 = 'static_template_view.views.render_500'


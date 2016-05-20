// Options for the TableSorter tables.
var pagerOptions = {
    container: '',
    // output string - default is '{page}/{totalPages}'; possible variables: {page}, {totalPages}, {startRow}, {endRow} and {totalRows}
    output: '{startRow} - {endRow} / {filteredRows} ({totalRows})',
    fixedHeight: false,
    removeRows: false,
    page: 0,
    size: 10,
    ajaxUrl: null,
    customAjaxUrl: function(table, url) { return url; },
    ajaxObject: { dataType: 'json' },
    ajaxProcessing: null,
    processAjaxOnInit: true,
    pageReset: 0,
    countChildRows: false,
    cssNext: '.next', // next page arrow
    cssPrev: '.prev', // previous page arrow
    cssFirst: '.first', // go to first page arrow
    cssLast: '.last', // go to last page arrow
    cssGoto: '.gotoPage', // select dropdown to allow choosing a page
    cssPageDisplay: '.pagedisplay', // location of where the "output" is displayed
    cssPageSize: '.pagesize', // page size selector - select dropdown that sets the "size" option
    cssDisabled: 'disabled', // Note there is no period "." in front of this class name
    cssErrorRow: 'tablesorter-errorRow' // ajax error information row
};
var tablesorterOptions = {
    theme: 'blue',
    widthFixed: true,
    widgets: ["zebra", "filter"],
    widgetOptions: {
        filter_columnFilters: true,
        filter_placeholder: {search: 'Search...'},
        filter_saveFilters: false
    }
};

// A loading status throbber setup.
// Initial object.
function LoadingStatus(list) {
    var self = this;
    setTimeout(function () {
        if (!self.checkStatus()) {
            self.showLoader();
        }
    }, 200);
    this.$list = {};
    $.each(list, function(i, v) {
        self.$list[v] = true;
    });
}
// Shows the loader.
LoadingStatus.prototype.showLoader = function () {
    if (!this.$loader) {
        this.$loader = $('<div class="lean-overlay"><img class="loading" src="/static/images/loading.gif"></div>');
        this.$loader.appendTo(document.body);
    }
    this.$loader.css('display','block');
};
// Hides the loader.
LoadingStatus.prototype.hideLoader = function () {
    if (this.$loader) {
        this.$loader.remove();
        this.$loader = null;
    }
};
// Checks the status of all operations.
LoadingStatus.prototype.checkStatus = function () {
    var status = true;
    $.each(this.$list, function(i, v) {
        if (v) {
            status = false;
        }
    });
    return status;
};
// Sets the current status for an operation.
LoadingStatus.prototype.setStatus = function (name) {
    this.$list[name] = false;
    this.loaderCheck();
};
// Checks the status and hides the loader if appropriate.
LoadingStatus.prototype.loaderCheck = function () {
    if (this.checkStatus()) {
        this.hideLoader();
    }
};

// Checks to see if the target/action is already in use.
function checkPermission(name, target, action) {
    var valid = true;
    var error = '';
    $.ajax({
        url: permissions_check_url,
        type: 'GET',
        async: false,
        data: {name: name, target: target, action: action},
        success: function(data) {
            valid = data.Valid;
            error = data.Error;
        }
    });
    if (valid) {
        return true;
    } else {
        return error;
    }
}

// Checks to see if this group exists at the access level.
function checkGroup(name, group_type) {
    var valid = true;
    var error = '';
    $.ajax({
        url: group_check_url,
        type: 'GET',
        async: false,
        data: {name: name, type: group_type},
        success: function(data) {
            valid = data.Valid;
            error = data.Error;
        }
    });
    if (valid) {
        return true;
    } else {
        return error;
    }
}

// Validate the data in the permission submit form.
function validatePermissionForm(type) {
    $('.error-box').removeClass('error-box');
    var valid = true;
    var errors = ['The following errors occurred:\n'];
    var name = $('#new-permission-submit input[name="name"]');
    if (!/[A-Za-z0-9]+/.test(name.val())) {
        valid = false;
        errors.push('Name is required.');
        name.addClass('error-box');
    }
    var target = $('#new-permission-submit input[name="target"]');
    if (!/[A-Za-z0-9]+/.test(target.val())) {
        valid = false;
        errors.push('Target is required.');
        target.addClass('error-box');
    }
    var action = $('#new-permission-submit input[name="action"]');
    if (!/[A-Za-z0-9]+/.test(action.val())) {
        valid = false;
        errors.push('Action is required.');
        action.addClass('error-box');
    }
    if (type == 'add') {
        var check_permission = checkPermission(name.val(), target.val(), action.val());
        if (check_permission !== true) {
            valid = false;
            errors.push(check_permission);
            name.addClass('error-box');
            target.addClass('error-box');
            action.addClass('error-box');
        }
    }
    if (!valid) {
        var error = errors.join('\n');
        alert(error);
    }
    return valid;
}

// Validate the data in the group submission form.
function validateGroupForm(type) {
    $('.error-box').removeClass('error-box');
    var valid = true;
    var errors = ['The following errors occurred:\n'];
    var name = $('#new-group-submit input[name="name"]');
    var access_level = $('#new-group-submit select[name="access_level"]');
    if (!/[A-Za-z0-9]+/.test(name.val())) {
        valid = false;
        errors.push('Name is required.');
        name.addClass('error-box');
    }
    if (type == 'add') {
        var check_group = checkGroup(name.val(), access_level.val());
        if (check_group !== true) {
            valid = false;
            errors.push(check_group);
            name.addClass('error-box');
            access_level.addClass('error-box');
        }
    }
    if (!valid) {
        var error = errors.join('\n');
        alert(error);
    }
    return valid;
}

// Generic function for POSTing form data.
function postForm(form, dialog, callback, passthrough) {
    var params = $(form).serialize();
    $.post($(form).attr('action'), params, function (data) {
        if (data.Success) {
            if (dialog) {
                dialog.hide();
            }
            if ($.isFunction(callback)) {
                if (typeof passthrough !== 'undefined') {
                    callback(passthrough);
                } else {
                    callback();
                }
            }
        } else {
            if (data.hasOwnProperty('Error') && data.Error == 'duplicate') {
                alert("This item is already part of this group. It can't be added again.")
            } else {
                alert('There was an error processing this request. Please contact the site admins for help.');
            }
        }
    });
}

// Update the permissions table data.
function updatePermissions() {
    $('#permissions-table tbody .data').remove();
    $('.permission-select-all:checked').prop({checked: false});
    $.get(permissions_list_url, function (data) {
        $.each(data, function (index, object) {
            var row = '<tr class="data">';
            row += '<td>' + object.name + '</td>';
            row += '<td>' + object.item + '</td>';
            row += '<td>' + object.action + '</td>';
            row += '<td class="check-column">';
            row += '<input type="checkbox" value="' + object.id + '" class="permission-select">&nbsp;';
            row += '<a href="#' + object.id + '" class="permission-edit"><img src="/static/images/portal-icons/pencil-icon.png"></a>';
            row += '</td>';
            row += '</tr> ';
            $('#permissions-table tbody').append(row);
        });
        permissionEditAttach();
        $('#permissions-table').trigger('update');
    });
}

// Update the groups table data.
function updateGroups() {
    $('#groups-table tbody .data').remove();
    $('.group-select-all:checked').prop({checked: false});
    $.get(group_list_url, function (data) {
        $.each(data, function (index, object) {
            var row = '<tr class="data group-select">';
            row += '<td>' + object.name + '</td>';
            row += '<td>' + object.access_level + '</td>';
            if (admin_rights) {
                row += '<td class="check-column">';
                row += '<input type="checkbox" value="' + object.id + '" class="group-select">&nbsp;';
                row += '<a href="#' + object.id + '" class="group-edit"><img src="/static/images/portal-icons/pencil-icon.png"></a>';
                row += '</td>';
            }
            row += '</tr> ';
            $('#groups-table tbody').append(row);
        });
        $('#groups-table').trigger('update');
        groupEditAttach();
        groupSelect();
    });
}

// Update the group members table data.
function updateGroupMembers(group_id, status) {
    $('#group-members-table tbody .data').remove();
    $('.user-select-all:checked').prop({checked: false});
    $.get(group_member_list_url, {group_id: group_id}, function (data) {
        $.each(data, function (index, object) {
            var row = '<tr class="data">';
            row += '<td>' + object.first_name + '</td>';
            row += '<td>' + object.last_name + '</td>';
            row += '<td>' + object.email + '</td>';
            row += '<td>' + object.state + '</td>';
            row += '<td>' + object.district + '</td>';
            row += '<td>' + object.school + '</td>';
            row += '<td class="check-column">';
            row += '<input type="checkbox" value="' + object.id + '" name="group_member_id[' + object.id + ']" class="user-select">';
            row += '</td>';
            row += '</tr>';
            $('#group-members-table tbody').append(row);
        });
        $('#group-members-table').trigger('update');
        status.setStatus('members');
    });
}

// Update the group permissions table data.
function updateGroupPermissions(group_id, status) {
    $('#group-permissions-table tbody .data').remove();
    $('.group-permission-select-all:checked').prop({checked: false});
    $.get(group_permissions_list_url, {group_id: group_id}, function (data) {
        $.each(data, function (index, object) {
            var row = '<tr class="data">';
            row += '<td>' + object.name + '</td>';
            row += '<td>' + object.item + '</td>';
            row += '<td>' + object.action + '</td>';
            if (admin_rights) {
                row += '<td class="check-column">';
                row += '<input type="checkbox" value="' + object.id + '" name="group_permission_id[' + object.id + ']" class="group-permission-select">';
                row += '</td>';
            }
            row += '</tr> ';
            $('#group-permissions-table tbody').append(row);
        });
        $('#group-permissions-table').trigger('update');
        status.setStatus('permissions');
    });
}

// Sets up the onclick on the group rows to load the member and permission data, enable the action buttons, and mark the
// currently selected group for any member and group permission actions.
function groupSelect() {
    $(".group-select").each(function () {
        $(this).children("td").slice(0, 1).click(function() {
            var parent = $(this).parents(".group-select");
            $('#groups-table tr').removeClass('selected-group');
            $(parent).addClass('selected-group');
            $('#add-group-permission').removeAttr('disabled');
            $('#add-group-member').removeAttr('disabled');
            $('#delete-group-permissions').removeAttr('disabled');
            $('#delete-group-members').removeAttr('disabled');
            var group_id = $(parent).find('input').attr('value');
            var status = new LoadingStatus(['members', 'permissions']);
            updateGroupMembers(group_id, status);
            updateGroupPermissions(group_id, status);
        });
    });
}

// Creates the modal form for adding/editing groups, as well as the submission handler for the form.
function groupEdit(type, id) {
    var button_name = 'Add';
    var name = '';
    var access_level = 'System';
    var access_levels = ['System', 'State', 'District', 'School'];
    if (type == 'edit') {
        button_name = 'Save';
        $.ajax({
            url: group_list_url,
            type: 'GET',
            async: false,
            data: {group_id: id},
            success: function(data) {
                name = data[0].name;
                access_level = data[0].access_level;
            }
        });
    }
    var content = '<form action="' + group_add_url + '" method="post" id="new-group-submit">';
    content += '<label>Group Name:<input type="text" name="name" value="' + name + '"></label>';
    content += '<label>Group Type:<select name="access_level">';
    $.each(access_levels, function (index, value) {
        var selected = '';
        if (value == access_level) {
            selected = ' selected="selected"';
        }
        content += '<option value="' + value + '"' + selected + '>' + value + '</option>'
    });
    content += '</select></label>';
    content += '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrf_token + '"/>';
    if (type == 'edit') {
        content += '<input type="hidden" name="group_id" value="' + id + '"/>';
    }
    content += '<input type="submit" name="submit" value="' + button_name + '">';
    content += '</form>';
    var dialog = new Dialog('#dialog');
    dialog.show('New Permission', content);
    $('#new-group-submit').submit(function (event) {
        event.preventDefault();
        if (validateGroupForm(type)) {
            postForm(this, dialog, updateGroups);
        }
    });
}

// Attaches the onclick to the add/edit buttons for groups.
function groupEditAttach() {
    $('#new-group').click(function () {
        groupEdit('add');
    });
    $('.group-edit').click(function (e) {
        e.preventDefault();
        var id = $(this).attr('href').substr(1);
        groupEdit('edit', id);
    });
}

// Creates the modal form for adding/editing permissions, as well as the submission handler for the form.
function permissionEdit(type, id) {
    var button_name = 'Add';
    var name = '';
    var target = '';
    var action = '';
    if (type == 'edit') {
        button_name = 'Save';
        $.ajax({
            url: permissions_list_url,
            type: 'GET',
            async: false,
            data: {permission_id: id},
            success: function(data) {
                name = data[0].name;
                target = data[0].item;
                action = data[0].action;
            }
        });
    }
    var content = '<form action="' + permission_add_url + '" method="post" id="new-permission-submit">';
    content += '<label>Permission Name:<input type="text" name="name" value="' + name + '"></label>';
    content += '<label>Permission Target:<input type="text" name="target" value="' + target + '"></label>';
    content += '<label>Permission Action:<input type="text" name="action" value="' + action + '"></label>';
    content += '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrf_token + '"/>';
    if (type == 'edit') {
        content += '<input type="hidden" name="permission_id" value="' + id + '"/>';
    }
    content += '<input type="submit" name="submit" value="' + button_name + '"></label>';
    content += '</form>';
    var dialog = new Dialog('#dialog');
    dialog.show('New Permission', content);
    $('#new-permission-submit').submit(function (event) {
        event.preventDefault();
        if (validatePermissionForm(type)) {
            postForm(this, dialog, updatePermissions);
        }
    });
}

// Attaches the onclick to the add/edit buttons for permissions.
function permissionEditAttach() {
    $('#new-permission').click(function () {
        permissionEdit('add');
    });
    $('.permission-edit').click(function (e) {
        e.preventDefault();
        var id = $(this).attr('href').substr(1);
        permissionEdit('edit', id);
    });
}

// attaches action for selecting all on the select all checkboxes on the various tables.
function selectAll(trigger_selector, target_selector) {
    $(trigger_selector).change(function () {
        var checked = false;
        if ($(this).is(':checked')) {
            checked = true;
        }
        $(target_selector).each(function () {
            $(this).prop('checked', checked);
        });
    });
}

// Initializes all the code for the page.
function initPermissions() {
    // Sets up the expansion of the sections of the page.
    $(".expand_title").click(function () {
        var $div = $(this).next("div.expand_div");
        if ($div.is(':visible')) {
            $div.slideUp();
            $(this).removeClass("expand_title_expanded");
        } else {
            $div.slideDown();
            $(this).addClass("expand_title_expanded");
        }
    });

    // Sets up the tablesorter tables for the 4 tables on the page.
    pagerOptions.container = $("#permissions-pager");
    $('#permissions-table').tablesorter(tablesorterOptions).tablesorterPager(pagerOptions);

    pagerOptions.container = $("#group-members-pager");
    $('#group-members-table').tablesorter(tablesorterOptions).tablesorterPager(pagerOptions);

    pagerOptions.container = $("#group-permissions-pager");
    $('#group-permissions-table').tablesorter(tablesorterOptions).tablesorterPager(pagerOptions);

    pagerOptions.container = $("#groups-pager");
    pagerOptions.size = 40;
    $('#groups-table').tablesorter(tablesorterOptions).tablesorterPager(pagerOptions);

    // Initialize the various onclicks for the page. The first 3 are separate functions as they need to be reinitialized
    // when the tables are updated. See the comments on the functions for descriptions.
    groupSelect();
    permissionEditAttach();
    groupEditAttach();

    // Creates the modal form for adding group permissions, as well as the submission handler for the form.
    $('#add-group-permission').click(function () {
        var group = $(".selected-group input").val();

        var content = '<form action="' + group_permission_add_url + '" method="post" id="add-permission-submit">';
        content += '<select name="permission">';

        $.ajax({
            url: permissions_list_url,
            type: 'GET',
            async: false,
            success: function(data) {
                $.each(data, function (index, object) {
                    content += '<option value="' + object.id + '">' + object.name + '</option>';
                });
            }
        });

        content += '</select>';
        content += '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrf_token + '"/>';
        content += '<input type=hidden name="group" value="' + group + '">';
        content += '<input type="submit" name="submit" value="Add">';
        content += '</form>';
        var dialog = new Dialog('#dialog');
        dialog.show('Add Permission', content);
        $('#add-permission-submit').submit(function (event) {
            event.preventDefault();
            postForm(this, dialog, updateGroupPermissions, group);
        });
    });

    // Creates the modal form for adding members, as well as the submission handler for the form.
    $('#add-group-member').click(function () {
        // Get the currently selected group ID.
        var group = $(".selected-group input").val();

        // Generate the form content.
        var content = '<form action="' + group_member_add_url + '" method="post" id="add-member-submit" enctype="multipart/form-data">';
        content += '<label><input type="radio" name="type" value="email" checked> Choose a user by email:<input type="text" name="member" id="add-user-email">';
        content += '<label><input type="radio" name="type" value="import"> <strong>Or</strong> import a group of users (text file or CSV with one email address per line): <input type="file" name="import_file" id="add-user-file" disabled></label>';
        content += '<label><input type="radio" name="type" value="group"> <strong>Or</strong> add a group of users: <span id="user-selection">Select State to Start</span></label>';
        content += '<label id="state-label">By State:<select name="state" id="state-select" disabled></select></label>';
        content += '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrf_token + '"/>';
        content += '<input type=hidden name="group" value="' + group + '">';
        content += '<input type="submit" name="submit" value="Add">';
        // Show the dialog.
        var dialog = new Dialog('#dialog');
        dialog.show('Add Member(s)', content);

        // Enable/disable the member addition types based on the radio selection.
        $("#add-member-submit input[name='type']").change(function () {
            if ($(this).attr('value') == 'email') {
                $('#add-user-email').prop({disabled: false});
                $('#add-user-file').prop({disabled: true});
                $('#state-select').prop({disabled: true});
                $('#district-select').prop({disabled: true});
                $('#school-select').prop({disabled: true});
            } else if ($(this).attr('value') == 'import') {
                $('#add-user-email').prop({disabled: true});
                $('#add-user-file').prop({disabled: false});
                $('#state-select').prop({disabled: true});
                $('#district-select').prop({disabled: true});
                $('#school-select').prop({disabled: true});
            } else if ($(this).attr('value') == 'group') {
                $('#add-user-email').prop({disabled: true});
                $('#add-user-file').prop({disabled: true});
                $('#state-select').prop({disabled: false});
                $('#district-select').prop({disabled: false});
                $('#school-select').prop({disabled: false});
            }
        });

        // Submission handler.
        $('#add-member-submit').submit(function (event) {
            // Don't submit normally.
            event.preventDefault();

            // If this is a single addition by email or addition of a selected group, just submit the form.
            if ($("#add-member-submit input[name='type']:checked").val() != 'import') {
                postForm(this, dialog, updateGroupMembers, group);
            } else {
                // If it is an import by CSV, we need a different POST handler.
                // Get the URL for submission.
                var url = $(this).attr('action');
                // Get the form data, including the uploaded file.
                var formData = new FormData($(this)[0]);
                // Submit the form, showing any errors that occurred during import.
                $.ajax({
                    url: url,
                    type: 'POST',
                    data: formData,
                    async: false,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (data) {
                        if (data.Success) {
                            // Update the members table.
                            updateGroupMembers(group);
                            // Hide the modal.
                            if (dialog) {
                                dialog.hide();
                            }
                            // If there were errors, show them in a separate modal.
                            if (data.Errors.length) {
                                var content = '<div id="import-errors"><strong>The following errors were encountered during the import:</strong><ul>';
                                $.each(data.Errors, function (index, item) {
                                    content += '<li>' + item.email + ' - ' + item.error + '</li>';
                                });
                                content += '</ul></div>';
                            }
                            dialog.show('Errors Encountered', content);
                        } else {
                            alert('There was an error processing this request. Please contact the site admins for help.');
                        }
                    }
                });
            }
        });

        // Sets up the various onchanges for the dropdowns to add by group, starting with state at the top.
        $('#state-select').change(function () {
            if ($(this).val()) {
                // Clear the current district and school options since the state changed.
                $('#district-label').remove();
                $('#school-label').remove();
                // Get the allowed Districts
                $.get(drop_districts_url, {state: $(this).val(), access_level: access_level}, function (data) {
                    // Build the district dropdown.
                    var content = '<label id="district-label">By District<select name="district" id="district-select">';
                    if (access_level == 'System' || access_level == 'State') {
                        content += '<option value=""></option>';
                    }
                    $.each(data, function (index, object) {
                        content += '<option value="' + object.id + '">' + object.name + '</option>';
                    });
                    content += '</select></label>';
                    // Add it to the form.
                    $('#state-label').after(content);
                    // Update the descriptive language at the top.
                    $('#user-selection').html('All users in ' + $('#state-select').children(':selected').text());

                    // Attach the onchange for the districts.
                    $('#district-select').change(function () {
                        if ($(this).val()) {
                            // Clear the current school options since the district changed.
                            $('#school-label').remove();
                            // Get the allowed schools.
                            $.get(drop_schools_url, {district: $(this).val()}, function (data) {
                                // Build the school dropdown.
                                var content = '<label id="school-label">By School<select name="school" id="school-select">';
                                if (access_level != 'School') {
                                    content += '<option value=""></option>';
                                }
                                $.each(data, function (index, object) {
                                    content += '<option value="' + object.id + '">' + object.name + '</option>';
                                });
                                content += '</select></label>';
                                // Add it to the form.
                                $('#district-label').after(content);
                                // Update the descriptive language at the top.
                                $('#user-selection').html('All users in district ' + $('#district-select').children(':selected').text());

                                // Attach the onchange for the schools.
                                $('#school-select').change(function () {
                                    // No further to go down the tree, so we just update the descriptive language.
                                    if ($(this).val()) {
                                        $('#user-selection').html('All users in school ' + $('#school-select').children(':selected').text());
                                    } else {
                                        $('#user-selection').html('All users in district ' + $('#district-select').children(':selected').text());
                                    }
                                });
                                // If you can't change the dropdown, make sure the language is still updated.
                                if (access_level == 'School') {
                                    $('#school-select').trigger('change');
                                }
                            });
                        } else {
                            // Revert the descriptive language if we unselected a district.
                            $('#user-selection').html('All users in ' + $('#state-select').children(':selected').text());
                        }
                    });
                    // If you can't change the dropdown, make sure the language is still updated.
                    if (access_level != 'System' && access_level != 'State') {
                        $('#district-select').trigger('change');
                    }
                });
            } else {
                // Revert the descriptive language if we unselected a state.
                $('#user-selection').html('Select State to Start');
            }
        });

        // Get the allowed states.
        $.get(drop_states_url, {access_level: access_level}, function (data) {
            // Build the options.
            var options = '';
            if (access_level == 'System') {
                options = '<option value=""></option>';
            }
            $.each(data, function (index, object) {
                options += '<option value="' + object.id + '">' + object.name + '</option>';
            });
            // Add them to the state dropdown.
            $('#state-select').append(options);
            // If you can't change the dropdown, make sure the language is still updated.
            if (access_level != 'System') {
                $('#state-select').trigger('change');
            }
        });

        // Add the autocomplete to the email field.
        $('#add-user-email').autocomplete(user_email_completion_url + '?access_level=' + access_level, {remoteDataType: 'json'});
    });

    // Creates the modal form for deleting permissions, as well as the submission handler for the form.
    $('#delete-permissions-form').submit(function (e) {
        e.preventDefault();
        var form = this;
        var dialog = new Dialog('#dialogYesNo');
        dialog.showYesNo('Delete Permission(s)', 'Are you sure you want to delete this permission? This action cannot be undone.', function(answer) {
            if (answer) {
                postForm(form, dialog, updatePermissions);
            } else {
                dialog.hide();
            }
        });
    });

    // Creates the modal form for deleting groups, as well as the submission handler for the form.
    $('#delete-groups-form').submit(function (e) {
        e.preventDefault();
        var form = this;
        var dialog = new Dialog('#dialogYesNo');
        dialog.showYesNo('Delete Group(s)', 'Are you sure you want to delete this group? This action cannot be undone.', function(answer) {
            if (answer) {
                postForm(form, dialog, updateGroups);
            } else {
                dialog.hide()
            }
        });
    });

    // Creates the modal form for deleting members, as well as the submission handler for the form.
    $('#delete-group-members-form').submit(function (e) {
        e.preventDefault();
        var form = this;
        var dialog = new Dialog('#dialogYesNo');
        dialog.showYesNo('Remove Group Member(s)', 'Are you sure you want to remove this group member? This action cannot be undone.', function(answer) {
            if (answer) {
                var group = $(".selected-group input").val();
                postForm(form, dialog, updateGroupMembers, group);
            } else {
                dialog.hide();
            }
        });
    });

    // Creates the modal form for deleting group permissions, as well as the submission handler for the form.
    $('#delete-group-permissions-form').submit(function (e) {
        e.preventDefault();
        var form = this;
        var dialog = new Dialog('#dialogYesNo');
        dialog.showYesNo('Remove Group Permission(s)', 'Are you sure you want to remove this group permission? This action cannot be undone.', function(answer) {
            if (answer) {
                var group = $(".selected-group input").val();
                postForm(form, dialog, updateGroupPermissions, group);
            } else {
                dialog.hide();
            }
        });
    });

    // Initialize the select all checkboxes.
    selectAll('.permission-select-all', '.permission-select');
    selectAll('.group-select-all', '.group-select');
    selectAll('.user-select-all', '.user-select');
    selectAll('.group-permission-select-all', '.group-permission-select');
}
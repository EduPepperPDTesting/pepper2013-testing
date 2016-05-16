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

function viewSelect(related_url, columns_url) {
    $('.view-select').change(function () {
        // Get the related views if any and add a dropdown for them.
        $(this).nextAll('select').remove();
        var view_num = getLineNumber($(this).attr('name')) + 1;
        var view_id = $(this).val();
        var self = this;
        $.get(related_url, {view_id: view_id}, function (data) {
            if (data.length) {
                var dropdown = ' + <select class="view-select" name="view[' + view_num + ']">';
                dropdown += '<option value="none">Select...</option>';
                $.each(data, function (index, value) {
                    dropdown += '<option value="' + value.id + '">' + value.name + '</option>';
                });
                dropdown += '</select>';
                $(self).after(dropdown);
                $('.view-select').off('change');
                viewSelect(related_url, columns_url);
            }
        });

        // Get the columns and add them to the column selector and filter dropdowns.
        var views = $('.view-select').val();
        var get_data = {};
        $.each(views, function (index, value) {
            get_data['view[' + index + ']'] = value;
        });
        $.get(columns_url, get_data, function (data) {
            // Add the checkbox selectors for the column selectors.
            if (data.length) {
                var second_column = Math.floor(data.length / 2);
                var remainder = data.length % 2;
                var first_column = second_column + remainder;

                var columns = '<ul>';
                for (var x = 0; x < data.length; x++) {
                    if (x == first_column) {
                        columns += '</ul><ul>';
                    }
                    columns += '<li><label>';
                    columns += '<input class="column-check" type="checkbox" name="column[' + x + ']" value="' + data[x].id + '"> ' + data[x].name + ' - ' + data[x].description;
                    columns += '</label></li>';
                }
                columns += '</ul>';
                $('.column-selector ul').not('#selected-columns').remove();
                $('#selected-columns li').remove();
                $('#order-title').after(columns);
                columnChangeHandler();
            }
            // Create the dropdown for the filters.
            var options = '';
            $.each(data, function (index, value) {
                options += '<option value="' + value.id + '">' + value.name + '</option>';
            });
            $('.filter-column').html(options);
        });
    });
}

function filterLines() {
    $('.minus').off('click');
    $('.minus').click(function () {
        var line_number = getLineNumber($(this).attr('name'));
        $('#where-row\\[' + line_number + '\\]').remove();
        renumberLines('where-row');
    });
    $('.plus').off('click');
    $('.plus').click(function () {
        var line_number = getLineNumber($(this).attr('name'));
        var row = '#where-row\\[' + line_number + '\\]';
        var select = $(row).children('.filter-column').clone().wrap('<p>').parent().html();
        var line = '<div class="where-row" id="where-row[]">';
        line += '    <select class="filter-conjunction" name="filter-conjunction[]">';
        line += '        <option value="AND">AND</option>';
        line += '        <option value="OR">OR</option>';
        line += '    </select>';
        line += select;
        line += '    <select class="filter-operator" name="filter-operator[]">';
        line += '        <option value="=">=</option>';
        line += '        <option value="!=">!=</option>';
        line += '        <option value=">">&gt;</option>';
        line += '        <option value="<">&lt;</option>';
        line += '        <option value=">=">&gt;=</option>';
        line += '        <option value="<=">&lt;=</option>';
        line += '    </select>';
        line += '    <input class="filter-value" type="text" name="filter-value[]"/>';
        line += '    <input class="plus" name="plus[]" type="button" value="+"/>';
        line += '    <input class="minus" name="minus[]" type="button" value="-"/>';
        line += '</div>';
        $(row).after(line);
        renumberLines('where-row');
        filterLines();
    });
}

function renumberLines(container) {
    $('.' + container).each(function (index) {
        $(this).attr('id', '');
        $(this).attr('id', container + '[' + index + ']');
        $(this).children().each(function () {
            $(this).attr('name', '');
            $(this).attr('name', $(this).attr('class') + '[' + index + ']');
        });
    });
}

function getLineNumber(string) {
    var number = string.substring(string.indexOf('[') + 1, string.length - 1);
    return number * 1;
}

function expandTitle() {
    $(".expand_title").off('click');
    $(".expand_title").click(function () {
        var $div = $(this).next("div.expand_div");
        if ($div.is(':visible')) {
            $div.slideUp();
            $(this).removeClass('expand_title_expanded');
        } else {
            $div.slideDown();
            $(this).addClass('expand_title_expanded');
        }
    });
}

function submitHandler(form, callback) {
    $(form).submit(function (e) {
        e.preventDefault();
        // TODO: add the error checking here.
        $.post($(this).attr('action'), $(this).serialize(), function (data) {
            if (data.success) {
                callback(data)
            } else {
                alert('The operation was not successful. The error was: ' + data.error);
            }
        });
    });
}

function submitButton(selector, target) {
    $(selector).click(function (e) {
        e.preventDefault();
        $(target).trigger('submit');
    });
}

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

function updateViews() {
    $.get(view_update_url, function (data) {
        var views = '';
        $.each(data.views, function (index, value) {
            var description = value.description ? value.description : '';
            views += '<tr class="data">';
            views += '    <td>' + value.name + '</td>';
            views += '    <td>' + description + '</td>';
            views += '    <td>' + value.columns + '</td>';
            views += '    <td class="check-column">';
            views += '        <input type="checkbox" value="' + value.id + '" name="view_id[' + value.id + ']" class="view-select">&nbsp;';
            views += '        <a href="#' + value.id + '" class="view-edit"><img src="/static/images/portal-icons/pencil-icon.png"></a>';
            views += '    </td>';
            views += '</tr>';
        });
        $('#views-table tbody').html(views);
        $('#views-table').trigger('update');

        var relationships = '';
        $.each(data.relationships, function (index, value) {
            relationships += '<tr class="data">';
            relationships += '    <td>' + value.relationship + '</td>';
            relationships += '    <td>' + value.columns + '</td>';
            relationships += '    <td class="check-column">';
            relationships += '        <input type="checkbox" value="' + value.id + '" name="relationship_id[' + value.id + ']" class="relationship-select">&nbsp;';
            relationships += '        <a href="#' + value.id + '" class="relationship-edit"><img src="/static/images/portal-icons/pencil-icon.png"></a>';
            relationships += '    </td>';
            relationships += '</tr>';
        });
        $('#relationships-table tbody').html(relationships);
        $('#relationships-table').trigger('update');

        addView();
        addRelationship();
    });
}

function filterColumns() {
    $('.minus').off('click');
    $('.minus').click(function () {
        var line_number = getLineNumber($(this).attr('name'));
        $('#column-row\\[' + line_number + '\\]').remove();
        renumberLines('column-row');
    });
    $('.plus').off('click');
    $('.plus').click(function () {
        var line_number = getLineNumber($(this).attr('name'));
        var row = '#column-row\\[' + line_number + '\\]';
        var line = '<div class="column-row" id="column-row[]">';
        line += '<input class="column_name" name="column_name[]" type="text" placeholder="Name">';
        line += '<input class="column_description" name="column_description[]" type="text" placeholder="Description">';
        line += '<input class="column_source" name="column_source[]" type="text" placeholder="Source">';
        line += '<input type="button" value="+" class="plus" name="plus[]">';
        line += '<input type="button" value="-" class="minus" name="minus[]">';
        line += '</div>';
        $(row).after(line);
        renumberLines('column-row');
        filterColumns();
    });
}

function addView() {
    $('.add-new-view, .view-edit').off('click');
    $('.add-new-view, .view-edit').click(function (e) {
        e.preventDefault();

        var current_data = false;
        if ($(this).attr('class') == 'view-edit') {
            $.ajax({
                method: 'GET',
                url: view_data_url,
                data: {view_id: $(this).attr('href').slice(1)},
                async: false,
                success: function (data) {
                    current_data = data;
                }
            });
        }

        var dialog = new Dialog('#view-dialog');
        var content = '<div id="add-view-wrapper">';
        content += '<form id="add-view-form" action="' + add_view_url + '">';
        if (current_data) {
            var description = current_data.description ? current_data.description : '';
            content += '<label>View Name:<input name="view_name" type ="text" value="' + current_data.name + '"></label>';
            content += '<label>View Description:<input name="view_description" type="text" value="' + description + '"></label>';
            content += '<label>View Source:<input name="view_source" type="text" value="' + current_data.source + '"></label>';
        } else {
            content += '<label>View Name:<input name="view_name" type ="text"></label>';
            content += '<label>View Description:<input name="view_description" type="text"></label>';
            content += '<label>View Source:<input name="view_source" type="text"></label>';
        }
        content += '<label>Columns:';
        if (current_data) {
            $.each(current_data.columns, function (index, value) {
                content += '<div class="column-row" id="column-row[' + index + ']">';
                content += '<input class="column_name" name="column_name[' + index + ']" type="text" placeholder="Name" value="' + value.name + '">';
                content += '<input class="column_description" name="column_description[' + index + ']" type="text" placeholder="Description" value="' + value.description + '">';
                content += '<input class="column_source" name="column_source[' + index + ']" type="text" placeholder="Source" value="' + value.source + '">';
                content += '<input type="button" value="+" class="plus" name="plus[' + index + ']">';
                if (index > 0) {
                    content += '<input type="button" value="-" class="minus" name="minus[' + index + ']">';
                }
                content += '</div>';
            });
        } else {
            content += '<div class="column-row" id="column-row[0]">';
            content += '<input class="column_name" name="column_name[0]" type="text" placeholder="Name">';
            content += '<input class="column_description" name="column_description[0]" type="text" placeholder="Description">';
            content += '<input class="column_source" name="column_source[0]" type="text" placeholder="Source">';
            content += '<input type="button" value="+" class="plus" name="plus[0]">';
            content += '</div>';
        }
        content += '</label>';
        if (current_data) {
            content += '<input type="hidden" name="view_id" value="' + current_data.id + '">'
            content += '<input type="submit" value="Save">';
        } else {
            content += '<input type="submit" value="Add">';
        }
        content += '</form>';
        content += '</div>';
        dialog.show('Add New View', content);

        submitHandler('#add-view-form', function (data) {
            dialog.hide();
            alert('View Saved Successfully.');
            updateViews();
        });

        filterColumns();
    });
}

function updateColumnSelect(view, selector, selected) {
    if (view != '') {
        $.get(column_list_url, {'view[0]': view}, function (data) {
            var html = '';
            $.each(data, function (index, value) {
                if (selected === value.id) {
                    html += '<option value="' + value.id + '" selected>' + value.name + '</option>';
                } else {
                    html += '<option value="' + value.id + '">' + value.name + '</option>';
                }
            });
            $(selector).html(html);
        });
    } else {
        $(selector).html('');
    }
}

function addRelationship() {
    $('.add-new-relationship, .relationship-edit').off('click');
    $('.add-new-relationship, .relationship-edit').click(function (e) {
        e.preventDefault();

        var current_data = false;
        if ($(this).attr('class') == 'relationship-edit') {
            $.ajax({
                method: 'GET',
                url: relationship_data_url,
                data: {relationship_id: $(this).attr('href').slice(1)},
                async: false,
                success: function (data) {
                    current_data = data;
                }
            });
        }

        $.get(view_list_url, function (data) {
            var dialog = new Dialog('#view-dialog');
            var content = '<div id="add-relationship-wrapper">';
            content += '<form id="add-relationship-form" action="' + add_relationship_url + '">';
            content += '<div><label>Left View:<select id="left-view" name="left_view"><option value="">Select</option>';
            $.each(data, function (index, value) {
                if (current_data && current_data.left_view == index) {
                    content += '<option value="' + index + '" selected>' + value + '</option>';
                } else {
                    content += '<option value="' + index + '">' + value + '</option>';
                }
            });
            content += '</select></label>';
            content += '<label>Right View:<select id="right-view" name="right_view"><option value="">Select</option>';
            $.each(data, function (index, value) {
                if (current_data && current_data.right_view == index) {
                    content += '<option value="' + index + '" selected>' + value + '</option>';
                } else {
                    content += '<option value="' + index + '">' + value + '</option>';
                }
            });
            content += '</select></label></div>';
            content += '<div><label>Left Column:<select id="left-column" name="left_column"></select></label>';
            content += '<label>Right Column:<select id="right-column" name="right_column"></select></label></div>';
            if (current_data) {
                content += '<input type="hidden" name="relationship_id" value="' + current_data.id + '">';
                content += '<input type="submit" value="Save">';
            } else {
                content += '<input type="submit" value="Add">';
            }
            content += '</form></div>';
            dialog.show('Add New View Relationship', content);
            if (current_data) {
                updateColumnSelect($('#left-view').val(), '#left-column', current_data.left_column);
                updateColumnSelect($('#right-view').val(), '#right-column', current_data.right_column);
            }
            $('#left-view').change(function () {
                updateColumnSelect($(this).val(), '#left-column', false);
            });
            $('#right-view').change(function () {
                updateColumnSelect($(this).val(), '#right-column', false);
            });

            submitHandler('#add-relationship-form', function (data) {
                dialog.hide();
                alert('Relationship Saved Successfully.');
                updateViews();
            });
        });
    });
}

function markDirty() {
    is_dirty = true;
    $('#dirty-message').fadeIn();
    $('#save-report-order input').prop('disabled', false);
}

function markClean() {
    is_dirty = false;
    $('#dirty-message').fadeOut();
    $('#save-report-order input').prop('disabled', true);
}

function animateToggle() {
    $('.main.hidden-category, #save-report-order').slideToggle();
    $('.move, .imove').animate({
        opacity: 'toggle',
        width: 'toggle',
        paddingRight: 'toggle'
    });
    $('.new-category, .delete-report, .edit-report, .delete-category').fadeToggle();
    $('.expand_title').not('.expand_title_expanded').trigger('click');
}

function afterDrop($item, container, _super, event) {
    markDirty();
    _super($item, container);
    $item.show().find(':hidden').show();
}

function checkCategoryStatus() {
    $('.main').each(function () {
        if ($(this).find('li').length) {
            $(this).removeClass('hidden-category');
        } else {
            $(this).addClass('hidden-category').show();
        }
    });
}

function manageHandler() {
    var $categories = $("ul#categories");
    var $reports = $("ul.reports");
    $categories.sortable({
        group: 'categories',
        nested: false,
        itemSelector: 'ul#categories > li',
        handle: '.move',
        onDrop: function ($item, container, _super, event) {
            afterDrop($item, container, _super, event);
        },
        isValidTarget: function  ($item, container) {
            // TODO: see if I can figure out how to not allow things before Drafts.
            return true;
        }
    });
    $reports.sortable({
        group: 'reports',
        itemSelector: 'ul.reports > li',
        handle: '.imove',
        onDrop: function ($item, container, _super, event) {
            afterDrop($item, container, _super, event);
        }
    });
    $categories.sortable('disable');
    $reports.sortable('disable');
    $('.manage').click(function (e) {
        e.preventDefault();
        if ($(this).hasClass('enabled')) {
            if (is_dirty && confirm('You have unsaved changes. Are you sure you want to discard them?')) {
                window.location.reload();
            } else if (!is_dirty) {
                animateToggle();
                $categories.sortable('disable');
                $reports.sortable('disable');
                $(this).removeClass('enabled');
            }
        } else {
            animateToggle();
            $categories.sortable('enable');
            $reports.sortable('enable');
            $(this).addClass('enabled');
        }
    });
}

function addCategoryHandler() {
    $('.new-category').click(function (e) {
        e.preventDefault();
        var dialog = new Dialog('#dialog');
        var content = '<form action="' + category_save_url + '" id="category-save">';
        content += '<label>Category Name:<input type="text" name="name"></label>';
        content += '<input type="submit" value="Add">';
        content += '</form>';
        dialog.show('Add Category', content);
        submitHandler('#category-save', function (data) {
            dialog.hide();
            if (data.success) {
                var category = '<li class="main hidden-category">';
                category += '    <div class="expand_title expand_title_collapse">';
                category += '        <a class="delete-category" href="#"><img src="/static/images/icons/Delete-64.png"></a>';
                category += '        <img class="move" src="/static/images/icons/move.png">' + data.name;
                category += '        <div class="icon"></div>';
                category += '    </div>';
                category += '    <div class="expand_div">';
                category += '        <ul class="reports"></ul>';
                category += '    </div>';
                category += '</li>';
                $('#categories').append(category);
                var $new_category = $('.main').last();
                $new_category.show().find(':hidden').show();
                $new_category.children('.expand_title').addClass('expand_title_expanded');
                expandTitle();
                $("ul#categories").sortable('refresh');
                $("ul.reports").sortable('refresh');
            } else {
                alert('The category was not saved successfully. The error was: ' + data.error);
            }
        });
    });
}

function getFullOrder() {
    var $categories = $("ul#categories");
    var $reports = $("ul.reports");

    var category_order = $categories.sortable('serialize').get();
    var full_order = [];

    $.each(category_order[0], function (index, value) {
        full_order[index] = value;
        var report_order = [];
        $($reports[index]).children('li').each(function (index, item) {
            report_order[index] = {id: $(this).attr('data-id'), name: $(this).attr('data-name')}
        });
        full_order[index].reports = report_order
    });

    return JSON.stringify(full_order, null, ' ')
}

function saveOrderHandler() {
    $('#save-report-order input').click(function (e) {
        e.preventDefault();
        $.ajax({
            url: order_save_url,
            data: getFullOrder(),
            contentType: 'application/json',
            type: 'POST',
            success: function (data) {
                if (data.success) {
                    markClean();
                    checkCategoryStatus();
                } else {
                    alert('There was a problem saving the order. The error was: ' + data.error);
                }
            }
        });
    });
}

function deleteReportHandler() {
    $('.delete-report').click(function (e) {
        e.preventDefault();
        var $parent = $(this).parent();
        var report_id = $parent.attr('data-id');
        if (confirm('Are you sure you want to delete this report?')) {
            $.post(report_delete_url, {report_id: report_id}, function (data) {
                if (data.success) {
                    $parent.remove();
                    checkCategoryStatus();
                } else {
                    alert('There was a problem when trying to delete this report. The error was: ' + data.error);
                }
            });
        }
    });
}

function deleteCategoryHandler() {
    $('.delete-category').click(function (e) {
        e.preventDefault();
        var $parent = $(this).parents('.main');
        var category_id = $parent.attr('data-id');
        if (confirm('Are you sure you want to delete this category? If there are any reports in this category, they will be unpublished until you choose another category.')) {
            $.post(category_delete_url, {category_id: category_id}, function (data) {
                if (data.success) {
                    $parent.find('ul.reports li').appendTo('.reports:first');
                    $parent.remove();
                    checkCategoryStatus();
                } else {
                    alert('There was a problem when trying to delete this category. The error was: ' + data.error);
                }
            });
        }
    });
}

function columnChangeHandler() {
    $('.column-check').change(function () {
        var column_id = $(this).attr('value');
        var text = $(this).parent().text();
        var name = $.trim(text.slice(0, text.indexOf('-')));
        if ($(this).is(':checked')) {
            $('#selected-columns').append('<li data-id="' + column_id + '"><img class="move" src="/static/images/icons/move.png"> ' + name + '</li>');
        } else {
            $('#selected-columns li[data-id=' + column_id + ']').remove();
        }
        $('#selected-columns').sortable('refresh');
    });
}

function columnOrdering() {
    $('#selected-columns').sortable({
        group: 'columns',
        itemSelector: 'ul#selected-columns > li',
        handle: '.move',
        onDrop: function ($item, container, _super, event) {
            _super($item, container);
            $('.selected-column').remove();
            var order = $('#selected-columns').sortable('serialize').get();
            $.each(order[0], function (index, item) {
                $('.report-name').append('<input type="hidden" value="' + index + '" class="selected-column" name="selected-column[' + item.id + ']">')
            });
        }
    });
    columnChangeHandler();
}

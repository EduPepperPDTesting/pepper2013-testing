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
                var third_column = Math.floor(data.length / 3);
                var remainder = data.length % 3;
                var first_column = remainder > 0 ? third_column + 1 : third_column;
                var second_column = remainder > 1 ? first_column * 2 : first_column * 2 - 1;

                var columns = '<ul>';
                for (var x = 0; x < data.length; x++) {
                    if (x == first_column || x == second_column) {
                        columns += '</ul><ul>';
                    }
                    columns += '<li><label>';
                    columns += '<input type="checkbox" name="column[' + x + ']" value="' + data[x].id + '"> ' + data[x].name + ' - ' + data[x].description;
                    columns += '</label></li>';
                }
                columns += '</ul>';
                $('.column-selector ul').remove();
                $('.column-selector h2').after(columns);
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

function addView() {
    $('.add-new-view').click(function (e) {
        e.preventDefault();
        var dialog = new Dialog('#view-dialog');
        var content = '<div id="add-view-wrapper">';
        content += '<form id="add-view-form" action="' + add_view_url + '">';
        content += '<label>View Name:<input name="view_name" type ="text"></label>';
        content += '<label>View Description:<input name="view_description" type="text"></label>';
        content += '<label>View Source:<input name="view_source" type="text"></label>';
        content += '<label>Columns:<div class="single-line">';
        content += '<input name="column_name[0]" type="text" placeholder="Name">';
        content += '<input name="column_description[0]" type="text" placeholder="Description">';
        content += '<input name="column_source[0]" type="text" placeholder="Source">';
        content += '<input type="button" value="+" class="plus">';
        content += '</div></label>';
        content += '<input type="submit" value="Add">';
        content += '</form>';
        content += '</div>';
        dialog.show('Add New View', content);

        submitHandler('#add-view-form', function (data) {
            dialog.hide();
            alert('View Created Successfully.');
            // TODO: add a refresh here.
        });
    });
}

function updateColumnSelect(view, selector) {
    if (view != '') {
        $.get(column_list_url, {'view[0]': view}, function (data) {
            var html = '';
            $.each(data, function (index, value) {
                html += '<option value="' + value.id + '">' + value.name + '</option>';
            });
            $(selector).html(html);
        });
    } else {
        $(selector).html('');
    }
}

function addRelationship(url) {
    $('.add-new-relationship').click(function (e) {
        e.preventDefault();
        $.get(view_list_url, function (data) {
            var dialog = new Dialog('#view-dialog');
            var content = '<div id="add-relationship-wrapper">';
            content += '<form id="add-relationship-form" action="' + add_relationship_url + '">';
            content += '<div><label>Left View:<select id="left-view" name="left_view"><option value="">Select</option>';
            $.each(data, function (index, value) {
                content += '<option value="' + index + '">' + value + '</option>';
            });
            content += '</select></label>';
            content += '<label>Right View:<select id="right-view" name="right_view"><option value="">Select</option>';
            $.each(data, function (index, value) {
                content += '<option value="' + index + '">' + value + '</option>';
            });
            content += '</select></label></div>';
            content += '<div><label>Left Column:<select id="left-column" name="left_column"></select></label>';
            content += '<label>Right Column:<select id="right-column" name="right_column"></select></label></div>';
            content += '<input type="submit" value="Add">';
            content += '</form></div>';
            dialog.show('Add New View Relationship', content);
            $('#left-view').change(function () {
                updateColumnSelect($(this).val(), '#left-column');
            });
            $('#right-view').change(function () {
                updateColumnSelect($(this).val(), '#right-column');
            });

            submitHandler('#add-relationship-form', function (data) {
                dialog.hide();
                alert('Relationship Created Successfully.');
                // TODO: add a refresh here.
            });
        });
    });
}
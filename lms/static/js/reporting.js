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

function submitHandler(form, success_url) {
    $(form).submit(function (e) {
        e.preventDefault();
        // TODO: add the error checking here.
        $.post($(this).attr('action'), $(this).serialize(), function (data) {
            if (data.success) {
                window.location = success_url.replace('placeholder', data.report_id);
            } else {
                new Dialog('#dialog').show('Error Saving Report', 'The report did not save successfully. The error was: ' + data.error);
            }
        });
    });
}

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
                viewSelect();
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
                var second_column = remainder > 1 ? third_column + 1 : third_column;

                var columns = '<ul>';
                for (var x = 0; x < first_column; x++) {
                    columns += '<li><label>';
                    columns += '<input type="checkbox" name="column[' + x + ']" value="' + data[x].id + '"> ' + data[x].name + ' - ' + data[x].description;
                    columns += '</label></li>';
                    if (x == second_column || x == third_column) {
                        columns += '</ul><ul>';
                    }
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
            $('.filter-view').html(options);
        });
    });
}

function filterLines() {
    $('.minus').click(function () {
        var line_number = getLineNumber($(this).attr('name'));
        $('#where-row[' + line_number + ']').remove();
        renumberLines('where-row');
    });
    $('.plus').click(function () {
        var line = '<div class="where-row" id="where-row[]">';
        line += '    <select class="filter-view" name="filter-view[]">'
        line += '    </select>';
        line += '    <select name="filter-operator[]">';
        line += '        <option value="=">=</option>';
        line += '        <option value="!=">!=</option>';
        line += '        <option value=">">&gt;</option>';
        line += '        <option value="<">&lt;</option>';
        line += '        <option value=">=">&gt;=</option>';
        line += '        <option value="<=">&lt;=</option>';
        line += '    </select>';
        line += '    <input class="filter-value" type="text" name="filter-value[]"/>';
        line += '    <input class="plus" name="plus[]" type="button" value="+"/>';
        line += '</div>';
        var line_number = getLineNumber($(this).attr('name'));
        $('#where-row[' + line_number + ']').after(line);
        renumberLines('where-row');
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
    var number = string.substring(string.indexOf('['), string.length - 1);
    return number * 1;
}

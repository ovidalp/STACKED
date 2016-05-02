
$(function() {

    $('[data-toggle="tooltip"]').tooltip();

    $('#result_tabs a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
    })

    $("#select_all_button").on('click', function() {
        $("#algorithms_table tr").trigger('check');
    });

    $("#algorithms_table tr").each(function() {
        var row = $(this);
        var radio = row.find('input[type=radio]');
        var checkbox = row.find('input[type=checkbox]');

        row.bind('check', function() {
            if ( !checkbox.is(':disabled') ) {
                checkbox.prop('checked', true);
                checkbox.trigger('change');
            }
        });

        row.bind('enableCheck',function() {
            checkbox.prop('disabled', false);
        });

        radio.on('change', function() {
            if ( $(this).is(":checked") ) {
                checkbox.attr('checked', false).prop('disabled', true);
                row.siblings().removeClass('danger').trigger('enableCheck');
                row.addClass('danger').removeClass('info');
            }
        });

        checkbox.on('change', function() {
            if ( $(this).is(":checked") ) {
                row.addClass('info');
            } else {
                row.removeClass('info');
            }
        });
    });

    var csrftoken = $.cookie('csrftoken');

    // Form Request

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    function process_data(data) {
        $("#raw_data_area").val(data['cmp_details']);
        $("#conclusion_area").val(data['conclusion']);

        var series_data_mean = [];
        var series_data_sd = [];

        var table_data = $("#table_data");
        table_data.find('.result_line').remove();

        data['cmp_summary'].forEach(function(obj, idx) {
            var row = $("<tr class='result_line'></tr>");

            row.append( $("<td class='text-center'></td>").html(obj['COMPARING SYSTEMS']) );
            row.append( $("<td class='text-center'></td>").html(obj['Confidence interval']) );
            row.append( $("<td class='text-center'></td>").html(obj['Number Observation']) );
            row.append( $("<td class='text-center'></td>").html(obj['Range']) );
            row.append( $("<td class='text-center'></td>").html(obj['Sample Mean']) );
            row.append( $("<td class='text-center'></td>").html(obj['Sample SD']) );
            row.append( $("<td class='text-center'></td>").html(obj['Sample Variance']) );

            var mean = obj['Sample Mean'];
            var range = obj['Range'];

            series_data_mean.push( mean );
            series_data_sd.push([ mean - range, mean + range ])

            table_data.append(row);
        });

        var distance_axis = data['distance_scale'];
        var series_data = [];

        var color_list = [
            "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF", "#000000",
            "#800000", "#008000", "#000080", "#808000", "#800080", "#008080", "#808080",
            "#C00000", "#00C000", "#0000C0", "#C0C000", "#C000C0", "#00C0C0", "#C0C0C0",
            "#400000", "#004000", "#000040", "#404000", "#400040", "#004040", "#404040",
            "#200000", "#002000", "#000020", "#202000", "#200020", "#002020", "#202020",
            "#600000", "#006000", "#000060", "#606000", "#600060", "#006060", "#606060",
            "#A00000", "#00A000", "#0000A0", "#A0A000", "#A000A0", "#00A0A0", "#A0A0A0",
            "#E00000", "#00E000", "#0000E0", "#E0E000", "#E000E0", "#00E0E0", "#E0E0E0",
        ];

        data['dif_cmp'].forEach(function(values, idx) {

            series_data.push({
                name: data['name_cmp'][idx],
                data: values,
                lineWidth: 1,
                marker: {
                    enabled: false  ,
                    radius: 2
                }
            });

        });

        $("#graph_diff_tab_button").click();
        $('#graph_content_difference').highcharts({
            title: {
                text: ''
            },
            colors: color_list,
            exporting: {
                // sourceWidth: 1000
            },
            xAxis: {
                title: {
                    text: 'distance (cm)'
                },

                categories: distance_axis
            },
            yAxis: {
                title: {
                    text: 'Difference Data'
                },
                plotLines: [{
                    value: 0,
                    width: 2,
                    color: '#ff503d'
                }]
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0
            },
            series: series_data
        });

        var mean_axis = [];
        data['name_cmp'].forEach(function(val, idx) {
            mean_axis.push(idx + 'sdj');
        });

        $("#graph_mean_tab_button").click();

        $('#graph_content_mean').highcharts({
            chart: {
                type: 'scatter'
            },
            exporting: {
                // sourceWidth: 1000
            },
            title: {
                text: ''
            },
            xAxis: {
                title: {
                    text: 'Compared Algorithms'
                },

                categories: data['name_cmp']
            },
            yAxis: {
                title: {
                    text: 'Mean'
                },
                plotLines: [{
                    value: 0,
                    width: 2,
                    color: '#ff503d'
                }]
            },
            legend: {
                enabled: false,
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0
            },
            series: [{
                name: 'Mean',
                color: '#4572A7',
                data: series_data_mean,
                marker: {
                    radius: 5
                },
                tooltip: {
                    headerFormat: '',
                    // pointFormat: '{point.y}'
                    pointFormatter: function() {
                        return this.category + '<br><b>' + this.series.name + '</b>: ' + this.y;
                    }
                }
            }, {
                name: 'Error',
                type: 'errorbar',
                color: '#4572A7',
                stemWidth: 1,
                whiskerWidth: 1,
                valueDecimals: 2,
                pointRange: 1,
                data: series_data_sd
            }]
        });
    }

    $("#form_download").on('submit', function(evt) {
        evt.preventDefault();

        var ajax_data = new FormData();

        var data = $(this).serializeArray();

        if ($("#user_result").get(0).files.length > 0) {
            user_file = $("#user_result").get(0).files[0];

            ajax_data.append("user_result", user_file, "user_result");
        }

        var main_alg_test = false;
        var sec_alg_test = false;

        data.forEach(function(obj) {
            if (obj.name === 'main_alg') {
                main_alg_test = true;
            }

            if (obj.name === 'sec_alg') {
                sec_alg_test = true;
            }

            ajax_data.append(obj.name, obj.value);
        });

        var error_msg = '';

        if (!main_alg_test) {
            error_msg += 'Select one Main Algorithm to Compare.\n';
        }

        if (!sec_alg_test) {
            error_msg += 'Select at least one Secondary Algorithm to compare.\n';
        }

        if (main_alg_test && sec_alg_test) {

            $.ajax('comparedata', {
                cache: false,
                dataType: 'json',
                processData: false,
                contentType: false,
                data: ajax_data,
                success: function(data) {
                    process_data(data);
                },
                type: 'POST'
            });
        } else {
            alert(error_msg);
        }
    });
});

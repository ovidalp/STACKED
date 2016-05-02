
$(function() {

    $('[data-toggle="tooltip"]').tooltip();

    $('#result_tabs a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
    })

    $("#algorithms_select button").click(function(e) {
        e.preventDefault();

        $("#algorithms_select button").removeClass('active btn-success').addClass('btn-warning');
        $("#user_result").removeClass('active btn-success').addClass('btn-warning').val('');

        $(this).addClass('active btn-success').removeClass('btn-warning');
    });

    $("#user_result").on("change", function() {
        var value = $(this).val();

        if (value) {
            $("#algorithms_select button").removeClass('active btn-success').addClass('btn-warning');
            $(this).addClass('active btn-success').removeClass('btn-warning');
        }
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

        $("#conclusion_data_area").val(data['conclusion']);
        $("#raw_data_area").val(data['evaluate_detail']);

        var series_data = [];

        data['factor_NAME'].forEach(function(value, index) {
            series_data.push({
                name: value,
                y: data['ss'][index]
            });
        });

        $("#graph_factor_tab_button").click();
        $('#graph_content_factor').highcharts({
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie'
            },
            title: {
                text: ''
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
                pie: {
                    dataLabels: {
                        enabled: false
                    },
                    showInLegend: true
                }
            },
            series: [{
                name: '',
                colorByPoint: true,
                data: series_data,
            }]
        });

        $("#raw_tab_button").click();
    }

    $("#form_download").on('submit', function(evt) {
        evt.preventDefault();

        var alg = $("#algorithms_select button.active").data("value") || $("#user_result").val();

        var error_msg = '';

        if (!alg) {
            error_msg += 'Select one Algorithm show factors.';
        }

        if (alg) {
            var ajax_data = new FormData();

            if ($("#user_result").val()) {
                user_file = $("#user_result").get(0).files[0];
                ajax_data.append("user_result", user_file, "user_result");
            } else {
                ajax_data.append("algorithm", alg);
            }

            $.ajax('factordata', {
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

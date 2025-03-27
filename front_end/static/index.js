$(document).ready(function() {
    
    var datasets = [{
        'id' : 1,
        'name' : 'Sales Demand Forecast.ipynb'
    }]; // To store datasets
    var currentDatasetId = null;
    var rules = []; // To store rules for the current dataset
    var data = {};
    var data_classes = {};
    var data_annotations = {};

    var displayedRuleId = null;

    function loadDatasets(datasetId = null) {
        var selector = $('#dataset-selector');
        $.each(datasets, function(index, dataset) {
                        selector.append($('<option>', {
                        value: dataset.id,
                        text: dataset.name
                        }));
                    });
        // For simulation, we'll hardcode some datasets
        // showLoader();
        // $.ajax({
        //     url: '/datasets',
        //     type: 'GET',
        //     success: function(data) {
        //         datasets = data['datasets'];
        //         var selector = $('#dataset-selector');
        //         selector.empty();
        //         $.each(datasets, function(index, dataset) {
        //             selector.append($('<option>', {
        //             value: dataset.id,
        //             text: dataset.name
        //             }));
        //         });

        //         if (Object.keys(datasets).length > 0) {
        //             currentDatasetId = datasetId || Object.keys(datasets)[0];
        //             selector.val(currentDatasetId);
        //             loadRules();
        //             loadDataPreview();
        //         }
        //     },
        //     error: function(response) {
        //         alert("Error loading datasets: " + response.responseText);
        //     },
        //     complete: function() {
        //         clearLoader();
        //     }
        // });
    }

    var dp_toggle = true;
    $(document).on('click', '#data-preview-panel-heading', function() {
        if (dp_toggle) {
            res = $('#data-preview-panel-body').collapse('hide')
            $('#data-preview-panel-heading i').removeClass('bi-chevron-down').addClass('bi-chevron-right');
            dp_toggle = false;  
        }
        else {
            res = $('#data-preview-panel-body').collapse('show')
            $('#data-preview-panel-heading i').removeClass('bi-chevron-right').addClass('bi-chevron-down');
            dp_toggle = true;
        }
    });

    let load_summary = function() {
        $.ajax({
            url: '/summary',
            type: 'GET',
            success: function(data) {
                $('#data-preview-panel-body').html(data);
            },
            error: function(response) {
                alert("Error loading summary: " + response.responseText);
            },
            complete: function() {
            }
        });
    };
    
    load_summary();
    loadDatasets();

});

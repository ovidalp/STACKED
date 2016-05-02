from django.shortcuts import render
from django.http import HttpResponse

from django.core.files import File
from django.conf import settings

from django.http import JsonResponse

import os
import string

from stacked_bib import load_DICT_data_from_csv, get_cmp_system_vs_all, load_single_dictionary, get_factor_impact

def load_dataset(dataset, name):
    dataset[name] = {
        'csv': settings.MEDIA_ROOT + "data_system_cmp_" + name + ".csv",
        'range_csv': settings.MEDIA_ROOT + "range_values_" + name + ".csv",
        # 'factor_csv': settings.MEDIA_ROOT + "data_factor_impact_" + name + ".csv",
    }

    dataset[name]['result'] = load_DICT_data_from_csv(dataset[name]['csv'])
    dataset[name]['range_result'] = load_single_dictionary(dataset[name]['range_csv'])

dataset = {}
dataset_list = ['SCALE', 'ROTATION', 'TRANSLATION']

for ds in dataset_list:
    load_dataset(dataset, ds)

ALG_LIST = dataset[dataset_list[0]]['result'].keys()
ALG_LIST.sort()

LABELS = dataset[dataset_list[0]]['range_result'].values()
LABELS = map(float, LABELS)
LABELS.sort()

dataset_evaluation = load_DICT_data_from_csv(settings.MEDIA_ROOT + "data_factor_impact_EVALUATION.csv")

def comparation_view(request):
    return render(request, 'codeapp/comparation.html', {
        'dataset_list': dataset_list,
        'alg_list': ALG_LIST
    })

def compare_data(request):
    data = request.POST.copy()

    user_csv = None
    if 'user_result' in request.FILES:
        user_csv = load_DICT_data_from_csv(request.FILES['user_result'], True)

    dataset_name = data.get('dataset_name')
    main_alg = data.get('main_alg')
    secondary_algs = [main_alg]
    if 'sec_alg' in data:
        secondary_algs.extend(data.pop('sec_alg'))

    sys_reference = main_alg
    reference_data = { k:v for (k, v) in dataset[dataset_name]['result'].items() if k in secondary_algs }

    if user_csv and ('user_result' in secondary_algs):
        user_algorith_name = user_csv.keys()[0]

        secondary_algs.remove('user_result')
        secondary_algs.append(user_algorith_name)

        reference_data[user_algorith_name] = user_csv[user_algorith_name]

        if sys_reference == u'user_result':
            sys_reference = user_algorith_name

    name_cmp, dif_cmp, cmp_result, cmp_details, cmp_summary, conclusion = get_cmp_system_vs_all(sys_reference, reference_data)

    output = {
        'name_cmp': name_cmp,
        'dif_cmp': dif_cmp,
        'cmp_result': cmp_result,
        'cmp_details': cmp_details,
        'cmp_summary': cmp_summary,
        'conclusion': conclusion,
        'distance_scale': LABELS
    }

    return JsonResponse(output);

def factor_view(request):
    return render(request, 'codeapp/factor.html', {
        'dataset_list': dataset_list,
        'alg_list': ALG_LIST
    })

def factor_data(request):
    # Get request
    data = request.POST.copy()

    dataset = None
    algorithm_name = None

    if 'algorithm' in data:
        algorithm_name = data['algorithm']
        dataset = dataset_evaluation[algorithm_name]

    elif 'user_result' in request.FILES:
        user_csv = load_DICT_data_from_csv(request.FILES['user_result'], True)

        algorithm_name = user_csv.keys()[0]
        dataset = user_csv[algorithm_name]

    # Prepare data
    rep = 10

    # Compute data
    evaluate_detail, conclusion, factor_NAME, SS_xF = get_factor_impact(dataset, rep, algorithm_name, 0)

    # Make output
    output = {
        'evaluate_detail': evaluate_detail,
        'conclusion': conclusion,
        'factor_NAME': factor_NAME,
        'ss': SS_xF
    }

    return JsonResponse(output);

def download_dataset(request):
    name = request.GET['name']
    file_name = settings.MEDIA_ROOT + name

    csv_file = open(file_name, 'r')
    csv_file = File(csv_file)

    response = HttpResponse(csv_file, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=' + name

    return response

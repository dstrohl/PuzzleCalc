from django.shortcuts import render
from django.http import HttpResponseNotAllowed
from PC.pc_lib import *
import logging
from copy import deepcopy


log = logging.getLogger(__name__)


def convert_element_dict_to_list(e_dict_in, line_length=0, row_count=0):
    """
    :param e_dict_in:
                dict:
                    {
                        'l0': '1,2,3,4',
                        'l0m0': 'x',
                        'l0m1': '0',
                    }


    :return:

                list: [
                        {
                            'row_num': 0,
                            'mask': ['X', '0', '.', ...],
                            'elements': '3','4','5','6', ...],
                        },
                        ...
                        ]

    """

    return list(tmp_ret), line_length, row_count


def pc_view(request, line_length=10, row_count=1, elements=None):

    if request.method == 'GET':
        query = request.GET
    elif request.method == 'POST':
        query = request.POST
    else:
        raise HttpResponseNotAllowed(['GET', 'POST'])
    log.debug('query=%r', query)
    query = query.dict()
    line_length = int(query.pop('line_length', line_length))
    row_count = int(query.pop('row_count', row_count))
    mask = query.pop('mask', None)
    elements = query.pop('elements', elements)

    tmp_data = {}
    if mask:
        for index, item in enumerate(mask):
            tmp_data[f'l0m{index}'] = item
    if elements:
        tmp_data['l0'] = elements

    if query:
        tmp_data.update(query)



    lines = PcList()
    base_tmp_line = {'mask': PcList(), 'elements': []}
    mask_len = 0
    ret_len = 0

    for key, value in tmp_data.items():
        if len(key) < 2 or key[0] != 'l' or not key[1].isdigit():
            continue
        try:
            counter = key[1:]
            mask_offset = -1
            if 'm' in counter:
                counter, mask_offset = counter.split('m')
                mask_offset = int(mask_offset)
                mask_len = max(mask_len, mask_offset)
            counter = int(counter)
            ret_len = max(ret_len, counter)
            lines.pad(counter+1, deepcopy(base_tmp_line))
            if mask_offset == -1:
                lines[counter]['elements'] = list(split_string(value, as_int=True, check_dot=True))
            else:
                lines[counter]['mask'].pad(mask_offset+1, config.unknown)
                lines[counter]['mask'][mask_offset] = str(value).upper()
        except ValueError:
            continue

    if mask_len > line_length:
        line_length = mask_len
    if ret_len > row_count:
        row_count = ret_len

    lines.pad(row_count, deepcopy(base_tmp_line))
    data = []
    for index, item in enumerate(lines):
        item['mask'].pad(line_length, config.unknown)
        # item['mask'] = list(item['mask'])
        item['line_num'] = index
        item['line_length'] = line_length
        tmp_line = PcLine(**item)
        data.append(tmp_line)
        # log.debug('Line created: %r', tmp_line)

    log.debug('Parsed request: ' + repr(data))

    context = dict(
        line_length=line_length,
        row_count=row_count,
        length_range=range(line_length),
        row_range=range(row_count),
        lines=data,
    )

    return render(request, 'pc_view.html', context=context)




def line_view(request):
    if request.method == 'GET':
        query = request.GET
    elif request.method == 'POST':
        query = request.POST
    else:
        raise HttpResponseNotAllowed(['GET', 'POST'])

    mask = query.get('mask', None)
    elements = query.get('elements', None)
    length = query.get('length', None)

    if length is None:
        if mask is None:
            length=10
        else:
            length = len(mask)
    else:
        length = int(length)
    if mask is None:
        mask = '.' * length
    elements = split_string(elements)
    context = dict(
        mask=mask,
        elements=elements,
        length=length,
        length_range=range(1, length+1),
    )
    if elements:
        line = PcLine(length, elements, knowns=mask)
        context['line'] = line
        return render(request, 'line_view.html', context=context)
    else:
        return render(request, 'line_edit.html', context=context)


def matrix_view(request):

    if request.method == 'GET':
        query = request.GET
    elif request.method == 'POST':
        query = request.POST
    else:
        raise HttpResponseNotAllowed(['GET', 'POST'])

    length = int(query.get('length', 10))
    rows = int(query.get('rows', length))

    data = convert_element_dict_to_list(query, length, rows)
    context = dict(length=length, rows=rows)

    if data:
        matrix = PcMatrix(line_length=length, line_count=rows, lines=data)
        context['line'] = matrix
        return render(request, 'matrix_view.html', context=context)
    else:
        return render(request, 'matrix_edit.html', context=context)

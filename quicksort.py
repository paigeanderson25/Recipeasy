def partition(dict, low, high):
    pivot = dict[low][0]
    up = low
    down = high

    while up < down:
        j = up
        while j < high:
            if dict[up][type] > pivot:
                break
            up += 1
            j += 1
        j = high
        while j > low:
            if dict[down][type] < pivot:
                break
            down -= 1
            j -= 1
        if up < down:
            dict[up], dict[down] = dict[down], dict[up]
    dict[low], dict[down] = dict[down], dict[low]
    return down


def quickSort(dict, low, high):
    if low < high:
        pivot = partition(dict, low, high, type)
        quickSort(dict, low, pivot - 1, type)
        quickSort(dict, pivot + 1, high, type)
    return dict

import pandas as pd

df = pd.read_csv("RAW_recipes.csv")
df['index'] = df.index

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i][0] < right_half[j][0]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

def mergesortbyTime(dataframe):
    container = []
    index = 0
    for value in dataframe['minutes']:
        container.append([value, index])
        index += 1
    merge_sort(container)
    
    return container

timesortedlist = mergesortbyTime(df)
for i in range(10):
    index = timesortedlist[i][1]
    print(df.loc[index])

def partition(dict, low, high):
    pivot = dict[low]
    up = low
    down = high

    while up < down:
        j = up
        while j < high:
            if dict[up] > pivot:
                break
            up += 1
            j += 1
        j = high
        while j > low:
            if dict[down] < pivot:
                break
            down -= 1
            j -= 1
        if up < down:
            dict[up], dict[down] = dict[down], dict[up]
    dict[low], dict[down] = dict[down], dict[low]
    return down


def quickSort(dict, low, high):
    if low < high:
        pivot = partition(dict, low, high)
        quickSort(dict, low, pivot - 1)
        quickSort(dict, pivot + 1, high)
    return dict



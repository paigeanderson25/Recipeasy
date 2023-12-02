import pandas as pd

df = pd.read_csv("RAW_recipes.csv")
df['index'] = df.index

import time
currClock1 = time.time()
currClock2 = time.time()
print(currClock2 - currClock1)


def filter(dict, min, max, param):
    newDict = {}
    count = 0
    for i in dict:
        if dict[i][param] >= min:
            if dict[i][param] <= max:
                newDict[count] = [dict[0], dict[1], dict[2], dict[3]]
                count += 1
    dict = newDict

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

def partition(dict, low, high, type):
    pivot = dict[low][type]
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

def quickSort(dict, low, high, type):
    if low < high:
        pivot = partition(dict, low, high, type)
        quickSort(dict, low, pivot - 1, type)
        quickSort(dict, pivot + 1, high, type)
    return dict


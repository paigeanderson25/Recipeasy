import pandas as pd
import time

start_time=time.time()
df = pd.read_csv("RAW_recipes.csv")
df['index'] = df.index

def partition(dictionary, low, high):
    pivot = dictionary[low][0]
    
    up = low
    down = high

    while up < down:
        j = up
        while j < high:
        
            if dictionary[up][0] > pivot:
                break
            up += 1
            j += 1
            
        j = down
        while j > low:
            if dictionary[down][0] < pivot:
                break
            down -= 1
            j -= 1
        if up < down:
            temp = dictionary[up]
            dictionary[up] = dictionary[down]
            dictionary[down] = temp
    dictionary[low], dictionary[down] = dictionary[down], dictionary[low]
    return down


def quickSort(dictionary, low, high):
    if low < high:
        pivot = partition(dictionary, low, high)
        quickSort(dictionary, low, pivot - 1)
        quickSort(dictionary, pivot + 1, high)
    return dictionary


def quicksortandnarrowbyTime(dataframe, min_time, max_time):
    dictionary = {}
    index = 0
    for value in dataframe['minutes']:
        recipe_id = dataframe.loc[index, 'id']
        dictionary[index] = [value, recipe_id]
        index += 1

    dictionary = quickSort(dictionary, 0, len(dictionary) - 1)
    
    narrowedtimesorteddict = {}
    for i in range(len(dictionary)):

        if (dictionary[i][0] >= min_time):
            narrowedtimesorteddict[i] = dict[i]
        if (dictionary[i][0] > max_time):
            break
    return narrowedtimesorteddict


final_dict = quicksortandnarrowbyTime(df, 30, 35)
print(final_dict[0])


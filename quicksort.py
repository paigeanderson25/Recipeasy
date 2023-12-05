import pandas as pd
import time
import random

start_time = time.time()
'''df = pd.read_csv("RAW_recipes.csv")
df['index'] = df.index'''

#implements Dijkstra's 3 way partition method, elements are either less than, equal to, or greater than the pivot
def partition(arr, low, high):
    pivot = arr[random.randint(low, high)][0]
    i = low
    j = low
    k = high

    while j <= k:
        if arr[j][0] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
            j += 1
        elif arr[j][0] > pivot:
            arr[j], arr[k] = arr[k], arr[j]
            k -= 1
        else:
            j += 1

    return i, j

#main quicksort method
def quickSort(arr, low, high): 
    if low < high:
        i, j = partition(arr, low, high)
        quickSort(arr, low, i - 1)
        quickSort(arr, j, high)
        
#constructs a list from the data elements and calls quicksort to sort by time
def quicksortandnarrowbyTime(dataframe, min_time, max_time):
    container = []
    index = 0
    for value in dataframe['minutes']:
        container.append([value, index])
        index += 1

    quickSort(container, 0, len(container) - 1)
    
#iterates through the returned sorted list to find all elements that fit minute range criteria
    narrowedtimesortedlist = []
    for i in range(len(container)):
        if container[i][0] >= min_time:
            narrowedtimesortedlist.append(container[i])
        if container[i][0] > max_time:
            break

    return narrowedtimesortedlist

#takes a given list with format [[minutes, index]] and filters by calories
def XtoCalandnarrow(dataframe, Xlist, min, max):
    callist = []
    for i in range(len(Xlist)):
        nutrition = dataframe.loc[Xlist[i][1], 'nutrition']
        float_calories = float(nutrition)

        callist.append([float_calories, Xlist[i][1]])

    narrowedcallist = []
    for i in range(len(callist)):
        if (callist[i][0] <= max and callist[i][0] >= min):
            narrowedcallist.append([callist[i][0], callist[i][1]])

    return narrowedcallist

#repeats quicksort and filter method for calories
def quicksortandnarrowbyCal(dataframe, min, max):
    container = []
    index = 0
    for value in dataframe['nutrition']:
        float_calories = float(value)
        
        container.append([float_calories, index])
        index += 1
    quickSort(container, 0, len(container) - 1)
    
    narrowedcalsortedlist = []
    for i in range(len(container)):

        if (container[i][0] >= min):
            narrowedcalsortedlist.append(container[i])
        if (container[i][0] > max):
            break
    
    return narrowedcalsortedlist

#repeats quicksort and filter method for number of steps
def quicksortandnarrowbyDiff(dataframe, difficulty):
    container = []
    index = 0
    for value in dataframe['n_steps']:
        container.append([value, index])
        index += 1
    quickSort(container, 0, len(container) - 1)

    narroweddiffsortedlist = []
    range1 = []

    #sets range of step numbers to look for, depending on difficulty level chosen
    if difficulty == "easy":
        range1 = [0, 5]
    elif difficulty == "medium":
        range1 = [6, 9]
    else:
        range1 = [10, 99999]

    for i in range(len(container)):
        if (container[i][0] >= range1[0] and container[i][0] <= range1[1]):
            narroweddiffsortedlist.append(container[i])
        if (container[i][0] > range1[1]):
            break
    return narroweddiffsortedlist

#takes a given list with format [[minutes, index]] and filters by number of steps
def XtoDiffandnarrow(dataframe, Xlist, difficulty):
    difflist = []
    for i in range(len(Xlist)):
        steps = dataframe.loc[Xlist[i][1], 'n_steps']

        difflist.append([steps, Xlist[i][1]])

    narroweddiffsortedlist = []

    if difficulty == "easy":
        range1 = [0, 5]
    elif difficulty == "medium":
        range1 = [6, 9]
    else:
        range1 = [10, 99999]
    for i in range(len(difflist)):
        if (difflist[i][0] >= range1[0] and difflist[i][0] <= range1[1]):
            narroweddiffsortedlist.append(difflist[i])

    return narroweddiffsortedlist

#checks if elements from filtered list can be found matching specified ingredient search terms
def checkIngredients(dataframe, Xlist, ing1, ing2, ing3):
    result_list = []
    for i in range(len(Xlist)):
        ingredients = (dataframe.loc[Xlist[i][1], 'ingredients'])
        if ing1 == "-1" and ing2 == "-1" and ing3 == "-1":
            return Xlist
        elif ing1 in ingredients and ing2 == "-1" and ing3 == "-1":
            result_list.append(Xlist[i][1])
        elif ing1 in ingredients and ing2 in ingredients and ing3 == "-1":
            result_list.append(Xlist[i][1])
        elif ing1 in ingredients and ing2 in ingredients and ing3 in ingredients:
            result_list.append(Xlist[i][1])

    return result_list


def ingredientsonlyList(dataframe):
    container = []
    index = 0
    for value in dataframe['n_steps']:
        container.append([value, index])
        index += 1
    return container

#main method that controls how user-specified parameters are used to call necessary functions
def controlQuickSort(dataframe, min_time, max_time, min_cals, max_cals, difficulty, ing1, ing2, ing3):
    if max_time != -1:
        n_resultlist = quicksortandnarrowbyTime(dataframe, min_time, max_time)
        if max_cals != -1:
            n_resultlist = XtoCalandnarrow(dataframe, n_resultlist, min_cals, max_cals)
            if difficulty != "-1":
                n_resultlist = XtoDiffandnarrow(dataframe, n_resultlist, difficulty)
        else:
            if difficulty != "-1":
                n_resultlist = XtoDiffandnarrow(dataframe, n_resultlist, difficulty)
    else:
        if max_cals != -1:
            n_resultlist = quicksortandnarrowbyCal(dataframe, min_cals, max_cals)
            if difficulty != "-1":
                n_resultlist = XtoDiffandnarrow(dataframe, n_resultlist, difficulty)

        else:
            if difficulty != "-1":
                n_resultlist = quicksortandnarrowbyDiff(dataframe, difficulty)
            else:
                n_resultlist = ingredientsonlyList(dataframe)

    if ing1 != "-1":
        final_resultlist = checkIngredients(dataframe, n_resultlist, ing1, ing2, ing3)
    else:
        final_resultlist = [inner_list[1] for inner_list in n_resultlist]

    final_dict = {}

    for i in range(len(final_resultlist)):
        l = [i, dataframe.loc[final_resultlist[i], 'id']]
        final_dict[i] = l
    return final_dict

import pandas as pd
import time

start_time=time.time()
'''df = pd.read_csv("RAW_recipes.csv")
df['index'] = df.index'''

def merge_sort(arr): #merge sort, works for minutes, cals, and difficulty. Takes in 2D list with format[[value(ex.minutes), alphabetical index]]
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i][0] <= right_half[j][0]:
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

def mergesortandnarrowbyTime(dataframe, min, max): #sets up container for merge sort in minutes
    container = []
    index = 0
    for value in dataframe['minutes']:
        container.append([value, index])
        index += 1
    merge_sort(container)
    
    narrowedtimesortedlist = []
    for i in range(len(container)):

        if (container[i][0] >= min):
            narrowedtimesortedlist.append(container[i])
        if (container[i][0] > max):
            break
    return narrowedtimesortedlist


def findCals(nutrition_string):
    print(nutrition_string)
    calories = ""
    for i in range (1, 10):
        if nutrition_string[i] == ',':
            break
        calories += nutrition_string[i]
    
    f_calories = float(calories)

    return f_calories

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

def mergesortandnarrowbyCal(dataframe, min, max):
    container = []
    index = 0
    for value in dataframe['nutrition']:
        float_calories = float(value)
        container.append([float_calories, index])
        index += 1
    merge_sort(container)
    narrowedcalsortedlist = []
    for i in range(len(container)):

        if (container[i][0] >= min):
            narrowedcalsortedlist.append(container[i])
        if (container[i][0] > max):
            break
    return narrowedcalsortedlist

def mergesortandnarrowbyDiff(dataframe, difficulty):
    container = []
    index = 0
    for value in dataframe['n_steps']:
        container.append([value, index])
        index += 1
    merge_sort(container)
    
    narroweddiffsortedlist = []
    range1 = []
    
    if difficulty == "easy":
        range1 = [0, 5]
    elif difficulty== "medium":
        range1 = [6, 9]
    else:
        range1 = [10, 99999]

    for i in range(len(container)):
        if (container[i][0] >= range1[0] and container[i][0] <= range1[1]):
            narroweddiffsortedlist.append(container[i])
        if (container[i][0] > range1[1]):
            break
    return narroweddiffsortedlist

def XtoDiffandnarrow(dataframe, Xlist, difficulty):
    difflist = []
    for i in range(len(Xlist)):
        steps = dataframe.loc[Xlist[i][1], 'n_steps']
        
        difflist.append([steps, Xlist[i][1]])
    
    
    narroweddiffsortedlist = []

    if difficulty == "easy":
        range1 = [0, 5]
    elif difficulty== "medium":
        range1 = [6, 9]
    else:
        range1 = [10, 99999]
    for i in range(len(difflist)):
        if (difflist[i][0] >= range1[0] and difflist[i][0] <= range1[1]):
            narroweddiffsortedlist.append(difflist[i])
    
    return narroweddiffsortedlist


def fixPunctuation(input_name):
    current = 0
    name = str(input_name)
    newName = ""
    while current != len(name):
        
        if current == 0:
            newName += name[current].capitalize()
            current += 1
        elif current < len(name) - 2:
            if name[current] == " " and name[current + 1] == " ":
                
                current += 1
            elif name[current] == " " and name[current - 1] == "n" and name[current + 1] == "t" and name[current + 2] == " ":
                newName += "'t"
                current += 2
            elif name[current] == " " and name[current - 1] == "t" and name[current + 1] == "s" and name[current + 2] == " ":
                newName += "s"
                current += 2
            elif name[current] == " " and name[current - 1] != "" and name[current + 1] == "s" and name[current + 2] == " ":
                newName += "'s"
                current += 2
            
            elif name[current] == " " and name[current + 1] != " ":
                newName += " " + name[current + 1].capitalize()
                current += 2
            else:
                newName += name[current]
                current += 1

        else:
            newName += name[current]
            current += 1

    return newName 

def fixIngredientlist(ingredientstring):
    newingredientstring = ""
    for i in range(len(ingredientstring)):
        if ingredientstring[i] != "[" and ingredientstring[i] != "]" and ingredientstring[i] != "'":
            
            if ingredientstring[i - 1] == "'":
                newingredientstring += ingredientstring[i].capitalize()
            else:
                newingredientstring += ingredientstring[i]
    return newingredientstring

def fixSteps(string):
    final_steps = ""
    j = 1
    for i in range(len(string)):
        if string[i] == "[" or string[i] == "]" or string[i] == "'" or string[i] == ",":
            if string[i] == "," and string[i - 1] == " ":
                final_steps = final_steps[:-1]
                final_steps += ","
            
        else:
            if string[i - 1] == "'":
                final_steps += "\n" + str(j) + ". " + string[i].capitalize()
                j += 1
            else:
                final_steps += string[i]
    return final_steps



#print(fixIngredientlist(['apple', 'banana', 'beans']))

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



def controlMergeSort(dataframe, min_time, max_time, min_cals, max_cals, difficulty, ing1, ing2, ing3):
    if max_time != -1:
        n_resultlist = mergesortandnarrowbyTime(dataframe, min_time, max_time)
        if max_cals != -1:
            n_resultlist = XtoCalandnarrow(dataframe, n_resultlist, min_cals, max_cals)
            if difficulty != "-1":
                n_resultlist = XtoDiffandnarrow(dataframe, n_resultlist, difficulty)
        else:
            if difficulty != "-1":
                n_resultlist = XtoDiffandnarrow(dataframe, n_resultlist, difficulty)
    else:
        if max_cals != -1:
            n_resultlist = mergesortandnarrowbyCal(dataframe, min_cals, max_cals)
            if difficulty != "-1":
                n_resultlist = XtoDiffandnarrow(dataframe, n_resultlist, difficulty)
                
        else:
            if difficulty != "-1":
                n_resultlist = mergesortandnarrowbyDiff(dataframe, difficulty)
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


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

def mergesortbyTime(dataframe):
    container = []
    index = 0
    for value in dataframe['minutes']:
        container.append([value, index])
        index += 1
    merge_sort(container)
    
    return container

def narrowdownbyTime(sortedtimelist, min, max):
    narrowedtimesortedlist = []
    for i in range(len(sortedtimelist)):

        if (sortedtimelist[i][0] >= min):
            narrowedtimesortedlist.append(sortedtimelist[i])
        if (sortedtimelist[i][0] > max):
            break
    return narrowedtimesortedlist

def findCals(nutrition_string):
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
        float_calories = findCals(nutrition)
        
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
        float_calories = findCals(value)
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
    


'''timesortedlist = mergesortbyTime(df)
n_timesortedlist = narrowdownbyTime(timesortedlist, 0, 30)
n_callist = XtoCalandnarrow(df, n_timesortedlist, 100, 200)
print(timesortedlist[0:10])
print(n_timesortedlist[0:10])
print(n_callist[0:10])'''

n = 1
print("Welcome to Recipeasy!")
option = int(input("What would you like to sort by:\n1. Time\n2. Nutrition\n3. Both\nSelect a number: "))
if option != 2:
    minimum_time = int(input("Enter Minimum Time: "))
    maximum_time = int(input("Enter Maximum Time: "))
if option != 1:
    minimum_cal = int(input("Enter Minimum Calories: "))
    maximum_cal = int(input("Enter Maximum Calories: "))

if option == 1:
    timesortedlist = mergesortbyTime(df)
    n_resultlist = narrowdownbyTime(timesortedlist, minimum_time, maximum_time)
elif option == 2:
    n_resultlist = mergesortandnarrowbyCal(df, minimum_cal, maximum_cal)
else:
    timesortedlist = mergesortbyTime(df)
    n_timesortedlist = narrowdownbyTime(timesortedlist, minimum_time, maximum_time)
    n_resultlist = XtoCalandnarrow(df, n_timesortedlist, minimum_cal, maximum_cal)
option = 0
while option == 0 or (n * 10 < len(n_resultlist)):
    print("Here are some recipes you may like: ")
    for i in range(n * 10):
            index = n_resultlist[i][1]
            print(f"{i + 1} {df.loc[index, 'name']}")

    option = int(input("Select a recipe # to learn more, type 0 to see more recipes, or type anything else to quit: "))
    n += 1
    if 1 <= option <= n * 10:
        index = n_resultlist[option - 1][1]
        print(f"Name: {df.loc[index, 'name']}\nTime: {df.loc[index, 'minutes']}\nCalories: {findCals(df.loc[index, 'nutrition'])}\nIngredients: {df.loc[index, 'ingredients']}")
        break








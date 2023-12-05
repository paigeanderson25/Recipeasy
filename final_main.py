import pandas as pd
import PySimpleGUI as sg
import mergesort as ms
import quicksort as qs
import time

from selenium.webdriver.support.wait import WebDriverWait
import PIL
from PIL import ImageTk, Image

PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
from io import BytesIO
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import ChromiumOptions
from selenium.webdriver.common.by import By
import time
import random
from selenium.webdriver.support import expected_conditions as EC

useragents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1"]

useragent = random.choice(useragents)
options = ChromiumOptions()
options.add_argument("--headless=new")
options.add_argument(f"--user-agent={useragent}")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)


def getimages(name):
    driver.get('https://images.google.com/');

    search_box = driver.find_element("name", "q")

    search_box.send_keys(name + " food recipe")

    search_box.submit()

    img = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img')))

    src = img.get_attribute('src')

    data = src[22:]

    bytes_decoded = base64.b64decode(data)

    img = PIL.Image.open(BytesIO(bytes_decoded))

    out_jpg = img.convert("RGB")
    out_jpg.save("img.png")

# load in recipe dataset as dataframe
df = pd.read_csv("RAW_recipes.csv")
df['index'] = df.index
# filter df by including ingredients, time, nutrition (calories only), difficulty
df = df[['index', 'id', 'name', 'minutes', 'nutrition', 'n_steps', 'ingredients', 'steps']]
calOnly = df['nutrition'].str.split(',').str[0].str.replace('[', '').str.strip()
df['nutrition'] = calOnly

# check if min and max values are only digits
def CatchCharForInt(minVal, maxVal):
    if (minVal.isdigit() == False and minVal != '-1'):
        return False
    elif (maxVal.isdigit() == False and maxVal != '-1'):
        return False
    else:
        return True

# check if min values entered is greater than max value
def CatchInvalidInputInts(minVal, maxVal):
    if (minVal > maxVal):
        return False
    else:
        return True

# catch if ingredients contain characters other than letters or spaces
def CatchInvalidInputIngredients(ing1, ing2, ing3):
    if (ing1 != '-1' and not all(char.isalpha() or char.isspace() for char in ing1)):
        return False
    elif (ing2 != '-1' and not all(char.isalpha() or char.isspace() for char in ing2)):
        return False
    elif (ing3 != '-1' and not all(char.isalpha() or char.isspace() for char in ing3)):
        return False

    return True

# create error window if no recipes are found with matching input
def NoRecipesFound():
    layout = [[sg.Text('ERROR: no recipes found with ingredient(s)')]]
    errorWindow = sg.Window('Error', layout)
    event, values = errorWindow.read()
    errorWindow.close()

# create error window if an error is found
def ErrorPopup():
    layout = [[sg.Text('ERROR: INVALID INPUT')],
              [sg.Text('Please re-enter valid input values')]]
    errorWindow = sg.Window('Error', layout)
    event, values = errorWindow.read()
    errorWindow.close()

# creates recipe table using dataframe, final dictionary and final time
def CreateTable(df, final_dict, final_time):
    page = 0
    # Extracting the second list value from each dictionary key
    someValues = [i[1] for i in final_dict.values()]

    # Filtering the original DataFrame based on the 'id' column
    bigDf = df[df['id'].isin(someValues)]

    if len(bigDf.index) > 5:
        bigDf = bigDf.sample(frac=1)

    # Extracting the 'name' column from the filtered DataFrame
    nameDf = bigDf[['name']]

    # fix punctuation of names 
    nameList = []
    for value in nameDf['name']:
        properName = ms.fixPunctuation(value)
        nameList.append([properName])

    start = 0
    maxSize = len(nameList)
    end = min(5, maxSize)

    # set table window layout (table of recipes, buttons) 
    tableLayout = [
        [sg.Text(
            "Select a recipe and press to learn more:          Sort time: " + str(round(final_time, 4)) + ' seconds')],
        [sg.Table(border_width=0, num_rows=5, row_height=70, values=nameList[0:min(5, maxSize)], header_border_width=0,
                  header_background_color='white', headings=['Recipe Names'], header_font=('arima koshi', 16),
                  font=('arima koshi', 12),
                  expand_y=True, expand_x=True, hide_vertical_scroll=True, justification='left', auto_size_columns=True,
                  col_widths=[300],
                  key='table')],
        [sg.Button('Learn More')],
        [sg.Button('Next Page')],
        [sg.Button('Previous Page')],
        [sg.Button('Close')]
    ]
    window2 = sg.Window('Recipes', tableLayout, size=(800, 600))

    
    while True:
        event, values = window2.read()

        if event == sg.WINDOW_CLOSED or event == 'Close':
            break

        # if learn more is selected show recipe info
        elif event == 'Learn More':
            tableIndex = values['table'][0]
            tableIndex += page * 5
            if tableIndex != -1:
                row = bigDf.iloc[tableIndex]
                getimages(row['name'])
                ingredients = row['ingredients']
                steps = row['steps']
                formatData = f"Name: {ms.fixPunctuation(row['name'])}\nTime: {row['minutes']}\nCalories: {row['nutrition']}\nNumber of Steps: {row['n_steps']}\nIngredients: {ms.fixIngredientlist(ingredients)}\nSteps: {ms.fixSteps(steps)}"
                sg.popup_scrolled('Recipe Details', f"{formatData}", image="img.png")

        # if next page is selected show next 5 recipes
        elif event == 'Next Page':

            if start + 5 <= maxSize:
                start += 5
                end = min(end + 5, maxSize)
                window2['table'].update(values=nameList[start:end])
                page += 1

        # if previouse page is selected show previous 5 recipes
        elif event == 'Previous Page':

            if start - 5 >= 0:
                start -= 5
                end = min(end, end - 5)
                window2['table'].update(values=nameList[start:end])
                page -= 1

    start = start
    end = end
    page = page

    window2.close()


startingValue = ''
sg.theme('LightBrown3')

# set theme of overall window (checkbozes, input boxes, radio buttons, sort button)
layout = [[sg.Column(layout=[[sg.Text('WELCOME TO RECIPEASY', justification='center', font=('Any', 16))]],
                     element_justification='center', expand_x=True)],
          [sg.Text('Please select how you would like to filter your recipes:', justification='center',
                   font=('Any', 12))],

          [sg.Checkbox('Time', enable_events=True, key='time')],
          [sg.Text('Min Time:', key='min1', visible=False),
           sg.Input(startingValue, size=(len(startingValue), 1), key='minTime', visible=False),
           sg.Text('Max Time:', key='max1', visible=False),
           sg.Input(startingValue, size=(len(startingValue), 1), key='maxTime', visible=False)],

          [sg.Checkbox('Nutrition', enable_events=True, key='nutrition')],
          [sg.Text('Min Calories:', key='min2', visible=False),
           sg.Input(startingValue, size=(len(startingValue), 1), key='minCals', visible=False),
           sg.Text('Max Calories:', key='max2', visible=False),
           sg.Input(startingValue, size=(len(startingValue), 1), key='maxCals', visible=False)],

          [sg.Checkbox('Difficulty', enable_events=True, key='difficulty')],
          [sg.Radio('Easy', 'diffR', default=True, key='easy', visible=False),
           sg.Radio('Medium', 'diffR', key='medium', visible=False),
           sg.Radio('Hard', 'diffR', key='hard', visible=False)],

          [sg.Checkbox('Ingredients', enable_events=True, key='ingredients')],
          [sg.Text('Ingredient 1:', key='val1', visible=False),
           sg.Input(startingValue, size=(len(startingValue), 1), key='ing1', visible=False),
           sg.Text('Ingredient 2:', key='val2', visible=False),
           sg.Input(startingValue, size=(len(startingValue), 1), key='ing2', visible=False),
           sg.Text('Ingredient 3:', key='val3', visible=False),
           sg.Input(startingValue, size=(len(startingValue), 1), key='ing3', visible=False)],

          [sg.Radio('Merge Sort', 'sortMeth', default=True, key='merge', visible=True),
           sg.Radio('Quick Sort', 'sortMeth', key='quick', visible=True)],

          [sg.Button('Sort', size=(20, 2))]]

window = sg.Window('Recipeasy', layout, size=(800, 600))


while True:
    sg.theme('LightBrown3')
    minTime = '-1'
    maxTime = '-1'
    minCals = '-1'
    maxCals = '-1'
    selectedDif = '-1'
    ing1 = '-1'
    ing2 = '-1'
    ing3 = '-1'
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

    # if time is selected make min/max time input boxes visible
    elif event == 'time':
        if values['time']:
            window['min1'].update(visible=True)
            window['minTime'].update(visible=True)
            window['max1'].update(visible=True)
            window['maxTime'].update(visible=True)
        else:
            window['min1'].update(visible=False)
            window['minTime'].update(visible=False)
            window['max1'].update(visible=False)
            window['maxTime'].update(visible=False)

    # if nutrition is selected make min/max calories boxes visible
    elif event == 'nutrition':
        if values['nutrition']:
            window['min2'].update(visible=True)
            window['minCals'].update(visible=True)
            window['max2'].update(visible=True)
            window['maxCals'].update(visible=True)
        else:
            window['min2'].update(visible=False)
            window['minCals'].update(visible=False)
            window['max2'].update(visible=False)
            window['maxCals'].update(visible=False)

    # if difficulty is selected make easy, medium, hard radio buttons visible
    elif event == 'difficulty':
        if values['difficulty']:
            window['easy'].update(visible=True)
            window['medium'].update(visible=True)
            window['hard'].update(visible=True)
        else:
            window['easy'].update(visible=False)
            window['medium'].update(visible=False)
            window['hard'].update(visible=False)

    # if ingredients is selected make three ingredient input boxes visible
    elif event == 'ingredients':
        if values['ingredients']:
            window['val1'].update(visible=True)
            window['ing1'].update(visible=True)
            window['val2'].update(visible=True)
            window['ing2'].update(visible=True)
            window['val3'].update(visible=True)
            window['ing3'].update(visible=True)
        else:
            window['val1'].update(visible=False)
            window['ing1'].update(visible=False)
            window['val2'].update(visible=False)
            window['ing2'].update(visible=False)
            window['val3'].update(visible=False)
            window['ing3'].update(visible=False)

    # if sort is selected set values accordingly and call sort functions
    elif event == 'Sort':

        # if merge/quick selected then assign appropriate value to sorting method
        if values['merge']:
            sortMeth = 'merge'
        else:
            sortMeth = 'quick'

        # assign values to time variables, -1 if no input
        if (values['time']):
            minTime = values['minTime']
            maxTime = values['maxTime']

            if minTime == "":
                minTime = '-1'
            if maxTime == "":
                maxTime = '-1'

        # assign values to nutrition variables, -1 if no input
        if (values['nutrition']):
            minCals = values['minCals']
            maxCals = values['maxCals']

            if minCals == "":
                minCals = '-1'

            if maxCals == "":
                maxCals = '-1'

        # assign values to difficulty variables
        if (values['difficulty']):
            if values['easy']:
                selectedDif = 'easy'
            elif values['medium']:
                selectedDif = 'medium'
            elif values['hard']:
                selectedDif = 'hard'

        # assign values to ingredients, -1 if no input
        if (values['ingredients']):
            ing1 = values['ing1']
            ing2 = values['ing2']
            ing3 = values['ing3']

            if ing1 == "":
                ing1 = '-1'

            if ing2 == "":
                ing2 = '-1'

            if ing3 == "":
                ing3 = '-1'

        # assign min/max time values if only one input box is entered in
        if (minTime == "-1" and maxTime != "-1"):
            minTime = '0'
        elif (minTime != "-1" and maxTime == '-1'):
            maxTime = '100000'

        if (minCals == '-1' and maxCals != '-1'):
            minCals = '0'
        elif (minCals != '-1' and maxCals == '-1'):
            maxCals = '100000'
            
        # check if integers are not characters
        c1 = CatchCharForInt(minTime, maxTime)
        c2 = CatchCharForInt(minCals, maxCals)

        # check if ingredients are characters
        c3 = CatchInvalidInputIngredients(ing1, ing2, ing3)

        # check if min values are not greater than max values
        if c1 == True and c2 == True:
            c4 = CatchInvalidInputInts(int(minTime), int(maxTime))
            c5 = CatchInvalidInputInts(int(minCals), int(maxCals))
        else:
            c4 = False
            c5 = False

        # if any error occurs, show error popup
        if (c1 == False or c2 == False or c3 == False or c4 == False or c5 == False):
            sg.theme('DarkRed1')
            ErrorPopup()

        # perform sort functions if no errors
        else:
            final_time = 0
            i_minTime = int(minTime)
            i_maxTime = int(maxTime)
            i_minCals = int(minCals)
            i_maxCals = int(maxCals)

            # show loading gif, show perform merge sort, if recipes found create table and if not show error message
            if sortMeth == "merge":
                for i in range(160):
                    sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, time_between_frames=40)
                start_time = time.time()
                final_dictionary = ms.controlMergeSort(df, i_minTime, i_maxTime, i_minCals, i_maxCals, selectedDif,
                                                       ing1, ing2, ing3)
                end_time = time.time()

                final_time = end_time - start_time
                sg.PopupAnimated(None)
                if final_dictionary == {}:
                    sg.theme('DarkRed1')
                    NoRecipesFound()
                else:
                    CreateTable(df, final_dictionary, final_time)

            # show loading gif, show perform quick sort, if recipes found create table and if not show error message
            if sortMeth == "quick":
                for i in range(160):
                    sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, time_between_frames=40)
                start_time = time.time()
                final_dictionary = qs.controlQuickSort(df, i_minTime, i_maxTime, i_minCals, i_maxCals, selectedDif,
                                                       ing1, ing2, ing3)
                end_time = time.time()

                final_time = end_time - start_time
                sg.PopupAnimated(None)
                if final_dictionary == {}:
                    sg.theme('DarkRed1')
                    NoRecipesFound()
                else:
                    CreateTable(df, final_dictionary, final_time)

window.close()

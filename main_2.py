import pandas as pd
df = pd.read_csv("RAW_recipes.csv")
df['index'] = df.index
# filter df by including ingredients, time, nutrition (calories only), difficulty
df = df[['index', 'id', 'name', 'minutes', 'nutrition', 'n_steps', 'ingredients', 'description']]
calOnly = df['nutrition'].str.split(',').str[0].str.replace('[', '').str.strip()
#apply(lambda x: x[1] if len(x) > 1 else None))
df['nutrition'] = calOnly


ingredientsChecked = False # ingredients
timeChecked = True # minutes
nutritionChecked = False # nutrition --> first value
difficultyChecked = False # n_steps

# create GUI and change boolean values

smallDf = df = df[['index', 'id', 'minutes', 'nutrition', 'n_steps', 'ingredients']]
dic = df.set_index('index').T.to_dict('list')

if timeChecked == True :
    minTime = 0
    maxTime = 1000
    # use if statements: set minTime to first box; set max time to second box
    # insert sort function (sorts and filters data --> passes in dict, minTime, maxTime, time)


if nutritionChecked == True :
    minCal = 0
    maxCal = 100000
    # use if statements: set minCal to first box; set maxCal to second box
    # insert sort function (sorts and filters data --> passes in dict, minCal, maxCal, nutrition)



if difficultyChecked == True :
    minSteps = 0
    maxSteps = 1000
    # use if statements: set minSteps to first box; set maxSteps to second box
    # insert sort function (sorts and filters data --> passes in dict, minSteps, maxSteps, difficulty)



if ingredientsChecked == True :
    ing1 = 'cheese'
    ing2 = 'eggs'
    ing3 = 'meat'
    # use if statements: set ing1 to first box, ing2 to second box, ing3 to third box
    # no sort function, covert dic to df2
    filter2 = df.loc[(df['ingredients'].str.contains(ing1)) & (df['ingredients'].str.contains(ing2)) & (df['ingredients'].str.contains(ing3))]

#else :
    # convert dict to final df


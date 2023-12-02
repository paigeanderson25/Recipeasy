def finalids(dict): #maps final dict back to data frame
    someValues = []
    for i in dict.values():
        someValues.append(i[1])
    return someValues


def createDict(dataframe, param): #creates dictionary from the data frame
    df2 = dataframe[['index', param, 'id']]
    container = df2.set_index('index').T.to_dict('list')
    return container


def narrow_down(dict, min, max): #filter dict by min and max
    newdict = {}
    count = 0
    for key, value in dict.items():
        if value[0] >= min:
            newdict[count] = value
            count += 1
        if value[0] > max:
            break
    return newdict


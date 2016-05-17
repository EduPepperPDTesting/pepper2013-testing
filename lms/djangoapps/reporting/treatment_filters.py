
def mySplit(s, sep):
    s1 = s.replace(sep, sep + sep)
    lis = s1.split(sep)
    while '' in lis:
        lis[lis.index('')] = sep
    return lis


def midfixToPostfix(_midfixStr):
    pOut = {
        '#': 0,
        '(': 7,
        ')': 1,
        'and': 2,
        'or': 2
    }
    pIn = {
        '#': 0,
        '(': 1,
        ')': 7,
        'and': 2,
        'or': 2
    }

    string = _midfixStr
    inputList = string.split(' ')
    inputLen = len(inputList)

    tempList = list()   #stack
    tempList.append('#')
    resultList = list()

    x = 0
    while x < inputLen:
        if inputList[x] not in ['or', 'and', ')', '(']:
            resultList.append(inputList[x])

        elif inputList[x] == ')':
            while tempList[-1] != '(':
                resultList.append(tempList.pop())
            tempList.pop()

        else:
            if pOut[inputList[x]] > pIn[tempList[-1]]:
                tempList.append(inputList[x])
            else:
                while pOut[inputList[x]] <= pIn[tempList[-1]]:
                    resultList.append(tempList.pop())
                tempList.append(inputList[x])
        x += 1

    while tempList[-1] != '#':
        resultList.append(tempList.pop())

    return resultList


def postfixToMongo(_postfixList):
    postfixList = _postfixList
    postfixListLen = len(postfixList)

    resultList = list()

    x = 0
    while x < postfixListLen:
        key = None
        op = None
        value = None
        if postfixList[x] not in ['or', 'and']:
            sep = None
            '''
            for i in postfixList[x]:
                if i in ['=', '>', '<', '>=', '<=', '!=']:
                    sep = i
            '''
            sep = get_operator(postfixList[x])
            opList = mySplit(postfixList[x], sep)
            key = opList[0]
            op = opList[1]
            value = opList[2]
            if op == '=':
                result = "{'" + key + "':" + value + '}'
            elif op == '>':
                result = "{'" + key + "':{'$gt':" + value + '}}'
            elif op == '<':
                result = "{'" + key + "':{'$lt':" + value + '}}'
            elif op == '>=':
                result = "{'" + key + "':{'$gte':" + value + '}}'
            elif op == '<=':
                result = "{'" + key + "':{'$lte':" + value + '}}'
            elif op == '!=':
                result = "{'" + key + "':{'$ne':" + value + '}}'
            else:
                print 'something wrong! this is not a operator!'
            resultList.append(result)

        elif postfixList[x] == 'or':
            result = "{'$or':[" + resultList.pop(-1) + ',' + resultList.pop(-1) + ']}'
            resultList.append(result)

        elif postfixList[x] == 'and':
            result = "{'$and':[" + resultList.pop(-1) + ',' + resultList.pop(-1) + ']}'
            resultList.append(result)

        else:
            print 'something wrong! this is not a valid parameter!'

        x += 1

    return resultList.pop(-1)


def get_mongo_filters(str):
    postfixList = midfixToPostfix(str)
    filters = postfixToMongo(postfixList)
    return filters


def get_operator(condition):
    operators = ['>=', '<=', '>', '<', '!=', '=']
    for op in operators:
        if condition.find(op) >= 0:
            return op

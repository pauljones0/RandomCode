from itertools import combinations, combinations_with_replacement
def translate(input):
    count = 1
    while sum(input) > 0:
        input = (abs(input[0] - input[1]), abs(input[1] - input[2]), abs(input[2] - input[3]), abs(input[3] - input[0]))
        count += 1
    return count


def compute(x):
    maxSteps = 1
    minVals = []
    valuesToGoOver = combinations(range(x+1), 2)
    for i in valuesToGoOver:
        zero = [0]
        zero.extend(i)
        zero.append(x)
        steps = translate(zero)
        if steps > maxSteps:
            maxSteps = steps
            minVals = [i]
        elif steps == maxSteps:
            minVals.append(i)
    minValue = 999999999999999
    finalMinVals = []
    for i in minVals:
        curMin = sum(i)
        if curMin < minValue:
            minValue = sum(i)
            finalMinVals = [i]
        elif minValue == sum(i):
            finalMinVals.append(i)
    return maxSteps, minVals, minValue, finalMinVals

for i in range(8646064,8646065,1):
    answer = compute(i)
    if answer[0] > 20:
        print(str(i)+": ", answer[0], answer[3])

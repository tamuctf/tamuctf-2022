import string

from random import randint

with open("data.txt", "r") as rFile:
    data = rFile.read()

    # THIS GETS US THE NUM
    # ---------------------
    # for num in range(4, 17):
    #     partList = [[] for _ in range(num)]
    #     for i,c in enumerate(data):
    #         partList[i % num].append(c)

    #     indCoAvg = 0
    #     for p in partList:
    #         alphaCounts = dict()

    #         for c in p:
    #             if c in string.ascii_uppercase:
    #                 if c not in alphaCounts:
    #                     alphaCounts[c] = 1
    #                 else:
    #                     alphaCounts[c] += 1
    #         
    #         # print(alphaCounts)

    #         total = 0
    #         sumTotal = 0
    #         for k in alphaCounts.keys():
    #             v = alphaCounts[k]
    #             total += v
    #             sumTotal += v*(v-1)

    #         indCo = sumTotal * (1 / (total * (total-1)))
    #         indCoAvg += indCo
    #     print(num, indCoAvg / num)

    ## ONCE you get num = 12, you do the code below
    ## The numbers at the bottom require manual tuning but it is easy based on common english words

    num = 12
    partList = [[] for _ in range(num)]
    for i,c in enumerate(data):
        partList[i % num].append(c)

    alphaList = []
    for p in partList:
        alphaCounts = dict()

        for c in p:
            if c in string.ascii_uppercase:
                if c not in alphaCounts:
                    alphaCounts[c] = 1
                else:
                    alphaCounts[c] += 1
        alphaList.append(alphaCounts)
        
    keyList = [max(L, key=L.get) for L in alphaList]
    keyList = [ord(c) - 65 for c in keyList]

    keyList[0] = 12
    keyList[1] = 10
    keyList[2] = 22
    keyList[3] = 14
    keyList[4] = 5
    keyList[5] = 21
    keyList[6] = 13
    keyList[7] = 9
    keyList[8] = 14
    keyList[9] = 9
    keyList[10] = 20
    keyList[11] = 14

    print(keyList)
    
    shifted = []
    counter = 0
    for i,c in enumerate(data):
        if c not in string.ascii_uppercase:
            shifted.append(c)
        else:
            t = ord(c) - 65
            t -= keyList[i % num]
            t %= 26
            t += 65
            shifted.append(chr(t))

    shiftedData = "".join(shifted)
    print(shiftedData)

import math
# 计算点到线段的距离 P3 到线段P1P2的距离
def PointToSegDist(P1, P2, P3):
    x1, y1, x2, y2, x, y = P1[0], P1[1], P2[0], P2[1], P3[0], P3[1]

    cross = (x2 - x1) * (x - x1) + (y2 - y1) * (y - y1)
    if cross <= 0:
        return ((x - x1) * (x - x1) + (y - y1) * (y - y1)) ** 0.5

    d2 = (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)
    if cross >= d2:
        return ((x - x2) * (x - x2) + (y - y2) * (y - y2)) ** 0.5

    A = y2 - y1
    B = x1 - x2
    C = x2 * y1 - x1 * y2
    # 计算c点到直线距离
    distance = 0
    Q = A * A + B * B
    # print(Q - 0)
    if Q == 0:
        print('A*A+B*B = 0')
    else:
        distance = abs(A * x + B * y + C) / math.sqrt(A * A + B * B)
        # print ('2The distance of Point C to the line AB is:%f'%distance)
    return distance

def get_Distance_and_Coordinate(P1, P2, P3):
    x1, y1, x2, y2, x, y = P1[0], P1[1], P2[0], P2[1], P3[0], P3[1]
    # print("x1, y1, x2, y2, x, y:",x1, y1, x2, y2, x, y)

    cross = (x2 - x1) * (x - x1) + (y2 - y1) * (y - y1)
    if cross <= 0:
        return ((x - x1) * (x - x1) + (y - y1) * (y - y1)) ** 0.5 , (x1,y1)

    d2 = (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)
    if cross >= d2:
        return ((x - x2) * (x - x2) + (y - y2) * (y - y2)) ** 0.5 , (x2,y2)

    A = y2 - y1
    B = x1 - x2
    C = x2 * y1 - x1 * y2
    # 计算c点到直线距离
    distance = 0
    Q = A * A + B * B
    # print(Q - 0)
    if Q == 0:
        print('A*A+B*B = 0')
    else:
        distance = abs(A * x + B * y + C) / math.sqrt(A * A + B * B)
        d0 = math.sqrt(abs((x-x1)*(x-x1) + (y-y1)*(y-y1) - distance*distance))
        x0 = (d0 / math.sqrt(d2)) * (x2-x1) + x1
        y0 = (d0 / math.sqrt(d2)) * (y2-y1) + y1
        # print ('2The distance of Point C to the line AB is:%f'%distance)
    return distance,(x0,y0)

def get_mindisandcordinations(seg, P):
    minD = []
    minD_C = []
    tempHeadC = []
    temp1 = 0
    tempList1 = []
    tempList2 = []
    tempList3 = []
    for itemC in seg.cordinations:
        if len(tempHeadC) != 0:
            tempList1.append(get_Distance_and_Coordinate(tempHeadC, itemC, P)[0])
            tempList2.append(get_Distance_and_Coordinate(tempHeadC, itemC, P)[1])
            tempList3.append([tempHeadC,itemC])
            # print(get_Distance_and_Coordinate(tempHeadC, itemC, P))
            # print(tempList2)
        tempHeadC = itemC
    minD = min(tempList1)
    minD_C= tempList2[tempList1.index(min(tempList1))]
    minD_app = tempList3[tempList1.index(min(tempList1))]

    return minD,minD_C,minD_app
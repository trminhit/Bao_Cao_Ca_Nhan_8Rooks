def RookCost(state, col, n=8):
    row = len(state)       #Quan sap dat nam o hang row
    cost = 0

    cost += n - 1
    cost += (n - row - 1)

    return cost
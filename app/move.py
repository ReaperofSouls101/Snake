import numpy as np

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

UNOCCUPIED = 1
OCCUPIED   = -1
FOOD       = 1
HEAD       = -2
HUNT      = 1


TAIL       = 4
HEALTHLIM = 100
game_state = ""
directions = {'up': 0, 'down': 0, 'left': 0, 'right': 0}
goodfood = []


def calculate_move(new_board, game_state):
    myHealth = game_state['you']["health"]
#    print("Health Remaining " + str(myHealth))
#    if (myHealth > 98):
    find_food(game_state, new_board)
#    else:
#    find_heads(game_state, new_board)

    print(max(directions, key=lambda k: directions[k]))
    print("UP", directions["up"])
    print("DOWN", directions["down"])
    print("LEFT", directions["left"])
    print("RIGHT", directions["right"])
    return max(directions, key=lambda k: directions[k])

def find_food(game_state, board_matrix ):
    print("Getting Food")
    minsum = 1000
    y = game_state['you']["body"][0]["y"]
    x = game_state['you']["body"][0]["x"]
    directions["up"] = 0
    directions["down"] = 0
    directions["left"] = 0
    directions["right"] = 0
    print("Your Coordinates "+ str(x) + ", " + str(y))
    for food in game_state["board"]["food"]:
        tot = abs(food["x"] - x)
        tot += abs(food["y"] - y)
        if (tot < minsum):
            goodfood = food
            minsum = tot
    print("Target Coordinates "+ str(goodfood["x"]) + ", " + str(goodfood["y"]))
    best_move= find_path(game_state, board_matrix,x,y, goodfood["x"], goodfood["y"])
    print("Best Move before dodge "+best_move)
    dodgeGrid = dodgeGridCreation(game_state, board_matrix, goodfood["x"], goodfood["y"], best_move)
    threeByThree = moveAura(x, y, dodgeGrid)
    remakeMove = ensureBestMove(threeByThree)
    print(np.matrix(dodgeGrid))
    print(np.matrix(threeByThree))

#def find_heads(game_state, board_matrix ):
#
##    doesn't work
#    print("Attacking Heads")
#    minsum = 1000
#    y = game_state['you']["body"][0]["y"]
#    x = game_state['you']["body"][0]["x"]
#    directions["up"] = 0
#    directions["down"] = 0
#    directions["left"] = 0
#    directions["right"] = 0
#    print("Your Coordinates "+ str(x) + ", " + str(y))
##    attackHead = game_state["board"]["snakes"][0]["body"][0]
#    for head in game_state["board"]["snakes"]:
#        tot = abs(head["body"][0]["x"] - x)
#        tot += abs(head["body"][0]["y"] - y)
#        if tot < minsum and tot > 2:
#            attackHead = head["body"][0]
#            minsum = tot
#    print("Target Coordinates "+ str(attackHead["x"]) + ", " + str(attackHead["y"]))
#    find_path(game_state, board_matrix,x,y, attackHead["x"], attackHead["y"])


def dodgeGridCreation(game_state, board_matrix, targetx, targety, best_move):
#    check if snake is there
    height = game_state["board"]["height"]
    width = game_state["board"]["width"]

    dodgeGrid = [[UNOCCUPIED for y in range(height)] for x in range(width)]
    
    for snake in game_state["board"]["snakes"]:
        snakeBody = snake["body"]
        for part in snakeBody:
            dodgeGrid[part["y"]][part["x"]] = OCCUPIED
            if part["x"] == targetx and part["y"] == targety:
                directions[best_move] -= 1000
                                 
    return dodgeGrid

def moveAura(yourX, yourY, occupiedSpaces):
    aura = [[None for y in range(3)] for x in range(3)]

    for i in range(len(aura)):
        for j in range(len(aura[i])):
            if yourX<=0 or yourY<=0:
                aura[i][j] = OCCUPIED
            else:
                aura[i][j] = occupiedSpaces[yourY+i-1][yourX+j-1]

    return aura


def ensureBestMove(aura):
    for i in range(len(aura)):
        for j in range(len(aura[i])):
            if i==0 and j==0:
                directions["right"] += 10;
                directions["down"] += 10;
            elif i==0 and j==1:
                directions["down"] += 10;
            elif i==0 and j==2:
                directions["left"] += 10;
                directions["down"] += 10;
            elif i==1 and j==0:
                directions["right"] += 10;
            elif i==1 and j==2:
                directions["left"] += 10;
            elif i==2 and j==0:
                directions["right"] += 10;
                directions["up"] += 10;
            elif i==2 and j==0:
                directions["up"] += 10;
            elif i==2 and j==0:
                directions["left"] += 10;
                directions["up"] += 10;


def find_path(game_state, board_matrix, x, y, targetx, targety):
    height = game_state["board"]["height"]
    grid = Grid(width=height, height=height, matrix=board_matrix)
    start = grid.node(x, y)
    end = grid.node(targetx, targety)
    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, runs = finder.find_path(start, end, grid)
    
    if (len(path) > 0):
        pathx = path[1][0]
        pathy = path[1][1]
        print("Next Move Coordinates "+ str(path[1][0]) + ", " + str(path[1][1]))
        y = game_state['you']["body"][0]["y"]
        x = game_state['you']["body"][0]["x"]
        # go up
        if ((y - 1) == pathy) and (x == pathx):
            directions["up"] += 20
            return "up"
        # go down
        if ((y + 1) == pathy) and (x == pathx):
            directions["down"] += 20
            return "down"
        # go left
        if ((x - 1) == pathx) and (y == pathy):
            directions["left"] += 20
            return "left"
        # go right
        if ((x + 1) == pathx) and (y == pathy):
            directions["right"] += 20
            return "right"

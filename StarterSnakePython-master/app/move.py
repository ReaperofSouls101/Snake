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

def pick_state(board_matrix, game_state) :
    if len(game_state["snakes"]) == 1 and HUNT == 1 :
        hunt(board_matrix, game_state)
    else:
        stay_alive(board_matrix, game_state)

def stay_alive(board_matrix, game_state):
    calculate_move(board_matrix, game_state)

def hunt(board_matrix, game_state) :
    calculate_move(board_matrix, game_state)

def calculate_move(board_matrix, game_state):
    set_game_state(game_state)
    height = game_state["board"]["height"]
    head = game_state['you']["body"][0]
    x = head["x"]
    y = head["y"]
    print(x,y)
    print(board_matrix)
    health = game_state['you']["health"]
    directions['up'] = 0
    directions['down'] = 0
    directions['right'] = 0
    directions['left'] = 0
    global HEALTHLIM

    largest_snek = 0
    for snek in game_state["board"]["snakes"]:
        snake_body = snek['body']
        if(len(snake_body) > largest_snek) :
            largest_snek = len(snake_body)

    if(len(game_state['you']["body"]) < largest_snek) :
        HEALTHLIM = 100
    else:
        HEALTHLIM = 25

    if health < HEALTHLIM and len(game_state['board']['food'])>0:
        find_food(game_state, board_matrix)
    else:
        find_edge(game_state, board_matrix)

    # Check up
    if head["y"] - 1 < 0 or board_matrix[y-1][x] == OCCUPIED :
        directions["up"] = -1000
    else:
        directions["up"] += sum(board_matrix, head["x"], head["y"] - 1, height, game_state)


    # Check down
    if head["y"] + 1 > (height - 1) or board_matrix[y+1][x] == OCCUPIED :
        directions["down"] = -1000
    else:
        directions["down"] += sum(board_matrix, head["x"], head["y"] + 1, height, game_state)


    # Check Left
    if head["x"] - 1 < 0 or board_matrix[y][x-1] == OCCUPIED :
        directions["left"] = -1000
    else:
        directions["left"] += sum(board_matrix, head["x"] - 1, head["y"], height, game_state)


    # check right
    if head["x"] + 1 > (height - 1) or board_matrix[y][x+1]== OCCUPIED :
        directions["right"] = -1000
    else:
        directions["right"] += sum(board_matrix, head["x"] + 1, head["y"], height, game_state)

    quad(board_matrix, game_state)
    best_move =  max(directions, key=lambda k: directions[k])
    if(check_move(x,y,best_move, board_matrix, height) == 4 ) :
        directions[best_move] += -500
    print(max(directions, key=lambda k: directions[k]))
    print("UP", directions["up"])
    print("DOWN", directions["down"])
    print("LEFT", directions["left"])
    print("RIGHT", directions["right"])
    return max(directions, key=lambda k: directions[k])


def check_move(x, y, best_move, board_matrix, height) :
    sum_move = 0
    if(best_move == 'right') :
        x = x+1
    if(best_move == 'left') :
        x = x-1
    if(best_move == 'up') :
        y = y-1
    if(best_move == 'down') :
        y = y+1


    # Check up
    if y - 1 > 0 and board_matrix[y-1][x] == OCCUPIED :
        sum_move = sum_move + 1


    # Check down
    if y + 1 < (height - 1) and board_matrix[y+1][x] == OCCUPIED :
        sum_move = sum_move + 1


    # Check Left
    if x - 1 > 0 and board_matrix[y][x-1] == OCCUPIED :
        sum_move = sum_move + 1


    # check right
    if x + 1 < (height - 1) and  board_matrix[y][x+1]== OCCUPIED :
        sum_move = sum_move + 1

    return sum_move



def find_food(game_state, board_matrix ):
    minsum = 1000
    y = game_state['you']["body"][0]["y"]
    x = game_state['you']["body"][0]["x"]

    for food in game_state["board"]["food"]:
        tot = abs(food['x'] - x)
        tot += abs(food['y'] - y)
        if (tot < minsum):
            goodfood = food
            minsum = tot

    find_path(game_state, board_matrix,x,y, goodfood["x"], goodfood['y'])


def find_edge(game_state, board_matrix ) :
    height = game_state["board"]["height"]
    y = game_state['you']["body"][0]["y"]
    x = game_state['you']["body"][0]["x"]
    pathx = 0
    pathy = 0
    shortess_path = 10000

    for spot_x in range(height) :
        if 1 :
            height = game_state["board"]["height"]
            grid = Grid(width=height, height=height, matrix=board_matrix)
            start = grid.node(x, y)
            end = grid.node(spot_x, 0)
            finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
            path, runs = finder.find_path(start, end, grid)

            if len(path) < shortess_path and len(path) > 1:
                pathx = path[1][0]
                pathy = path[1][1]
                shortess_path = len(path)

    for spot_x in range(height) :
        if 1 :
            height = game_state["board"]["height"]
            grid = Grid(width=height, height=height, matrix=board_matrix)
            start = grid.node(x, y)
            end = grid.node(spot_x, height-1)
            finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
            path, runs = finder.find_path(start, end, grid)

            if len(path) < shortess_path and len(path) > 1:
                pathx = path[1][0]
                pathy = path[1][1]
                shortess_path = len(path)

    for spot_y in range(height) :
        if 1 :
            height = game_state["board"]["height"]
            grid = Grid(width=height, height=height, matrix=board_matrix)
            start = grid.node(x, y)
            end = grid.node(0, spot_y)
            finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
            path, runs = finder.find_path(start, end, grid)

            if len(path) < shortess_path and len(path) > 1:
                pathx = path[1][0]
                pathy = path[1][1]
                shortess_path = len(path)

    for spot_y in range(height) :
        if 1 :
            height = game_state["board"]["height"]
            grid = Grid(width=height, height=height, matrix=board_matrix)
            start = grid.node(x, y)
            end = grid.node(height-1, spot_y)
            finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
            path, runs = finder.find_path(start, end, grid)

            if len(path) < shortess_path and len(path) > 1:
                pathx = path[1][0]
                pathy = path[1][1]
                shortess_path = len(path)

    if (1):

        if ((y - 1) == pathy) and (x == pathx):
            directions["up"] += 15
            print("Pick: UP")
        # go down
        if ((y + 1) == pathy) and (x == pathx):
            directions["down"] += 15
            print("Pick: down")
        # go left
        if ((x - 1) == pathx) and (y == pathy):
            directions["left"] += 15
            print("Pick: left")
        # go right
        if ((x + 1) == pathx) and (y == pathy):
            directions["right"] += 15
            print("Pick: right")




def find_path(game_state, board_matrix, x, y, foodx, foody):
    height = game_state["board"]["height"]
    grid = Grid(width=height, height=height, matrix=board_matrix)
    start = grid.node(x, y)
    end = grid.node(foodx, foody)
    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, runs = finder.find_path(start, end, grid)

    if (len(path) > 0):
        pathx = path[1][0]
        pathy = path[1][1]

        y = game_state['you']["body"][0]["y"]
        x = game_state['you']["body"][0]["x"]
        # go up
        if ((y - 1) == pathy) and (x == pathx):
            directions["up"] += 20
            print("Pick: UP")
        # go down
        if ((y + 1) == pathy) and (x == pathx):
            directions["down"] += 20
            print("Pick: down")
        # go left
        if ((x - 1) == pathx) and (y == pathy):
            directions["left"] += 20
            print("Pick: left")
        # go right
        if ((x + 1) == pathx) and (y == pathy):
            directions["right"] += 20
            print("Pick: right")


def sum(matrix, x, y, height, gamestate):
    sum = 0
    if matrix[y ][x] == HEAD:
        snek = get_snek(x, y , game_state)
        if is_bigger(snek, gamestate):
            sum += 20
        else:
            sum += -75
            print(snek)

    if (x - 1) >= 0:
        sum += matrix[y][x-1]
        if matrix[y][x-1] == HEAD :
            snek = get_snek(x-1, y, game_state)
            if is_bigger(snek, gamestate):
                sum += 20
            else:
                sum += -75
                print(snek)

    if (x + 1) < height:
        sum += matrix[y][x+1]
        if matrix[y][x+1] == HEAD :
            snek = get_snek(x+1, y, game_state)
            if(is_bigger(snek, gamestate)):
                sum += 20
            else:
                sum += -75
                print(snek)

    if (y - 1) >= 0:
        sum += matrix[y-1][x]
        if matrix[y-1][x] == HEAD :
            snek = get_snek(x, y-1, game_state)
            if is_bigger(snek, gamestate):
                sum += 20
            else:
                sum += -75
                print(snek)

    if (y + 1) < height:
        sum += matrix[y+1][x]
        if matrix[y+1][x] == HEAD :
            snek = get_snek(x, y+1, game_state)
            if is_bigger(snek, gamestate):
                sum += 20
            else:
                sum += -75
                print(snek)

    if (x-1) >= 0 and (y+1) < height:
        sum += matrix[y+1][x-1]

    if (x-1) >= 0 and (y-1) > 0:
        sum += matrix[y-1][x-1]

    if (x+1)< height and (y+1) < height:
        sum += matrix[y+1][x+1]

    if (x-1) > 0 and (y-1) > 0:
        sum += matrix[y-1][x-1]

    return sum + matrix[y][x]



def quad(matrix, game_state):
    x = game_state["you"]["body"][0]["x"]
    y = game_state["you"]["body"][0]["y"]
    height = game_state['board']['height']
    quad1 = 0
    quad2 = 0
    quad3 = 0
    quad4 = 0
    for i in range(y):
        for j in range(x):
            if(matrix[j][i]== UNOCCUPIED):
                quad1 += 3

    for i in range(y):
        for j in range(x, height):
            if(matrix[j][i]== UNOCCUPIED):
                quad2 += 3

    for i in range(y, height):
        for j in range(x):
            if(matrix[j][i]== UNOCCUPIED):
                quad3 += 3

    for i in range(y, height):
        for j in range(x, height):
            if(matrix[j][i]== UNOCCUPIED):
                quad4 += 3
    directions['up'] += (quad1 + quad2)/height
    directions['down'] += (quad3 + quad4)/height
    directions['left'] += (quad1 + quad3)/height
    directions['right'] += (quad2 + quad4)/height
    print(quad1, quad2, quad3, quad4)



def is_bigger(snek, game):
    if len(game["you"]["body"]) > snek:
        print("length**************")

        return True
    print("SNake length", snek, "our length ", len(game['you']['body']))
    return False

def get_snek(x, y, game_state):
    for snek in game_state["board"]["snakes"]:
        snake_body = snek['body']
        for xy in snake_body[0:]:
            if( xy["y"]== y and xy["x"]==x):
                return len(snake_body)


def set_game_state(new_game_state):
    global game_state
    game_state = new_game_state


def get_game_State():
    return game_state

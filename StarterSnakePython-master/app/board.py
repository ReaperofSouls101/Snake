import numpy as np

UNOCCUPIED = 1
OCCUPIED   = -1
FOOD       = 1
HEAD       = -2



def update_board(state):
    height = state["board"]["height"]
    Matrix = [[UNOCCUPIED for x in range(height)] for y in range(height)]
    board_state = state['board']
    food_coords = board_state['food']
    snakes = board_state['snakes']
    my_body = state['you']['body']

    for coord in food_coords:
        Matrix[coord['y']][coord['x']] = FOOD

    for snake in snakes:
        snake_body = snake['body']
        for coord in snake_body[1:]:
            Matrix[coord['y']][coord['x']] = OCCUPIED
        Tail_coord = snake_body[len(snake_body)-1]
        one_coord = snake_body[len(snake_body) - 2]
        Matrix[Tail_coord['y']][Tail_coord['x']] = UNOCCUPIED
        if Tail_coord['x'] == one_coord['x'] and Tail_coord['y'] == Tail_coord['y']:
            Matrix[Tail_coord['y']][Tail_coord['x']] = OCCUPIED
        head_coord = snake_body[0]
        Matrix[head_coord['y']][head_coord['x']] = HEAD

    for coord in my_body[0:]:
        Matrix[coord['y']][coord['x']] = OCCUPIED
    tail = my_body[len(my_body)-1]
    oneback = my_body[len(my_body) - 2]
    Matrix[tail['y']][tail['x']] = 4
    if state['turn']< 3:
        Matrix[tail['y']][tail['x']] = OCCUPIED
    if tail['x']== oneback['x'] and tail['y'] == oneback['y']:
        Matrix[tail['y']][tail['x']] = OCCUPIED


    # print('Updated board state for turn ' + str(state['turn']) + ':\n\n' + str(board) + '\n\n')
   # for x in range(len(Matrix)):
   # print(Matrix[x])
    return Matrix

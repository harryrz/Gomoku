"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Oct. 28, 2022
"""

#return true if no stone on board
def is_empty(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != " ":
                return False
    return True

#return true if board is full
def is_full(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == " ":
                return False
    return True


#check if the input y and x is a valid location on board
def is_sq_in_board(board, y, x):
    #since board is a square, len of row and col is the same
    col_row_length = len(board)
    if (x >= 0 and x+1 <= col_row_length) and (y >= 0 and y+1 <= col_row_length):
        return True
    return False

# #reverse the direction since in is_bounded we are checking from end to start
# def reverse_d(d_y, d_x):
# return d_y * -1, d_x * -1


def is_bounded(board, y_end, x_end, length, d_y, d_x):
    num_close = 0

    #check the location after the end one, valid? closed?
    y_after = y_end + d_y
    x_after = x_end + d_x
    #if valid location, check if blocked
    if is_sq_in_board(board, y_after, x_after):
        if not board[y_after][x_after] == " ":
            num_close += 1
    #if out of bound
    else:
        num_close += 1

    #check the location before the start one, valid?
    y_before = y_end - length * d_y
    x_before = x_end - length * d_x
    if is_sq_in_board(board, y_before, x_before):
        if not board[y_before][x_before] == " ":
            num_close += 1
    else:
        num_close += 1

    if num_close == 2:
        return "CLOSED"
    elif num_close == 1:
        return "SEMIOPEN"
    else:
        return "OPEN"











#direction y and x can only be 1 or -1 or 0 (technically -1 is unnecessary)
def is_sequence_complete(board, col, y_start, x_start, length, d_y, d_x):
    #first check if sequence exists
    y = y_start
    x = x_start

    for i in range(length):
        #if cur checking square is not the color we want or it's out of bound
        if  (not is_sq_in_board(board, y, x)) or board[y][x] != col:
            return False
        y += d_y
        x += d_x

    #if sequence exist, check boundary cases before and after
    before_y = y_start - d_y
    before_x = x_start - d_x

    #if before square is valid square
    if is_sq_in_board(board, before_y, before_x):
        if board[before_y][before_x] == col:
            return False

    #if after square is valid square
    if is_sq_in_board(board, y, x):
        if board[y][x] == col:
            return False

    return True





def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count = 0
    semi_open_seq_count = 0

    cur_y = y_start
    cur_x = x_start

    #keep checking rows/columns/diagonals when cur_y/x is in bound of board
    while is_sq_in_board(board, cur_y, cur_x):
        #using another method, if cur location contain a complete sequence match length and direction
        if is_sequence_complete(board, col, cur_y, cur_x, length, d_y, d_x):
            #check bounded condition, note the cur x and y send into the fcn is actually the end point
            condition = is_bounded(board, cur_y + (length-1) * d_y, cur_x + (length-1) * d_x, length, d_y, d_x)
            if condition == "OPEN":
                open_seq_count += 1
            elif condition == "SEMIOPEN":
                semi_open_seq_count += 1

        #go to next location in a row
        cur_y += d_y
        cur_x += d_x
    return open_seq_count, semi_open_seq_count






#detect open and semi open sequence for whole board
def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0


    for i in range(len(board)):
        #check direction left to right for all rows
        temp_open, temp_semi = detect_row(board, col, i, 0, length, 0, 1)
        open_seq_count += temp_open
        semi_open_seq_count += temp_semi

        #check direction up to bottom for all rows
        temp_open, temp_semi = detect_row(board, col, 0, i, length, 1, 0)
        open_seq_count += temp_open
        semi_open_seq_count += temp_semi

        #check direction top left to bottom right for TOP HALF of rows
        temp_open, temp_semi = detect_row(board, col, 0, i, length, 1, 1)
        open_seq_count += temp_open
        semi_open_seq_count += temp_semi

        #check direction top right to bottom left for TOP HALF of rows
        temp_open, temp_semi = detect_row(board, col, 0, i, length, 1, -1)
        open_seq_count += temp_open
        semi_open_seq_count += temp_semi

    #check diagonal for rest of rows: we seperate from horizontal and vertical bc diagonal required to check additional len - 1 cols
    for j in range(1, len(board)):
        #check top left bottom right for LEFT MOST rows, note start from 1, 0 not 0, 0
        temp_open, temp_semi = detect_row(board, col, j, 0, length, 1, 1)
        open_seq_count += temp_open
        semi_open_seq_count += temp_semi

        #print(j, 0)

        #check top right bottom left for RIGHT MOST rows
        temp_open, temp_semi = detect_row(board, col, j, len(board) - 1, length, 1, -1)
        open_seq_count += temp_open
        semi_open_seq_count += temp_semi

    return open_seq_count, semi_open_seq_count





#check placing stone to which location will maximize the score calculated in fcn
def search_max(board):
    move_y = -1
    move_x = -1
    max_score = -100000000

    for i in range (len(board)):
        for j in range (len(board)):
            #if cur location is empty, it's a possible location to put stone
            if board[i][j] == " ":
                #locationo is not important as we only put one stone
                put_seq_on_board(board, i, j, 1, 1, 1, "b")

                #if cur move make score maximum, record this move
                cur_score = score(board)
                if cur_score > max_score:
                    max_score = cur_score
                    move_y = i
                    move_x = j

                #make board to original state (remove that black stone)
                board[i][j] = " "

    return move_y, move_x







def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)

    #determine if any white or black has a row of 5
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE


    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])





#tell whether the game ends and if so who wins
def is_win(board):
    #check if any white in row of 5
    cur_score = score(board)
    #if black has at least 1 row of 5, score fcn will return MAX_SCORE value
    if cur_score == 100000:
        return "Black won"
    #if white has at least 1 row of 5, score fcn return -Max score
    elif cur_score == -100000:
        return "White won"
    #if board is full and none win
    elif is_full(board):
        return "Draw"
    else:
        return "Continue playing"




#print layout of current board
def print_board(board):
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    print(s)


#create empty board
def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))






def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])




    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res





        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x













#tests================================================================================================

def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 6; d_x = 1; d_y = 1; length = 2
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 7
    x_end = 6

    print(is_bounded(board, y_end, x_end, length, d_y, d_x))


    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'CLOSED':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 6; y = 1; d_x = -1; d_y = 1; length = 2
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")

    x = 3; y = 4; d_x = -1; d_y = 1; length = 2
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")

    x = 0; y = 7; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")

    x = 5; y = 6; d_x = 1; d_y = 1; length = 2
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")


    print_board(board)
    if detect_row(board, "w", 1,0, 2,d_y,d_x) == (2,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)

    x = 6; y = 1; d_x = -1; d_y = 1; length = 2;
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")

    x = 3; y = 4; d_x = -1; d_y = 1; length = 2
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")

    x = 0; y = 7; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")

    x = 0; y = 0; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")

    x = 6; y = 3; d_x = 1; d_y = 1; length = 2
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")


    print_board(board)

    col = "w"; length = 3
    print(detect_rows(board, col, length))


    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 6; y = 1; d_x = -1; d_y = 1; length = 2;
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")

    x = 3; y = 4; d_x = -1; d_y = 1; length = 2
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")

    x = 0; y = 7; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")

    x = 0; y = 0; d_x = 0; d_y = 1; length = 2
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")

    x = 6; y = 3; d_x = 1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")



    print_board(board)

    print(search_max(board))


    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0




if __name__ == '__main__':
    # test_is_empty()
    # test_is_bounded()
    # test_detect_row()
    # test_detect_rows()
    # test_search_max()
    print(play_gomoku(8))
    #some_tests()
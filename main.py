import numpy as np
#import pytracy

#pytracy.enable_tracing(True)    

class Node:
    def __init__(self, square = None, digit = None):
        self.children = []
        self.square = square
        self.digit = digit
        self.current_child = 0

##This is probably causing overhead too.

class Board:

    BOX_COORDS = [[0, 1, 2, 9, 10, 11, 18, 19, 20], 
                  [3, 4, 5, 12, 13, 14, 21, 22, 23],
                  [6, 7, 8, 15, 16, 17, 24, 25, 26],
                  [27, 28, 29, 36, 37, 38, 45, 46, 47],
                  [30, 31, 32, 39, 40, 41, 48, 49, 50],
                  [33, 34, 35, 42, 43, 44, 51, 52, 53],
                  [54, 55, 56, 63, 64, 65, 72, 73, 74],
                  [57, 58, 59, 66, 67, 68, 75, 76, 77],
                  [60, 61, 62, 69, 70, 71, 78, 79, 80]]
    #I got annoyed by all the maths

    def __init__(self):

        #Can't believe I am actually phasing out BitwiseInt but the class overhead is just too high
        self.rows = [0b000000000 for i in range(9)]
        self.columns = [0b000000000 for i in range(9)]
        self.boxes = [0b000000000 for i in range(9)]

        #self.squares = [BitwiseInt(0) for i in range(81)]
        self.solution = [0 for i in range(81)]
        self.free_squares = [0 for i in range(81)]

        self.invalid_puzzle = False

    def set_up_board(self, inputted_arr):
        inputted_arr = np.array(inputted_arr)
        
        for row in range(9):
            self.rows[row] = self.get_mask_from_arr(inputted_arr[row])

        for column in range(9):
            new_column = [inputted_arr[i][column] for i in range(9)]
            self.columns[column] = self.get_mask_from_arr(new_column)

        for box in range(9):
            new_box = []

            for i in self.BOX_COORDS[box]:
                box_row = i // 9
                box_column = i % 9
                new_box.append(inputted_arr[box_row][box_column])

            self.boxes[box] = self.get_mask_from_arr(new_box)

        self.solution = inputted_arr.flatten().tolist()

        #self.update_all_squares()

    def get_mask_from_arr(self, arr):
        current = 0
        for i in range(9):
            if arr[i] != 0:
                if ((current & 0b000000001 << (arr[i] - 1)) == (0b000000001 << (arr[i] - 1))):
                    self.invalid_puzzle = True
                current |= (0b000000001 << (arr[i] - 1))
        
        return current

    def update_all_squares(self): #This might be unnecessary now
        for i in range(81):

            row = i // 9
            column = i % 9
            box = self.calculate_box(i)

            """if i == 45:
                print(bin(self.rows[row].mask))
                print (bin(self.columns[column].mask))
                print (bin(self.boxes[box].mask))"""

            new_mask = self.rows[row].mask
            new_mask |= self.columns[column].mask
            new_mask |= self.boxes[box].mask

            #self.squares[i].mask = new_mask

    def place_number(self, square_index, digit):
        square_row = square_index // 9
        square_column = square_index % 9
        square_box = self.calculate_box(square_index)

        digit_mask = (0b000000001 << digit)

        self.rows[square_row] |= digit_mask
        self.columns[square_column] |= digit_mask
        self.boxes[square_box] |= digit_mask

        self.solution[square_index] = digit + 1
        #self.free_squares.remove(square_index)
        
        #self.update_all_squares() This is inefficient
        #having squares is inefficient
        #we dont have inefficiency anymore


    def remove_number(self, square_index, digit):
        square_row = square_index // 9
        square_column = square_index % 9
        square_box = self.calculate_box(square_index)

        digit_mask = (0b111111111) - (0b000000001 << digit)

        self.rows[square_row] &= digit_mask
        self.columns[square_column] &= digit_mask
        self.boxes[square_box] &= digit_mask

        self.solution[square_index] = 0
        #self.free_squares.append(square_index)

    def calculate_box(self, square_index):
        #Gonna precompute values for speed - 1 list lookup is probably faster than calculating it all
        #If I could use bit operations that'd be even faster
        #Precomputing is about 3 times slower....


        box_row = (square_index // 9) // 3
        box_column = ((square_index % 9) // 3)

        #print(f"Index: {square_index} Box Row: {box_row} Box Col: {box_column} Box: {(box_row * 3) + box_column}")

        return (box_row * 3) + box_column

        for box in range(9):
            if square_index in self.BOX_COORDS[box]:
                return box
            
    def get_holes(self, mask):
        counting_mask = mask
        holes = []
        for i in range(9):
            if counting_mask % 2 == 0:
                holes.append(i)
            counting_mask >>= 1
        return holes

    #Here lies where get_moves once stood
    #What was I thinking

    def get_moves_for_square(self, square_index):
        moves = []

        square = self.get_candidate_mask(square_index)
        
        holes = self.get_holes(square)

        for hole in holes:
            moves.append((square_index, hole))

        return moves

    def find_open_squares(self):
        best_square = -1
        MRV_val = 10 #cant get 10 wrong 
    
        for index in range(81) :
            if self.solution[index] != 0:
                continue

            current = self.get_candidate_mask(index)
            
            if current == 0b111111111:
                return -1 #kill the child

            holes = 9 - current.bit_count()

            
            if holes == 1:
                return index

            

            if holes < MRV_val:
                MRV_val = holes
                best_square = index

        return best_square


    def get_candidate_mask(self, square_index):
        new_int = 0b000000000

        square_row = square_index // 9
        square_column = square_index % 9
        square_box = self.calculate_box(square_index)

        #print(square_index)
        
        board_row = self.rows[square_row]
        board_column = self.columns[square_column]
        board_box = self.boxes[square_box]

        new_int = (board_row | board_column | board_box)

        return new_int

class Game:

    def __init__(self, input_sudoku):
        self.is_solution = True
        self.game_stack = []
        self.board = Board()
        self.board.set_up_board(input_sudoku)
        self.moves = []

        #self.current_node = Node()

        self.current_node = [[], None, None, 0]

        self.current_node[0] = self.populate_node_children()
        if self.current_node[0] == [-1]:
            self.is_solution = False

        if self.board.invalid_puzzle:
            self.is_solution = False

    def populate_node_children(self):
        open_square = self.board.find_open_squares()

        if open_square == -1:
            return [-1]

        moves = self.board.get_moves_for_square(open_square)

        children = []
        for move in moves:
            #new_node = Node(move[0], move[1])

            new_node = [[], move[0], move[1], 0]
            children.append(new_node)
        
        return children

    def push_to_stack(self):
        self.game_stack.append(self.current_node)

    def pop_from_stack(self):

        while self.game_stack: #THIS WAS THE WHOLE ISSUE

            prev_node = self.game_stack.pop()
            self.board.remove_number(self.current_node[1], self.current_node[2])

            prev_node[3] += 1
            self.current_node = prev_node

            if prev_node[3] < len(prev_node[0]):
                return True

        self.is_solution = False
        return None

    def check_if_complete(self):
        for i in range(81):
            if self.board.solution[i] == 0:
                return False
        return True

    def main_loop(self):

        while self.is_solution:

            if self.current_node[0] == [-1]:
                if not self.pop_from_stack():
                    return -1

            if self.current_node[3] == len(self.current_node[0]):
                if not self.pop_from_stack():
                    return -1

            next_node = self.current_node[0][self.current_node[3]]
            self.push_to_stack()
            self.current_node = next_node

            self.board.place_number(self.current_node[1], self.current_node[2])

            if self.check_if_complete():
                return self.board.solution
            else:
                self.current_node[0] = self.populate_node_children()
            
        return -1

#Adding the boilerplating for the coursework
def sudoku_solver(sudoku):

    sudoku = np.array(sudoku, dtype = int)
    sudoku = sudoku.tolist()
    
    game = Game(sudoku)

    solution = game.main_loop()

    if solution == -1:
        return np.array([[-1, -1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1, -1]])


    else:
        #print(solution)
        arr_solution = np.array([
                        solution[0:9], solution[9:18], solution[18:27],
                        solution[27:36], solution[36:45], solution[45:54],
                        solution[54:63], solution[63:72], solution[72:]
                    ])
    return arr_solution
# YOUR CODE HERE
    raise NotImplementedError()


TEST_SUDOKU = [[0, 8, 0, 4, 3, 0, 0, 0, 0],
 [0, 0, 5, 0, 0, 9, 0, 0, 0],
 [6, 0, 0, 0, 8 ,0 ,0, 7, 0],
 [0, 0, 0, 0, 9 ,0 ,0, 0 ,3],
 [0, 0, 0, 8, 0, 7, 0, 0, 0],
 [9, 0, 0, 0, 0, 0, 0, 5, 4],
 [0, 6, 0, 0, 0, 0, 0, 0, 5],
 [0, 0, 8, 0, 0, 0, 4, 0, 0],
 [0, 4, 0, 0, 0, 6, 0, 1, 0]]

print(sudoku_solver(TEST_SUDOKU))
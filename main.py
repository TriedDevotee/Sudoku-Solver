import numpy as np

class BitwiseInt:
    def __init__(self, in_mask):
        self.mask = in_mask #9 bit int for the missing values
                                #full is when no spaces available
                                #means either contradiction in puzzle of solved number

    def flip_bit(self, index):
        self.mask ^= (0b000000001 << (index))

    def set_bit(self, index):
            self.mask |= (0b000000001 << (index))

    def clear_bit(self, index):
            self.mask &= ((0b111111111) - (0b000000001 << (index)))

    def is_full(self):
        return (self.mask == 0b111111111)

    def get_bit_state(self, index):
        return ((self.mask & 0b000000001 << (index)) == (0b000000001 << (index)))

    def count_holes(self):
        counting_mask = self.mask
        holes = []
        for i in range(9):
            if counting_mask % 2 == 0:
                holes.append(i)
            counting_mask >>= 1
        return holes

class Node:
    def __init__(self, square = None, digit = None):
        self.children = []
        self.square = square
        self.digit = digit
        self.current_child = 0

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
        self.rows = [BitwiseInt(0) for i in range(9)]
        self.columns = [BitwiseInt(0) for i in range(9)]
        self.boxes = [BitwiseInt(0) for i in range(9)]
        self.squares = [BitwiseInt(0) for i in range(81)]
        self.solution = [0 for i in range(81)]

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

        self.update_all_squares()

    def get_mask_from_arr(self, arr):
        current = BitwiseInt(0)
        for i in range(9):
            if arr[i] != 0:
                current.set_bit(arr[i] - 1)

        return current

    def update_all_squares(self):
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

            self.squares[i].mask = new_mask

    def place_number(self, square_index, digit):
        square_row = square_index // 9
        square_column = square_index % 9
        square_box = self.calculate_box(square_index)

        digit_mask = (0b000000001 << digit)

        self.rows[square_row].mask |= digit_mask
        self.columns[square_column].mask |= digit_mask
        self.boxes[square_box].mask |= digit_mask

        self.solution[square_index] = digit + 1
        
        #self.update_all_squares() This is inefficient

        self.update_selected_squares(square_row, square_column, square_box)

    def update_selected_squares(self, changed_row, changed_column, changed_box):
        
        for i in range(9):
            square_position = (changed_row * 9) + i
            self.squares[square_position].mask |= self.rows[changed_row].mask

        for i in range(9):
            square_position = (i * 9) + changed_column
            self.squares[square_position].mask |= self.columns[changed_column].mask

        for i in range(9):
            box = self.BOX_COORDS[changed_box]
            self.squares[box[i]].mask |= self.boxes[changed_box].mask




    def remove_number(self, square_index, digit):
        square_row = square_index // 9
        square_column = square_index % 9
        square_box = self.calculate_box(square_index)

        digit_mask = (0b111111111) - (0b000000001 << digit)

        self.rows[square_row].mask &= digit_mask
        self.columns[square_column].mask &= digit_mask
        self.boxes[square_box].mask &= digit_mask

        self.solution[square_index] = 0
        self.update_all_squares()

    def calculate_box(self, square_index):
        box_row = (square_index // 9) // 3
        box_column = ((square_index % 9) // 3)

        #print(f"Index: {square_index} Box Row: {box_row} Box Col: {box_column} Box: {(box_row * 3) + box_column}")

        return (box_row * 3) + box_column

        for box in range(9):
            if square_index in self.BOX_COORDS[box]:
                return box

    def get_moves(self):
        moves = []
        for square_index in range(81):
            current = self.squares[square_index]
            if self.solution[square_index] != 0:
                continue

            holes = current.count_holes()
            index_freq = len(holes)

            for hole in holes:
                moves.append((square_index, hole, index_freq))

        return moves

    def get_moves_for_square(self, square_index):
        moves = []
        square = self.squares[square_index]
        holes = square.count_holes()

        for hole in holes:
            moves.append((square_index, hole))

        return moves

    def find_open_squares(self):
        open_squares = []
    
        for i in range(81):
            if self.solution[i] != 0:
                continue

            current = self.squares[i]

            if current.mask == 0b111111111:
                return [-1] #kill the child

            holes = len(current.count_holes())

            open_squares.append((i, holes))

        open_squares = sorted(open_squares, key = lambda index: index[1])
        return [square[0] for square in open_squares]

class Game:

    def __init__(self, input_sudoku):
        self.is_solution = True
        self.game_stack = []
        self.board = Board()
        self.board.set_up_board(input_sudoku)
        self.moves = []

        self.current_node = Node()
        self.current_node.children = self.populate_node_children()
        if self.current_node.children == [-1]:
            self.is_solution = False

    def populate_node_children(self):
        open_squares = self.board.find_open_squares()

        if open_squares == [-1]:
            return [-1]

        if open_squares == []:
            return []

        square = open_squares[0]

        moves = self.board.get_moves_for_square(square)

        children = []
        for move in moves:
            new_node = Node(move[0], move[1])
            children.append(new_node)
        
        return children

    def get_moves(self):
        moves = self.board.get_moves()

        if moves == [-1]:
            return [-1]

        moves = sorted(moves, key = lambda index: index[2])
        moves = [move[:2] for move in moves]

        #print (moves)

        return moves

    def push_to_stack(self):
        self.game_stack.append(self.current_node)

    def pop_from_stack(self):

        while self.game_stack: #THIS WAS THE WHOLE ISSUE

            prev_node = self.game_stack.pop()
            self.board.remove_number(self.current_node.square, self.current_node.digit)

            prev_node.current_child += 1
            self.current_node = prev_node

            if prev_node.current_child < len(prev_node.children):
                return True

        self.is_solution = False
        return None

    def check_if_complete(self):
        for i in range(81):
            if self.board.solution[i] == 0:
                return False
        return True

    def main_loop(self):

        #ON TURN
        """
            - Take the next available child from the current node
            - Push the current node to the stack
            - Make the current node the next available
            - Apply move described by current node
            - Expand its children
            - If no children, puzzle complete
            - Otherwise, repeat
            - If we find a contradiction, i.e. square not solved but no available
                - Pop the previous node
                - Increment the child counter
                - Expand that next node
                - If child counter == num children (out of range)
                - Pop again
        """

        while self.is_solution:

            if self.current_node.children == [-1]:
                if not self.pop_from_stack():
                    return -1

            if self.current_node.current_child == len(self.current_node.children):
                if not self.pop_from_stack():
                    return -1

            next_node = self.current_node.children[self.current_node.current_child]
            self.push_to_stack()
            self.current_node = next_node

            self.board.place_number(self.current_node.square, self.current_node.digit)

            if self.check_if_complete():
                return self.board.solution
            else:
                self.current_node.children = self.populate_node_children()
            
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


TEST_SUDOKU = [[3, 7, 4, 5, 8, 0, 6, 2, 9],
 [8, 2, 5, 7, 9, 6, 4, 0, 1],
 [6, 9, 1, 2, 3 ,4 ,8, 7, 5],
 [1, 4, 2, 0, 5 ,3 ,7, 9 ,8],
 [7, 8, 6, 9, 4, 2, 1, 5, 3],
 [9, 5, 3, 8, 1, 7, 2, 4, 6],
 [4, 6, 9, 1, 7, 5, 3, 8, 2],
 [5, 1, 7, 3, 2, 8, 0, 6, 4],
 [2, 3, 8, 6, 0, 9, 5, 1, 7]]

print(sudoku_solver(TEST_SUDOKU))
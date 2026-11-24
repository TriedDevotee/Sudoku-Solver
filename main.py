class BitwiseInt:
    def __init__(self, in_mask):
        self.mask = in_mask #9 bit int for the missing values
                                #full is when its all 1s

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

    def set_up_board(self, inputted_arr):
        for row in range(0, 9):
            for column in range(0, 9):
                self.rows[row] = self.get_mask_from_arr(inputted_arr[row])

                new_col = []
                for i in range(9):
                    new_col.append(inputted_arr[i][column])

                self.columns[row] = self.get_mask_from_arr(new_col)

                for box in range(9):
                    new_box = []

                    for i in self.BOX_COORDS[box]:
                        row = i // 9
                        column = i % 9
                        new_box.append(inputted_arr[row][column])

                    self.boxes[box] = self.get_mask_from_arr(new_box)

        self.update_all_squares()

    def get_mask_from_arr(self, arr):
        current = BitwiseInt(0)
        for i in range(9):
            if arr[i] != 0:
                current.set_bit(i)

        return current

    def update_squares(self, square_index):
        square_row = square_index // 9
        square_col = square_index % 9
        square_box = self.calculate_box(square_index)

        self.rows[square_row].mask |= self.squares[square_index].mask
        self.columns[square_col].mask |= self.squares[square_index].mask
        self.boxes[square_box].mask |= self.squares[square_index].mask

    def update_all_squares(self):
        for i in range(81):
            row = i // 9
            column = i % 9
            box = self.calculate_box(i)

            new_mask = self.rows[row].mask
            new_mask |= self.columns[column].mask
            new_mask |= self.boxes[box].mask

            self.squares[i].mask = new_mask

    def calculate_box(self, square_index):
        box_row = (square_index // 9) % 3
        box_column = (square_index % 9) // 3

        return (box_row * 3) + box_column

    def print_values(self):
        print(F"Row masks:")
        for row in self.rows:
            print(row.mask)
        print(f"Column masks:")
        for column in self.columns:
            print(column.mask)
        print(F"Box masks:")
        for box in self.boxes:
            print(box.mask)
        print(f"Square masks:")
        for square in self.squares:
            print(square.mask)

TEST_SUDOKU = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
               [0, 2, 3, 4, 5, 6, 7, 8, 0],
               [0, 2, 3, 4, 5, 6, 7, 0, 9],
               [0, 2, 3, 4, 5, 6, 0, 8, 9],
               [0, 2, 3, 4, 5, 0, 7, 8, 9],
               [0, 2, 3, 4, 0, 6, 7, 8, 9],
               [0, 2, 3, 0, 5, 6, 7, 8, 9],
               [0, 2, 0, 4, 5, 6, 7, 8, 9],
               [0, 0, 3, 4, 5, 6, 7, 8, 9]]

print(TEST_SUDOKU)

test_board = Board()
test_board.set_up_board(TEST_SUDOKU)

test_board.print_values()
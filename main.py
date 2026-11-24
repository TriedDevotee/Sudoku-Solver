class BitwiseInt:
    def __init__(self, in_mask):
        self.mask = in_mask #9 bit int for the missing values
                                #full is when its all 1s

        print(f"Mask initilialised as {self.mask}")

    def flip_bit(self, index):
        self.mask ^= (0b000000001 << (index - 1))
        print (f"Updated value of mask to {self.mask}")

    def set_bit(self, index):
            self.mask |= (0b000000001 << (index - 1))
            print (f"Updated value of mask to {self.mask}")

    def clear_bit(self, index):
            self.mask &= ((0b111111111) - (0b000000001 << (index - 1)))
            print (f"Updated value of mask to {self.mask}")

    def is_full(self):
        return (self.mask == 0b111111111)

    def get_bit_state(self, index):
        return ((self.mask & 0b000000001 << (index - 1)) == (0b000000001 << (index - 1)))

class Board:
    def __init__(self):
        self.rows = [BitwiseInt(0)] * 9
        self.columns = [BitwiseInt(0)] * 9
        self.boxes = [BitwiseInt(0)] * 9
        self.squares = [BitwiseInt(0) for i in range(81)]

    def set_up_board(self, inputted_arr):
        for row in range(0, 9):
            for column in range(0, 9):
                self.rows[column] = self.get_mask_from_arr(inputted_arr[row])

                new_col = []
                for i in range(9):
                    new_col.append(inputted_arr[i][column])

                self.columns[row] = self.get_mask_from_arr(new_col)

        for i in range(9):
            x_offset = i % 3
            y_offset = i // 3

            new_box = []

            for row in range(3):
                for col in range(3):
                    new_box.append(inputted_arr[row + x_offset][col + y_offset])

            self.boxes[i] = self.get_mask_from_arr(new_box)




    def get_mask_from_arr(self, arr):
        current = BitwiseInt(0)
        for i in range(9):
            if arr[i] != 0:
                current.set_bit(i)

        return current

    def update_squares(self, square_index):
        square = self.square[square_index]

        square_row = square_index // 9
        square_column = square_index % 9
        square_box = self.calculate_box(square_index)

        for mask in self.rows[square_row]:
            mask |= square.mask

        for mask in self.columns[square_column]:
            mask |= square.mask

        for mask in self.boxes[square_box]:
            mask != square.mask

    def calculate_box(square_index):
        box_row = (square_index // 9) % 3
        box_column = (square_index % 9) // 3

        return (box_row * 3) + box_column



newInt = BitwiseInt()
newInt.flip_bit(4)
newInt.set_bit(3)
newInt.flip_bit(4)
newInt.clear_bit(3)
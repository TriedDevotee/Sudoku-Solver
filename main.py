class BitwiseInt:
    def __init__(self):
        self.mask = 0b000000000 #9 bit int for the missing values
                                #full is when its all 1s
        print(f"Mask initilialised as {self.mask}")

    def flip_bit(self, index):
        self.mask ^= (0b000000001 << index)
        print (f"Updated value of mask to {self.mask}")

    def set_bit(self, index):
            self.mask |= (0b000000001 << index)
            print (f"Updated value of mask to {self.mask}")

    def clear_bit(self, index):
            self.mask &= ((0b111111111) - (0b000000001 << index))
            print (f"Updated value of mask to {self.mask}")

    def is_full(self):
          return (self.mask == 0b111111111)

newInt = BitwiseInt()
newInt.flip_bit(4)
newInt.set_bit(3)
newInt.flip_bit(4)
newInt.clear_bit(3)
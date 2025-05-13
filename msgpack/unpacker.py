class Unpacker:
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def unpack(self):
        if self.pos >= len(self.data):
            raise EOFError("No more data to unpack")

        byte = self.data[self.pos]
        self.pos += 1
        # nil (0xc0)
        if byte == 0xc0:
            return None
        # true (0xc3)
        elif byte == 0xc3:
            return True
        # false (0xc2)
        elif byte == 0xc2:
            return False
        return None
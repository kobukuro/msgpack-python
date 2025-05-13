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
        return None
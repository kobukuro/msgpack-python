import struct


class Unpacker:
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def unpack(self):
        if self.pos >= len(self.data):
            raise EOFError("No more data to unpack")

        byte = self.data[self.pos]
        self.pos += 1
        # positive fixint (0x00 - 0x7f)
        if byte <= 0x7f:
            return byte
        # nil (0xc0)
        elif byte == 0xc0:
            return None
        # false (0xc2)
        elif byte == 0xc2:
            return False
        # true (0xc3)
        elif byte == 0xc3:
            return True
        # float 32,64 (0xca,0xcb)
        elif byte == 0xca:
            value = struct.unpack('>f', self.data[self.pos:self.pos + 4])[0]
            self.pos += 4
            return value
        elif byte == 0xcb:
            value = struct.unpack('>d', self.data[self.pos:self.pos + 8])[0]
            self.pos += 8
            return value
        # uint 8,16,32,64 (0xcc-0xcf)
        elif byte == 0xcc:
            value = self.data[self.pos]
            self.pos += 1
            return value
        elif byte == 0xcd:
            value = int.from_bytes(self.data[self.pos:self.pos + 2], 'big')
            self.pos += 2
            return value
        elif byte == 0xce:
            value = int.from_bytes(self.data[self.pos:self.pos + 4], 'big')
            self.pos += 4
            return value
        elif byte == 0xcf:
            value = int.from_bytes(self.data[self.pos:self.pos + 8], 'big')
            self.pos += 8
            return value
        # int 8,16,32,64 (0xd0-0xd3)
        elif byte == 0xd0:
            value = int.from_bytes(self.data[self.pos:self.pos + 1], 'big', signed=True)
            self.pos += 1
            return value
        elif byte == 0xd1:
            value = int.from_bytes(self.data[self.pos:self.pos + 2], 'big', signed=True)
            self.pos += 2
            return value
        elif byte == 0xd2:
            value = int.from_bytes(self.data[self.pos:self.pos + 4], 'big', signed=True)
            self.pos += 4
            return value
        elif byte == 0xd3:
            value = int.from_bytes(self.data[self.pos:self.pos + 8], 'big', signed=True)
            self.pos += 8
            return value
        # negative fixint (0xe0-0xff)
        elif byte >= 0xe0:
            return byte - 0x100
        raise ValueError(f"Unknown type byte: {hex(byte)}")

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
        # fixstr (0xa0 - 0xbf)
        elif 0xa0 <= byte <= 0xbf:
            return self._read_str(byte & 0x1f)
        # nil (0xc0)
        elif byte == 0xc0:
            return None
        # false (0xc2)
        elif byte == 0xc2:
            return False
        # true (0xc3)
        elif byte == 0xc3:
            return True
        # bin 8,16,32 (0xc4,0xc5,0xc6)
        elif byte == 0xc4:
            length = self.data[self.pos]
            self.pos += 1
            return self._read_bytes(length)
        elif byte == 0xc5:
            length = int.from_bytes(self.data[self.pos:self.pos + 2], 'big')
            self.pos += 2
            return self._read_bytes(length)
        elif byte == 0xc6:
            length = int.from_bytes(self.data[self.pos:self.pos + 4], 'big')
            self.pos += 4
            return self._read_bytes(length)
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
        # str 8,16,32 (0xd9-0xdb)
        elif byte == 0xd9:
            length = self.data[self.pos]
            self.pos += 1
            return self._read_str(length)
        elif byte == 0xda:
            length = int.from_bytes(self.data[self.pos:self.pos + 2], 'big')
            self.pos += 2
            return self._read_str(length)
        elif byte == 0xdb:
            length = int.from_bytes(self.data[self.pos:self.pos + 4], 'big')
            self.pos += 4
            return self._read_str(length)
        # negative fixint (0xe0-0xff)
        elif byte >= 0xe0:
            return byte - 0x100
        raise ValueError(f"Unknown type byte: {hex(byte)}")

    def _read_str(self, length):
        return self._read_bytes(length).decode('utf-8')

    def _read_bytes(self, length):
        end = self.pos + length
        result = self.data[self.pos:end]
        self.pos = end
        return result

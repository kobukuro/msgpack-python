class Packer:
    def pack(self, obj):
        if obj is None:
            return bytes([0xc0])  # nil
        elif isinstance(obj, bool):
            return bytes([0xc3]) if obj else bytes([0xc2])  # true/false
        elif isinstance(obj, int):
            return self._pack_int(obj)
        return None

    def _pack_int(self, n):
        if n >= 0:
            if n <= 127:
                return bytes([n])  # positive fixint
            elif n <= 255:
                return bytes([0xcc, n])  # uint 8
            elif n <= 65535:
                return bytes([0xcd]) + n.to_bytes(2, 'big')  # uint 16
            elif n <= 4294967295:
                return bytes([0xce]) + n.to_bytes(4, 'big')  # uint 32
            else:
                return bytes([0xcf]) + n.to_bytes(8, 'big')  # uint 64
        else:
            if n >= -32:
                return bytes([0xe0 + (n + 32)])  # negative fixint
            elif n >= -128:
                return bytes([0xd0]) + n.to_bytes(1, 'big', signed=True)  # int 8
            elif n >= -32768:
                return bytes([0xd1]) + n.to_bytes(2, 'big', signed=True)  # int 16
            elif n >= -2147483648:
                return bytes([0xd2]) + n.to_bytes(4, 'big', signed=True)  # int 32
            else:
                return bytes([0xd3]) + n.to_bytes(8, 'big', signed=True)  # int 64

class Packer:
    def pack(self, obj):
        if obj is None:
            return bytes([0xc0])  # nil
        elif isinstance(obj, bool):
            return bytes([0xc3]) if obj else bytes([0xc2])  # true/false
        elif isinstance(obj, int):
            return self._pack_int(obj)
        elif isinstance(obj, float):
            return self._pack_float(obj)
        elif isinstance(obj, str):
            return self._pack_str(obj)
        elif isinstance(obj, bytes):
            return self._pack_bin(obj)
        elif isinstance(obj, (list, tuple)):
            return self._pack_array(obj)
        elif isinstance(obj, dict):
            return self._pack_map(obj)
        raise TypeError(f"Unsupported type: {type(obj)}")

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

    def _pack_float(self, n):
        import struct
        if abs(n) < 3.4028234663852886e+38:  # float 32 range
            return bytes([0xca]) + struct.pack('>f', n)
        return bytes([0xcb]) + struct.pack('>d', n)  # float 64

    def _pack_str(self, s):
        data = s.encode('utf-8')
        length = len(data)
        if length <= 31:
            return bytes([0xa0 | length]) + data  # fixstr
        elif length <= 255:
            return bytes([0xd9, length]) + data  # str 8
        elif length <= 65535:
            return bytes([0xda]) + length.to_bytes(2, 'big') + data  # str 16
        return bytes([0xdb]) + length.to_bytes(4, 'big') + data  # str 32

    def _pack_bin(self, b):
        length = len(b)
        if length <= 255:
            return bytes([0xc4, length]) + b  # bin 8
        elif length <= 65535:
            return bytes([0xc5]) + length.to_bytes(2, 'big') + b  # bin 16
        return bytes([0xc6]) + length.to_bytes(4, 'big') + b  # bin 32

    def _pack_array(self, arr):
        length = len(arr)
        if length <= 15:
            header = bytes([0x90 | length])  # fixarray
        elif length <= 65535:
            header = bytes([0xdc]) + length.to_bytes(2, 'big')  # array 16
        else:
            header = bytes([0xdd]) + length.to_bytes(4, 'big')  # array 32
        return header + b''.join(self.pack(x) for x in arr)

    def _pack_map(self, d):
        length = len(d)
        if length <= 15:
            header = bytes([0x80 | length])  # fixmap
        elif length <= 65535:
            header = bytes([0xde]) + length.to_bytes(2, 'big')  # map 16
        else:
            header = bytes([0xdf]) + length.to_bytes(4, 'big')  # map 32
        return header + b''.join(self.pack(k) + self.pack(v) for k, v in d.items())

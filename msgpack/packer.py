class Packer:
    def pack(self, obj):
        if obj is None:
            return bytes([0xc0]) # nil
        elif isinstance(obj, bool):
            return bytes([0xc3]) if obj else bytes([0xc2]) # true/false
        return None
class Packer:
    def pack(self, obj):
        if obj is None:
            return bytes([0xc0]) # nil
        return None
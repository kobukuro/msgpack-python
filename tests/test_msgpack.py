import unittest
from msgpack.packer import Packer
from msgpack.unpacker import Unpacker


class TestMessagePack(unittest.TestCase):
    def test_nil(self):
        packed = Packer().pack(None)
        self.assertEqual(packed, b'\xc0')
        self.assertEqual(Unpacker(packed).unpack(), None)

    def test_boolean(self):
        self.assertEqual(Packer().pack(True), b'\xc3')
        self.assertEqual(Packer().pack(False), b'\xc2')
        self.assertEqual(Unpacker(b'\xc3').unpack(), True)
        self.assertEqual(Unpacker(b'\xc2').unpack(), False)

    def test_integer(self):
        test_cases = [
            0, 127, 128, 255, 256, 65535, 65536,  # positive
            -1, -32, -33, -128, -129, -32768, -32769  # negative
        ]
        for n in test_cases:
            packed = Packer().pack(n)
            unpacked = Unpacker(packed).unpack()
            self.assertEqual(unpacked, n)

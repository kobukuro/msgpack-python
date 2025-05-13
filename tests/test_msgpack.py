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

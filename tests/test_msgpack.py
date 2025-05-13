import unittest
from msgpack.packer import Packer
from msgpack.unpacker import Unpacker

class TestMessagePack(unittest.TestCase):
    def test_nil(self):
        packed = Packer().pack(None)
        self.assertEqual(packed, b'\xc0')
        self.assertEqual(Unpacker(packed).unpack(), None)

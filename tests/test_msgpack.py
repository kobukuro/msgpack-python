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

    def test_float(self):
        # Test regular float numbers
        regular_cases = [0.0, 1.0, -1.0, 3.14, -0.12345]
        for n in regular_cases:
            packed = Packer().pack(n)
            unpacked = Unpacker(packed).unpack()
            self.assertAlmostEqual(unpacked, n, places=6)

        # Test large numbers with relative tolerance
        large_cases = [1e38, 1e39, -1e38]
        for n in large_cases:
            packed = Packer().pack(n)
            unpacked = Unpacker(packed).unpack()
            # Use relative tolerance for large numbers
            self.assertTrue(abs((unpacked - n) / n) < 1e-6,
                            f"Large float comparison failed: {unpacked} != {n}")

    def test_string(self):
        test_cases = ["", "hello", "世界", "a" * 32, "a" * 256]
        for s in test_cases:
            packed = Packer().pack(s)
            unpacked = Unpacker(packed).unpack()
            self.assertEqual(unpacked, s)

    def test_binary(self):
        test_cases = [b"", b"hello", bytes([x for x in range(256)])]
        for b in test_cases:
            packed = Packer().pack(b)
            unpacked = Unpacker(packed).unpack()
            self.assertEqual(unpacked, b)

    def test_array(self):
        test_cases = [
            [],
            [1, 2, 3],
            [1, "hello", True, None],
            list(range(16)),  # test fixarray limit
            list(range(65536))  # test array16 limit
        ]
        for arr in test_cases:
            packed = Packer().pack(arr)
            unpacked = Unpacker(packed).unpack()
            self.assertEqual(unpacked, arr)

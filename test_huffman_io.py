"""Simple tests for Huffman I/O utilities.

These cover tree serialization round-trips and bit packing.
"""

import unittest

from huffman_frequency_heap import Node
from huffman_io import (
    serialize_tree,
    deserialize_tree,
    pack_bits_to_bytes,
    unpack_bytes_to_bits,
)


def trees_equal(left, right):
    if left is right:
        return True
    if left is None or right is None:
        return False
    return (
        left.char == right.char
        and trees_equal(left.left, right.left)
        and trees_equal(left.right, right.right)
    )


def build_simple_tree():
    left = Node(ord('a'), 1)
    right = Node(ord('b'), 1)
    return Node(None, 2, left, right)


def build_complex_tree():
    leaf_a = Node(ord('a'), 2)
    leaf_b = Node(ord('b'), 3)
    leaf_c = Node(ord('c'), 5)
    internal = Node(None, 5, leaf_a, leaf_b)
    return Node(None, 10, internal, leaf_c)


class HuffmanIOTests(unittest.TestCase):
    def test_simple_tree_round_trip(self):
        root = build_simple_tree()
        serialized = serialize_tree(root)
        expected = bytes([0, 1, ord('a'), 1, ord('b')])

        self.assertEqual(serialized, expected)
        self.assertTrue(trees_equal(root, deserialize_tree(serialized)))

    def test_complex_tree_round_trip(self):
        root = build_complex_tree()
        self.assertTrue(trees_equal(root, deserialize_tree(serialize_tree(root))))

    def test_pack_bits_to_bytes_exact_byte(self):
        bits = '11010110'
        packed, padding = pack_bits_to_bytes(bits)

        self.assertEqual(padding, 0)
        self.assertEqual(packed, bytes([0b11010110]))
        self.assertEqual(unpack_bytes_to_bits(packed, padding), bits)

    def test_pack_bits_to_bytes_with_padding(self):
        bits = '110101'
        packed, padding = pack_bits_to_bytes(bits)

        self.assertEqual(padding, 2)
        self.assertEqual(packed, bytes([0b11010100]))
        self.assertEqual(unpack_bytes_to_bits(packed, padding), bits)

    def test_empty_bitstring_round_trip(self):
        self.assertEqual(pack_bits_to_bytes(''), (b'', 0))
        self.assertEqual(unpack_bytes_to_bits(b'', 0), '')


if __name__ == '__main__':
    unittest.main(verbosity=2)

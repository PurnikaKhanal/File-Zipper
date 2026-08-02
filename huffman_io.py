"""Huffman file I/O utilities for tree serialization and bit packing.

A Huffman tree is stored in preorder using marker bytes:
 - 0 = internal node
 - 1 = leaf node followed by the byte value
This makes the tree easy to save and rebuild.
"""

from huffman_frequency_heap import Node

INTERNAL_NODE = 0
LEAF_NODE = 1


def is_leaf(node):
    return node.left is None and node.right is None


def serialize_tree(root):
    """Serialize a Huffman tree into bytes using preorder markers."""
    if root is None:
        return b''

    result = bytearray()

    def encode(node):
        if is_leaf(node):
            result.extend((LEAF_NODE, node.char))
            return

        result.append(INTERNAL_NODE)
        encode(node.left)
        encode(node.right)

    encode(root)
    return bytes(result)


def deserialize_tree(data):
    """Rebuild a Huffman tree from serialized bytes."""
    if not data:
        return None

    iterator = iter(data)

    def decode():
        marker = next(iterator)
        if marker == LEAF_NODE:
            value = next(iterator)
            return Node(value, 0)

        if marker == INTERNAL_NODE:
            left = decode()
            right = decode()
            return Node(None, 0, left, right)

        raise ValueError(f"Invalid tree marker: {marker}")

    return decode()


def pack_bits_to_bytes(bit_string):
    """Pack a string of '0' and '1' characters into bytes.

    Returns:
        tuple[bytes, int]: packed bytes and number of padding bits added.
    """
    if not bit_string:
        return b'', 0

    padding = (-len(bit_string)) % 8
    bit_string += '0' * padding

    byte_array = bytearray()
    for index in range(0, len(bit_string), 8):
        chunk = bit_string[index:index + 8]
        byte_array.append(int(chunk, 2))

    return bytes(byte_array), padding


def unpack_bytes_to_bits(byte_data, padding):
    """Unpack bytes back into a bit string and remove padding."""
    if not byte_data:
        return ''

    bit_string = ''.join(f'{byte:08b}' for byte in byte_data)
    return bit_string[:-padding] if padding else bit_string
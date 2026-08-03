"""
DECOMPRESSION PIPELINE

This module contains the decompress() function and the decode() function.
It reads a .huf file and reconstructs the original file.

IMPORTANT: The decode() function must be written by (Member 3).
It's the reverse of Member 1's encode() function.

CONNECTION MAP:
    decompress(input_file, output_file)                         

 1. Read .huf file                                           
 2. Parse header (size, tree_size, padding)                 
 3. Call huffman_io: deserialize_tree()                     
 4. Decode the packed bytes using the Huffman tree         
 5. Write original file                                      
 6. Write original file                                      

"""

import struct
import os
from huffman_io import deserialize_tree, unpack_bytes_to_bits

def decode(root, binary_string):
    """
    Decode the binary string using the Huffman tree.
    Walks the tree bit by bit until reaching a leaf node (character).
    """
    if not root or not binary_string:
        return b''

    decoded = bytearray()
    current = root

    for bit in binary_string:
        # Navigate tree based on bit value
        current = current.left if bit == '0' else current.right

        # Leaf node → character found
        if current.left is None and current.right is None:
            decoded.append(current.char)
            current = root  # reset for next symbol

    return bytes(decoded)


def decompress(input_file, output_file):
    """
    Complete decompression pipeline:
    1. Validate input file
    2. Read and parse header
    3. Deserialize Huffman tree
    4. Convert compressed bytes back to bit string
    5. Decode using Huffman tree
    6. Write recovered file
    """
    print("\n==============================")
    print("Starting Decompression")
    print("==============================")

    try:
        if not os.path.isfile(input_file):
            raise FileNotFoundError(f"File not found: {input_file}")

        # Header layout: [original_size:4][compressed_size:4][tree_size:2][padding:1][reserved:5]
        with open(input_file, 'rb') as f:
            header = f.read(16)
            if len(header) < 16:
                raise IOError("Invalid .huf file: header too small")

            original_size = struct.unpack('I', header[0:4])[0]
            compressed_size = struct.unpack('I', header[4:8])[0]
            tree_size = struct.unpack('H', header[8:10])[0]
            padding = struct.unpack('B', header[10:11])[0]

            tree_data = f.read(tree_size)
            compressed_binary = f.read(compressed_size)

        # Empty file case
        if original_size == 0:
            open(output_file, 'wb').close()
            print("Empty file decompressed successfully.")
            return {
                'original_size': 0,
                'compressed_size': os.path.getsize(input_file),
                'decompression_ratio': 0,
                'input_file': input_file,
                'output_file': output_file,
                'success': True
            }

        # Rebuild Huffman tree
        root = deserialize_tree(tree_data)

        # Convert bytes back to bit string (removes padding)
        binary_string = unpack_bytes_to_bits(compressed_binary, padding)

        # Decode data
        decoded_data = decode(root, binary_string)

        # Write recovered file
        with open(output_file, 'wb') as f:
            f.write(decoded_data)

        comp_size = os.path.getsize(input_file)
        ratio = (original_size / comp_size) * 100 if comp_size > 0 else 0

        print("==============================")
        print("Decompression Successful!")
        print("==============================")
        print(f"Original size: {original_size} bytes")
        print(f"Compressed size: {comp_size} bytes")
        print(f"Recovered size: {len(decoded_data)} bytes")
        print(f"Decompression ratio: {ratio:.1f}%")
        print("==============================")

        return {
            'original_size': original_size,
            'compressed_size': comp_size,
            'decompression_ratio': ratio,
            'input_file': input_file,
            'output_file': output_file,
            'success': True
        }

    except Exception as e:
        print(f"Error during decompression: {e}")
        return {
            'original_size': 0,
            'compressed_size': 0,
            'decompression_ratio': 0,
            'error': str(e),
            'success': False
        }


if __name__ == "__main__":
    # Test: decompress the file created by compression
    result = decompress("test_input.txt.huf", "test_output.txt")
    print(result)

"""
This module has the compress() function which runs the whole compression process.
It reads a file and produces a compressed .huf output.

Steps inside compress():
    1. Read file bytes
    2. Count character frequencies
    3. Build Huffman tree
    4. Generate Huffman codes
    5. Encode data
    6. Serialize tree
    7. Pack bits into bytes
    8. Write everything into a .huf file
"""

import struct   # helps write integers as raw bytes
import os       # for file handling

from huffman_frequency_heap import FrequencyCounter
from huffman_algorithm import buildHuffmanTree, generateCodes, encode
from huffman_io import serialize_tree, pack_bits_to_bytes


def compress(input_file, output_file):
    print("============================================================")
    print("COMPRESSION STARTING")
    print("============================================================")
    
    try:
        # Step 1: Check if the input file actually exists
        print("[1/7] Validating input file:", input_file)
        
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file '{input_file}' not found")
        
        if not os.path.isfile(input_file):
            raise IOError(f"'{input_file}' is not a file")
        
        # Step 2: Read the file as raw bytes
        print("[2/7] Reading file into memory...")
        with open(input_file, 'rb') as f:
            data = f.read()
        
        original_size = len(data)
        print("   Read", original_size, "bytes")
        
        # If the file is empty, just write a header and stop
        if original_size == 0:
            print("   Warning: Input file is empty")
            with open(output_file, 'wb') as f:
                f.write(struct.pack('I', 0))  # Original size
                f.write(struct.pack('I', 0))  # Compressed size
                f.write(struct.pack('H', 0))  # Tree size
            return {
                'original_size': 0,
                'compressed_size': 16,
                'compression_ratio': 0,
                'input_file': input_file,
                'output_file': output_file,
                'success': True
            }
        
        # Step 3: Count how often each character appears
        print("[3/7] Counting character frequencies...")
        counter = FrequencyCounter()
        freq = counter.count_from_data(data)
        
        print("   Found", len(freq), "unique characters")
        print("   Frequency range:", min(freq.values()), "to", max(freq.values()))
        
        # Step 4: Build Huffman tree from frequencies
        print("[4/7] Building Huffman tree...")
        root = buildHuffmanTree(freq)
        print("   Tree built successfully")
        
        # Step 5: Generate Huffman codes (map chars → bit strings)
        print("[5/7] Generating Huffman codes...")
        codes = generateCodes(root)
        print("   Generated", len(codes), "codes")
        
        code_lengths = [len(code) for code in codes.values()]
        print("   Code lengths: min =", min(code_lengths), ", max =", max(code_lengths))
        
        # Step 6: Encode the actual data using those codes
        print("[6/7] Encoding data to binary...")
        binary_string = encode(data, codes)
        
        print("   Binary string length:", len(binary_string), "bits")
        print("   Original data:", original_size * 8, "bits")
        
        theoretical_compression = (1 - len(binary_string) / (original_size * 8)) * 100
        print("   Theoretical compression:", f"{theoretical_compression:.1f}%")
        
        # Step 7: Save the Huffman tree + pack bits into bytes
        print("[7/7] Serializing tree and packing bytes...")
        tree_data = serialize_tree(root)
        print("   Serialized tree size:", len(tree_data), "bytes")
        
        compressed_binary, padding = pack_bits_to_bytes(binary_string)
        print("   Packed binary data:", len(compressed_binary), "bytes")
        print("   Padding bits added:", padding)
        
        # Final step: Write everything into the .huf file
        print("Writing .huf file:", output_file)
        with open(output_file, 'wb') as f:
            f.write(struct.pack('I', original_size))          # Original size
            f.write(struct.pack('I', len(compressed_binary))) # Compressed size
            f.write(struct.pack('H', len(tree_data)))         # Tree size
            f.write(struct.pack('B', padding))                # Padding bits
            f.write(b'\x00' * 5)                              # Reserved space
            f.write(tree_data)                                # Huffman tree
            f.write(compressed_binary)                        # Compressed data
        
        compressed_size = os.path.getsize(output_file)
        compression_ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
        
        print("============================================================")
        print("COMPRESSION SUCCESSFUL")
        print("============================================================")
        print("Original size:     ", original_size, "bytes")
        print("Compressed size:   ", compressed_size, "bytes")
        print("Compression ratio: ", f"{compression_ratio:.1f}%")
        print("Bytes saved:       ", original_size - compressed_size, "bytes")
        print("============================================================")
        
        return {
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': compression_ratio,
            'input_file': input_file,
            'output_file': output_file,
            'success': True
        }
    
    except FileNotFoundError as e:
        print("ERROR:", e)
        return {
            'original_size': 0,
            'compressed_size': 0,
            'compression_ratio': 0,
            'error': str(e),
            'success': False
        }
    
    except Exception as e:
        print("ERROR during compression:", e)
        import traceback
        traceback.print_exc()
        return {
            'original_size': 0,
            'compressed_size': 0,
            'compression_ratio': 0,
            'error': str(e),
            'success': False
        }


if __name__ == "__main__":
    # Quick test: make a sample file and compress it
    test_file = "test_input.txt"
    with open(test_file, 'w') as f:
        f.write("Hello World! This is a test file for Huffman compression. " * 10)
    
    result = compress(test_file, test_file + ".huf")
    print(result)

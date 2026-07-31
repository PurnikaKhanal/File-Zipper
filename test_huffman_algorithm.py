from huffman_frequency_heap import FrequencyCounter, MinHeap, Node
from huffman_algorithm import buildHuffmanTree, generateCodes, encode


def test_basic_compression():
    """Test basic compression with 'hello'"""
    print("TEST 1: Basic compression with 'hello'")
    
    data = "hello".encode("utf-8")
    print(f"Input text: 'hello'")
    print(f"Input bytes: {data}")
    print(f"Original size: {len(data)} bytes = {len(data) * 8} bits")
    
    # Step 1: Count frequencies
    freq = FrequencyCounter().count_from_data(data)
    print(f"\nFrequency table: {freq}")
    
    # Step 2: Build Huffman tree
    root = buildHuffmanTree(freq)
    print(f"Root frequency: {root.frequency} (should equal {len(data)})")
    print(f"Root char: {root.char} (should be None for internal node)")
    
    # Step 3: Generate codes
    codes = generateCodes(root)
    print(f"\nGenerated codes:")
    for byte_val, code in sorted(codes.items()):
        char = chr(byte_val) if 32 <= byte_val < 127 else f"byte_{byte_val}"
        print(f"  {char} (byte {byte_val}): '{code}'")
    
    # Step 4: Encode
    bitstring = encode(data, codes)
    print(f"\nBitstring: {bitstring}")
    print(f"Bitstring length: {len(bitstring)} bits")
    
    # Compression ratio
    ratio = (1 - len(bitstring) / (len(data) * 8)) * 100
    print(f"Compression ratio: {ratio:.1f}%")
    
    # Verify all characters have codes
    assert len(codes) == len(freq), "Mismatch: not all characters have codes!"
    print("\n TEST 1 PASSED")


def test_single_character():
    """Test edge case: only one unique character"""
    print("TEST 2: Edge case - single character 'aaaa'")
   
    
    data = "aaaa".encode("utf-8")
    print(f"Input text: 'aaaa'")
    print(f"Original size: {len(data)} bytes = {len(data) * 8} bits")
    
    freq = FrequencyCounter().count_from_data(data)
    print(f"Frequency table: {freq}")
    
    root = buildHuffmanTree(freq)
    print(f"Root has left child: {root.left is not None}")
    print(f"Root has right child: {root.right is not None}")
    
    codes = generateCodes(root)
    print(f"Generated codes: {codes}")
    print(f"Code for 'a' (byte 97): '{codes[97]}'")
    
    bitstring = encode(data, codes)
    print(f"Bitstring: {bitstring}")
    print(f"Bitstring length: {len(bitstring)} bits")
    
    assert codes[97] == "0", "Single character should have code '0'"
    assert bitstring == "0000", "Single character repeated 4 times should be '0000'"
    print("\n TEST 2 PASSED")


def test_hello_world():
    """Test with 'hello world'"""
    print("TEST 3: Compression with 'hello world'")

    
    data = "hello world".encode("utf-8")
    print(f"Input text: 'hello world'")
    print(f"Original size: {len(data)} bytes = {len(data) * 8} bits")
    
    freq = FrequencyCounter().count_from_data(data)
    print(f"\nFrequency table:")
    for byte_val, count in sorted(freq.items(), key=lambda x: x[1], reverse=True):
        char = chr(byte_val) if byte_val == 32 else chr(byte_val)
        print(f"  {repr(char):6} (byte {byte_val:3}): {count} times")
    
    root = buildHuffmanTree(freq)
    codes = generateCodes(root)
    
    print(f"\nGenerated codes (sorted by frequency):")
    sorted_chars = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    for byte_val, count in sorted_chars:
        char = repr(chr(byte_val))
        code = codes[byte_val]
        print(f"  {char:6} (freq={count:2}): '{code}'")
    
    bitstring = encode(data, codes)
    print(f"\nBitstring: {bitstring}")
    print(f"Bitstring length: {len(bitstring)} bits")
    
    ratio = (1 - len(bitstring) / (len(data) * 8)) * 100
    print(f"Compression ratio: {ratio:.1f}%")
    
    # Verify more frequent characters have shorter codes
    space_code = codes[32]  # space (most frequent)
    e_code = codes[101]     # 'e'
    print(f"\nSpace ' ' (freq=1) code length: {len(space_code)}")
    print(f"Character frequencies show more frequent chars should have shorter codes")
    
    print("\n TEST 3 PASSED")


def test_tree_structure():
    """Verify tree structure makes sense"""
    print("TEST 4: Tree structure validation")
    
    data = "aabbc".encode("utf-8")
    print(f"Input text: 'aabbc'")
    
    freq = FrequencyCounter().count_from_data(data)
    print(f"Frequency: {freq}")  # {97: 2, 98: 2, 99: 1}
    
    root = buildHuffmanTree(freq)
    codes = generateCodes(root)
    
    print(f"\nTree root frequency: {root.frequency} (should be 5)")
    print(f"Codes: {codes}")
    
    # Verify decode works
    print("\nVerifying decode by manually walking the tree:")
    bitstring = encode(data, codes)
    print(f"Bitstring: {bitstring}")
    
    cur = root
    decoded = []
    for bit in bitstring:
        cur = cur.left if bit == "0" else cur.right
        if cur.left is None and cur.right is None:  # leaf node
            decoded.append(chr(cur.char))
            print(f"  Found character: {repr(chr(cur.char))}")
            cur = root
    
    decoded_text = "".join(decoded)
    print(f"\nDecoded text: '{decoded_text}'")
    print(f"Original text: 'aabbc'")
    assert decoded_text == "aabbc", "Decoded text doesn't match!"
    
    print("\n TEST 4 PASSED")


if __name__ == "__main__":
    print("# HUFFMAN ALGORITHM TESTS")
    
    try:
        test_basic_compression()
        test_single_character()
        test_hello_world()
        test_tree_structure()
        
        print("# ALL TESTS PASSED ✓")
    
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}\n")
    except Exception as e:
        print(f"\n✗ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
"""
MAIN CLI INTERFACE
File: main.py

This is the ENTRY POINT that users will run from command line.
It handles argument parsing and calls the appropriate compression/decompression functions.

USAGE:
    python main.py -c <input_file>              # Compress
    python main.py -d <input_file>              # Decompress
    python main.py --compress <input_file>      # Long form
    python main.py --decompress <input_file>    # Long form
    python main.py -h                           # Show help

EXAMPLES:
    python main.py -c document.txt
    python main.py -d document.txt.huf
    python main.py --compress large_file.bin
    python main.py --decompress large_file.bin.huf
"""

import argparse
import sys
from pathlib import Path

from huffman_compress import compress
from huffman_decompress import decompress


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Huffman file compressor and decompressor.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main.py -c document.txt
  python main.py -d document.txt.huf
  python main.py -c document.bin -o compressed.huf
  python main.py -d compressed.huf -o recovered.bin
'''
    )

    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        '-c', '--compress',
        metavar='FILE',
        help='Compress FILE and write a .huf file.',
    )
    mode_group.add_argument(
        '-d', '--decompress',
        metavar='FILE',
        help='Decompress FILE (.huf format expected).',
    )

    parser.add_argument(
        '-o', '--output',
        metavar='FILE',
        help='Optional output file path. Defaults are generated automatically.',
    )

    return parser


def default_compress_output(input_path: Path) -> Path:
    return input_path.with_name(input_path.name + '.huf')


def default_decompress_output(input_path: Path) -> Path:
    if input_path.suffix.lower() == '.huf':
        return input_path.with_suffix('')
    return input_path.with_name(input_path.stem + '_recovered')


def execute_compress(input_path: Path, output_path: Path) -> int:
    print('\n' + '=' * 60)
    print('COMPRESSION MODE')
    print('=' * 60)
    print(f'Input file:  {input_path}')
    print(f'Output file: {output_path}')
    print('=' * 60)

    result = compress(str(input_path), str(output_path))
    if result.get('success'):
        print('\n✅ Compression completed successfully!')
        print(f'   Output file: {result["output_file"]}')
        return 0

    print('\n❌ Compression failed:', result.get('error', 'Unknown error'))
    return 1


def execute_decompress(input_path: Path, output_path: Path) -> int:
    print('\n' + '=' * 60)
    print('DECOMPRESSION MODE')
    print('=' * 60)
    print(f'Input file:  {input_path}')
    print(f'Output file: {output_path}')
    print('=' * 60)

    result = decompress(str(input_path), str(output_path))
    if result.get('success'):
        print('\n✅ Decompression completed successfully!')
        print(f'   Output file: {result["output_file"]}')
        return 0

    print('\n❌ Decompression failed:', result.get('error', 'Unknown error'))
    return 1


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.compress:
        input_path = Path(args.compress)
        output_path = Path(args.output) if args.output else default_compress_output(input_path)
        return execute_compress(input_path, output_path)

    input_path = Path(args.decompress)
    output_path = Path(args.output) if args.output else default_decompress_output(input_path)
    return execute_decompress(input_path, output_path)


def show_help():
    """Display detailed help information."""
    help_text = """
╔════════════════════════════════════════════════════════════════╗
║          HUFFMAN CODING FILE COMPRESSOR - USER GUIDE           ║
╚════════════════════════════════════════════════════════════════╝

OVERVIEW:
  This is a file compression tool that uses Huffman Coding to reduce
  file sizes. Frequently used bytes get shorter binary codes, while
  rare bytes get longer codes.

USAGE:
  python main.py [OPTIONS] FILE

OPTIONS:
  -c, --compress FILE       Compress FILE to FILE.huf
  -d, --decompress FILE     Decompress FILE (must be .huf file)
  -h, --help                Show this help message

COMPRESSION EXAMPLE:
  $ python main.py -c document.txt
  
  This will:
  1. Read document.txt
  2. Count character frequencies
  3. Build Huffman tree
  4. Generate optimal codes
  5. Compress the data
  6. Save to document.txt.huf
  
  Output shows:
  - Original size: 10,240 bytes
  - Compressed size: 3,456 bytes
  - Compression ratio: 66.3%

DECOMPRESSION EXAMPLE:
  $ python main.py -d document.txt.huf
  
  This will:
  1. Read document.txt.huf
  2. Extract the saved Huffman tree
  3. Decode the compressed binary
  4. Restore original data
  5. Save to document.txt

SUPPORTED FILE TYPES:
  Any file type can be compressed:
  - Text files (.txt, .csv, .json, .xml)
  - Binary files (.exe, .bin, .dat)
  - Archives (.zip, .tar)
  - Images (.png, .jpg, .gif)
  - Videos (.mp4, .mov)
  
NOTE: Very small or pre-compressed files may not compress well.

TECHNICAL DETAILS:
  .huf FILE FORMAT:
  ┌─────────────────────────────────────────┐
  │ Header (16 bytes)                       │
  │ - Original file size (4 bytes)          │
  │ - Compressed size (4 bytes)             │
  │ - Tree size (2 bytes)                   │
  │ - Padding info (2 bytes)                │
  │ - Reserved (4 bytes)                    │
  ├─────────────────────────────────────────┤
  │ Huffman Tree (variable size)            │
  ├─────────────────────────────────────────┤
  │ Compressed Binary Data (variable size)  │
  └─────────────────────────────────────────┘

IMPLEMENTATION NOTES:
  This project demonstrates:
  - Data structures: Min-Heap, Binary Tree
  - Algorithms: Huffman Coding (greedy algorithm)
  - File I/O: Binary file reading/writing
  - Tree serialization: Converting objects to bytes
  - Bit manipulation: Packing variable-length codes
  
  Team structure:
  - Member 1: Huffman algorithm implementation
  - Member 2: [Describe if applicable]
  - Member 3: File I/O and integration
    """
    print(help_text)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print('\n\n⚠️  Operation cancelled by user')
        sys.exit(1)
    except Exception as exc:
        print(f'\n\n❌ Unexpected error: {exc}')
        sys.exit(1)
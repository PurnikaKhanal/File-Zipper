import argparse     # Used to parse command-line arguments (e.g., -c for compress, -d for decompress)
import sys          # Provides system-level functions (e.g., clean program exit with sys.exit)
from pathlib import Path  # Pathlib makes file path handling easier and more cross-platform

from huffman_compress import compress
from huffman_decompress import decompress


def build_parser() -> argparse.ArgumentParser:
    """Builds the command-line argument parser."""
    # argparse.ArgumentParser creates a parser object that understands command-line options
    parser = argparse.ArgumentParser(
        description='Huffman file compressor and decompressor.',   # Shown in help text
        formatter_class=argparse.RawDescriptionHelpFormatter,      # Keeps formatting of epilog examples
        epilog='''                                                 # Extra usage examples shown in help
Examples:
  python main.py -c document.txt
  python main.py -d document.txt.huf
  python main.py -c document.bin -o compressed.huf
  python main.py -d compressed.huf -o recovered.bin
'''
    )

    # Mutually exclusive group ensures user can only choose compress OR decompress, not both
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        '-c', '--compress',
        metavar='FILE',   # Placeholder name shown in help
        help='Compress FILE and write a .huf file.',   # Help text
    )
    mode_group.add_argument(
        '-d', '--decompress',
        metavar='FILE',
        help='Decompress FILE (.huf format expected).',
    )

    # Optional output file argument
    parser.add_argument(
        '-o', '--output',
        metavar='FILE',
        help='Optional output file path. Defaults are generated automatically.',
    )

    return parser


def default_compress_output(input_path: Path) -> Path:
    """Default output filename for compression: adds .huf extension."""
    return input_path.with_name(input_path.name + '.huf')  # e.g., document.txt → document.txt.huf


def default_decompress_output(input_path: Path) -> Path:
    """Default output filename for decompression: removes .huf or adds _recovered."""
    if input_path.suffix.lower() == '.huf':
        return input_path.with_suffix('')  # e.g., document.txt.huf → document.txt
    return input_path.with_name(input_path.stem + '_recovered')  # e.g., file.bin → file_recovered


def execute_compress(input_path: Path, output_path: Path) -> int:
    """Runs compression and prints status messages."""
    print("\n============================================================")
    print("COMPRESSION MODE")
    print("============================================================")
    print(f"Input file:  {input_path}")
    print(f"Output file: {output_path}")
    print("============================================================")

    result = compress(str(input_path), str(output_path))  # Call compressor
    if result.get('success'):
        print("\nCompression completed successfully.")
        print(f"Output file: {result['output_file']}")
        return 0  # Return code 0 = success

    print("\nCompression failed:", result.get('error', 'Unknown error'))
    return 1  # Return code 1 = failure


def execute_decompress(input_path: Path, output_path: Path) -> int:
    """Runs decompression and prints status messages."""
    print("\n============================================================")
    print("DECOMPRESSION MODE")
    print("============================================================")
    print(f"Input file:  {input_path}")
    print(f"Output file: {output_path}")
    print("============================================================")

    result = decompress(str(input_path), str(output_path))  # Call decompressor
    if result.get('success'):
        print("\nDecompression completed successfully.")
        print(f"Output file: {result['output_file']}")
        return 0

    print("\nDecompression failed:", result.get('error', 'Unknown error'))
    return 1


def main(argv=None) -> int:
    """Main entry point: parse arguments and run compression/decompression."""
    parser = build_parser()
    args = parser.parse_args(argv)  # Parse command-line arguments

    # If user chose compression
    if args.compress:
        input_path = Path(args.compress)
        output_path = Path(args.output) if args.output else default_compress_output(input_path)
        return execute_compress(input_path, output_path)

    # Otherwise user chose decompression
    input_path = Path(args.decompress)
    output_path = Path(args.output) if args.output else default_decompress_output(input_path)
    return execute_decompress(input_path, output_path)


if __name__ == '__main__':
    # Program entry point when run directly
    try:
        sys.exit(main())  # Run main() and exit with its return code
    except KeyboardInterrupt:
        # Handles Ctrl+C gracefully
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as exc:
        # Catch-all for unexpected errors
        print(f"\nUnexpected error: {exc}")
        sys.exit(1)

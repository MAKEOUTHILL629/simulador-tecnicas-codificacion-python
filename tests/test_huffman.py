import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.huffman import HuffmanCoding

class TestHuffmanCoding(unittest.TestCase):

    def test_compression_decompression(self):
        huffman_coder = HuffmanCoding()
        text = "this is an example for huffman encoding"

        compressed_bits = huffman_coder.compress(text)
        decompressed_text = huffman_coder.decompress(compressed_bits)

        self.assertEqual(text, decompressed_text)

    def test_empty_string(self):
        huffman_coder = HuffmanCoding()
        text = ""

        compressed_bits = huffman_coder.compress(text)
        self.assertEqual(compressed_bits, "")

        decompressed_text = huffman_coder.decompress(compressed_bits)
        self.assertEqual(decompressed_text, "")

    def test_single_character(self):
        huffman_coder = HuffmanCoding()
        text = "aaaaa"

        compressed_bits = huffman_coder.compress(text)
        decompressed_text = huffman_coder.decompress(compressed_bits)

        self.assertEqual(text, decompressed_text)

if __name__ == '__main__':
    unittest.main()

"""
Source Encoder Module
Implements Huffman (text), DCT (image), MDCT (audio), and H.265-like (video) encoding
"""

import numpy as np
from collections import Counter
import heapq
from PIL import Image


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq


class SourceEncoder:
    def __init__(self, source_type):
        self.source_type = source_type
        self.huffman_tree = None
        self.huffman_codes = {}
    
    def encode(self, data):
        """Encode data based on source type"""
        if self.source_type == "Texto":
            return self._encode_text(data)
        elif self.source_type == "Imagen":
            return self._encode_image(data)
        elif self.source_type == "Audio":
            return self._encode_audio(data)
        elif self.source_type == "Video":
            return self._encode_video(data)
        else:
            raise ValueError(f"Unknown source type: {self.source_type}")
    
    def _encode_text(self, text):
        """Simple 8-bit ASCII encoding for text (educational purposes)"""
        if not text:
            return np.array([], dtype=int)
        
        # Use simple 8-bit ASCII encoding for better reconstruction
        # This makes the educational simulator more understandable
        bits = []
        for char in text:
            # Convert character to 8-bit binary
            ascii_val = ord(char)
            bits_str = format(ascii_val, '08b')
            bits.extend([int(b) for b in bits_str])
        
        return np.array(bits, dtype=int)
    
    def _generate_huffman_codes(self, node, code):
        """Generate Huffman codes recursively"""
        if node is None:
            return
        
        if node.char is not None:
            self.huffman_codes[node.char] = code if code else "0"
            return
        
        self._generate_huffman_codes(node.left, code + "0")
        self._generate_huffman_codes(node.right, code + "1")
    
    def _encode_image(self, image):
        """DCT-based encoding for images (JPEG-like) - RGB support"""
        # Convert PIL Image to numpy array, preserving RGB
        if isinstance(image, Image.Image):
            img_array = np.array(image.convert('RGB'))  # Keep RGB
        else:
            img_array = np.array(image)
            if len(img_array.shape) == 2:
                # Convert grayscale to RGB
                img_array = np.stack([img_array] * 3, axis=2)
        
        # Resize to manageable size for simulation
        if img_array.shape[0] > 64 or img_array.shape[1] > 64:
            from PIL import Image as PILImage
            img_pil = PILImage.fromarray(img_array.astype(np.uint8))
            img_pil = img_pil.resize((64, 64))
            img_array = np.array(img_pil)
        
        # Process each color channel separately
        all_bits = []
        for channel in range(3):  # R, G, B
            channel_data = img_array[:, :, channel]
            h, w = channel_data.shape
            h_blocks = h // 8
            w_blocks = w // 8
            
            dct_coeffs = []
            
            for i in range(h_blocks):
                for j in range(w_blocks):
                    block = channel_data[i*8:(i+1)*8, j*8:(j+1)*8].astype(float)
                    dct_block = self._dct2d(block)
                    
                    # Reduced quantization to /2 for better quality
                    quantized = np.round(dct_block / 2).astype(int)
                
                    # Reduced quantization to /2 for better quality
                    quantized = np.round(dct_block / 2).astype(int)
                    
                    # Zigzag scan and flatten
                    dct_coeffs.extend(quantized.flatten())
            
            # Convert to binary representation for this channel
            for coeff in dct_coeffs:
                # Use 8-bit signed representation
                val = int(coeff) & 0xFF
                all_bits.extend([int(b) for b in format(val, '08b')])
        
        return np.array(all_bits, dtype=int)
    
    def _dct2d(self, block):
        """2D DCT Transform"""
        N = block.shape[0]
        dct = np.zeros_like(block, dtype=float)
        
        for u in range(N):
            for v in range(N):
                sum_val = 0
                for i in range(N):
                    for j in range(N):
                        sum_val += block[i, j] * \
                                   np.cos((2*i + 1) * u * np.pi / (2*N)) * \
                                   np.cos((2*j + 1) * v * np.pi / (2*N))
                
                cu = 1/np.sqrt(2) if u == 0 else 1
                cv = 1/np.sqrt(2) if v == 0 else 1
                dct[u, v] = 0.25 * cu * cv * sum_val
        
        return dct
    
    def _encode_audio(self, audio_signal):
        """Simplified audio encoding for educational purposes"""
        # Normalize audio to [-1, 1] range
        max_val = np.max(np.abs(audio_signal))
        if max_val > 0:
            normalized = audio_signal / max_val
        else:
            normalized = audio_signal
        
        # Quantize to 12-bit representation (-2048 to 2047)
        quantized = np.round(normalized * 2047).astype(int)
        
        # Convert to binary (12 bits per sample)
        bits = []
        for sample in quantized:
            val = int(sample) & 0xFFF  # 12 bits
            bits.extend([int(b) for b in format(val, '012b')])
        
        return np.array(bits, dtype=int)
    
    def _encode_video(self, frame):
        """H.265-like encoding for video (simplified) - RGB support"""
        # Convert to RGB if needed
        if isinstance(frame, np.ndarray):
            if len(frame.shape) == 2:
                # Convert grayscale to RGB
                frame = np.stack([frame] * 3, axis=2)
            elif len(frame.shape) == 3 and frame.shape[2] == 3:
                # Already RGB, keep as is
                pass
        
        # Process each color channel
        all_bits = []
        for channel in range(3):  # R, G, B
            channel_data = frame[:, :, channel]
            h, w = channel_data.shape
            
            # DCT of channel
            dct_coeffs = []
            for i in range(0, h, 8):
                for j in range(0, w, 8):
                    if i+8 <= h and j+8 <= w:
                        block = channel_data[i:i+8, j:j+8].astype(float)
                        dct_block = self._dct2d(block)
                        # Reduced quantization to /2 for high quality
                        quantized = np.round(dct_block / 2).astype(int)
                        dct_coeffs.extend(quantized.flatten())
            
            # Convert to binary for this channel
            for coeff in dct_coeffs:
                val = int(coeff) & 0xFF
                all_bits.extend([int(b) for b in format(val, '08b')])
        
        return np.array(all_bits, dtype=int)

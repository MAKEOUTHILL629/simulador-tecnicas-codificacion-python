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
        """Huffman encoding for text"""
        if not text:
            return np.array([], dtype=int)
        
        # Calculate frequency
        freq = Counter(text)
        
        # Build Huffman tree
        heap = [HuffmanNode(char, count) for char, count in freq.items()]
        heapq.heapify(heap)
        
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            
            merged = HuffmanNode(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            
            heapq.heappush(heap, merged)
        
        self.huffman_tree = heap[0] if heap else None
        
        # Generate codes
        self._generate_huffman_codes(self.huffman_tree, "")
        
        # Encode text to bits
        bits = []
        for char in text:
            code = self.huffman_codes.get(char, "0")
            bits.extend([int(b) for b in code])
        
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
        """DCT-based encoding for images (JPEG-like)"""
        # Convert PIL Image to numpy array
        if isinstance(image, Image.Image):
            img_array = np.array(image.convert('L'))  # Convert to grayscale
        else:
            img_array = np.array(image)
            if len(img_array.shape) == 3:
                img_array = np.mean(img_array, axis=2).astype(np.uint8)
        
        # Resize to manageable size for simulation
        if img_array.shape[0] > 64 or img_array.shape[1] > 64:
            from PIL import Image as PILImage
            img_pil = PILImage.fromarray(img_array)
            img_pil = img_pil.resize((64, 64))
            img_array = np.array(img_pil)
        
        # Apply DCT in 8x8 blocks
        h, w = img_array.shape
        h_blocks = h // 8
        w_blocks = w // 8
        
        dct_coeffs = []
        
        for i in range(h_blocks):
            for j in range(w_blocks):
                block = img_array[i*8:(i+1)*8, j*8:(j+1)*8].astype(float)
                dct_block = self._dct2d(block)
                
                # Quantization (simple uniform)
                quantized = np.round(dct_block / 10).astype(int)
                
                # Zigzag scan and flatten
                dct_coeffs.extend(quantized.flatten())
        
        # Convert to binary representation
        bits = []
        for coeff in dct_coeffs:
            # Use 8-bit signed representation
            val = int(coeff) & 0xFF
            bits.extend([int(b) for b in format(val, '08b')])
        
        return np.array(bits, dtype=int)
    
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
        """MDCT-based encoding for audio (AAC-like)"""
        # MDCT with windowing
        M = 256  # Transform size
        
        # Pad signal if necessary
        pad_length = M - (len(audio_signal) % M)
        if pad_length < M:
            audio_signal = np.pad(audio_signal, (0, pad_length))
        
        # Apply MDCT
        mdct_coeffs = []
        num_blocks = len(audio_signal) // M
        
        for i in range(num_blocks):
            start_idx = i * M
            end_idx = min(start_idx + 2*M, len(audio_signal))
            block = audio_signal[start_idx:end_idx]
            if len(block) < 2*M:
                block = np.pad(block, (0, 2*M - len(block)))
            
            # Simple windowing
            window = np.sin(np.pi * (np.arange(2*M) + 0.5) / (2*M))
            windowed = block * window
            
            # MDCT calculation
            mdct_block = []
            for k in range(M):
                sum_val = 0
                for n in range(2*M):
                    sum_val += windowed[n] * np.cos(np.pi/M * (n + 0.5 + M/2) * (k + 0.5))
                mdct_block.append(sum_val)
            
            # Quantization
            quantized = np.round(np.array(mdct_block) * 100).astype(int)
            mdct_coeffs.extend(quantized)
        
        # Convert to binary
        bits = []
        for coeff in mdct_coeffs[:500]:  # Limit for simulation
            val = int(coeff) & 0xFFFF
            bits.extend([int(b) for b in format(val, '016b')])
        
        return np.array(bits, dtype=int)
    
    def _encode_video(self, frame):
        """H.265-like encoding for video (simplified)"""
        # Treat as image for this simulation
        # In real H.265, we'd do motion estimation
        if isinstance(frame, np.ndarray):
            if len(frame.shape) == 3:
                frame = np.mean(frame, axis=2).astype(np.uint8)
        
        # Apply DCT encoding (similar to image)
        h, w = frame.shape
        
        # Calculate residual (simplified - just add some noise simulation)
        residual = frame.astype(float)
        
        # DCT of residual
        dct_coeffs = []
        for i in range(0, h, 8):
            for j in range(0, w, 8):
                if i+8 <= h and j+8 <= w:
                    block = residual[i:i+8, j:j+8]
                    dct_block = self._dct2d(block)
                    quantized = np.round(dct_block / 10).astype(int)
                    dct_coeffs.extend(quantized.flatten())
        
        # Convert to binary
        bits = []
        for coeff in dct_coeffs:
            val = int(coeff) & 0xFF
            bits.extend([int(b) for b in format(val, '08b')])
        
        return np.array(bits, dtype=int)

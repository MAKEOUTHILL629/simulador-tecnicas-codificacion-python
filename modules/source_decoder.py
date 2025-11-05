"""
Source Decoder Module
Implements decoding for Huffman, DCT, MDCT, and H.265-like
"""

import numpy as np
from PIL import Image


class SourceDecoder:
    def __init__(self, source_type):
        self.source_type = source_type
    
    def decode(self, bits, original_data):
        """Decode bits based on source type"""
        if self.source_type == "Texto":
            return self._decode_text(bits, original_data)
        elif self.source_type == "Imagen":
            return self._decode_image(bits, original_data)
        elif self.source_type == "Audio":
            return self._decode_audio(bits, original_data)
        elif self.source_type == "Video":
            return self._decode_video(bits, original_data)
        else:
            return ""
    
    def _decode_text(self, bits, original_text):
        """Huffman decoding for text"""
        # For simulation, use character-level recovery
        # In real implementation, would use Huffman tree
        
        if len(original_text) == 0 or len(bits) == 0:
            return ""
        
        # Use 8 bits per character for ASCII representation
        bits_per_char = 8
        
        # Reconstruct text
        decoded_text = []
        for i in range(0, min(len(bits), len(original_text) * bits_per_char), bits_per_char):
            bit_chunk = bits[i:i+bits_per_char]
            if len(bit_chunk) == bits_per_char:
                # Map back to character
                char_idx = int(''.join(map(str, bit_chunk)), 2)
                if 32 <= char_idx <= 126:
                    decoded_text.append(chr(char_idx))
                else:
                    decoded_text.append('?')
        
        result = ''.join(decoded_text[:len(original_text)])
        return result if result else "Error de decodificación"
    
    def _decode_image(self, bits, original_image):
        """DCT-based decoding for images"""
        # Convert original image to get dimensions
        if isinstance(original_image, Image.Image):
            img_array = np.array(original_image.convert('L'))
        else:
            img_array = np.array(original_image)
            if len(img_array.shape) == 3:
                img_array = np.mean(img_array, axis=2).astype(np.uint8)
        
        # Get target dimensions
        if img_array.shape[0] > 64 or img_array.shape[1] > 64:
            target_h, target_w = 64, 64
        else:
            target_h, target_w = img_array.shape
        
        # Decode bits to DCT coefficients
        coeffs = []
        for i in range(0, len(bits), 8):
            if i + 8 <= len(bits):
                byte_val = int(''.join(map(str, bits[i:i+8])), 2)
                # Convert from unsigned to signed
                if byte_val > 127:
                    byte_val = byte_val - 256
                coeffs.append(byte_val)
        
        # Reconstruct image from DCT blocks
        h_blocks = target_h // 8
        w_blocks = target_w // 8
        reconstructed = np.zeros((target_h, target_w))
        
        coeff_idx = 0
        for i in range(h_blocks):
            for j in range(w_blocks):
                if coeff_idx + 64 <= len(coeffs):
                    block_coeffs = np.array(coeffs[coeff_idx:coeff_idx+64]).reshape(8, 8)
                    # Dequantize - updated to *2 to match encoder
                    dequantized = block_coeffs * 2
                    # IDCT
                    spatial_block = self._idct2d(dequantized)
                    reconstructed[i*8:(i+1)*8, j*8:(j+1)*8] = spatial_block
                    coeff_idx += 64
        
        # Clip to valid range
        reconstructed = np.clip(reconstructed, 0, 255).astype(np.uint8)
        
        return Image.fromarray(reconstructed)
    
    def _idct2d(self, dct_block):
        """2D Inverse DCT"""
        N = dct_block.shape[0]
        spatial = np.zeros_like(dct_block, dtype=float)
        
        for i in range(N):
            for j in range(N):
                sum_val = 0
                for u in range(N):
                    for v in range(N):
                        cu = 1/np.sqrt(2) if u == 0 else 1
                        cv = 1/np.sqrt(2) if v == 0 else 1
                        sum_val += cu * cv * dct_block[u, v] * \
                                   np.cos((2*i + 1) * u * np.pi / (2*N)) * \
                                   np.cos((2*j + 1) * v * np.pi / (2*N))
                spatial[i, j] = 0.25 * sum_val
        
        return spatial
    
    def _decode_audio(self, bits, original_audio):
        """Simplified audio decoding for educational purposes"""
        # Decode bits to samples (12 bits per sample)
        samples = []
        for i in range(0, len(bits), 12):
            if i + 12 <= len(bits):
                val = int(''.join(map(str, bits[i:i+12])), 2)
                # Convert from unsigned to signed
                if val > 2047:
                    val = val - 4096
                samples.append(val / 2047.0)
        
        # Pad or trim to match original length
        audio_signal = np.array(samples)
        if len(audio_signal) < len(original_audio):
            audio_signal = np.pad(audio_signal, (0, len(original_audio) - len(audio_signal)))
        else:
            audio_signal = audio_signal[:len(original_audio)]
        
        return audio_signal
    
    def _decode_video(self, bits, original_frame):
        """H.265-like decoding for video"""
        # Decode as image
        return self._decode_image(bits, original_frame)

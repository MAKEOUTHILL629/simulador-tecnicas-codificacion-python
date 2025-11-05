"""
Metrics Module
Calculates information theory metrics and integrity metrics
"""

import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim


class InformationMetrics:
    """Calculate information theory metrics"""
    
    def calculate_entropy(self, bits):
        """Calculate Shannon entropy H(X)"""
        if len(bits) == 0:
            return 0.0
        
        # Count occurrences
        unique, counts = np.unique(bits, return_counts=True)
        probabilities = counts / len(bits)
        
        # Calculate entropy
        entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))
        return entropy
    
    def calculate_mutual_information(self, input_bits, output_bits):
        """Calculate mutual information I(X;Y)"""
        # Ensure same length
        min_len = min(len(input_bits), len(output_bits))
        input_bits = input_bits[:min_len]
        output_bits = output_bits[:min_len]
        
        if min_len == 0:
            return 0.0
        
        # H(X)
        h_x = self.calculate_entropy(input_bits)
        
        # H(Y)
        h_y = self.calculate_entropy(output_bits)
        
        # H(X,Y) - Joint entropy
        # Create 2D histogram
        joint_hist = np.zeros((2, 2))
        for x, y in zip(input_bits, output_bits):
            joint_hist[int(x), int(y)] += 1
        
        joint_probs = joint_hist / min_len
        h_xy = -np.sum(joint_probs * np.log2(joint_probs + 1e-10))
        
        # I(X;Y) = H(X) + H(Y) - H(X,Y)
        mutual_info = h_x + h_y - h_xy
        return max(0, mutual_info)
    
    def calculate_self_information(self, probability):
        """Calculate self-information I(x) = -log2(p(x))"""
        return -np.log2(probability + 1e-10)


class IntegrityMetrics:
    """Calculate integrity and quality metrics"""
    
    def calculate_ber(self, original_bits, received_bits):
        """Calculate Bit Error Rate"""
        min_len = min(len(original_bits), len(received_bits))
        if min_len == 0:
            return 1.0
        
        errors = np.sum(original_bits[:min_len] != received_bits[:min_len])
        return errors / min_len
    
    def calculate_bler(self, original_bits, received_bits, block_size=100):
        """Calculate Block Error Rate"""
        min_len = min(len(original_bits), len(received_bits))
        if min_len < block_size:
            return self.calculate_ber(original_bits, received_bits)
        
        num_blocks = min_len // block_size
        error_blocks = 0
        
        for i in range(num_blocks):
            start = i * block_size
            end = start + block_size
            
            block_orig = original_bits[start:end]
            block_recv = received_bits[start:end]
            
            if np.any(block_orig != block_recv):
                error_blocks += 1
        
        return error_blocks / num_blocks if num_blocks > 0 else 1.0
    
    def calculate_psnr(self, original_image, received_image):
        """Calculate Peak Signal-to-Noise Ratio"""
        # Convert to numpy arrays
        if isinstance(original_image, Image.Image):
            orig = np.array(original_image.convert('L'))
        else:
            orig = np.array(original_image)
            if len(orig.shape) == 3:
                orig = np.mean(orig, axis=2)
        
        if isinstance(received_image, Image.Image):
            recv = np.array(received_image.convert('L'))
        else:
            recv = np.array(received_image)
            if len(recv.shape) == 3:
                recv = np.mean(recv, axis=2)
        
        # Ensure same dimensions
        if orig.shape != recv.shape:
            # Resize received to match original
            from PIL import Image as PILImage
            recv_pil = PILImage.fromarray(recv.astype(np.uint8))
            recv_pil = recv_pil.resize((orig.shape[1], orig.shape[0]))
            recv = np.array(recv_pil)
        
        # Calculate MSE
        mse = np.mean((orig.astype(float) - recv.astype(float)) ** 2)
        
        if mse == 0:
            return float('inf')  # Perfect match, theoretical PSNR is infinite
        
        # PSNR calculation
        max_pixel = 255.0
        psnr = 10 * np.log10((max_pixel ** 2) / mse)
        return psnr
    
    def calculate_ssim(self, original_image, received_image):
        """Calculate Structural Similarity Index"""
        # Convert to numpy arrays
        if isinstance(original_image, Image.Image):
            orig = np.array(original_image.convert('L'))
        else:
            orig = np.array(original_image)
            if len(orig.shape) == 3:
                orig = np.mean(orig, axis=2)
        
        if isinstance(received_image, Image.Image):
            recv = np.array(received_image.convert('L'))
        else:
            recv = np.array(received_image)
            if len(recv.shape) == 3:
                recv = np.mean(recv, axis=2)
        
        # Ensure same dimensions
        if orig.shape != recv.shape:
            from PIL import Image as PILImage
            recv_pil = PILImage.fromarray(recv.astype(np.uint8))
            recv_pil = recv_pil.resize((orig.shape[1], orig.shape[0]))
            recv = np.array(recv_pil)
        
        # Calculate SSIM
        ssim_value = ssim(orig, recv, data_range=255)
        return ssim_value

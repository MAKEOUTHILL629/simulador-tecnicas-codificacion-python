"""
Demodulator Module
Implements soft demodulation with LLR calculation
"""

import numpy as np


class Demodulator:
    def __init__(self, modulation_type):
        self.modulation_type = modulation_type
        self.constellation = self._generate_constellation()
    
    def _generate_constellation(self):
        """Generate constellation points (same as modulator)"""
        if self.modulation_type == "QPSK" or self.modulation_type == "DeepJSCC (Neural)":
            return np.array([
                1 + 1j, 1 - 1j,
                -1 + 1j, -1 - 1j
            ]) / np.sqrt(2)
        
        elif self.modulation_type == "16-QAM":
            points = []
            for i in [-3, -1, 1, 3]:
                for q in [-3, -1, 1, 3]:
                    points.append(i + 1j*q)
            return np.array(points) / np.sqrt(10)
        
        elif self.modulation_type == "64-QAM":
            points = []
            for i in [-7, -5, -3, -1, 1, 3, 5, 7]:
                for q in [-7, -5, -3, -1, 1, 3, 5, 7]:
                    points.append(i + 1j*q)
            return np.array(points) / np.sqrt(42)
        
        elif self.modulation_type == "256-QAM":
            points = []
            for i in range(-15, 16, 2):
                for q in range(-15, 16, 2):
                    points.append(i + 1j*q)
            return np.array(points) / np.sqrt(170)
        
        else:
            return np.array([1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j]) / np.sqrt(2)
    
    def demodulate(self, received_symbols, snr_db):
        """Soft demodulation with LLR calculation"""
        # Calculate noise variance
        N0 = 10**(-snr_db / 10)
        
        # Determine bits per symbol
        bits_per_symbol = self._get_bits_per_symbol()
        
        # Calculate LLRs for all bits
        llrs = []
        
        for symbol in received_symbols:
            # Calculate LLR for each bit position
            for bit_pos in range(bits_per_symbol):
                llr = self._calculate_llr(symbol, bit_pos, N0)
                llrs.append(llr)
        
        return np.array(llrs)
    
    def _calculate_llr(self, y, bit_pos, N0):
        """Calculate Log-Likelihood Ratio for a bit position"""
        # Max-Log-MAP approximation
        # LLR(b_i|y) ≈ (1/N0) * [min_{x in X_i,1} |y-x|^2 - min_{x in X_i,0} |y-x|^2]
        
        bits_per_symbol = self._get_bits_per_symbol()
        
        # Find constellation points where bit at bit_pos is 0 or 1
        dist_bit0 = []
        dist_bit1 = []
        
        for idx, x in enumerate(self.constellation):
            # Get bit pattern for this constellation point
            bit_pattern = format(idx, f'0{bits_per_symbol}b')
            
            # Calculate distance
            dist = np.abs(y - x)**2
            
            # Classify by bit value at position
            if bit_pattern[bit_pos] == '0':
                dist_bit0.append(dist)
            else:
                dist_bit1.append(dist)
        
        # Check if both lists have values (should always be true for valid constellation)
        if not dist_bit0 or not dist_bit1:
            # This should never happen with proper constellation mapping
            # Return neutral LLR if it does
            return 0.0
        
        # Max-Log-MAP: min distance for each hypothesis
        min_dist_0 = min(dist_bit0)
        min_dist_1 = min(dist_bit1)
        
        # LLR calculation
        llr = (1 / N0) * (min_dist_1 - min_dist_0)
        
        return llr
    
    def _get_bits_per_symbol(self):
        """Return bits per symbol"""
        if self.modulation_type == "QPSK" or self.modulation_type == "DeepJSCC (Neural)":
            return 2
        elif self.modulation_type == "16-QAM":
            return 4
        elif self.modulation_type == "64-QAM":
            return 6
        elif self.modulation_type == "256-QAM":
            return 8
        return 2
    
    def hard_decision(self, llrs):
        """Convert LLRs to hard bits"""
        return (llrs < 0).astype(int)

"""
Modulator Module
Implements QPSK, 16-QAM, 64-QAM, and 256-QAM modulation
"""

import numpy as np


class Modulator:
    def __init__(self, modulation_type):
        self.modulation_type = modulation_type
        self.constellation = self._generate_constellation()
    
    def _generate_constellation(self):
        """Generate constellation points for the modulation scheme"""
        if self.modulation_type == "QPSK":
            # 4 points, 2 bits per symbol
            return np.array([
                1 + 1j, 1 - 1j,
                -1 + 1j, -1 - 1j
            ]) / np.sqrt(2)
        
        elif self.modulation_type == "16-QAM":
            # 16 points, 4 bits per symbol
            points = []
            for i in [-3, -1, 1, 3]:
                for q in [-3, -1, 1, 3]:
                    points.append(i + 1j*q)
            return np.array(points) / np.sqrt(10)
        
        elif self.modulation_type == "64-QAM":
            # 64 points, 6 bits per symbol
            points = []
            for i in [-7, -5, -3, -1, 1, 3, 5, 7]:
                for q in [-7, -5, -3, -1, 1, 3, 5, 7]:
                    points.append(i + 1j*q)
            return np.array(points) / np.sqrt(42)
        
        elif self.modulation_type == "256-QAM":
            # 256 points, 8 bits per symbol
            points = []
            for i in range(-15, 16, 2):
                for q in range(-15, 16, 2):
                    points.append(i + 1j*q)
            return np.array(points) / np.sqrt(170)
        
        elif self.modulation_type == "DeepJSCC (Neural)":
            # For 6G simulation, use QPSK as base
            return np.array([
                1 + 1j, 1 - 1j,
                -1 + 1j, -1 - 1j
            ]) / np.sqrt(2)
        
        else:
            raise ValueError(f"Unknown modulation type: {self.modulation_type}")
    
    def modulate(self, bits):
        """Modulate bits to complex symbols"""
        # Determine bits per symbol
        if self.modulation_type == "QPSK" or self.modulation_type == "DeepJSCC (Neural)":
            bits_per_symbol = 2
        elif self.modulation_type == "16-QAM":
            bits_per_symbol = 4
        elif self.modulation_type == "64-QAM":
            bits_per_symbol = 6
        elif self.modulation_type == "256-QAM":
            bits_per_symbol = 8
        else:
            bits_per_symbol = 2
        
        # Pad bits if necessary
        num_symbols = int(np.ceil(len(bits) / bits_per_symbol))
        padded_bits = np.pad(bits, (0, num_symbols * bits_per_symbol - len(bits)))
        
        # Group bits into symbols
        bit_groups = padded_bits.reshape(-1, bits_per_symbol)
        
        # Map to constellation
        symbols = []
        for bit_group in bit_groups:
            # Convert bit group to integer index
            idx = int(''.join(map(str, bit_group)), 2)
            symbols.append(self.constellation[idx % len(self.constellation)])
        
        return np.array(symbols)
    
    def get_bits_per_symbol(self):
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

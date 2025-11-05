"""
Channel Encoder Module
Implements LDPC encoding for 5G/5G-Advanced
"""

import numpy as np


class ChannelEncoder:
    def __init__(self, network_type, code_rate=0.5):
        self.network_type = network_type
        self.code_rate = code_rate
    
    def encode(self, bits):
        """Encode bits with channel coding"""
        if self.network_type == "6G (JSCC)":
            # No separate channel coding in 6G JSCC mode
            return bits
        else:
            # Use LDPC for 5G/5G-Advanced
            return self._ldpc_encode(bits)
    
    def _ldpc_encode(self, bits):
        """Simplified LDPC encoding"""
        # For simulation, use a simple repetition code approximation
        # Real LDPC would use proper parity check matrix
        
        k = len(bits)  # Information bits
        n = int(k / self.code_rate)  # Total bits after encoding
        
        # Ensure we have enough bits for the code rate
        if n <= k:
            return bits
        
        # Simple systematic encoding: original bits + parity bits
        parity_bits = n - k
        
        # Generate parity bits using simple XOR of groups
        encoded = np.zeros(n, dtype=int)
        encoded[:k] = bits
        
        # Simple parity generation (not true LDPC but functional for simulation)
        for i in range(parity_bits):
            # Each parity bit is XOR of a subset of information bits
            start_idx = int(i * k / parity_bits)
            end_idx = int((i + 1) * k / parity_bits)
            encoded[k + i] = np.sum(bits[start_idx:end_idx]) % 2
        
        return encoded
    
    def get_code_parameters(self):
        """Return code parameters"""
        return {
            'network_type': self.network_type,
            'code_rate': self.code_rate
        }

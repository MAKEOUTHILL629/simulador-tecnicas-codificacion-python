"""
Wireless Channel Module
Implements AWGN, Rayleigh, and Rician fading
"""

import numpy as np


class WirelessChannel:
    def __init__(self, snr_db, eb_n0_db, fading_type, k_factor=10):
        self.snr_db = snr_db
        self.eb_n0_db = eb_n0_db
        self.fading_type = fading_type
        self.k_factor = k_factor  # For Rician fading
    
    def transmit(self, symbols):
        """Transmit symbols through the channel"""
        # Calculate noise variance from SNR
        signal_power = np.mean(np.abs(symbols)**2)
        snr_linear = 10**(self.snr_db / 10)
        noise_variance = signal_power / snr_linear
        
        # Apply fading
        if self.fading_type == "AWGN (Sin desvanecimiento)":
            faded_symbols = symbols
        elif self.fading_type == "Rayleigh (NLOS)":
            faded_symbols = self._apply_rayleigh_fading(symbols)
        elif self.fading_type == "Rician (LOS)":
            faded_symbols = self._apply_rician_fading(symbols)
        else:
            faded_symbols = symbols
        
        # Add AWGN noise
        noise = self._generate_awgn(len(faded_symbols), noise_variance)
        received = faded_symbols + noise
        
        return received
    
    def _apply_rayleigh_fading(self, symbols):
        """Apply Rayleigh fading (NLOS scenario)"""
        # Generate complex Gaussian random variables
        h_real = np.random.randn(len(symbols))
        h_imag = np.random.randn(len(symbols))
        h = (h_real + 1j * h_imag) / np.sqrt(2)
        
        # Apply fading coefficient
        return h * symbols
    
    def _apply_rician_fading(self, symbols):
        """Apply Rician fading (LOS scenario)"""
        K = self.k_factor  # K-factor (linear, not dB)
        
        # LOS component (deterministic)
        h_los = np.sqrt(K / (K + 1))
        
        # NLOS component (Rayleigh)
        h_real = np.random.randn(len(symbols))
        h_imag = np.random.randn(len(symbols))
        h_nlos = (h_real + 1j * h_imag) / np.sqrt(2) * np.sqrt(1 / (K + 1))
        
        # Combined Rician channel coefficient
        h = h_los + h_nlos
        
        return h * symbols
    
    def _generate_awgn(self, length, variance):
        """Generate Additive White Gaussian Noise"""
        noise_real = np.random.randn(length) * np.sqrt(variance / 2)
        noise_imag = np.random.randn(length) * np.sqrt(variance / 2)
        return noise_real + 1j * noise_imag
    
    def get_noise_variance(self, signal_power):
        """Calculate noise variance from SNR"""
        snr_linear = 10**(self.snr_db / 10)
        return signal_power / snr_linear

"""
Visualizer Module
Creates visualizations for each stage of the pipeline
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


class Visualizer:
    """Create visualizations for the simulator"""
    
    def plot_bitstream(self, bits, title="Bitstream"):
        """Plot a bitstream"""
        fig = Figure(figsize=(10, 3))
        ax = fig.add_subplot(111)
        
        # Limit visualization to first 100 bits
        bits_to_plot = bits[:100]
        
        ax.step(range(len(bits_to_plot)), bits_to_plot, where='post', linewidth=2)
        ax.set_xlabel('Bit Index')
        ax.set_ylabel('Bit Value')
        ax.set_title(title)
        ax.set_ylim([-0.5, 1.5])
        ax.set_yticks([0, 1])
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def plot_constellation(self, symbols, title="Constellation Diagram"):
        """Plot constellation diagram"""
        fig = Figure(figsize=(8, 8))
        ax = fig.add_subplot(111)
        
        # Extract I and Q components
        I = np.real(symbols)
        Q = np.imag(symbols)
        
        # Plot
        ax.scatter(I, Q, alpha=0.5, s=10)
        ax.set_xlabel('In-Phase (I)')
        ax.set_ylabel('Quadrature (Q)')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='k', linewidth=0.5)
        ax.axvline(x=0, color='k', linewidth=0.5)
        
        # Set equal aspect ratio
        max_val = max(np.max(np.abs(I)), np.max(np.abs(Q)))
        ax.set_xlim([-max_val*1.1, max_val*1.1])
        ax.set_ylim([-max_val*1.1, max_val*1.1])
        ax.set_aspect('equal')
        
        return fig
    
    def plot_llr_histogram(self, llrs, title="LLR Distribution"):
        """Plot histogram of LLR values"""
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        
        # Clip extreme values for better visualization
        llrs_clipped = np.clip(llrs, -20, 20)
        
        ax.hist(llrs_clipped, bins=50, alpha=0.7, edgecolor='black')
        ax.set_xlabel('LLR Value')
        ax.set_ylabel('Frequency')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        ax.axvline(x=0, color='r', linestyle='--', linewidth=2, label='Decision Threshold')
        ax.legend()
        
        # Add text annotations
        positive_llrs = np.sum(llrs > 0)
        negative_llrs = np.sum(llrs < 0)
        ax.text(0.02, 0.98, f'LLR > 0 (bit=0): {positive_llrs}\nLLR < 0 (bit=1): {negative_llrs}',
                transform=ax.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        return fig
    
    def plot_audio_signal(self, signal, title="Audio Signal"):
        """Plot audio waveform"""
        fig = Figure(figsize=(10, 4))
        ax = fig.add_subplot(111)
        
        time = np.arange(len(signal))
        ax.plot(time, signal, linewidth=0.5)
        ax.set_xlabel('Sample')
        ax.set_ylabel('Amplitude')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def plot_spectrum(self, signal, sample_rate, title="Frequency Spectrum"):
        """Plot frequency spectrum"""
        fig = Figure(figsize=(10, 4))
        ax = fig.add_subplot(111)
        
        # FFT
        fft = np.fft.fft(signal)
        freqs = np.fft.fftfreq(len(signal), 1/sample_rate)
        
        # Plot only positive frequencies
        positive_freqs = freqs[:len(freqs)//2]
        positive_fft = np.abs(fft[:len(fft)//2])
        
        ax.plot(positive_freqs, positive_fft)
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Magnitude')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def plot_ber_curve(self, snr_range, ber_values, title="BER vs SNR"):
        """Plot BER curve"""
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        
        ax.semilogy(snr_range, ber_values, marker='o', linewidth=2)
        ax.set_xlabel('SNR (dB)')
        ax.set_ylabel('Bit Error Rate (BER)')
        ax.set_title(title)
        ax.grid(True, which='both', alpha=0.3)
        
        return fig
    
    def plot_image_comparison(self, original, received, title="Image Comparison"):
        """Plot original vs received image"""
        fig = Figure(figsize=(12, 6))
        
        ax1 = fig.add_subplot(121)
        ax1.imshow(original, cmap='gray')
        ax1.set_title('Original')
        ax1.axis('off')
        
        ax2 = fig.add_subplot(122)
        ax2.imshow(received, cmap='gray')
        ax2.set_title('Received')
        ax2.axis('off')
        
        fig.suptitle(title)
        
        return fig

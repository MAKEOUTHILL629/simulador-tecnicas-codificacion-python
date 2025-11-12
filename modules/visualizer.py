"""
Visualizer Module
Creates visualizations for each stage of the pipeline
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


class Visualizer:
    """Create visualizations for the simulator"""
    
    def plot_bitstream(self, bits, title="Bitstream", show_stats=True):
        """Plot a bitstream with statistics"""
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
        
        # Add statistics
        if show_stats and len(bits) > 0:
            ones = np.sum(bits == 1)
            zeros = np.sum(bits == 0)
            total = len(bits)
            stats_text = f'Total: {total} bits\n1s: {ones} ({ones/total*100:.1f}%)\n0s: {zeros} ({zeros/total*100:.1f}%)'
            ax.text(0.02, 0.98, stats_text,
                   transform=ax.transAxes, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7),
                   fontsize=9)
        
        return fig
    
    def plot_channel_encoding_comparison(self, source_bits, channel_bits, title="Codificación de Canal"):
        """Plot showing redundancy added by channel encoder"""
        fig = Figure(figsize=(10, 4))
        ax = fig.add_subplot(111)
        
        # Show structure of channel encoded bits
        sample_size = min(200, len(channel_bits))
        x = np.arange(sample_size)
        
        # Plot channel bits
        ax.step(x, channel_bits[:sample_size], where='post', linewidth=1.5, label='Bits con LDPC', alpha=0.8)
        
        # Highlight redundancy pattern (simplified visualization)
        # In LDPC, systematic part comes first, then parity
        systematic_len = len(source_bits)
        if sample_size > systematic_len:
            ax.axvspan(systematic_len, sample_size, alpha=0.2, color='red', label='Bits de Paridad')
        
        ax.set_xlabel('Bit Index')
        ax.set_ylabel('Bit Value')
        ax.set_title(title)
        ax.set_ylim([-0.5, 1.5])
        ax.set_yticks([0, 1])
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right')
        
        # Add statistics
        info_rate = len(source_bits) / len(channel_bits)
        stats_text = f'Datos: {len(source_bits)} bits\nTotal: {len(channel_bits)} bits\nRedundancia: {len(channel_bits)-len(source_bits)} bits\nTasa: {info_rate:.2f}'
        ax.text(0.02, 0.70, stats_text,
               transform=ax.transAxes, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8),
               fontsize=9)
        
        return fig
    
    def plot_constellation(self, symbols, modulation_type="QPSK", title="Constellation Diagram"):
        """Plot constellation diagram showing both theoretical and actual points"""
        fig = Figure(figsize=(10, 8))
        ax = fig.add_subplot(111)
        
        # Extract I and Q components from actual symbols
        I = np.real(symbols)
        Q = np.imag(symbols)
        
        # Plot actual received symbols
        ax.scatter(I, Q, alpha=0.3, s=20, c='blue', label='Received Symbols')
        
        # Generate and plot theoretical constellation points
        if modulation_type == "QPSK":
            theo_points = np.array([1+1j, 1-1j, -1+1j, -1-1j]) / np.sqrt(2)
        elif modulation_type == "16-QAM":
            theo_points = []
            for i in [-3, -1, 1, 3]:
                for q in [-3, -1, 1, 3]:
                    theo_points.append(i + 1j*q)
            theo_points = np.array(theo_points) / np.sqrt(10)
        elif modulation_type == "64-QAM":
            theo_points = []
            for i in [-7, -5, -3, -1, 1, 3, 5, 7]:
                for q in [-7, -5, -3, -1, 1, 3, 5, 7]:
                    theo_points.append(i + 1j*q)
            theo_points = np.array(theo_points) / np.sqrt(42)
        elif modulation_type == "256-QAM":
            theo_points = []
            for i in range(-15, 16, 2):
                for q in range(-15, 16, 2):
                    theo_points.append(i + 1j*q)
            theo_points = np.array(theo_points) / np.sqrt(170)
        else:
            theo_points = np.array([1+1j, 1-1j, -1+1j, -1-1j]) / np.sqrt(2)
        
        # Plot theoretical constellation points
        theo_I = np.real(theo_points)
        theo_Q = np.imag(theo_points)
        ax.scatter(theo_I, theo_Q, alpha=1.0, s=100, c='red', marker='x', 
                  linewidths=2, label=f'Ideal {modulation_type} Points')
        
        ax.set_xlabel('In-Phase (I)', fontsize=12)
        ax.set_ylabel('Quadrature (Q)', fontsize=12)
        ax.set_title(f'{title}\n{len(symbols)} símbolos, {len(theo_points)} puntos ideales', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='k', linewidth=0.5)
        ax.axvline(x=0, color='k', linewidth=0.5)
        ax.legend(loc='upper right')
        
        # Set equal aspect ratio
        max_val = max(np.max(np.abs(theo_I)), np.max(np.abs(theo_Q)), 
                     np.max(np.abs(I)) if len(I) > 0 else 1, 
                     np.max(np.abs(Q)) if len(Q) > 0 else 1)
        ax.set_xlim([-max_val*1.2, max_val*1.2])
        ax.set_ylim([-max_val*1.2, max_val*1.2])
        ax.set_aspect('equal')
        
        # Add info text
        info_text = f'Puntos teóricos: {len(theo_points)}\nSímbolos transmitidos: {len(symbols)}'
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes, 
               verticalalignment='top', fontsize=10,
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
        
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
    
    def plot_audio_comparison(self, original_signal, received_signal):
        """Plot original and received audio waveforms for comparison"""
        fig = Figure(figsize=(12, 6))
        
        # Original signal
        ax1 = fig.add_subplot(211)
        time1 = np.arange(len(original_signal))
        ax1.plot(time1, original_signal, linewidth=0.5, color='blue', alpha=0.7)
        ax1.set_ylabel('Amplitude')
        ax1.set_title('Señal de Audio Original')
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim([0, len(original_signal)])
        
        # Received signal
        ax2 = fig.add_subplot(212)
        time2 = np.arange(len(received_signal))
        ax2.plot(time2, received_signal, linewidth=0.5, color='red', alpha=0.7)
        ax2.set_xlabel('Sample')
        ax2.set_ylabel('Amplitude')
        ax2.set_title('Señal de Audio Recibida')
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim([0, len(received_signal)])
        
        # Add correlation metric
        if len(original_signal) == len(received_signal):
            correlation = np.corrcoef(original_signal, received_signal)[0, 1]
            fig.suptitle(f'Comparación de Audio (Correlación: {correlation:.4f})', 
                        fontsize=14, fontweight='bold')
        
        fig.tight_layout()
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

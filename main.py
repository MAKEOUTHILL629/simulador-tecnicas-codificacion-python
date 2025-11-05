from src.huffman import HuffmanCoding
from src.modulation import qpsk_modulate, qpsk_demodulate_llr
from src.channel import awgn_channel
from src.channel_coding import ldpc_encode, ldpc_decode
from src.visualization import plot_constellation
import numpy as np

def main():
    # --- Simulation Parameters ---
    snr_db = 15  # Signal-to-Noise Ratio in dB

    # --- Source ---
    input_filepath = "data/sample_text.txt"
    with open(input_filepath, 'r') as f:
        original_text = f.read()

    print(f"Original Text:\n{original_text}\n")

    # --- Source Coding (Huffman) ---
    huffman_coder = HuffmanCoding()
    source_coded_bits = huffman_coder.compress(original_text)
    print(f"Source Coded Bits (first 50): {source_coded_bits[:50]}...")
    print(f"Compressed Bit Length: {len(source_coded_bits)}\n")

    # --- Channel Coding (Placeholder) ---
    channel_coded_bits = ldpc_encode(source_coded_bits)

    # --- Modulation (QPSK) ---
    # Ensure even number of bits for QPSK
    if len(channel_coded_bits) % 2 != 0:
        channel_coded_bits += '0'

    transmitted_symbols = qpsk_modulate(channel_coded_bits)
    print("Modulation: QPSK")
    print(f"Number of Transmitted Symbols: {len(transmitted_symbols)}\n")
    plot_constellation(transmitted_symbols, title="Transmitted Constellation")

    # --- Channel ---
    # Calculate noise variance for the given SNR
    signal_power = np.mean(np.abs(transmitted_symbols)**2)
    snr_linear = 10**(snr_db / 10.0)
    noise_variance = signal_power / snr_linear

    received_symbols = awgn_channel(transmitted_symbols, snr_db)
    print(f"Channel: AWGN with SNR = {snr_db} dB\n")
    plot_constellation(received_symbols, title="Received Constellation")


    # --- Demodulation (QPSK LLR) ---
    received_llrs = qpsk_demodulate_llr(received_symbols, noise_variance)
    print("Demodulation: QPSK to LLRs\n")

    # --- Channel Decoding (Placeholder) ---
    channel_decoded_bits = ldpc_decode(received_llrs)

    # --- Source Decoding (Huffman) ---
    decoded_text = huffman_coder.decompress(channel_decoded_bits)
    print(f"Decoded Text:\n{decoded_text}\n")

    # --- Verification ---
    if original_text == decoded_text:
        print("Success: Decoded text matches original text.")
    else:
        print("Error: Decoded text does not match original text.")

    # --- Metrics ---
    num_errors = sum(1 for a, b in zip(source_coded_bits, channel_decoded_bits) if a != b)
    ber = num_errors / len(source_coded_bits)
    print(f"Bit Error Rate (BER): {ber:.6f} ({num_errors}/{len(source_coded_bits)})")


if __name__ == "__main__":
    main()

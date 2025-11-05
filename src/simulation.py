from src.huffman import HuffmanCoding
from src.modulation import qpsk_modulate, qpsk_demodulate_llr
from src.channel import awgn_channel
from src.channel_coding import ldpc_encode, ldpc_decode
from src.visualization import plot_constellation, plot_huffman_tree, plot_llr_histogram
import numpy as np

def run_simulation(snr_db, input_filepath):
    # --- Source ---
    with open(input_filepath, 'r') as f:
        original_text = f.read()

    # --- Source Coding (Huffman) ---
    huffman_coder = HuffmanCoding()
    source_coded_bits = huffman_coder.compress(original_text)
    plot_huffman_tree(huffman_coder.tree_root)

    # --- Channel Coding (Placeholder) ---
    channel_coded_bits = ldpc_encode(source_coded_bits)

    # --- Modulation (QPSK) ---
    if len(channel_coded_bits) % 2 != 0:
        channel_coded_bits += '0'

    transmitted_symbols = qpsk_modulate(channel_coded_bits)
    plot_constellation(transmitted_symbols, title="Transmitted Constellation")

    # --- Channel ---
    signal_power = np.mean(np.abs(transmitted_symbols)**2)
    snr_linear = 10**(snr_db / 10.0)
    noise_variance = signal_power / snr_linear
    received_symbols = awgn_channel(transmitted_symbols, snr_db)
    plot_constellation(received_symbols, title="Received Constellation")

    # --- Demodulation (QPSK LLR) ---
    received_llrs = qpsk_demodulate_llr(received_symbols, noise_variance)
    plot_llr_histogram(received_llrs)

    # --- Channel Decoding (Placeholder) ---
    channel_decoded_bits = ldpc_decode(received_llrs)

    # --- Source Decoding (Huffman) ---
    decoded_text = huffman_coder.decompress(channel_decoded_bits)

    # --- Metrics ---
    num_errors = sum(1 for a, b in zip(source_coded_bits, channel_decoded_bits) if a != b)
    ber = num_errors / len(source_coded_bits) if source_coded_bits else 0

    return {
        "original_text": original_text,
        "decoded_text": decoded_text,
        "ber": ber,
        "num_errors": num_errors,
        "bit_count": len(source_coded_bits)
    }

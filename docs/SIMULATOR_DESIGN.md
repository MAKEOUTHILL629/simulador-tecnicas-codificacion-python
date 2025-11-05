# Simulator Design

This document outlines the high-level design of the communications simulator.

## Architecture

The simulator follows a modular pipeline architecture, where each stage of the communication chain is implemented as a separate Python module. This allows for clear visualization of the signal at each step and facilitates the testing and extension of individual modules.

### Core Modules (Version 0.1.0)

1.  **Source (`main.py`):** Generates the input data by reading a text file (`data/sample_text.txt`).
2.  **Source Coder (`src/huffman.py`):** Compresses the source text using Huffman coding.
3.  **Channel Coder (`src/channel_coding.py`):** Placeholder for LDPC channel coding. Currently, it passes the data through without modification.
4.  **Modulator (`src/modulation.py`):** Maps the coded bits to complex symbols using QPSK.
5.  **Channel (`src/channel.py`):** Simulates an AWGN channel with a configurable SNR.
6.  **Demodulator (`src/modulation.py`):** Computes log-likelihood ratios (LLRs) from the received symbols using a max-log-MAP demodulator for QPSK.
7.  **Channel Decoder (`src/channel_coding.py`):** Placeholder for LDPC channel decoding. It performs hard-decision decoding based on the LLR signs.
8.  **Source Decoder (`src/huffman.py`):** Decompresses the data using the Huffman tree to reconstruct the original text.
9.  **Visualization (`src/visualization.py`):** Generates constellation plots using `matplotlib`.

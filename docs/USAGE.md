# How to Use the Simulator

This document explains how to run the communications system simulator.

## Prerequisites

- Python 3.x
- `numpy`
- `matplotlib`

You can install the required packages using pip:

```bash
pip install numpy matplotlib
```

## Running the Simulator

To run the text simulation, execute the `main.py` script from the root directory of the project:

```bash
python3 main.py
```

### Output

The simulator will print the following information to the console:

- The original text.
- The compressed bit stream from the Huffman coder.
- The modulation scheme being used.
- The channel conditions (SNR).
- The decoded text.
- A success or error message indicating if the decoded text matches the original.
- The Bit Error Rate (BER).

The simulator will also generate two PNG images in the root directory:

- `transmitted_constellation.png`: A plot of the QPSK constellation before the channel.
- `received_constellation.png`: A plot of the QPSK constellation after the channel noise has been added.

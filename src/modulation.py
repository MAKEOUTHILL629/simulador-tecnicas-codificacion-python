import numpy as np

def qpsk_modulate(bit_stream):
    """
    Modulates a bit stream using QPSK.

    Args:
        bit_stream (str): A string of '0's and '1's.

    Returns:
        np.ndarray: An array of complex numbers representing the QPSK symbols.
    """
    if len(bit_stream) % 2 != 0:
        raise ValueError("The length of the bit stream must be even.")

    symbols = []
    for i in range(0, len(bit_stream), 2):
        b0 = int(bit_stream[i])
        b1 = int(bit_stream[i+1])
        symbol = (1 / np.sqrt(2)) * ((1 - 2 * b0) + 1j * (1 - 2 * b1))
        symbols.append(symbol)

    return np.array(symbols)

def qpsk_demodulate_llr(received_symbols, noise_variance):
    """
    Demodulates QPSK symbols to LLRs using the max-log-MAP approximation.

    Args:
        received_symbols (np.ndarray): An array of received complex symbols.
        noise_variance (float): The variance of the noise (N0).

    Returns:
        np.ndarray: An array of LLRs for each bit.
    """
    # QPSK constellation points
    constellation = {
        '00': (1/np.sqrt(2)) * (1 + 1j),
        '01': (1/np.sqrt(2)) * (1 - 1j),
        '10': (1/np.sqrt(2)) * (-1 + 1j),
        '11': (1/np.sqrt(2)) * (-1 - 1j)
    }

    # Subsets of the constellation for each bit
    x_i0 = [constellation[s] for s in constellation if s[0] == '0']
    x_i1 = [constellation[s] for s in constellation if s[0] == '1']
    x_q0 = [constellation[s] for s in constellation if s[1] == '0']
    x_q1 = [constellation[s] for s in constellation if s[1] == '1']

    llrs = []
    for y in received_symbols:
        # LLR for the first bit (in-phase)
        min_dist_i0 = np.min([np.abs(y - x)**2 for x in x_i0])
        min_dist_i1 = np.min([np.abs(y - x)**2 for x in x_i1])
        llr_i = (1 / noise_variance) * (min_dist_i1 - min_dist_i0)
        llrs.append(llr_i)

        # LLR for the second bit (quadrature)
        min_dist_q0 = np.min([np.abs(y - x)**2 for x in x_q0])
        min_dist_q1 = np.min([np.abs(y - x)**2 for x in x_q1])
        llr_q = (1 / noise_variance) * (min_dist_q1 - min_dist_q0)
        llrs.append(llr_q)

    return np.array(llrs)

import numpy as np

def awgn_channel(symbols, snr_db):
    """
    Simulates an AWGN channel.

    Args:
        symbols (np.ndarray): An array of complex symbols.
        snr_db (float): The signal-to-noise ratio in dB.

    Returns:
        np.ndarray: The received symbols with AWGN.
    """
    # Calculate signal power
    signal_power = np.mean(np.abs(symbols)**2)

    # Calculate noise power from SNR
    snr = 10**(snr_db / 10)
    noise_power = signal_power / snr

    # Generate complex Gaussian noise
    noise = np.sqrt(noise_power / 2) * (np.random.randn(len(symbols)) + 1j * np.random.randn(len(symbols)))

    return symbols + noise

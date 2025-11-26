"""
Test full pipeline to identify where quality degrades
"""

import numpy as np
from PIL import Image
from modules.source_encoder import SourceEncoder
from modules.source_decoder import SourceDecoder
from modules.channel_encoder import ChannelEncoder
from modules.channel_decoder import ChannelDecoder
from modules.modulator import Modulator
from modules.demodulator import Demodulator
from modules.channel import WirelessChannel
from modules.metrics import IntegrityMetrics

print("=" * 60)
print("FULL PIPELINE TEST - Image with Perfect Conditions")
print("=" * 60)

# Create test image
img = Image.new('L', (64, 64), color=128)
pixels = np.array(img)
pixels[20:40, 20:40] = 255
img = Image.fromarray(pixels)
img.save('/tmp/pipeline_original.png')
print(f"✓ Original image created: 64x64, white square on gray background")

# Configuration (matching user's settings)
network_type = "5G"
code_rate = 0.50
modulation = "QPSK"
snr_db = 10
eb_n0_db = 10
fading_type = "AWGN (Sin desvanec...)"
k_factor = 1.0

# Initialize modules
source_enc = SourceEncoder('Imagen')
channel_enc = ChannelEncoder(network_type, code_rate)
mod = Modulator(modulation)
channel = WirelessChannel(snr_db, eb_n0_db, fading_type, k_factor)
demod = Demodulator(modulation)
channel_dec = ChannelDecoder(network_type, code_rate)
source_dec = SourceDecoder('Imagen')
metrics = IntegrityMetrics()

print("\n" + "-" * 60)
print("STAGE 1: Source Encoding")
print("-" * 60)
encoded_source = source_enc.encode(img)
print(f"✓ Encoded bits: {len(encoded_source)}")
print(f"  Sample (first 20 bits): {encoded_source[:20]}")

print("\n" + "-" * 60)
print("STAGE 2: Channel Encoding (LDPC)")
print("-" * 60)
encoded_channel = channel_enc.encode(encoded_source)
print(f"✓ Channel encoded bits: {len(encoded_channel)}")
print(f"  Overhead: {len(encoded_channel) - len(encoded_source)} bits ({(len(encoded_channel)/len(encoded_source)-1)*100:.1f}%)")
print(f"  Sample (first 20 bits): {encoded_channel[:20]}")

print("\n" + "-" * 60)
print("STAGE 3: Modulation ({})".format(modulation))
print("-" * 60)
modulated_signal = mod.modulate(encoded_channel)
print(f"✓ Symbols: {len(modulated_signal)}")
print(f"  Sample (first 5 symbols): {modulated_signal[:5]}")

print("\n" + "-" * 60)
print("STAGE 4: Channel (SNR={} dB, {})".format(snr_db, fading_type))
print("-" * 60)
received_signal = channel.transmit(modulated_signal)
print(f"✓ Received symbols: {len(received_signal)}")
print(f"  Sample (first 5 symbols): {received_signal[:5]}")
print(f"  Noise added: Mean error = {np.mean(np.abs(modulated_signal - received_signal)):.4f}")

print("\n" + "-" * 60)
print("STAGE 5: Demodulation")
print("-" * 60)
llrs = demod.demodulate(received_signal, snr_db)
print(f"✓ LLRs: {len(llrs)}")
print(f"  Sample (first 20 LLRs): {llrs[:20]}")
hard_decisions = (llrs < 0).astype(int)
bit_errors_after_demod = np.sum(encoded_channel[:len(hard_decisions)] != hard_decisions)
print(f"  Bit errors after demod: {bit_errors_after_demod} / {len(hard_decisions)} ({bit_errors_after_demod/len(hard_decisions)*100:.2f}%)")

print("\n" + "-" * 60)
print("STAGE 6: Channel Decoding")
print("-" * 60)
decoded_channel = channel_dec.decode(llrs)
print(f"✓ Decoded bits: {len(decoded_channel)}")
print(f"  Sample (first 20 bits): {decoded_channel[:20]}")
bit_errors = np.sum(encoded_source[:len(decoded_channel)] != decoded_channel[:len(encoded_source)])
ber = bit_errors / min(len(encoded_source), len(decoded_channel))
print(f"  Bit errors: {bit_errors} / {min(len(encoded_source), len(decoded_channel))} (BER = {ber:.6f})")

print("\n" + "-" * 60)
print("STAGE 7: Source Decoding")
print("-" * 60)
output_data = source_dec.decode(decoded_channel, img)
output_data.save('/tmp/pipeline_reconstructed.png')
print(f"✓ Image reconstructed")

# Calculate final metrics
psnr = metrics.calculate_psnr(img, output_data)
ssim = metrics.calculate_ssim(img, output_data)

print("\n" + "=" * 60)
print("FINAL RESULTS")
print("=" * 60)
print(f"BER: {ber:.6f} ({(1-ber)*100:.2f}% correct)")
print(f"PSNR: {psnr:.2f} dB")
print(f"SSIM: {ssim:.4f}")

# Pixel-level comparison
orig_array = np.array(img)
recon_array = np.array(output_data)
pixel_diff = np.abs(orig_array.astype(float) - recon_array.astype(float))
print(f"\nPixel errors:")
print(f"  Mean: {pixel_diff.mean():.2f}")
print(f"  Max: {pixel_diff.max():.2f}")
print(f"  Std: {pixel_diff.std():.2f}")

print("\n" + "=" * 60)
if psnr < 20:
    print("⚠️  WARNING: PSNR is very low even with BER near 0!")
    print("    Problem likely in source encoder/decoder quantization")
elif psnr < 30:
    print("⚠️  WARNING: PSNR is below expected for BER near 0")
    print("    Some quality loss in pipeline")
else:
    print("✓ Quality looks good!")
print("=" * 60)

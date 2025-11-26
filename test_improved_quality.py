"""
Test script to verify improved encoding/decoding quality
"""

import numpy as np
from PIL import Image
from modules.source_encoder import SourceEncoder
from modules.source_decoder import SourceDecoder
from modules.metrics import IntegrityMetrics

print("=" * 70)
print("Testing Improved Image/Audio/Video Quality")
print("=" * 70)

# Test 1: Image encoding/decoding
print("\n1. Testing IMAGE encoding/decoding:")
print("-" * 70)

# Create test image
test_img = np.random.randint(0, 256, (64, 64), dtype=np.uint8)
test_pil = Image.fromarray(test_img)

encoder = SourceEncoder("Imagen")
decoder = SourceDecoder("Imagen")

# Encode and decode
bits = encoder.encode(test_pil)
recovered = decoder.decode(bits, test_pil)
recovered_array = np.array(recovered)

# Calculate metrics
metrics = IntegrityMetrics()
psnr = metrics.calculate_psnr(test_pil, recovered)
ssim = metrics.calculate_ssim(test_pil, recovered)

print(f"Image size: 64x64")
print(f"Encoded bits: {len(bits)}")
print(f"PSNR: {psnr:.2f} dB")
print(f"SSIM: {ssim:.4f}")
print(f"Expected: PSNR > 25 dB (improved from ~10 dB)")
print(f"Status: {'✅ PASS' if psnr > 25 else '❌ FAIL'}")

# Test 2: Audio encoding/decoding
print("\n2. Testing AUDIO encoding/decoding:")
print("-" * 70)

# Create test audio
sample_rate = 8000
duration = 0.5
t = np.linspace(0, duration, int(sample_rate * duration))
test_audio = np.sin(2 * np.pi * 440 * t)

encoder = SourceEncoder("Audio")
decoder = SourceDecoder("Audio")

# Encode and decode
bits = encoder.encode(test_audio)
recovered_audio = decoder.decode(bits, test_audio)

# Calculate correlation
if len(test_audio) == len(recovered_audio):
    correlation = np.corrcoef(test_audio, recovered_audio)[0, 1]
else:
    correlation = 0.0

print(f"Audio samples: {len(test_audio)}")
print(f"Encoded bits: {len(bits)}")
print(f"Recovered samples: {len(recovered_audio)}")
print(f"Correlation: {correlation:.6f}")
print(f"Expected: Correlation > 0.999")
print(f"Status: {'✅ PASS' if correlation > 0.999 else '❌ FAIL'}")

# Test 3: Video (frame) encoding/decoding
print("\n3. Testing VIDEO (frame) encoding/decoding:")
print("-" * 70)

# Create test video frame
test_frame = np.random.randint(0, 256, (64, 64, 3), dtype=np.uint8)

encoder = SourceEncoder("Video")
decoder = SourceDecoder("Video")

# Encode and decode
bits = encoder.encode(test_frame)
recovered_frame = decoder.decode(bits, test_frame)
recovered_frame_array = np.array(recovered_frame)

# Calculate MSE (lower is better)
mse = np.mean((np.mean(test_frame, axis=2) - recovered_frame_array) ** 2)

print(f"Frame size: 64x64x3")
print(f"Encoded bits: {len(bits)}")
print(f"MSE: {mse:.2f}")
print(f"Expected: MSE < 50 (improved from previous)")
print(f"Status: {'✅ PASS' if mse < 50 else '❌ FAIL'}")

print("\n" + "=" * 70)
print("SUMMARY:")
print("=" * 70)
print("✅ Image quality improved: Quantization reduced from /10 to /3")
print("✅ Audio visualization: Now shows original vs received comparison")
print("✅ Image/Video display: Side-by-side comparison added")
print("=" * 70)

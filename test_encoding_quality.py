#!/usr/bin/env python3
"""
Comprehensive test to verify encoding/decoding for all source types
Tests input vs output quality under perfect conditions
"""

import numpy as np
from PIL import Image
import sys

from modules.source_encoder import SourceEncoder
from modules.source_decoder import SourceDecoder
from modules.metrics import IntegrityMetrics, InformationMetrics

print("=" * 70)
print("TESTING SOURCE ENCODING/DECODING FOR ALL TYPES")
print("=" * 70)

# Test 1: Text
print("\n1. TEXT ENCODING/DECODING TEST")
print("-" * 70)
text_input = "Hola Mundo 5G - Testing 123"
print(f"Input:  '{text_input}'")

encoder = SourceEncoder("Texto")
encoded_bits = encoder.encode(text_input)
print(f"Encoded: {len(encoded_bits)} bits ({len(text_input)} chars × 8 bits)")

decoder = SourceDecoder("Texto")
decoded_text = decoder.decode(encoded_bits, text_input)
print(f"Output: '{decoded_text}'")

if decoded_text == text_input:
    print("✓ TEXT: Perfect reconstruction")
else:
    print(f"✗ TEXT: Mismatch! Expected '{text_input}' but got '{decoded_text}'")
    print(f"  Match rate: {sum(c1 == c2 for c1, c2 in zip(text_input, decoded_text))}/{len(text_input)}")

# Test 2: Image
print("\n2. IMAGE ENCODING/DECODING TEST")
print("-" * 70)

# Create a simple test pattern image
test_image = np.zeros((64, 64), dtype=np.uint8)
# Add some patterns
test_image[10:20, 10:20] = 255  # White square
test_image[30:40, 30:40] = 128  # Gray square
test_image[20:30, 40:50] = 64   # Dark square

print(f"Input: 64×64 grayscale image with test patterns")
print(f"  Values: min={test_image.min()}, max={test_image.max()}, mean={test_image.mean():.1f}")

# Convert to PIL Image
pil_image = Image.fromarray(test_image)

# Encode
encoder = SourceEncoder("Imagen")
encoded_bits = encoder.encode(pil_image)
print(f"Encoded: {len(encoded_bits)} bits ({len(encoded_bits)//8} bytes)")

# Decode
decoder = SourceDecoder("Imagen")
decoded_image = decoder.decode(encoded_bits, pil_image)

# Convert back to array for comparison
decoded_array = np.array(decoded_image)
print(f"Output: {decoded_array.shape} image")
print(f"  Values: min={decoded_array.min()}, max={decoded_array.max()}, mean={decoded_array.mean():.1f}")

# Calculate metrics
integrity = IntegrityMetrics()
mse = np.mean((test_image.astype(float) - decoded_array.astype(float)) ** 2)
psnr = integrity.calculate_psnr(pil_image, decoded_image)
ssim = integrity.calculate_ssim(pil_image, decoded_image)

print(f"\nImage Quality Metrics:")
print(f"  MSE:  {mse:.2f}")
print(f"  PSNR: {psnr:.2f} dB")
print(f"  SSIM: {ssim:.4f}")

if psnr > 30 and ssim > 0.9:
    print("✓ IMAGE: Good reconstruction quality")
elif psnr > 20:
    print("⚠ IMAGE: Acceptable quality but has degradation")
else:
    print("✗ IMAGE: Poor reconstruction quality")

# Show some sample comparisons
print(f"\nSample pixel comparison (first white square):")
print(f"  Original[15,15]: {test_image[15,15]}")
print(f"  Decoded[15,15]:  {decoded_array[15,15]}")
print(f"  Original[35,35]: {test_image[35,35]}")
print(f"  Decoded[35,35]:  {decoded_array[35,35]}")

# Test 3: Audio
print("\n3. AUDIO ENCODING/DECODING TEST")
print("-" * 70)

# Generate a simple sine wave
sample_rate = 8000
duration = 0.5
t = np.linspace(0, duration, int(sample_rate * duration))
frequency = 440  # A4 note
audio_input = np.sin(2 * np.pi * frequency * t)

print(f"Input: {len(audio_input)} samples, {duration}s at {sample_rate}Hz")
print(f"  Frequency: {frequency}Hz (sine wave)")
print(f"  Values: min={audio_input.min():.3f}, max={audio_input.max():.3f}")

# Encode
encoder = SourceEncoder("Audio")
encoded_bits = encoder.encode(audio_input)
print(f"Encoded: {len(encoded_bits)} bits")

# Decode
decoder = SourceDecoder("Audio")
decoded_audio = decoder.decode(encoded_bits, audio_input)

print(f"Output: {len(decoded_audio)} samples")
print(f"  Values: min={decoded_audio.min():.3f}, max={decoded_audio.max():.3f}")

# Calculate correlation
if len(decoded_audio) == len(audio_input):
    correlation = np.corrcoef(audio_input, decoded_audio)[0, 1]
    mse_audio = np.mean((audio_input - decoded_audio) ** 2)
    print(f"\nAudio Quality Metrics:")
    print(f"  Correlation: {correlation:.4f}")
    print(f"  MSE: {mse_audio:.6f}")
    
    if correlation > 0.95:
        print("✓ AUDIO: High correlation, good reconstruction")
    elif correlation > 0.8:
        print("⚠ AUDIO: Moderate correlation, some degradation")
    else:
        print("✗ AUDIO: Low correlation, poor reconstruction")
else:
    print(f"✗ AUDIO: Length mismatch! {len(audio_input)} vs {len(decoded_audio)}")

# Test 4: Video Frame
print("\n4. VIDEO FRAME ENCODING/DECODING TEST")
print("-" * 70)

# Create a simple video frame (color)
video_frame = np.zeros((64, 64, 3), dtype=np.uint8)
video_frame[10:30, 10:30] = [255, 0, 0]    # Red square
video_frame[30:50, 30:50] = [0, 255, 0]    # Green square
video_frame[15:25, 40:50] = [0, 0, 255]    # Blue rectangle

print(f"Input: 64×64×3 RGB video frame")
print(f"  Values: min={video_frame.min()}, max={video_frame.max()}")

# Encode
encoder = SourceEncoder("Video")
encoded_bits = encoder.encode(video_frame)
print(f"Encoded: {len(encoded_bits)} bits")

# Decode
decoder = SourceDecoder("Video")
decoded_frame = decoder.decode(encoded_bits, video_frame)

# Convert to array
if isinstance(decoded_frame, Image.Image):
    decoded_frame_array = np.array(decoded_frame)
else:
    decoded_frame_array = decoded_frame

print(f"Output: {decoded_frame_array.shape}")
print(f"  Values: min={decoded_frame_array.min()}, max={decoded_frame_array.max()}")

# For video, compare as grayscale (since encoding converts to grayscale)
video_gray = np.mean(video_frame, axis=2).astype(np.uint8)
if len(decoded_frame_array.shape) == 2:
    decoded_gray = decoded_frame_array
else:
    decoded_gray = np.mean(decoded_frame_array, axis=2).astype(np.uint8)

mse_video = np.mean((video_gray.astype(float) - decoded_gray.astype(float)) ** 2)
print(f"\nVideo Quality Metrics (grayscale comparison):")
print(f"  MSE: {mse_video:.2f}")

if mse_video < 100:
    print("✓ VIDEO: Good reconstruction")
elif mse_video < 500:
    print("⚠ VIDEO: Acceptable quality")
else:
    print("✗ VIDEO: Poor reconstruction")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("This test shows the encoding/decoding quality under perfect conditions")
print("(no channel noise, no transmission errors)")
print("\nKey observations:")
print("- Text: Should be perfect (lossless 8-bit ASCII)")
print("- Image: Lossy due to DCT quantization (acceptable quality)")
print("- Audio: Lossy due to MDCT (should have high correlation)")
print("- Video: Lossy (treated as image with DCT)")
print("\nFor the simulator, these are the BEST CASE results.")
print("Actual transmission will add channel noise, causing additional degradation.")


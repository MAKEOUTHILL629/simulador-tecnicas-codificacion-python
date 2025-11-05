"""
Test to diagnose image quality issues
"""

import numpy as np
from PIL import Image
from modules.source_encoder import SourceEncoder
from modules.source_decoder import SourceDecoder
from modules.metrics import IntegrityMetrics

# Create a simple test image with clear features
img = Image.new('L', (64, 64), color=0)
pixels = np.array(img)

# Add patterns: white square, gray square, gradient
pixels[10:30, 10:30] = 255  # White square
pixels[35:55, 35:55] = 128  # Gray square
for i in range(64):
    pixels[i, i] = 200  # Diagonal line

img = Image.fromarray(pixels)
img.save('/tmp/original_test.png')
print("Original image saved")

# Test encoding/decoding
encoder = SourceEncoder('Imagen')
decoder = SourceDecoder('Imagen')

# Encode
bits = encoder.encode(img)
print(f'Encoded: {len(bits)} bits')

# Decode (simulating perfect transmission - no errors)
reconstructed = decoder.decode(bits, img)
reconstructed.save('/tmp/reconstructed_test.png')
print("Reconstructed image saved")

# Calculate metrics
metrics = IntegrityMetrics()
psnr = metrics.calculate_psnr(img, reconstructed)
ssim = metrics.calculate_ssim(img, reconstructed)

print(f'\nMetrics:')
print(f'PSNR: {psnr:.2f} dB')
print(f'SSIM: {ssim:.4f}')

# Analyze pixel differences
orig_array = np.array(img)
recon_array = np.array(reconstructed)
diff = np.abs(orig_array.astype(float) - recon_array.astype(float))

print(f'\nPixel Analysis:')
print(f'Mean error: {diff.mean():.2f}')
print(f'Max error: {diff.max():.2f}')
print(f'Std error: {diff.std():.2f}')

# Show sample of original vs reconstructed
print(f'\nSample comparison (first 8x8 block):')
print('Original:')
print(orig_array[0:8, 0:8])
print('\nReconstructed:')
print(recon_array[0:8, 0:8])

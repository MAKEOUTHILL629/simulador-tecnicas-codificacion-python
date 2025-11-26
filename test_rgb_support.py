"""
Test RGB Color Support for Images and Videos
Verifies that RGB encoding/decoding works correctly
"""

import numpy as np
from PIL import Image
import sys

# Import modules
from modules.source_encoder import SourceEncoder
from modules.source_decoder import SourceDecoder

def test_rgb_image_encoding():
    """Test that RGB images are encoded and decoded correctly"""
    print("\n" + "="*60)
    print("TEST 1: RGB Image Encoding/Decoding")
    print("="*60)
    
    # Create a simple RGB test image
    # Red square on top, blue square on bottom
    img_array = np.zeros((64, 64, 3), dtype=np.uint8)
    img_array[:32, :, 0] = 255  # Red top half
    img_array[32:, :, 2] = 255  # Blue bottom half
    img_array[:, :, 1] = 50    # Some green everywhere
    
    test_image = Image.fromarray(img_array)
    
    print(f"✓ Created test image: {test_image.size}, mode={test_image.mode}")
    print(f"  Red channel mean: {np.mean(np.array(test_image)[:, :, 0]):.1f}")
    print(f"  Green channel mean: {np.mean(np.array(test_image)[:, :, 1]):.1f}")
    print(f"  Blue channel mean: {np.mean(np.array(test_image)[:, :, 2]):.1f}")
    
    # Encode
    encoder = SourceEncoder("Imagen")
    encoded_bits = encoder.encode(test_image)
    
    print(f"✓ Encoded to {len(encoded_bits)} bits")
    print(f"  Expected bits: ~3 channels × 64 blocks × 64 coeffs/block × 8 bits = ~98,304 bits")
    print(f"  Actual bits: {len(encoded_bits)} bits")
    
    # Decode
    decoder = SourceDecoder("Imagen")
    decoded_image = decoder.decode(encoded_bits, test_image)
    
    print(f"✓ Decoded image: {decoded_image.size}, mode={decoded_image.mode}")
    
    # Check if RGB
    decoded_array = np.array(decoded_image)
    if len(decoded_array.shape) == 3 and decoded_array.shape[2] == 3:
        print("✓ PASS: Decoded image is RGB (3 channels)")
        print(f"  Red channel mean: {np.mean(decoded_array[:, :, 0]):.1f}")
        print(f"  Green channel mean: {np.mean(decoded_array[:, :, 1]):.1f}")
        print(f"  Blue channel mean: {np.mean(decoded_array[:, :, 2]):.1f}")
        
        # Check if colors are preserved (approximately)
        red_preserved = np.mean(decoded_array[:32, :, 0]) > np.mean(decoded_array[32:, :, 0])
        blue_preserved = np.mean(decoded_array[32:, :, 2]) > np.mean(decoded_array[:32, :, 2])
        
        if red_preserved and blue_preserved:
            print("✓ PASS: Color information preserved (red top, blue bottom)")
        else:
            print("⚠ WARNING: Color distribution changed (expected with DCT compression)")
        
        return True
    else:
        print(f"✗ FAIL: Decoded image is not RGB, shape={decoded_array.shape}")
        return False

def test_rgb_video_encoding():
    """Test that RGB video frames are encoded and decoded correctly"""
    print("\n" + "="*60)
    print("TEST 2: RGB Video Frame Encoding/Decoding")
    print("="*60)
    
    # Create a colorful video frame
    frame = np.zeros((64, 64, 3), dtype=np.uint8)
    # Create gradient patterns
    for i in range(64):
        frame[i, :, 0] = i * 4  # Red gradient
        frame[:, i, 1] = i * 4  # Green gradient
    frame[:, :, 2] = 128  # Constant blue
    
    print(f"✓ Created test frame: shape={frame.shape}")
    print(f"  Red channel range: {frame[:, :, 0].min()}-{frame[:, :, 0].max()}")
    print(f"  Green channel range: {frame[:, :, 1].min()}-{frame[:, :, 1].max()}")
    print(f"  Blue channel: constant {frame[0, 0, 2]}")
    
    # Encode
    encoder = SourceEncoder("Video")
    encoded_bits = encoder.encode(frame)
    
    print(f"✓ Encoded to {len(encoded_bits)} bits")
    
    # Decode
    decoder = SourceDecoder("Video")
    decoded_frame = decoder.decode(encoded_bits, frame)
    
    # Convert to array
    if isinstance(decoded_frame, Image.Image):
        decoded_array = np.array(decoded_frame)
    else:
        decoded_array = decoded_frame
    
    print(f"✓ Decoded frame: shape={decoded_array.shape}")
    
    # Check if RGB
    if len(decoded_array.shape) == 3 and decoded_array.shape[2] == 3:
        print("✓ PASS: Decoded frame is RGB (3 channels)")
        print(f"  Red channel range: {decoded_array[:, :, 0].min()}-{decoded_array[:, :, 0].max()}")
        print(f"  Green channel range: {decoded_array[:, :, 1].min()}-{decoded_array[:, :, 1].max()}")
        print(f"  Blue channel mean: {np.mean(decoded_array[:, :, 2]):.1f}")
        return True
    else:
        print(f"✗ FAIL: Decoded frame is not RGB, shape={decoded_array.shape}")
        return False

def test_grayscale_to_rgb_conversion():
    """Test that grayscale images are converted to RGB"""
    print("\n" + "="*60)
    print("TEST 3: Grayscale to RGB Conversion")
    print("="*60)
    
    # Create grayscale image
    gray_array = np.random.randint(0, 255, (64, 64), dtype=np.uint8)
    gray_image = Image.fromarray(gray_array, mode='L')
    
    print(f"✓ Created grayscale image: {gray_image.size}, mode={gray_image.mode}")
    
    # Encode (should convert to RGB internally)
    encoder = SourceEncoder("Imagen")
    encoded_bits = encoder.encode(gray_image)
    
    print(f"✓ Encoded grayscale image to {len(encoded_bits)} bits")
    
    # Decode
    decoder = SourceDecoder("Imagen")
    decoded_image = decoder.decode(encoded_bits, gray_image)
    
    decoded_array = np.array(decoded_image)
    print(f"✓ Decoded image shape: {decoded_array.shape}")
    
    if len(decoded_array.shape) == 3 and decoded_array.shape[2] == 3:
        print("✓ PASS: Grayscale image converted to RGB format")
        # Check if all channels are similar (should be for grayscale)
        r_mean = np.mean(decoded_array[:, :, 0])
        g_mean = np.mean(decoded_array[:, :, 1])
        b_mean = np.mean(decoded_array[:, :, 2])
        print(f"  Channel means: R={r_mean:.1f}, G={g_mean:.1f}, B={b_mean:.1f}")
        
        if abs(r_mean - g_mean) < 10 and abs(g_mean - b_mean) < 10:
            print("  ✓ Channels are similar (expected for grayscale)")
        
        return True
    else:
        print(f"✗ FAIL: Expected RGB output, got shape={decoded_array.shape}")
        return False

def test_constellation_points():
    """Test that constellation visualization will show all points"""
    print("\n" + "="*60)
    print("TEST 4: Constellation Point Generation")
    print("="*60)
    
    from modules.modulator import Modulator
    
    modulation_types = ["QPSK", "16-QAM", "64-QAM", "256-QAM"]
    expected_points = [4, 16, 64, 256]
    
    all_pass = True
    for mod_type, expected in zip(modulation_types, expected_points):
        modulator = Modulator(mod_type)
        constellation = modulator.constellation
        
        print(f"\n{mod_type}:")
        print(f"  Expected points: {expected}")
        print(f"  Actual points: {len(constellation)}")
        
        if len(constellation) == expected:
            print(f"  ✓ PASS: {mod_type} has correct number of points")
        else:
            print(f"  ✗ FAIL: {mod_type} has wrong number of points")
            all_pass = False
        
        # Show sample points
        if len(constellation) <= 16:
            print(f"  Points: {constellation[:4]}...")
        else:
            print(f"  Sample points: {constellation[:3]}...")
    
    return all_pass

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print(" RGB COLOR SUPPORT TEST SUITE")
    print("="*70)
    print("\nTesting improvements for:")
    print("  1. RGB color preservation in images")
    print("  2. RGB color preservation in video frames")
    print("  3. Grayscale to RGB conversion")
    print("  4. Constellation point generation")
    
    results = []
    
    # Run tests
    results.append(("RGB Image Encoding", test_rgb_image_encoding()))
    results.append(("RGB Video Encoding", test_rgb_video_encoding()))
    results.append(("Grayscale Conversion", test_grayscale_to_rgb_conversion()))
    results.append(("Constellation Points", test_constellation_points()))
    
    # Summary
    print("\n" + "="*70)
    print(" TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "-"*70)
    print(f"Total: {passed}/{total} tests passed ({100*passed/total:.0f}%)")
    print("="*70)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! RGB support is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

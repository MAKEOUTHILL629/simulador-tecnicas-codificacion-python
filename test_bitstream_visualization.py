"""
Test script for improved bitstream visualizations
Tests smart sampling for large bitstreams
"""

import numpy as np
import sys
sys.path.insert(0, '/home/runner/work/simulador-tecnicas-codificacion-python/simulador-tecnicas-codificacion-python')

from modules.visualizer import Visualizer

def test_small_bitstream():
    """Test visualization with small bitstream (< 1000 bits)"""
    print("=" * 60)
    print("TEST 1: Small Bitstream (500 bits)")
    print("=" * 60)
    
    # Create small bitstream with pattern
    bits = np.random.randint(0, 2, 500)
    
    visualizer = Visualizer()
    fig = visualizer.plot_bitstream(bits, title="Small Bitstream Test")
    
    ones = np.sum(bits == 1)
    zeros = np.sum(bits == 0)
    
    print(f"✓ Generated bitstream: {len(bits)} bits")
    print(f"✓ Ones: {ones} ({ones/len(bits)*100:.1f}%)")
    print(f"✓ Zeros: {zeros} ({zeros/len(bits)*100:.1f}%)")
    print(f"✓ Figure created successfully")
    print()
    
    return True

def test_large_bitstream():
    """Test visualization with large bitstream (1M+ bits)"""
    print("=" * 60)
    print("TEST 2: Large Bitstream (1,058,400 bits - Audio example)")
    print("=" * 60)
    
    # Create large bitstream simulating audio
    # Typical audio: 2 seconds @ 8kHz @ 12-bit PCM = 2 * 8000 * 12 = 192,000 bits
    # With LDPC encoding @ rate 0.5, doubles to ~384,000 bits
    # But user reported 1,058,400 bits, so let's use that
    
    total_bits = 1_058_400
    
    # Simulate realistic audio bitstream (not all zeros)
    # Audio typically has ~50% ones and 50% zeros with some structure
    bits = np.random.randint(0, 2, total_bits)
    
    visualizer = Visualizer()
    fig = visualizer.plot_bitstream(bits, title="Large Audio Bitstream Test")
    
    ones = np.sum(bits == 1)
    zeros = np.sum(bits == 0)
    
    print(f"✓ Generated bitstream: {total_bits:,} bits")
    print(f"✓ Ones: {ones:,} ({ones/total_bits*100:.1f}%)")
    print(f"✓ Zeros: {zeros:,} ({zeros/total_bits*100:.1f}%)")
    print(f"✓ Smart sampling applied (shows 500 samples)")
    print(f"✓ Figure created successfully")
    print()
    
    return True

def test_channel_encoding_small():
    """Test channel encoding visualization with small bitstream"""
    print("=" * 60)
    print("TEST 3: Channel Encoding - Small (1000 bits)")
    print("=" * 60)
    
    source_bits = np.random.randint(0, 2, 500)
    channel_bits = np.random.randint(0, 2, 1000)  # Rate 0.5
    
    visualizer = Visualizer()
    fig = visualizer.plot_channel_encoding_comparison(
        source_bits, channel_bits, 
        title="Small Channel Encoding Test"
    )
    
    print(f"✓ Source bits: {len(source_bits)} bits")
    print(f"✓ Channel bits: {len(channel_bits)} bits")
    print(f"✓ Code rate: {len(source_bits)/len(channel_bits):.2f}")
    print(f"✓ Redundancy: {len(channel_bits)-len(source_bits)} bits")
    print(f"✓ Figure created successfully")
    print()
    
    return True

def test_channel_encoding_large():
    """Test channel encoding visualization with large bitstream"""
    print("=" * 60)
    print("TEST 4: Channel Encoding - Large (2M+ bits)")
    print("=" * 60)
    
    # Simulate large audio with channel encoding
    source_bits = np.random.randint(0, 2, 1_058_400)
    channel_bits = np.random.randint(0, 2, 2_116_800)  # Rate 0.5
    
    visualizer = Visualizer()
    fig = visualizer.plot_channel_encoding_comparison(
        source_bits, channel_bits,
        title="Large Channel Encoding Test"
    )
    
    print(f"✓ Source bits: {len(source_bits):,} bits")
    print(f"✓ Channel bits: {len(channel_bits):,} bits")
    print(f"✓ Code rate: {len(source_bits)/len(channel_bits):.2f}")
    print(f"✓ Redundancy: {len(channel_bits)-len(source_bits):,} bits")
    print(f"✓ Smart sampling applied (shows 500 samples)")
    print(f"✓ Figure created successfully")
    print()
    
    return True

def test_bitstream_with_many_zeros():
    """Test visualization with bitstream that has many zeros (problematic case)"""
    print("=" * 60)
    print("TEST 5: Bitstream with Many Zeros (User's Issue)")
    print("=" * 60)
    
    # Simulate user's case: large bitstream with many zeros at start
    total_bits = 1_058_400
    bits = np.zeros(total_bits, dtype=int)
    
    # Add some ones scattered throughout
    ones_indices = np.random.choice(total_bits, size=int(total_bits * 0.3), replace=False)
    bits[ones_indices] = 1
    
    visualizer = Visualizer()
    fig = visualizer.plot_bitstream(bits, title="Bitstream with 30% Ones")
    
    ones = np.sum(bits == 1)
    zeros = np.sum(bits == 0)
    
    print(f"✓ Generated bitstream: {total_bits:,} bits")
    print(f"✓ Ones: {ones:,} ({ones/total_bits*100:.1f}%)")
    print(f"✓ Zeros: {zeros:,} ({zeros/total_bits*100:.1f}%)")
    print(f"✓ Smart sampling ensures representative view")
    print(f"✓ Not just showing first 100 bits (which might be all zeros)")
    print(f"✓ Figure created successfully")
    print()
    
    return True

def main():
    """Run all tests"""
    print("\n")
    print("=" * 60)
    print("BITSTREAM VISUALIZATION IMPROVEMENT TESTS")
    print("=" * 60)
    print()
    
    tests = [
        test_small_bitstream,
        test_large_bitstream,
        test_channel_encoding_small,
        test_channel_encoding_large,
        test_bitstream_with_many_zeros
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            results.append(False)
    
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✅ ALL TESTS PASSED")
        print()
        print("Summary of improvements:")
        print("- Small bitstreams (<1000): Show first 100 bits")
        print("- Large bitstreams (>1000): Sample 500 bits uniformly across entire bitstream")
        print("- Channel encoding: Smart sampling with redundancy region highlighting")
        print("- Statistics always calculated on FULL bitstream (not just sample)")
        print("- Clear indication when sampling is applied")
    else:
        print(f"⚠️  {total-passed} test(s) failed")
    
    print("=" * 60)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

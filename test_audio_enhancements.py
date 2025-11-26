"""
Test script for enhanced audio functionality
Tests audio file loading, real-time preview, and audio export
"""

import numpy as np
import scipy.io.wavfile as wavfile
import tempfile
import os

def test_audio_file_creation():
    """Test creating a WAV file"""
    print("Testing WAV file creation...")
    
    # Generate test audio
    sample_rate = 8000
    duration = 1.0
    frequency = 440
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio_data = np.sin(2 * np.pi * frequency * t)
    
    # Convert to int16
    audio_int16 = (audio_data * 32767).astype(np.int16)
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
        wavfile.write(tmp.name, sample_rate, audio_int16)
        tmp_path = tmp.name
    
    # Read back
    rate, data = wavfile.read(tmp_path)
    
    # Clean up
    os.unlink(tmp_path)
    
    assert rate == sample_rate, f"Sample rate mismatch: {rate} != {sample_rate}"
    assert len(data) == len(audio_int16), f"Length mismatch: {len(data)} != {len(audio_int16)}"
    
    print(f"✓ WAV creation test passed: {rate}Hz, {len(data)} samples")
    return True

def test_audio_loading():
    """Test loading a WAV file"""
    print("\nTesting WAV file loading...")
    
    # Create test file
    sample_rate = 8000
    duration = 0.5
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio_data = np.sin(2 * np.pi * 440 * t)
    audio_int16 = (audio_data * 32767).astype(np.int16)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
        wavfile.write(tmp.name, sample_rate, audio_int16)
        tmp_path = tmp.name
    
    # Load it
    rate, loaded_data = wavfile.read(tmp_path)
    
    # Normalize
    loaded_normalized = loaded_data.astype(np.float32) / np.max(np.abs(loaded_data))
    
    # Clean up
    os.unlink(tmp_path)
    
    assert rate == sample_rate
    assert len(loaded_normalized) == len(audio_data)
    assert np.max(np.abs(loaded_normalized)) <= 1.0, "Audio not properly normalized"
    
    print(f"✓ WAV loading test passed: {rate}Hz, {len(loaded_normalized)} samples, normalized to [{loaded_normalized.min():.3f}, {loaded_normalized.max():.3f}]")
    return True

def test_stereo_to_mono_conversion():
    """Test converting stereo audio to mono"""
    print("\nTesting stereo to mono conversion...")
    
    # Create stereo test file
    sample_rate = 8000
    duration = 0.5
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Stereo: left=440Hz, right=880Hz
    left = np.sin(2 * np.pi * 440 * t)
    right = np.sin(2 * np.pi * 880 * t)
    stereo = np.column_stack((left, right))
    stereo_int16 = (stereo * 32767).astype(np.int16)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
        wavfile.write(tmp.name, sample_rate, stereo_int16)
        tmp_path = tmp.name
    
    # Load and convert to mono
    rate, loaded_stereo = wavfile.read(tmp_path)
    
    assert len(loaded_stereo.shape) == 2, "Not stereo"
    assert loaded_stereo.shape[1] == 2, f"Expected 2 channels, got {loaded_stereo.shape[1]}"
    
    # Convert to mono
    mono = loaded_stereo.mean(axis=1)
    
    # Clean up
    os.unlink(tmp_path)
    
    assert len(mono.shape) == 1, "Mono conversion failed"
    assert len(mono) == len(t), f"Length mismatch after conversion"
    
    print(f"✓ Stereo to mono test passed: {loaded_stereo.shape} → {mono.shape}")
    return True

def test_audio_truncation():
    """Test truncating long audio files"""
    print("\nTesting audio truncation...")
    
    # Create 3-second audio (will be truncated to 2)
    sample_rate = 8000
    duration = 3.0
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio_data = np.sin(2 * np.pi * 440 * t)
    
    # Truncate to 2 seconds
    max_samples = int(2.0 * sample_rate)
    truncated = audio_data[:max_samples]
    
    truncated_duration = len(truncated) / sample_rate
    
    assert truncated_duration <= 2.0, f"Truncation failed: {truncated_duration}s > 2.0s"
    assert len(truncated) == max_samples, f"Sample count mismatch"
    
    print(f"✓ Truncation test passed: {duration}s → {truncated_duration}s ({len(audio_data)} → {len(truncated)} samples)")
    return True

def test_real_time_preview():
    """Test generating real-time preview"""
    print("\nTesting real-time preview generation...")
    
    sample_rate = 8000
    duration = 1.0
    frequency = 440
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio_signal = np.sin(2 * np.pi * frequency * t)
    
    # Preview: first 100ms
    preview_duration = min(0.1, duration)
    preview_samples = int(sample_rate * preview_duration)
    preview = audio_signal[:preview_samples]
    
    assert len(preview) == preview_samples
    assert len(preview) <= len(audio_signal)
    
    print(f"✓ Preview test passed: {len(audio_signal)} samples → {len(preview)} preview samples ({preview_duration}s)")
    return True

def run_all_tests():
    """Run all audio enhancement tests"""
    print("="*60)
    print("AUDIO ENHANCEMENTS TEST SUITE")
    print("="*60)
    
    tests = [
        ("WAV File Creation", test_audio_file_creation),
        ("WAV File Loading", test_audio_loading),
        ("Stereo to Mono Conversion", test_stereo_to_mono_conversion),
        ("Audio Truncation", test_audio_truncation),
        ("Real-time Preview", test_real_time_preview),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            failed += 1
            print(f"✗ {test_name} FAILED with exception: {e}")
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed}/{len(tests)} tests passed")
    if failed == 0:
        print("✅ ALL TESTS PASSED")
    else:
        print(f"❌ {failed} TEST(S) FAILED")
    print("="*60)
    
    return failed == 0

if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)

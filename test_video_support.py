"""
Test script to verify video file support
"""

import numpy as np
import cv2
import tempfile
import os
from PIL import Image

def test_opencv_installation():
    """Test if OpenCV is properly installed"""
    print("=" * 60)
    print("TEST 1: OpenCV Installation")
    print("=" * 60)
    try:
        print(f"✓ OpenCV version: {cv2.__version__}")
        return True
    except Exception as e:
        print(f"✗ OpenCV not installed: {e}")
        return False

def test_video_creation():
    """Test creating a simple video file"""
    print("\n" + "=" * 60)
    print("TEST 2: Video Creation")
    print("=" * 60)
    
    try:
        # Create a temporary video file
        tmp_path = tempfile.mktemp(suffix='.mp4')
        
        # Video properties
        width, height = 640, 480
        fps = 30
        num_frames = 90  # 3 seconds
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(tmp_path, fourcc, fps, (width, height))
        
        print(f"Creating test video: {width}x{height}, {fps} FPS, {num_frames} frames")
        
        # Generate frames with different colors
        for i in range(num_frames):
            # Create a frame with gradient
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            color_val = int(255 * i / num_frames)
            frame[:, :] = [color_val, 128, 255 - color_val]
            
            # Add frame number text
            cv2.putText(frame, f"Frame {i}", (50, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            out.write(frame)
        
        out.release()
        
        # Verify the file exists
        if os.path.exists(tmp_path):
            file_size = os.path.getsize(tmp_path) / 1024  # KB
            print(f"✓ Video created successfully: {file_size:.2f} KB")
            
            # Try to read it back
            cap = cv2.VideoCapture(tmp_path)
            if cap.isOpened():
                total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                print(f"✓ Video readable: {total} frames")
                cap.release()
                
                # Clean up
                os.remove(tmp_path)
                return True
            else:
                print("✗ Could not open created video")
                os.remove(tmp_path)
                return False
        else:
            print("✗ Video file not created")
            return False
            
    except Exception as e:
        print(f"✗ Error creating video: {e}")
        return False

def test_frame_extraction():
    """Test extracting frames from video"""
    print("\n" + "=" * 60)
    print("TEST 3: Frame Extraction")
    print("=" * 60)
    
    try:
        # Create a small test video
        tmp_path = tempfile.mktemp(suffix='.avi')
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(tmp_path, fourcc, 10, (320, 240))
        
        # Write 30 frames
        for i in range(30):
            frame = np.random.randint(0, 256, (240, 320, 3), dtype=np.uint8)
            out.write(frame)
        out.release()
        
        # Extract specific frames
        cap = cv2.VideoCapture(tmp_path)
        frames_to_extract = [0, 15, 29]
        extracted_frames = []
        
        for frame_num in frames_to_extract:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = cap.read()
            if ret:
                extracted_frames.append(frame)
                print(f"✓ Extracted frame {frame_num}: shape {frame.shape}")
            else:
                print(f"✗ Failed to extract frame {frame_num}")
        
        cap.release()
        os.remove(tmp_path)
        
        if len(extracted_frames) == len(frames_to_extract):
            print(f"✓ Successfully extracted all {len(extracted_frames)} frames")
            return True
        else:
            print(f"✗ Only extracted {len(extracted_frames)}/{len(frames_to_extract)} frames")
            return False
            
    except Exception as e:
        print(f"✗ Error extracting frames: {e}")
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        return False

def test_video_formats():
    """Test different video formats"""
    print("\n" + "=" * 60)
    print("TEST 4: Video Format Support")
    print("=" * 60)
    
    formats = [
        ('.mp4', 'mp4v'),
        ('.avi', 'XVID'),
    ]
    
    results = []
    for ext, codec in formats:
        try:
            tmp_path = tempfile.mktemp(suffix=ext)
            fourcc = cv2.VideoWriter_fourcc(*codec)
            out = cv2.VideoWriter(tmp_path, fourcc, 10, (160, 120))
            
            # Write a few frames
            for i in range(10):
                frame = np.zeros((120, 160, 3), dtype=np.uint8)
                out.write(frame)
            out.release()
            
            # Try to read
            cap = cv2.VideoCapture(tmp_path)
            readable = cap.isOpened()
            cap.release()
            
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            
            if readable:
                print(f"✓ {ext} format supported")
                results.append(True)
            else:
                print(f"✗ {ext} format not readable")
                results.append(False)
                
        except Exception as e:
            print(f"✗ {ext} format error: {e}")
            results.append(False)
    
    return all(results)

def test_integration_with_encoder():
    """Test video frame processing with encoder"""
    print("\n" + "=" * 60)
    print("TEST 5: Integration with Encoder")
    print("=" * 60)
    
    try:
        from modules.source_encoder import SourceEncoder
        from modules.source_decoder import SourceDecoder
        
        # Create a test frame
        frame = np.random.randint(0, 256, (64, 64, 3), dtype=np.uint8)
        print(f"Input frame shape: {frame.shape}")
        
        # Encode
        encoder = SourceEncoder("Video")
        encoded = encoder.encode(frame)
        print(f"✓ Encoded to {len(encoded)} bits")
        
        # Decode
        decoder = SourceDecoder("Video")
        decoded = decoder.decode(encoded, frame)
        print(f"✓ Decoded to {type(decoded)}")
        
        if isinstance(decoded, (np.ndarray, Image.Image)):
            print(f"✓ Output is valid image type")
            return True
        else:
            print(f"✗ Output is not a valid image")
            return False
            
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("VIDEO SUPPORT TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("OpenCV Installation", test_opencv_installation),
        ("Video Creation", test_video_creation),
        ("Frame Extraction", test_frame_extraction),
        ("Video Formats", test_video_formats),
        ("Encoder Integration", test_integration_with_encoder),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Test '{name}' crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ TODAS LAS PRUEBAS DE VIDEO PASARON")
        return True
    else:
        print(f"\n⚠️ {total - passed} pruebas fallaron")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

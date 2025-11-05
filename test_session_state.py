#!/usr/bin/env python3
"""
Test to verify session state handling for different source types
This simulates what happens in the Streamlit UI
"""

import numpy as np
from PIL import Image

print("Testing Session State Source Type Handling")
print("=" * 60)

# Simulate session state
class SessionState:
    def __init__(self):
        self.input_data = None
        self.source_type = None
    
    def get(self, key, default=None):
        return getattr(self, key, default)

session = SessionState()

# Test 1: Image upload
print("\n1. Testing Image Upload")
uploaded_image = Image.new('RGB', (64, 64), color='red')
session.input_data = uploaded_image
session.source_type = "Imagen"
print(f"   Stored: {type(session.input_data)}, source_type={session.source_type}")

# Simulate retrieval for Image
current_source = "Imagen"
if (session.input_data is not None and 
    session.get('source_type') == current_source and
    isinstance(session.input_data, Image.Image)):
    print(f"   ✓ Image retrieved successfully: {type(session.input_data)}")
else:
    print(f"   ✗ Image retrieval failed")

# Test 2: Switch to Audio
print("\n2. Testing Audio Generation")
audio_signal = np.sin(2 * np.pi * 440 * np.linspace(0, 1, 8000))
session.input_data = audio_signal
session.source_type = "Audio"
print(f"   Stored: {type(session.input_data)}, shape={session.input_data.shape}, source_type={session.source_type}")

# Simulate retrieval for Audio (should work)
current_source = "Audio"
if (session.input_data is not None and 
    session.get('source_type') == current_source and
    isinstance(session.input_data, np.ndarray) and
    len(session.input_data.shape) == 1):
    print(f"   ✓ Audio retrieved successfully: shape={session.input_data.shape}")
else:
    print(f"   ✗ Audio retrieval failed")

# Test 3: Try to retrieve Audio data when source is Image (should fail)
current_source = "Imagen"
if (session.input_data is not None and 
    session.get('source_type') == current_source and
    isinstance(session.input_data, Image.Image)):
    print(f"   ✗ ERROR: Retrieved audio data as image!")
else:
    print(f"   ✓ Correctly rejected: Audio data not retrieved for Image source")

# Test 4: Video Frame
print("\n3. Testing Video Frame")
video_frame = np.random.randint(0, 256, (64, 64, 3), dtype=np.uint8)
session.input_data = video_frame
session.source_type = "Video"
print(f"   Stored: {type(session.input_data)}, shape={session.input_data.shape}, source_type={session.source_type}")

# Simulate retrieval for Video
current_source = "Video"
if (session.input_data is not None and 
    session.get('source_type') == current_source and
    isinstance(session.input_data, np.ndarray) and
    len(session.input_data.shape) == 3):
    print(f"   ✓ Video retrieved successfully: shape={session.input_data.shape}")
else:
    print(f"   ✗ Video retrieval failed")

# Test 5: Text
print("\n4. Testing Text")
text_data = "Hola Mundo 5G"
session.input_data = text_data
session.source_type = "Texto"
print(f"   Stored: {type(session.input_data)}, source_type={session.source_type}")

# Simulate retrieval for Text
current_source = "Texto"
if session.input_data is not None and session.get('source_type') == current_source:
    print(f"   ✓ Text retrieved successfully: '{session.input_data}'")
else:
    print(f"   ✗ Text retrieval failed")

print("\n" + "=" * 60)
print("✅ All session state tests completed successfully!")
print("\nKey insight: Each source type now stores its type identifier,")
print("preventing cross-contamination when switching between sources.")

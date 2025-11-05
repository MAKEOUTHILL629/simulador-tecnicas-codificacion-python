#!/usr/bin/env python3
"""
Script simple para probar los módulos del simulador sin dependencias externas
"""

import sys
import os

# Add modules directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_module_imports():
    """Test that all modules can be imported"""
    print("Testing module imports...")
    
    try:
        from modules import source_encoder
        print("✓ source_encoder module OK")
    except ImportError as e:
        print(f"✗ source_encoder failed: {e}")
    
    try:
        from modules import channel_encoder
        print("✓ channel_encoder module OK")
    except ImportError as e:
        print(f"✗ channel_encoder failed: {e}")
    
    try:
        from modules import modulator
        print("✓ modulator module OK")
    except ImportError as e:
        print(f"✗ modulator failed: {e}")
    
    try:
        from modules import channel
        print("✓ channel module OK")
    except ImportError as e:
        print(f"✗ channel failed: {e}")
    
    try:
        from modules import demodulator
        print("✓ demodulator module OK")
    except ImportError as e:
        print(f"✗ demodulator failed: {e}")
    
    try:
        from modules import channel_decoder
        print("✓ channel_decoder module OK")
    except ImportError as e:
        print(f"✗ channel_decoder failed: {e}")
    
    try:
        from modules import source_decoder
        print("✓ source_decoder module OK")
    except ImportError as e:
        print(f"✗ source_decoder failed: {e}")
    
    try:
        from modules import metrics
        print("✓ metrics module OK")
    except ImportError as e:
        print(f"✗ metrics failed: {e}")
    
    try:
        from modules import visualizer
        print("✓ visualizer module OK")
    except ImportError as e:
        print(f"✗ visualizer failed: {e}")

if __name__ == "__main__":
    test_module_imports()
    print("\nNota: Para ejecutar el simulador completo, instale las dependencias:")
    print("  pip install -r requirements.txt")
    print("  streamlit run simulador.py")

# 🚀 Quick Start - Simulador 5G/6G

## Installation (2 minutes)

```bash
# 1. Clone
git clone https://github.com/MAKEOUTHILL629/simulador-tecnicas-codificacion-python.git
cd simulador-tecnicas-codificacion-python

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run simulador.py
```

## First Simulation (30 seconds)

1. Open `http://localhost:8501` in browser
2. Leave default settings:
   - Red: **5G**
   - Fuente: **Texto**
   - Modulación: **QPSK**
   - SNR: **10 dB**
3. Type "Hello World" in text box
4. Click **🚀 Iniciar Simulación**
5. Watch the 7 stages process!

## What You'll See

### 7 Stages Visualized

1. **Codificación de Fuente** → Bitstream graph
2. **Codificación de Canal** → LDPC redundancy added
3. **Modulación** → I/Q constellation diagram
4. **Canal** → Noisy constellation
5. **Demodulación** → LLR histogram
6. **Decodificación de Canal** → Recovered bits
7. **Salida** → Reconstructed output + metrics

### Metrics Displayed

- **H(X)**: Entropy of input (~3-5 bits for text)
- **I(X;Y)**: Mutual information (should be close to H(X))
- **BER**: Bit Error Rate (lower is better)
- **Tasa de Bits Correctos**: Percentage correct (higher is better)

## Quick Experiments

### Experiment 1: Effect of Noise
```
Config: 5G, Texto, QPSK
Try: SNR = 20dB, 10dB, 0dB
Observe: BER increases as SNR decreases
```

### Experiment 2: Modulation Comparison
```
Config: 5G, Texto, SNR=15dB
Try: QPSK → 16-QAM → 64-QAM → 256-QAM
Observe: Higher order = more errors at same SNR
```

### Experiment 3: Image Transmission
```
Config: 5G, Imagen, 16-QAM, SNR=20dB
Upload: Small image (< 200KB)
Observe: PSNR and SSIM quality metrics
```

## Recommended Settings by Use Case

### For Class Demo (Always Works)
```
Red: 5G
Fuente: Texto (< 50 chars)
Modulación: QPSK
SNR: 15 dB
Canal: AWGN
```

### To Show Degradation
```
Red: 5G
Fuente: Imagen
Modulación: 64-QAM
SNR: 5 dB
Canal: Rayleigh
```

### For Best Quality
```
Red: 5G
Fuente: Any
Modulación: QPSK
SNR: 25 dB
Canal: AWGN
Tasa: 0.3
```

## Common Issues

**Slow performance?**
- Use smaller inputs (< 50 chars for text, < 128x128 for images)

**Gibberish output?**
- Increase SNR (try 15-20 dB)
- Use QPSK instead of higher QAM

**Module not found?**
- Run: `pip install -r requirements.txt --upgrade`

## Understanding the Results

### Good Transmission
- BER < 0.01 (1% errors)
- I(X;Y) ≈ H(X)
- Text readable
- PSNR > 30 dB (images)

### Poor Transmission
- BER > 0.1 (10% errors)
- I(X;Y) << H(X)
- Text garbled
- PSNR < 20 dB (images)

## Key Concepts Demonstrated

1. **Information Theory**
   - Entropy measures information content
   - Mutual information measures successful transfer

2. **Source Coding**
   - Huffman removes redundancy (text)
   - DCT/MDCT for multimedia (images/audio)

3. **Channel Coding**
   - LDPC adds redundancy for error protection
   - Trade-off: overhead vs robustness

4. **Modulation**
   - QPSK: Robust, low capacity
   - 256-QAM: Fragile, high capacity

5. **Wireless Channel**
   - Noise corrupts signal
   - Fading makes it worse
   - SNR is critical

## Documentation

- **USER_GUIDE.md**: Complete user manual (11 KB)
- **TECHNICAL_DOCUMENTATION.md**: How it works (12 KB)
- **TEST_CASES.md**: 20+ test scenarios (11 KB)
- **IMPLEMENTATION_SUMMARY.md**: Feature overview (14 KB)

## Command Cheat Sheet

```bash
# Install
pip install -r requirements.txt

# Run simulator
streamlit run simulador.py

# Test modules (no GUI)
python test_modules.py

# Clear cache if issues
streamlit cache clear

# Update dependencies
pip install -r requirements.txt --upgrade
```

## Support

- 📖 Read USER_GUIDE.md for detailed help
- 🧪 Check TEST_CASES.md for examples
- 🔧 See TECHNICAL_DOCUMENTATION.md for theory

---

**Ready in 2 minutes. First simulation in 30 seconds.** 🎉

# Audio Enhancements - Complete Guide

## Overview

The simulator now includes enhanced audio capabilities for a more intuitive and complete audio simulation experience.

## New Features

### 1. Audio File Upload 🎵

**What's New**: You can now upload real audio files instead of only using synthetic signals.

**Supported Formats**:
- WAV (`.wav`) - Recommended

**File Size Recommendations**:
- Maximum duration: **2 seconds** (automatically truncated)
- Sample rate: Any (will be used as-is)
- Channels: Mono or Stereo (stereo automatically converted to mono)

**How to Use**:
1. Select "Audio" as source type
2. Choose "Cargar archivo de audio"
3. Click "Browse files" and select your WAV file
4. The waveform will be displayed automatically
5. Audio info shows duration, sample rate, and sample count
6. Click "🚀 Iniciar Simulación" to process

**Technical Details**:
- Stereo files are converted to mono by averaging channels
- Audio is normalized to [-1, 1] range
- Files longer than 2 seconds are truncated with a warning
- Sample rate is preserved for accurate reconstruction

### 2. Real-Time Waveform Preview ⚡

**What's New**: When generating synthetic audio, you can see the waveform in real-time as you adjust parameters.

**How It Works**:
- Waveform updates automatically when you move the sliders
- Shows first 100ms of the signal for clarity
- No need to click "Generate" to see the shape
- Helps you understand the effect of frequency and duration

**Interactive Parameters**:
- **Duration**: 0.1 to 2.0 seconds
- **Frequency**: 100 to 2000 Hz

**Preview Display**:
- X-axis: Time in seconds
- Y-axis: Amplitude (-1 to 1)
- Title shows frequency and preview duration
- Grid for easy reading

### 3. Audio Download Capability 💾

**What's New**: After simulation, you can download the received audio as a WAV file.

**Features**:
- One-click download button
- File name includes SNR for easy identification
- Format: WAV (universal compatibility)
- Sample rate: Same as input
- Quality: 16-bit PCM (standard quality)

**File Naming**:
```
audio_recibido_<SNR>dB.wav
```
Examples:
- `audio_recibido_10dB.wav`
- `audio_recibido_-5dB.wav`
- `audio_recibido_20dB.wav`

**Use Cases**:
- Compare audio quality at different SNR levels
- Share results with others
- Use in presentations or reports
- Further analysis in audio software

## User Workflow

### Workflow 1: Upload Audio File

```
1. Select "Audio" as source type
2. Choose "Cargar archivo de audio"
3. Upload WAV file
   ↓
4. View automatic waveform display
5. Check audio info (duration, sample rate, samples)
6. Configure channel parameters (SNR, modulation, etc.)
7. Click "🚀 Iniciar Simulación"
   ↓
8. View original vs received waveforms
9. See correlation metric
10. Download received audio with button
```

### Workflow 2: Generate Synthetic Audio

```
1. Select "Audio" as source type
2. Choose "Generar señal sintética"
3. Adjust duration slider → See preview update
4. Adjust frequency slider → See preview update
   ↓
5. Review real-time waveform preview
6. Click "🎵 Generar y Usar este Audio"
7. Configure channel parameters
8. Click "🚀 Iniciar Simulación"
   ↓
9. View original vs received waveforms
10. Download received audio
```

## Technical Specifications

### Audio Processing Pipeline

```
Input Audio
  ↓
Normalize to [-1, 1]
  ↓
Truncate if > 2 seconds
  ↓
Convert stereo → mono (if needed)
  ↓
Source Encoding (12-bit PCM)
  ↓
Channel Encoding (LDPC)
  ↓
Modulation (QPSK/QAM)
  ↓
Wireless Channel (AWGN/Rayleigh/Rician)
  ↓
Demodulation
  ↓
Channel Decoding
  ↓
Source Decoding
  ↓
Output Audio (normalized)
  ↓
Export as WAV (16-bit PCM)
```

### File Format Details

**Input WAV Requirements**:
- Format: WAVE PCM
- Bit depth: Any (8, 16, 24, 32-bit)
- Channels: 1 (mono) or 2 (stereo)
- Sample rate: Any (preserved in processing)
- Duration: Max 2 seconds (truncated automatically)

**Output WAV Specifications**:
- Format: WAVE PCM
- Bit depth: 16-bit signed integer
- Channels: 1 (mono)
- Sample rate: Same as input
- Normalization: [-32768, 32767] range

### Memory Considerations

**File Size Estimates**:
- 1 second @ 8000 Hz = 16 KB (output WAV)
- 1 second @ 44100 Hz = 88 KB (output WAV)
- 2 seconds @ 8000 Hz = 32 KB (output WAV)
- 2 seconds @ 44100 Hz = 176 KB (output WAV)

**Recommendations**:
- Use 8000 Hz for fastest processing
- Use 16000-22050 Hz for better quality
- Use 44100 Hz only if high fidelity needed
- Keep duration ≤ 1 second for quick demos

## Quality Metrics

### Correlation

The correlation metric shows how similar the received audio is to the original:

- **1.0000**: Perfect match (lossless)
- **0.9999**: Excellent (12-bit PCM, no channel errors)
- **0.99**: Very good (minimal channel errors)
- **0.95**: Good (some degradation)
- **0.90**: Fair (noticeable degradation)
- **< 0.85**: Poor (significant distortion)

### What Affects Quality

1. **Source Encoding**: 12-bit PCM introduces quantization (minimal)
2. **Channel Errors**: BER > 0.001 causes audible degradation
3. **SNR**: Low SNR (<5 dB) significantly impacts quality
4. **Fading**: Rayleigh fading adds variance
5. **Modulation**: Higher-order QAM more susceptible to noise

### Expected Results

| Condition | BER | Correlation | Quality |
|-----------|-----|-------------|---------|
| Perfect (SNR 30 dB, AWGN) | 0.000000 | 1.0000 | Lossless |
| Excellent (SNR 20 dB, AWGN) | 0.000000 | 1.0000 | Lossless |
| Good (SNR 10 dB, AWGN, QPSK) | 0.000010 | 0.9999 | Excellent |
| Fair (SNR 5 dB, AWGN, QPSK) | 0.001000 | 0.995 | Good |
| Poor (SNR 0 dB, Rayleigh) | 0.010000 | 0.90 | Degraded |

## Troubleshooting

### Problem: "Error al cargar audio"

**Possible Causes**:
- File is not a valid WAV
- File is corrupted
- File is MP3 (not yet supported)

**Solutions**:
- Verify file is WAV format
- Convert MP3 → WAV using audio software
- Try a different file

### Problem: "Audio recortado a 2 segundos"

**Explanation**: This is intentional to keep simulation time reasonable.

**Solutions**:
- Edit audio file to be ≤ 2 seconds
- Choose a shorter portion of the original
- This is by design for educational purposes

### Problem: Preview doesn't update

**Possible Causes**:
- Browser issue
- Streamlit caching

**Solutions**:
- Move slider slightly
- Refresh page (Ctrl+R)
- Clear browser cache

### Problem: Download button doesn't appear

**Possible Causes**:
- Simulation not completed
- Audio output not generated
- Browser blocked download

**Solutions**:
- Ensure simulation completed successfully
- Check for error messages above
- Check browser download settings

## Best Practices

### For Educational Demonstrations

1. **Start Simple**: Use synthetic 440 Hz tone first
2. **Vary One Parameter**: Change only SNR or frequency at a time
3. **Compare Results**: Download audio at different SNR levels
4. **Show Degradation**: Demo with SNR 20 dB → 10 dB → 0 dB
5. **Explain Metrics**: Use correlation to quantify quality

### For Testing

1. **Use Short Audio**: 0.5-1.0 seconds is sufficient
2. **Test Extremes**: Try SNR -5 dB and 30 dB
3. **Verify Correlation**: Should be ~1.0 for high SNR
4. **Check Waveforms**: Visual comparison is valuable
5. **Download & Listen**: Audible quality assessment

### For Presentations

1. **Pre-generate Samples**: Create examples before class
2. **Use Descriptive Names**: `audio_440Hz_10dB.wav`
3. **Show Real-Time**: Live parameter adjustment is engaging
4. **Play Audio**: Let students hear the effect of channel
5. **Save Results**: Keep downloads for future reference

## Examples

### Example 1: Compare SNR Levels

```
1. Generate 440 Hz, 1 second audio
2. SNR = 20 dB → Simulate → Download as "high_snr.wav"
3. SNR = 10 dB → Simulate → Download as "medium_snr.wav"
4. SNR = 0 dB → Simulate → Download as "low_snr.wav"
5. Play all three to hear degradation
```

### Example 2: Test Modulation Schemes

```
1. Upload speech sample (< 2 sec)
2. QPSK, SNR 10 dB → Download → Check correlation
3. 16-QAM, SNR 10 dB → Download → Compare
4. 64-QAM, SNR 10 dB → Download → Note degradation
5. Observe: Higher QAM needs higher SNR
```

### Example 3: Fading Effects

```
1. Generate 1 kHz, 1 second tone
2. AWGN, SNR 15 dB → Download → Smooth degradation
3. Rayleigh, SNR 15 dB → Download → Bursty errors
4. Rician K=10, SNR 15 dB → Download → Between both
5. Listen to differences in error patterns
```

## Educational Value

### Learning Objectives

Students will understand:
1. **Source Encoding**: How PCM quantization affects quality
2. **Channel Effects**: Impact of noise on audio signals
3. **Modulation Trade-offs**: QAM orders vs robustness
4. **Fading Models**: AWGN vs Rayleigh vs Rician
5. **System Design**: SNR requirements for target quality

### Demonstration Ideas

1. **BER vs Audio Quality**: Correlate BER with perceived quality
2. **Modulation Comparison**: Same SNR, different modulations
3. **Coding Gain**: Show effect of code rate on quality
4. **Real-world Scenarios**: Simulate phone call, music streaming
5. **Error Correction**: Demonstrate LDPC effectiveness

## Technical Notes

### Implementation Details

- Uses `scipy.io.wavfile` for WAV I/O
- Real-time preview uses matplotlib for plotting
- Audio normalization prevents clipping
- Download uses Streamlit's native download button
- Session state preserves audio across reruns

### Performance

- File upload: <1 second for 2-second audio
- Preview generation: Instantaneous
- Simulation: 2-5 seconds depending on parameters
- Download preparation: <0.5 seconds

### Compatibility

- **Browsers**: Chrome, Firefox, Edge, Safari
- **Operating Systems**: Windows, macOS, Linux
- **Audio Players**: All standard media players
- **Audio Editors**: Audacity, Adobe Audition, etc.

## Future Enhancements

Potential improvements (not yet implemented):
- MP3 file support
- Multiple audio file formats
- Audio effects preview
- Spectrogram visualization
- Frequency domain analysis
- Side-by-side audio player
- Batch processing mode

## Summary

The enhanced audio features provide a complete, intuitive audio simulation experience:

✅ **Upload Audio Files**: Real audio for realistic testing
✅ **Real-Time Preview**: Immediate visual feedback
✅ **Download Results**: Save and analyze output
✅ **Educational Focus**: Perfect for demonstrations
✅ **Easy to Use**: Intuitive interface
✅ **Professional Quality**: 16-bit WAV output

These enhancements make the audio simulator production-ready for educational use while maintaining simplicity and performance.

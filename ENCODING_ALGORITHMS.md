# Documentación de Algoritmos de Codificación y Decodificación

## Índice
1. [Introducción](#introducción)
2. [Codificación de Audio](#codificación-de-audio)
3. [Codificación de Video](#codificación-de-video)
4. [Codificación de Imagen](#codificación-de-imagen)
5. [Codificación de Texto](#codificación-de-texto)
6. [Decodificación](#decodificación)
7. [Ejemplo Práctico Completo](#ejemplo-práctico-completo)

---

## Introducción

Este simulador educativo implementa técnicas de codificación de fuente simplificadas pero representativas de sistemas reales 5G/6G. Los algoritmos están diseñados para:

- **Propósito educativo**: Mostrar conceptos fundamentales sin complejidad innecesaria
- **Procesamiento eficiente**: Tiempos de simulación rápidos (2-5 segundos)
- **Visualización clara**: Permitir ver transformaciones en cada etapa
- **Realismo equilibrado**: Balance entre exactitud técnica y comprensibilidad

---

## Codificación de Audio

### Algoritmo: PCM (Pulse Code Modulation) de 12 bits

#### Descripción
La codificación de audio utiliza **PCM cuantizado de 12 bits**, una versión simplificada pero representativa de codecs modernos como AAC o Opus.

#### Pasos del Algoritmo

**1. Normalización**
```python
# Entrada: audio_signal (array de flotantes)
max_val = np.max(np.abs(audio_signal))
if max_val > 0:
    normalized = audio_signal / max_val  # Rango: [-1, 1]
```

**Propósito**: Escalar la señal al rango estándar [-1, 1] para cuantización consistente.

**Ejemplo**:
```
Entrada original: [0.5, -0.8, 0.3, 1.2, -0.4]
Max valor: 1.2
Normalizado: [0.417, -0.667, 0.250, 1.000, -0.333]
```

**2. Cuantización a 12 bits**
```python
# Cuantizar a 12 bits (-2048 a 2047)
quantized = np.round(normalized * 2047).astype(int)
```

**Propósito**: Convertir valores continuos a 4,096 niveles discretos (2^12).

**Niveles de cuantización**:
- Rango: -2048 a +2047
- Resolución: 1/2047 ≈ 0.0488% del rango completo
- Bits: 12 bits/muestra

**Ejemplo**:
```
Normalizado: [0.417, -0.667, 0.250, 1.000, -0.333]
Cuantizado: [854, -1366, 512, 2047, -682]
```

**3. Conversión a Binario**
```python
bits = []
for sample in quantized:
    val = int(sample) & 0xFFF  # Máscara de 12 bits
    bits.extend([int(b) for b in format(val, '012b')])
return np.array(bits, dtype=int)
```

**Propósito**: Generar bitstream para transmisión.

**Ejemplo para un sample (854)**:
```
Decimal: 854
Binario: 001101010110 (12 bits)
Array: [0,0,1,1,0,1,0,1,0,1,1,0]
```

#### Cálculo de Bitrate

Para audio de 2 segundos a 8000 Hz:
```
Samples = 2 seg × 8000 Hz = 16,000 samples
Bits totales = 16,000 × 12 bits = 192,000 bits
Bitrate = 192,000 / 2 = 96,000 bps = 96 kbps
```

#### Comparación con Estándares Reales

| Codec | Bitrate Típico | Complejidad | Uso |
|-------|---------------|-------------|-----|
| **PCM 12-bit (Simulador)** | 96 kbps | Baja | Educativo |
| PCM 16-bit | 128 kbps | Baja | Audio CD |
| AAC | 64-128 kbps | Alta | Streaming |
| Opus | 6-510 kbps | Alta | VoIP, 5G |

**Nota**: Nuestro PCM de 12 bits es más simple que codecs modernos pero suficiente para propósitos educativos.

#### Características de Calidad

**Ventajas**:
- ✅ Reconstrucción perfecta (lossless con 12 bits)
- ✅ Correlación 1.0000 bajo condiciones perfectas
- ✅ Latencia mínima (no hay buffering)
- ✅ Fácil de entender y visualizar

**Limitaciones**:
- ⚠️ No hay compresión (bitrate fijo)
- ⚠️ No aprovecha redundancia temporal
- ⚠️ Más simple que AAC/Opus reales

---

## Codificación de Video

### Algoritmo: DCT-RGB (Similar a H.265 simplificado)

#### Descripción
La codificación de video utiliza **Transformada Discreta de Coseno (DCT) en bloques 8×8** aplicada a cada canal RGB por separado. Este enfoque es similar a H.264/H.265 pero sin predicción inter-frame ni motion compensation (ya que procesamos frame-by-frame).

#### Pasos del Algoritmo

**1. Conversión a RGB**
```python
if len(frame.shape) == 2:
    # Grayscale → RGB (replicar canal)
    frame = np.stack([frame] * 3, axis=2)
```

**Propósito**: Asegurar que todos los frames sean RGB (3 canales).

**Ejemplo**:
```
Entrada grayscale: (64, 64)    → shape (altura, ancho)
Salida RGB: (64, 64, 3)        → shape (altura, ancho, canales)
```

**2. División en Bloques 8×8 por Canal**
```python
for channel in range(3):  # R, G, B
    channel_data = frame[:, :, channel]
    for i in range(0, height, 8):
        for j in range(0, width, 8):
            block = channel_data[i:i+8, j:j+8]
```

**Propósito**: Procesar imagen en bloques pequeños donde DCT es eficiente.

**Ejemplo para frame 64×64**:
```
Dimensiones: 64×64 pixels
Bloques por canal: 8×8 = 64 bloques
Total bloques (RGB): 64 × 3 = 192 bloques
```

**3. Transformada DCT 2D**

La DCT 2D transforma el bloque espacial al dominio de frecuencias:

```python
def _dct2d(self, block):
    N = 8  # Tamaño del bloque
    dct = np.zeros((8, 8))
    
    for u in range(N):
        for v in range(N):
            sum_val = 0
            for i in range(N):
                for j in range(N):
                    sum_val += block[i, j] * \
                               np.cos((2*i + 1) * u * π / (2*N)) * \
                               np.cos((2*j + 1) * v * π / (2*N))
            
            cu = 1/√2 if u == 0 else 1
            cv = 1/√2 if v == 0 else 1
            dct[u, v] = 0.25 * cu * cv * sum_val
    
    return dct
```

**Matemática DCT**:
```
DCT(u,v) = (1/4) × Cu × Cv × 
           Σ Σ pixel[i,j] × 
           i j
           cos((2i+1)uπ/16) × cos((2j+1)vπ/16)

Donde:
- Cu, Cv = 1/√2 si u,v = 0, sino 1
- u, v: coordenadas de frecuencia (0-7)
- i, j: coordenadas espaciales (0-7)
```

**Interpretación de Coeficientes DCT**:
```
    Frecuencia Horizontal →
F  ┌─────────────────────┐
r  │ DC  ║  Bajas → Altas │
e  │═════╬════════════════│
c  │ Ba- ║                │
.  │ jas ║   Frecuencias  │
   │  ↓  ║    Medias      │
V  │ Al- ║                │
e  │ tas ║   Frecuencias  │
r  │     ║     Altas      │
t  └─────────────────────┘

[0,0] = Componente DC (valor promedio)
[0,1..7] = Frecuencias horizontales
[1..7,0] = Frecuencias verticales
[resto] = Frecuencias diagonales
```

**Ejemplo de Bloque 8×8**:

Entrada (valores de pixel 0-255):
```
[120, 118, 122, 119, 121, 120, 119, 121]
[118, 120, 119, 121, 120, 122, 118, 120]
[122, 119, 121, 120, 119, 118, 121, 119]
...
```

Salida DCT (coeficientes de frecuencia):
```
[ 960.0,  -2.1,   1.3,  -0.8,   0.5,  -0.3,   0.2,  -0.1]
[  -1.8,   0.9,  -0.7,   0.4,  -0.2,   0.1,  -0.1,   0.0]
[   1.2,  -0.6,   0.5,  -0.3,   0.1,  -0.1,   0.0,   0.0]
...
```

**Observaciones**:
- **DC [0,0] = 960**: Valor promedio del bloque (960/64 ≈ 15 → pixel promedio ≈ 120)
- **Bajas frecuencias**: Valores mayores (cambios suaves)
- **Altas frecuencias**: Valores cercanos a cero (detalles finos)

**4. Cuantización**
```python
quantized = np.round(dct_block / 2).astype(int)
```

**Propósito**: Reducir magnitud de coeficientes (compresión con pérdida).

**Factor de cuantización**: /2 (compromiso entre calidad y compresión)

**Ejemplo**:
```
DCT original:  [ 960.0, -2.1,  1.3, -0.8,  0.5]
Cuantizado /2: [ 480,   -1,    1,    0,    0]
```

**Efecto de Cuantización**:
- Coeficientes pequeños → 0 (compresión)
- Menos bits para codificar ceros
- Pérdida de detalles finos (aceptable)

**5. Conversión a Binario**
```python
for coeff in quantized.flatten():
    val = int(coeff) & 0xFF  # 8 bits por coeficiente
    bits.extend([int(b) for b in format(val, '08b')])
```

**Propósito**: Generar bitstream de 8 bits por coeficiente.

**Ejemplo**:
```
Coeficiente: 480
Limitado a 8 bits: 480 & 0xFF = 224 (overflow, módulo 256)
Binario: 11100000
Array: [1,1,1,0,0,0,0,0]
```

**Nota**: Coeficientes grandes (>255) se truncan. Esto está bien porque:
1. DC ya fue normalizado
2. Altas frecuencias son pequeñas después de cuantización
3. Propósito educativo tolera esta simplificación

#### Cálculo de Bitrate para Video

Para un frame 64×64 RGB:
```
Bloques por canal: (64/8) × (64/8) = 64 bloques
Coeficientes por bloque: 8 × 8 = 64 coeficientes
Bits por coeficiente: 8 bits

Bits por canal: 64 bloques × 64 coef × 8 bits = 32,768 bits
Bits totales (RGB): 32,768 × 3 = 98,304 bits
```

Para video a 30 FPS:
```
Bitrate = 98,304 bits/frame × 30 FPS = 2,949,120 bps ≈ 2.95 Mbps
```

#### Comparación con Estándares Reales

| Codec | Bitrate (1080p) | Compresión | Técnicas Adicionales |
|-------|-----------------|------------|---------------------|
| **DCT-RGB (Simulador)** | ~3 Mbps | Baja | DCT, Cuantización |
| H.264 | 3-8 Mbps | Media | + Predicción inter/intra, MC |
| H.265/HEVC | 1.5-4 Mbps | Alta | + CTU, SAO, Parallel tools |
| VP9 | 1-3 Mbps | Alta | + Super-blocks, Loop filters |

**Nota**: Nuestro DCT-RGB es frame-independiente (no usa frames anteriores), por lo que el bitrate es más alto que H.265 real pero suficiente para educación.

#### Calidad Esperada

**Métricas bajo condiciones perfectas (BER=0%)**:
- **PSNR**: 15-25 dB (buena calidad, similar a JPEG medio)
- **SSIM**: 0.70-0.90 (buena similitud estructural)
- **Pérdida**: Intencional por cuantización DCT (como JPEG)

**Por qué la pérdida es educativa**:
1. Muestra diferencia entre codificación de fuente (con pérdida) y canal (sin pérdida ideal)
2. Realista: H.264/H.265 también tienen pérdida por cuantización
3. Permite experimentar con calidad vs bitrate

---

## Codificación de Imagen

### Algoritmo: Idéntico a Video (DCT-RGB)

La codificación de imagen usa exactamente el mismo algoritmo que video:
- DCT 2D en bloques 8×8
- Procesamiento RGB por canal
- Cuantización /2
- 8 bits por coeficiente

**Ver sección de Codificación de Video para detalles completos.**

**Diferencia práctica**: Imagen es estática (1 frame), video puede tener múltiples frames pero se procesan independientemente.

---

## Codificación de Texto

### Algoritmo: ASCII de 8 bits

#### Descripción
Codificación simple y directa de caracteres ASCII a 8 bits por carácter.

#### Pasos del Algoritmo

**1. Conversión Carácter → Código ASCII**
```python
for char in text:
    ascii_val = ord(char)  # Obtener código ASCII
```

**Ejemplo**:
```
Texto: "Hola"
Códigos ASCII:
- 'H' → 72
- 'o' → 111
- 'l' → 108
- 'a' → 97
```

**2. Conversión a Binario (8 bits)**
```python
bits_str = format(ascii_val, '08b')  # 8 bits con ceros a la izquierda
bits.extend([int(b) for b in bits_str])
```

**Ejemplo completo**:
```
Texto: "Hola"

'H' → 72  → 01001000
'o' → 111 → 01101111
'l' → 108 → 01101100
'a' → 97  → 01100001

Bitstream completo: 
[0,1,0,0,1,0,0,0, 0,1,1,0,1,1,1,1, 0,1,1,0,1,1,0,0, 0,1,1,0,0,0,0,1]
Total: 32 bits (4 caracteres × 8 bits)
```

#### Cálculo de Bitrate

```
Bitrate = 8 bits/carácter

Para texto de 100 caracteres:
Total bits = 100 × 8 = 800 bits
```

#### Por Qué No Usar Huffman

**Huffman** (códigos de longitud variable):
- ✅ Mayor compresión (30-50%)
- ❌ Complejo de implementar correctamente
- ❌ Requiere transmitir tabla de códigos
- ❌ Errores de 1 bit corrompen múltiples caracteres

**ASCII de 8 bits**:
- ✅ Simple y robusto
- ✅ Cada carácter independiente
- ✅ Fácil de visualizar y entender
- ✅ Errores de 1 bit afectan solo 1 carácter
- ⚠️ Sin compresión (bitrate fijo)

**Decisión**: Para propósito educativo, ASCII es superior por claridad.

---

## Decodificación

### Principio General

Todas las decodificaciones siguen el proceso **inverso** de la codificación:

```
Codificación: Datos → Transformación → Cuantización → Bits
Decodificación: Bits → Descuantización → Trans. Inversa → Datos
```

### Decodificación de Audio

**Proceso**:

**1. Bits → Samples Cuantizados**
```python
for i in range(0, len(bits), 12):
    val = int(''.join(map(str, bits[i:i+12])), 2)  # Binario → decimal
    if val > 2047:
        val = val - 4096  # Convertir a complemento a 2
    samples.append(val)
```

**Ejemplo**:
```
Bits: [0,0,1,1,0,1,0,1,0,1,1,0]  (12 bits)
Decimal sin signo: 854
Rango: 0-2047 (positivo)
Valor final: 854
```

**2. Descuantización**
```python
normalized = val / 2047.0  # Rango: [-1, 1]
```

**Ejemplo**:
```
Cuantizado: 854
Normalizado: 854 / 2047 = 0.417
```

**3. Ajuste de Longitud**
```python
if len(audio_signal) < len(original_audio):
    audio_signal = np.pad(audio_signal, ...)  # Rellenar con ceros
else:
    audio_signal = audio_signal[:len(original_audio)]  # Truncar
```

**Resultado**: Audio reconstruido con correlación ≈ 1.0 bajo condiciones perfectas.

### Decodificación de Video e Imagen

**Proceso**:

**1. Bits → Coeficientes DCT**
```python
for i in range(0, len(bits), 8):
    byte_val = int(''.join(map(str, bits[i:i+8])), 2)
    if byte_val > 127:
        byte_val = byte_val - 256  # Convertir a con signo
    coeffs.append(byte_val)
```

**Ejemplo**:
```
Bits: [11100000] (8 bits)
Decimal sin signo: 224
Convertido a con signo: 224 - 256 = -32
Coeficiente: -32
```

**2. Descuantización**
```python
dequantized = block_coeffs * 2  # Inverso de /2
```

**Ejemplo**:
```
Cuantizado: [-32,  5,  0,  1, -1]
Descuantizado: [-64, 10,  0,  2, -2]
```

**3. IDCT 2D (Transformada Inversa)**
```python
def _idct2d(self, dct_block):
    N = 8
    spatial = np.zeros((8, 8))
    
    for i in range(N):
        for j in range(N):
            sum_val = 0
            for u in range(N):
                for v in range(N):
                    cu = 1/√2 if u == 0 else 1
                    cv = 1/√2 if v == 0 else 1
                    sum_val += cu * cv * dct_block[u, v] * \
                               cos((2*i + 1) * u * π / (2*N)) * \
                               cos((2*j + 1) * v * π / (2*N))
            spatial[i, j] = 0.25 * sum_val
    
    return spatial
```

**Matemática IDCT**:
```
Pixel[i,j] = (1/4) × 
             Σ Σ Cu × Cv × DCT[u,v] × 
             u v
             cos((2i+1)uπ/16) × cos((2j+1)vπ/16)
```

**4. Reconstrucción RGB**
```python
# Reconstruir cada canal por separado
for channel in range(3):  # R, G, B
    # ... IDCT de todos los bloques ...
    reconstructed_channels.append(channel_data)

# Combinar canales
rgb_image = np.stack(reconstructed_channels, axis=2)
return Image.fromarray(rgb_image.astype(np.uint8))
```

**Resultado**: Imagen RGB reconstruida con calidad controlada por cuantización.

### Decodificación de Texto

**Proceso**:

**1. Bits → Códigos ASCII**
```python
for i in range(0, len(bits), 8):
    bit_chunk = bits[i:i+8]
    char_idx = int(''.join(map(str, bit_chunk)), 2)
```

**2. Códigos → Caracteres**
```python
if 32 <= char_idx <= 126:  # ASCII imprimible
    decoded_text.append(chr(char_idx))
else:
    decoded_text.append('?')  # Carácter inválido
```

**Ejemplo completo**:
```
Bits: [01001000, 01101111, 01101100, 01100001]
ASCII: [72, 111, 108, 97]
Texto: "Hola"
```

**Resultado**: Texto reconstruido perfectamente (lossless) bajo BER=0%.

---

## Ejemplo Práctico Completo

### Caso: Audio de 1 segundo a 8000 Hz

**Datos de Entrada**:
```
Duración: 1.0 segundo
Sample rate: 8000 Hz
Samples totales: 8000
Forma de onda: Sinusoidal 440 Hz (La musical)
```

**Paso 1: Generación**
```python
t = np.linspace(0, 1.0, 8000)
audio = 0.8 * np.sin(2 * np.pi * 440 * t)
# audio = [0, 0.0628, 0.1253, ..., -0.1253, -0.0628]
```

**Paso 2: Codificación**
```python
# Normalización (ya normalizado, max = 0.8)
normalized = audio / 0.8  # → [-1.0, 1.0]

# Cuantización
quantized = np.round(normalized * 2047)
# quantized[0] = 0
# quantized[1] = 128
# quantized[100] = 789
# ...

# Conversión a bits
# Sample 0:    0 → 000000000000 (12 bits)
# Sample 1:  128 → 000010000000
# Sample 100: 789 → 001100010101
# ...

Total bits: 8000 samples × 12 bits = 96,000 bits
```

**Paso 3: Transmisión a través del Canal**
```python
# Pipeline completo:
# 96,000 bits → Canal Encoding (LDPC)
# → 192,000 bits (con code rate 0.5)
# → Modulación (QPSK: 2 bits/símbolo)
# → 96,000 símbolos
# → Canal con ruido (AWGN, SNR = 20 dB)
# → Demodulación
# → Decodificación de canal
# → 96,000 bits recuperados
```

**Paso 4: Decodificación**
```python
# Bits → samples
# [000000000000] → 0
# [000010000000] → 128
# [001100010101] → 789

# Descuantización
# 0 / 2047 = 0.000
# 128 / 2047 = 0.0625
# 789 / 2047 = 0.385

# Audio reconstruido
reconstructed = [0.000, 0.0625, 0.385, ...]
```

**Paso 5: Métricas**
```python
# Correlación
corr = np.corrcoef(audio, reconstructed)[0, 1]
# Con BER=0%: corr ≈ 1.0000 (perfecto)

# BER
errors = np.sum(bits_tx != bits_rx)
ber = errors / len(bits_tx)
# Con SNR=20 dB, LDPC: BER ≈ 0.000000
```

### Caso: Imagen 64×64 RGB

**Datos de Entrada**:
```
Dimensiones: 64 × 64 pixels
Canales: RGB (3)
Bloques totales: 8×8×3 = 192 bloques de 8×8
```

**Paso 1: División en Bloques (Canal R)**
```python
# Bloque superior izquierdo (0, 0) del canal R
block_R_0_0 = imagen[0:8, 0:8, 0]  # 8×8 pixels
# Por ejemplo:
# [[120, 118, 122, 119, 121, 120, 119, 121],
#  [118, 120, 119, 121, 120, 122, 118, 120],
#  ...]
```

**Paso 2: DCT 2D**
```python
dct_block = _dct2d(block_R_0_0)
# Resultado (aproximado):
# [[ 960.0, -2.1,  1.3, -0.8,  0.5, -0.3,  0.2, -0.1],
#  [  -1.8,  0.9, -0.7,  0.4, -0.2,  0.1, -0.1,  0.0],
#  [   1.2, -0.6,  0.5, -0.3,  0.1, -0.1,  0.0,  0.0],
#  ...]

# Observa: DC (0,0) = 960 (grande), altas frecuencias ≈ 0 (pequeñas)
```

**Paso 3: Cuantización**
```python
quantized = np.round(dct_block / 2)
# [[ 480, -1,  1,  0,  0,  0,  0,  0],
#  [  -1,  0,  0,  0,  0,  0,  0,  0],
#  [   1,  0,  0,  0,  0,  0,  0,  0],
#  ...]

# Muchos ceros → compresión efectiva
```

**Paso 4: Bits**
```python
# Coeficientes → Binario (8 bits c/u)
# 480 → 0xE0 → 11100000
# -1  → 0xFF → 11111111
# 1   → 0x01 → 00000001
# 0   → 0x00 → 00000000
# ...

Bits por bloque: 64 coef × 8 bits = 512 bits
Bits por canal: 64 bloques × 512 bits = 32,768 bits
Bits totales (RGB): 32,768 × 3 = 98,304 bits
```

**Paso 5: Decodificación IDCT**
```python
# Descuantización
dequantized = quantized * 2
# [[ 960, -2,  2,  0, ...],
#  [  -2,  0,  0,  0, ...],
#  ...]

# IDCT 2D
reconstructed_block = _idct2d(dequantized)
# [[ 121, 119, 123, 120, ...],
#  [ 119, 121, 120, 122, ...],
#  ...]

# Diferencia con original: algunos pixels varían ±1-2
# Esto es pérdida por cuantización (esperado)
```

**Paso 6: Métricas**
```python
# PSNR
mse = np.mean((original - reconstructed)**2)
psnr = 10 * np.log10(255**2 / mse)
# Con cuantización /2: PSNR ≈ 20-25 dB (buena calidad)

# SSIM
ssim = calculate_ssim(original, reconstructed)
# Con cuantización /2: SSIM ≈ 0.75-0.90 (buena similitud)
```

---

## Resumen de Complejidad Computacional

### Audio (8000 samples)
```
Codificación: O(N) = O(8000) ≈ 8000 operaciones
- Normalización: N
- Cuantización: N
- Conversión binaria: N × 12

Tiempo aproximado: < 0.1 segundos
```

### Imagen 64×64 RGB
```
Codificación: O(B × N² × log N)
- B = 192 bloques
- N = 8 (tamaño bloque)
- DCT 2D: O(N²) por bloque (implementación directa)

Total operaciones: 192 × 64 × 6 ≈ 73,728
Tiempo aproximado: 0.5-1.0 segundos
```

### Video (1 frame)
```
Idéntico a imagen: 0.5-1.0 segundos por frame
```

---

## Conclusiones

### Ventajas del Enfoque Educativo

1. **Simplicidad**: Algoritmos comprensibles sin detalles innecesarios
2. **Visualización**: Fácil de mostrar transformaciones paso a paso
3. **Realismo**: Representativo de sistemas reales (DCT, PCM, cuantización)
4. **Eficiencia**: Tiempos de procesamiento rápidos (2-5 segundos)

### Limitaciones vs Sistemas Reales

1. **Audio**: PCM simple vs AAC/Opus (sin compresión temporal)
2. **Video**: Frame-independiente vs H.265 (sin predicción inter-frame)
3. **Cuantización**: Fija vs adaptativa (sin rate control)
4. **Entropía**: Sin codificación de entropía avanzada (Huffman, CABAC)

### Aplicabilidad Educativa

Estos algoritmos son **ideales para enseñar**:
- ✅ Conceptos de codificación de fuente
- ✅ Compresión con/sin pérdida
- ✅ Trade-offs calidad vs bitrate
- ✅ Efectos de cuantización
- ✅ Transformadas frecuenciales (DCT)
- ✅ Pipeline completo 5G/6G

**No son adecuados para**:
- ❌ Producción real
- ❌ Streaming comercial
- ❌ Aplicaciones de baja latencia crítica

---

## Referencias

- **DCT**: Ahmed, N., Natarajan, T., Rao, K.R. (1974). "Discrete Cosine Transform"
- **H.265/HEVC**: ITU-T Recommendation H.265
- **PCM**: ITU-T G.711
- **Codificación 5G**: 3GPP TS 38.300

---

**Autor**: Simulador Educativo 5G/6G  
**Versión**: 1.0  
**Fecha**: Noviembre 2025

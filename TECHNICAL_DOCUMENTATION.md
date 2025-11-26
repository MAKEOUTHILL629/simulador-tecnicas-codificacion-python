# Documentación Técnica - Simulador 5G/6G

## Índice
1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Fundamentos Teóricos](#fundamentos-teóricos)
3. [Módulos del Sistema](#módulos-del-sistema)
4. [Algoritmos Implementados](#algoritmos-implementados)
5. [Pipeline de Procesamiento](#pipeline-de-procesamiento)
6. [Consideraciones de Diseño](#consideraciones-de-diseño)
7. [Referencias Académicas](#referencias-académicas)

## Arquitectura del Sistema

### Diseño Modular

El simulador sigue una arquitectura modular basada en el pipeline estándar de comunicaciones digitales:

```
Input → Source Encoder → Channel Encoder → Modulator → Channel → 
Demodulator → Channel Decoder → Source Decoder → Output
```

### Componentes Principales

```
simulador-tecnicas-codificacion-python/
├── simulador.py              # Aplicación principal (GUI Streamlit)
├── modules/
│   ├── __init__.py
│   ├── source_encoder.py    # Codificación de fuente
│   ├── channel_encoder.py   # Codificación de canal (LDPC)
│   ├── modulator.py          # Modulación digital
│   ├── channel.py            # Canal inalámbrico
│   ├── demodulator.py        # Demodulación (LLR)
│   ├── channel_decoder.py    # Decodificación de canal
│   ├── source_decoder.py     # Decodificación de fuente
│   ├── metrics.py            # Métricas de información e integridad
│   └── visualizer.py         # Visualización
├── requirements.txt
├── CHANGELOG.md
├── USER_GUIDE.md
├── TECHNICAL_DOCUMENTATION.md
└── TEST_CASES.md
```

## Fundamentos Teóricos

### Teorema de Separación de Shannon

Para redes 5G y 5G Avanzado, el simulador implementa el paradigma de **Codificación Separada de Fuente y Canal (SSCC)**:

1. **Codificación de Fuente**: Elimina redundancia (compresión)
2. **Codificación de Canal**: Añade redundancia controlada (protección)

Este enfoque es óptimo en el límite asintótico según el Teorema de Separación de Shannon.

### Codificación Conjunta (6G)

Para 6G, el simulador está preparado para **Codificación Conjunta Fuente-Canal (JSCC)**, específicamente DeepJSCC, que abandona el principio de separación y optimiza de extremo a extremo.

### Capacidad del Canal

La capacidad teórica de Shannon:

```
C = B · log₂(1 + SNR)
```

Donde:
- C: Capacidad en bits/segundo
- B: Ancho de banda en Hz
- SNR: Relación señal a ruido (lineal)

## Módulos del Sistema

### 1. Source Encoder (`source_encoder.py`)

#### 1.1 Codificación Huffman (Texto)

**Algoritmo:**
1. Calcular frecuencias de caracteres
2. Construir árbol binario óptimo usando heap
3. Generar códigos de longitud variable (VLC)
4. Mapear texto a bits

**Clase:** `HuffmanNode`
- Estructura de árbol binario
- Comparación por frecuencia para heap

**Entropía:** 
```
H(X) = -Σ p(xᵢ) · log₂(p(xᵢ))
```

#### 1.2 Codificación DCT (Imagen)

**Transformada DCT-II:**

```
G[u,v] = (1/4) · C(u) · C(v) · Σᵢ Σⱼ x[i,j] · cos((2i+1)uπ/16) · cos((2j+1)vπ/16)
```

Donde:
- C(k) = 1/√2 si k=0, C(k)=1 si k>0
- Bloques 8×8 píxeles

**Proceso:**
1. Dividir imagen en bloques 8×8
2. Aplicar DCT-II a cada bloque
3. Cuantización uniforme: Q = round(G/Δ)
4. Serialización zigzag
5. Codificación de entropía

#### 1.3 Codificación MDCT (Audio)

**Transformada MDCT:**

```
X[k] = Σₙ x[n] · w[n] · cos(π/M · (n + 0.5 + M/2) · (k + 0.5))
```

Donde:
- M: Tamaño de transformada
- w[n]: Ventana (seno)
- Overlap 50%

**Características:**
- Elimina aliasing de bloque
- Compatible con overlap-add
- Base de AAC/MP3

#### 1.4 Codificación H.265 Simplificada (Video)

**Componentes:**
1. **Estimación de Movimiento**: SAD (Sum of Absolute Differences)
2. **Cálculo Residual**: E = Current - Predicted
3. **Transformada**: DCT del residual
4. **Cuantización**: Reducción de precisión

### 2. Channel Encoder (`channel_encoder.py`)

#### LDPC (Low-Density Parity-Check)

**Codificación Sistemática:**
```
C = [I | P]
```
Donde:
- I: Bits de información
- P: Bits de paridad

**Tasa de Código:**
```
R = k/n
```
Donde:
- k: Bits de información
- n: Bits totales

**Generación de Paridad:**
Para cada grupo de bits de información, se calcula:
```
p[i] = XOR(group[i]) = Σ bits[start:end] mod 2
```

**Nota:** La implementación actual es simplificada. Una implementación completa usaría:
- Matriz de paridad H (sparse)
- Base Graphs (BG1/BG2) según 3GPP TS 38.212
- Lifting con factor Z

### 3. Modulator (`modulator.py`)

#### Constelaciones Implementadas

**QPSK (M=4, k=2 bits/símbolo):**
```
S = (1/√2) · [(1-2b₀) + j(1-2b₁)]
```
Puntos: {±1±j}/√2

**16-QAM (M=16, k=4 bits/símbolo):**
```
I, Q ∈ {-3, -1, 1, 3}
S = A · (I + jQ)
A = 1/√10 (normalización de potencia)
```

**64-QAM (M=64, k=6 bits/símbolo):**
```
I, Q ∈ {-7, -5, -3, -1, 1, 3, 5, 7}
A = 1/√42
```

**256-QAM (M=256, k=8 bits/símbolo):**
```
I, Q ∈ {-15, -13, ..., 13, 15}
A = 1/√170
```

#### Mapeo Gray

Los bits se mapean usando codificación Gray para minimizar errores de bit en símbolos adyacentes.

### 4. Wireless Channel (`channel.py`)

#### Modelo Fundamental

```
R = h · S + N
```

Donde:
- R: Símbolo recibido
- h: Coeficiente de desvanecimiento
- S: Símbolo transmitido
- N: Ruido AWGN

#### 4.1 Canal AWGN

```
h = 1 (sin desvanecimiento)
N ~ CN(0, σ²)
```

Varianza del ruido:
```
σ² = Pₛ / SNR
```

#### 4.2 Canal Rayleigh (NLOS)

```
h = (X + jY) / √2
X, Y ~ N(0, 1)
```

La amplitud |h| sigue distribución de Rayleigh:
```
f(r) = (r/σ²) · exp(-r²/2σ²)
```

#### 4.3 Canal Rician (LOS)

```
h = √(K/(K+1)) · h_LOS + √(1/(K+1)) · h_NLOS
```

Donde:
- K: Factor Rician (lineal)
- h_LOS: Componente determinista
- h_NLOS: Componente Rayleigh

**Factor K en dB:**
```
K_dB = 10 · log₁₀(P_LOS / P_NLOS)
```

### 5. Demodulator (`demodulator.py`)

#### LLR (Log-Likelihood Ratio)

Definición:
```
L(bᵢ|y) = log(P(bᵢ=0|y) / P(bᵢ=1|y))
```

#### Aproximación Max-Log-MAP

```
L(bᵢ|y) ≈ (1/N₀) · [min_{x∈X₁} |y-x|² - min_{x∈X₀} |y-x|²]
```

Donde:
- X₀: Símbolos donde bit i = 0
- X₁: Símbolos donde bit i = 1
- N₀: Densidad espectral de ruido

**Interpretación:**
- L > 0: Bit probablemente es 0
- L < 0: Bit probablemente es 1
- |L| grande: Alta confianza

### 6. Channel Decoder (`channel_decoder.py`)

#### Decodificación LDPC Simplificada

**Algoritmo:**
1. Decisión dura: bits = (LLR < 0)
2. Extraer bits de información (sistemático)
3. Verificar paridad
4. Corregir errores en bits débiles (|LLR| mínimo)

**Decodificación Completa (no implementada):**
- Belief Propagation (BP)
- Sum-Product Algorithm
- Min-Sum approximation
- Iteraciones hasta convergencia

### 7. Source Decoder (`source_decoder.py`)

#### Operaciones Inversas

**IDCT-II:**
```
x[i,j] = (1/4) · Σᵤ Σᵥ C(u)C(v) · G[u,v] · cos((2i+1)uπ/16) · cos((2j+1)vπ/16)
```

**IMDCT:**
```
y[n] = Σₖ X[k] · cos(π/M · (n + 0.5 + M/2) · (k + 0.5))
```

Con overlap-add para continuidad.

### 8. Metrics (`metrics.py`)

#### Métricas de Información

**Entropía de Shannon:**
```
H(X) = -Σ p(xᵢ) · log₂(p(xᵢ))
```

**Información Mutua:**
```
I(X;Y) = H(X) + H(Y) - H(X,Y)
```

**Entropía Conjunta:**
```
H(X,Y) = -Σᵢ Σⱼ p(xᵢ,yⱼ) · log₂(p(xᵢ,yⱼ))
```

#### Métricas de Integridad

**BER (Bit Error Rate):**
```
BER = (# bits erróneos) / (# bits totales)
```

**BLER (Block Error Rate):**
```
BLER = (# bloques con errores) / (# bloques totales)
```

**PSNR (Peak Signal-to-Noise Ratio):**
```
MSE = (1/HW) · Σᵢ Σⱼ [X(i,j) - Y(i,j)]²
PSNR = 10 · log₁₀(MAX²/MSE)
```

**SSIM (Structural Similarity Index):**
```
SSIM(x,y) = [(2μₓμᵧ + C₁)(2σₓᵧ + C₂)] / [(μₓ² + μᵧ² + C₁)(σₓ² + σᵧ² + C₂)]
```

Donde:
- μ: Media local
- σ²: Varianza local
- σₓᵧ: Covarianza local
- C₁, C₂: Constantes de estabilización

### 9. Visualizer (`visualizer.py`)

#### Gráficos Generados

1. **Bitstream**: Señal digital en el tiempo
2. **Constelación I/Q**: Símbolos en plano complejo
3. **Histograma LLR**: Distribución de confianza
4. **Señal de Audio**: Forma de onda temporal
5. **Espectro**: Dominio de frecuencia (FFT)
6. **Curvas BER**: Rendimiento vs SNR

## Pipeline de Procesamiento

### Flujo de Datos Detallado

```
1. Input X (texto/imagen/audio/video)
   ↓
2. Source Encoding
   X → bits_source (Huffman/DCT/MDCT/H.265)
   ↓
3. Channel Encoding
   bits_source → bits_channel (LDPC)
   ↓
4. Modulation
   bits_channel → symbols (QPSK/QAM)
   ↓
5. Channel Transmission
   symbols → received (h·symbols + noise)
   ↓
6. Demodulation
   received → LLRs (soft decision)
   ↓
7. Channel Decoding
   LLRs → bits_decoded (error correction)
   ↓
8. Source Decoding
   bits_decoded → Output Y
   ↓
9. Metrics Calculation
   Compare X vs Y
```

### Estado en Cada Etapa

| Etapa | Tipo de Dato | Dimensión | Dominio |
|-------|--------------|-----------|---------|
| Input | Variable | Original | Fuente |
| Source Enc | int[] | k bits | Digital |
| Channel Enc | int[] | n bits | Digital |
| Modulation | complex[] | n/log₂(M) | I/Q |
| Channel | complex[] | n/log₂(M) | I/Q+Noise |
| Demodulation | float[] | n LLRs | Probabilidad |
| Channel Dec | int[] | k bits | Digital |
| Source Dec | Variable | ~Original | Fuente |

## Consideraciones de Diseño

### Simplificaciones Educativas

1. **LDPC Simplificado**: No usa matriz de paridad real
2. **Sin Rate Matching**: No implementa puncturing/repetition
3. **No Interleaving**: No hay entrelazado de bits
4. **Canal Ideal**: No hay sincronización ni ecualización
5. **JSCC Básico**: 6G usa modulación estándar, no red neuronal

### Parámetros por Defecto

```python
DEFAULTS = {
    'code_rate': 0.5,
    'snr_db': 10,
    'eb_n0_db': 10,
    'block_size': 8,      # Para DCT/MDCT
    'quantization': 10,   # Factor de cuantización
    'max_iterations': 20  # Para LDPC
}
```

### Optimizaciones

1. **Vectorización NumPy**: Operaciones matriciales rápidas
2. **Limitación de Tamaño**: Evita procesamiento excesivo
3. **Caching**: Streamlit cachea resultados
4. **Visualización Selectiva**: Solo primeros 100 bits

### Extensibilidad

El diseño modular permite:
- Añadir nuevos esquemas de modulación
- Implementar códigos polares para 5G control
- Integrar modelos DeepJSCC reales
- Añadir más tipos de desvanecimiento
- Implementar MIMO

## Referencias Académicas

### Estándares 3GPP
1. **3GPP TS 38.212**: Channel coding (LDPC, Polar)
2. **3GPP TS 38.214**: Physical layer procedures
3. **3GPP TS 38.211**: Physical channels and modulation

### Publicaciones
1. Shannon, C.E. (1948): "A Mathematical Theory of Communication"
2. Gallager, R. (1962): "Low-Density Parity-Check Codes"
3. Bourtsoulatze et al. (2019): "Deep Joint Source-Channel Coding"

### Algoritmos
1. Huffman, D. (1952): "A Method for the Construction of Minimum-Redundancy Codes"
2. Ahmed, Natarajan, Rao (1974): "Discrete Cosine Transform"
3. Princen, Bradley (1986): "Analysis/Synthesis Filter Bank Design"

### Métricas
1. Wang et al. (2004): "Image Quality Assessment: From Error Visibility to Structural Similarity"
2. Cover, Thomas (2006): "Elements of Information Theory"

## Notas de Implementación

### Dependencias Críticas
- NumPy: Álgebra lineal
- SciPy: Transformadas
- scikit-image: SSIM
- Streamlit: GUI reactiva

### Limitaciones Conocidas
1. No es una simulación bit-exact de 5G
2. LDPC no usa matrices 3GPP reales
3. No simula protocolo completo (solo PHY)
4. Rendimiento limitado para datos grandes

### Trabajo Futuro
1. Implementar LDPC completo con BP
2. Añadir códigos polares
3. Integrar DeepJSCC con PyTorch
4. Simular MIMO 2×2
5. Añadir modulación adaptativa (AMC)
6. Implementar CSI feedback

---

Esta documentación técnica describe la implementación actual del simulador. Para uso práctico, consulte USER_GUIDE.md.

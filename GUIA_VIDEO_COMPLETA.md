# 📹 Guía Completa de Simulación de Video

## 1. Introducción

Esta guía documenta en detalle cómo funciona la simulación de video en el Simulador 5G/6G, incluyendo el proceso técnico, restricciones, métricas, y cómo interpretar los resultados.

---

## 2. Proceso de Simulación de Video

### 2.1 Flujo Completo del Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PIPELINE DE SIMULACIÓN DE VIDEO                          │
│                         (7 Etapas Completas)                                 │
└─────────────────────────────────────────────────────────────────────────────┘

                              TRANSMISIÓN
    ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
    │  VIDEO   │ → │ SOURCE   │ → │ CHANNEL  │ → │MODULATOR │
    │  INPUT   │   │ ENCODER  │   │ ENCODER  │   │  (QAM)   │
    │ (Frame)  │   │ (DCT-RGB)│   │  (LDPC)  │   │          │
    └──────────┘   └──────────┘   └──────────┘   └──────────┘
         │              │              │              │
    Frame RGB     Bits DCT      Bits + Paridad   Símbolos IQ
     64×64×3      98,304 bits    ~196,608 bits    ~49,152
                                                      │
                                                      ▼
                                              ┌──────────────┐
                                              │    CANAL     │
                                              │  INALÁMBRICO │
                                              │  (AWGN/Fade) │
                                              └──────────────┘
                                                      │
                              RECEPCIÓN               ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────────┐
    │  VIDEO   │ ← │ SOURCE   │ ← │ CHANNEL  │ ← │ DEMODULATOR  │
    │  OUTPUT  │   │ DECODER  │   │ DECODER  │   │   (LLR)      │
    │ (Frame)  │   │(IDCT-RGB)│   │  (LDPC)  │   │              │
    └──────────┘   └──────────┘   └──────────┘   └──────────────┘
         │              │              │              │
    Frame RGB     Bits DCT       Bits Info       Soft Bits
     64×64×3      98,304 bits    98,304 bits     (LLRs)
```

### 2.2 Etapa 1: Carga y Preprocesamiento del Video

```python
# PROCESO DE CARGA
video_file → cv2.VideoCapture() → Extracción de propiedades
                                   │
                                   ├── Resolución (width × height)
                                   ├── Total de frames
                                   ├── FPS (frames por segundo)
                                   └── Duración total
                                   
# SELECCIÓN DE FRAME
frame_number → cap.set(cv2.CAP_PROP_POS_FRAMES, n) → cap.read()
                                                      │
                                                      ▼
                                                  frame RGB
```

**Restricciones de entrada:**
- Tamaño máximo recomendado: < 10 MB
- Formatos soportados: MP4, AVI, MOV, MKV, WebM
- El frame se redimensiona a 64×64 píxeles para simulación

### 2.3 Etapa 2: Codificación de Fuente (DCT-RGB)

```python
# ALGORITMO DE CODIFICACIÓN DCT
Para cada canal de color (R, G, B):
    1. Dividir en bloques de 8×8 píxeles
    2. Aplicar DCT-2D a cada bloque:
    
       DCT(u,v) = (1/4) × Cu × Cv × 
                  Σ Σ pixel[i,j] × cos((2i+1)uπ/16) × cos((2j+1)vπ/16)
                  i j
                  
    3. Cuantizar coeficientes: Q = round(DCT / 2)
    4. Convertir a binario (8 bits por coeficiente)
```

**Cálculo de bits:**
```
Frame 64×64×3 (RGB):
├── Bloques por canal: (64/8) × (64/8) = 64 bloques
├── Coeficientes por bloque: 8×8 = 64
├── Total coeficientes por canal: 64 × 64 = 4,096
├── Bits por coeficiente: 8
├── Bits por canal: 4,096 × 8 = 32,768
└── Total bits (RGB): 32,768 × 3 = 98,304 bits
```

### 2.4 Etapa 3: Codificación de Canal (LDPC)

```python
# CODIFICACIÓN LDPC
bits_entrada = 98,304
tasa_codigo = 0.5  # Ejemplo

bits_paridad = bits_entrada × (1/tasa_codigo - 1)
bits_salida = bits_entrada + bits_paridad

# Para tasa 0.5:
bits_salida = 98,304 + 98,304 = 196,608 bits
```

### 2.5 Etapa 4: Modulación

```python
# MODULACIÓN QAM
Esquema       | Bits/Símbolo | Símbolos para 196,608 bits
──────────────|──────────────|────────────────────────────
QPSK          |      2       | 98,304 símbolos
16-QAM        |      4       | 49,152 símbolos
64-QAM        |      6       | 32,768 símbolos
256-QAM       |      8       | 24,576 símbolos
```

### 2.6 Etapa 5: Canal Inalámbrico

```python
# MODELOS DE CANAL
AWGN:     y = x + n          # n ~ N(0, σ²)
Rayleigh: y = h × x + n      # h ~ CN(0, 1)
Rician:   y = (h_los + h_nlos) × x + n  # K-factor
```

### 2.7 Etapa 6-7: Demodulación y Decodificación

```python
# DEMODULACIÓN (Soft Decision)
LLR = log(P(bit=0|r) / P(bit=1|r))

# DECODIFICACIÓN LDPC (Iterativa)
Para cada iteración (max 50):
    1. Paso de nodos variable
    2. Paso de nodos check
    3. Verificar síndrome
```

---

## 3. Restricciones Técnicas

### 3.1 Restricciones de Entrada

| Parámetro | Restricción | Razón |
|-----------|-------------|-------|
| **Tamaño archivo** | < 10 MB (recomendado) | Memoria de Streamlit |
| **Resolución** | 64×64 (procesamiento) | Tiempo de cómputo |
| **Formato** | MP4, AVI, MOV, MKV, WebM | OpenCV soporte |
| **Tipo de frame** | Único (no secuencia) | Propósito educativo |
| **Color** | RGB (3 canales) | Procesamiento estándar |

### 3.2 Restricciones de Procesamiento

| Etapa | Restricción | Impacto |
|-------|-------------|---------|
| **DCT** | Bloques 8×8 fijos | Pérdida de detalles finos |
| **Cuantización** | Factor /2 | Pérdida de calidad base |
| **LDPC** | 50 iteraciones máx | Capacidad de corrección |
| **Modulación** | QPSK a 256-QAM | Throughput vs robustez |

### 3.3 Restricciones de Salida

- PSNR base (sin ruido): 20-25 dB
- SSIM base (sin ruido): 0.75-0.90
- No hay compresión inter-frame (solo intra-frame)
- No hay motion estimation

---

## 4. Métricas de Evaluación

### 4.1 Métricas de Teoría de Información

```
┌─────────────────────────────────────────────────────────────┐
│ ENTROPÍA H(X): Medida de incertidumbre de los bits         │
│                                                             │
│ H(X) = -Σ p(x) × log₂(p(x))                                │
│                                                             │
│ Interpretación:                                             │
│ • H(X) ≈ 1.0: Alta diversidad de bits                      │
│ • H(X) < 0.5: Patrones repetitivos                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ INFORMACIÓN MUTUA I(X;Y): Información preservada           │
│                                                             │
│ I(X;Y) = H(X) - H(X|Y)                                     │
│                                                             │
│ Interpretación:                                             │
│ • I(X;Y) ≈ H(X): Canal casi perfecto                       │
│ • I(X;Y) << H(X): Mucha información perdida                │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Métricas de Integridad

```
┌─────────────────────────────────────────────────────────────┐
│ BER (Bit Error Rate): Tasa de error de bits                │
│                                                             │
│ BER = (bits erróneos) / (bits totales)                     │
│                                                             │
│ Interpretación:                                             │
│ • BER = 0.000000: Transmisión perfecta                     │
│ • BER < 0.001: Excelente (< 0.1%)                          │
│ • BER < 0.01: Aceptable (< 1%)                             │
│ • BER > 0.05: Degradación visible (> 5%)                   │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Métricas de Calidad de Video

```
┌─────────────────────────────────────────────────────────────┐
│ PSNR (Peak Signal-to-Noise Ratio)                          │
│                                                             │
│ PSNR = 10 × log₁₀(MAX² / MSE)                              │
│                                                             │
│ Rangos típicos para video:                                  │
│ • > 40 dB: Excelente (imperceptible)                       │
│ • 30-40 dB: Muy bueno                                       │
│ • 25-30 dB: Bueno                                           │
│ • 20-25 dB: Aceptable (nuestro baseline)                   │
│ • < 20 dB: Degradación visible                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ SSIM (Structural Similarity Index)                          │
│                                                             │
│ SSIM = f(luminancia, contraste, estructura)                │
│                                                             │
│ Rangos:                                                     │
│ • > 0.95: Visualmente idéntico                             │
│ • 0.90-0.95: Muy similar                                    │
│ • 0.80-0.90: Similar (nuestro baseline)                    │
│ • 0.70-0.80: Diferencias notables                          │
│ • < 0.70: Diferencias significativas                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Escenarios de Prueba

### 5.1 Escenario 1: Condiciones Ideales

```
CONFIGURACIÓN:
- SNR: 30 dB
- Canal: AWGN
- Modulación: QPSK
- Tasa de código: 0.5

RESULTADOS ESPERADOS:
- BER: 0.000000 (0%)
- PSNR: 22-25 dB
- SSIM: 0.80-0.90

CONCLUSIÓN: La degradación visible es por la compresión DCT 
(intencional), no por errores de transmisión.
```

### 5.2 Escenario 2: Ruido Moderado

```
CONFIGURACIÓN:
- SNR: 10 dB
- Canal: AWGN
- Modulación: QPSK
- Tasa de código: 0.5

RESULTADOS ESPERADOS:
- BER: 0.001-0.01 (0.1-1%)
- PSNR: 18-22 dB
- SSIM: 0.65-0.80

CONCLUSIÓN: Algunos errores de transmisión, la codificación 
LDPC corrige la mayoría pero puede haber artefactos.
```

### 5.3 Escenario 3: Condiciones Adversas

```
CONFIGURACIÓN:
- SNR: 5 dB
- Canal: Rayleigh
- Modulación: 16-QAM
- Tasa de código: 0.5

RESULTADOS ESPERADOS:
- BER: 0.01-0.05 (1-5%)
- PSNR: 12-18 dB
- SSIM: 0.40-0.65

CONCLUSIÓN: Canal desafiante, errores frecuentes, 
artefactos visibles y posible pérdida de información.
```

### 5.4 Escenario 4: Límite de Operación

```
CONFIGURACIÓN:
- SNR: 0 dB
- Canal: Rayleigh
- Modulación: 64-QAM
- Tasa de código: 0.9

RESULTADOS ESPERADOS:
- BER: > 0.1 (> 10%)
- PSNR: < 12 dB
- SSIM: < 0.40

CONCLUSIÓN: Sistema sobrepasado, imagen inutilizable,
se necesita mejor protección (menor tasa de código, 
modulación más robusta).
```

---

## 6. Experimentos Recomendados

### 6.1 Experimento: Efecto del SNR en Calidad

```
Objetivo: Demostrar cómo el SNR afecta la calidad del video

Parámetros fijos:
- Modulación: QPSK
- Canal: AWGN
- Tasa de código: 0.5

Variable: SNR (0, 5, 10, 15, 20, 25, 30 dB)

Registrar: BER, PSNR, SSIM para cada SNR

Resultado esperado:
┌───────┬────────────┬───────────┬───────────┐
│  SNR  │    BER     │   PSNR    │   SSIM    │
├───────┼────────────┼───────────┼───────────┤
│  0 dB │  ~0.05     │  ~12 dB   │  ~0.40    │
│  5 dB │  ~0.01     │  ~16 dB   │  ~0.55    │
│ 10 dB │  ~0.001    │  ~20 dB   │  ~0.70    │
│ 15 dB │  ~0.0001   │  ~22 dB   │  ~0.80    │
│ 20 dB │  ~0.00001  │  ~24 dB   │  ~0.85    │
│ 25 dB │  ~0        │  ~25 dB   │  ~0.88    │
│ 30 dB │  0         │  ~25 dB   │  ~0.90    │
└───────┴────────────┴───────────┴───────────┘

Conclusión: Existe un "piso" de calidad (PSNR ~25 dB) 
determinado por la compresión DCT, independiente del SNR.
```

### 6.2 Experimento: Comparación de Modulaciones

```
Objetivo: Comparar robustez vs eficiencia de modulaciones

Parámetros fijos:
- SNR: 15 dB
- Canal: AWGN
- Tasa de código: 0.5

Variable: Modulación (QPSK, 16-QAM, 64-QAM, 256-QAM)

Resultado esperado:
┌───────────┬────────────┬───────────┬────────────────────┐
│Modulación │    BER     │ Eficiencia│  Uso recomendado   │
├───────────┼────────────┼───────────┼────────────────────┤
│ QPSK      │  ~0.00001  │  2 b/s    │ Alto ruido, IoT    │
│ 16-QAM    │  ~0.0001   │  4 b/s    │ Balance general    │
│ 64-QAM    │  ~0.001    │  6 b/s    │ SNR bueno          │
│ 256-QAM   │  ~0.01     │  8 b/s    │ SNR excelente      │
└───────────┴────────────┴───────────┴────────────────────┘

Conclusión: Mayor eficiencia espectral implica menor 
robustez al ruido. La elección depende del escenario.
```

### 6.3 Experimento: Efecto de la Tasa de Código

```
Objetivo: Demostrar el trade-off redundancia vs eficiencia

Parámetros fijos:
- SNR: 10 dB (ruido moderado)
- Canal: AWGN
- Modulación: QPSK

Variable: Tasa de código (0.3, 0.5, 0.7, 0.9)

Resultado esperado:
┌──────────┬────────────┬────────────┬──────────────────┐
│   Tasa   │    BER     │  Overhead  │   Observación    │
├──────────┼────────────┼────────────┼──────────────────┤
│   0.3    │  ~0.00001  │   233%     │ Muy protegido    │
│   0.5    │  ~0.001    │   100%     │ Buen balance     │
│   0.7    │  ~0.01     │    43%     │ Eficiente        │
│   0.9    │  ~0.05     │    11%     │ Poco protegido   │
└──────────┴────────────┴────────────┴──────────────────┘

Conclusión: Tasa más baja = más redundancia = más 
protección pero menos eficiencia espectral.
```

---

## 7. Generación de Conclusiones

### 7.1 Plantilla de Conclusiones para Simulación

```markdown
## CONCLUSIONES DE LA SIMULACIÓN

### Configuración Utilizada
- Tipo de fuente: Video
- Resolución procesada: 64×64 RGB
- Modulación: [MODULACIÓN]
- SNR: [X] dB
- Canal: [TIPO DE CANAL]
- Tasa de código: [X.X]

### Resultados Obtenidos
| Métrica | Valor | Interpretación |
|---------|-------|----------------|
| BER | [X.XXXXXX] | [Excelente/Bueno/Aceptable/Pobre] |
| PSNR | [XX.XX] dB | [Calidad visual: ...] |
| SSIM | [X.XXXX] | [Similitud estructural: ...] |
| H(X) | [X.XXXX] bits | [Diversidad de datos] |
| I(X;Y) | [X.XXXX] bits | [Información preservada] |

### Observaciones
1. [Descripción de la calidad visual del frame]
2. [Comparación entrada vs salida]
3. [Efecto del ruido observado]

### Conclusiones Técnicas
1. Con SNR=[X] dB y modulación [TIPO], el sistema logra 
   un BER de [X], lo cual es [adecuado/insuficiente] para 
   transmisión de video.
   
2. El PSNR de [X] dB indica que la calidad es [descripción],
   donde [X-Y] dB corresponden a pérdidas por compresión DCT
   y [Y-Z] dB a errores de transmisión.

3. La similitud estructural (SSIM=[X]) sugiere que 
   [los detalles finos se preservan/hay artefactos visibles].

### Recomendaciones
- Para mejorar calidad: [aumentar SNR/usar tasa más baja/...]
- Para aumentar eficiencia: [usar modulación más alta/...]
- Trade-offs observados: [descripción]
```

### 7.2 Ejemplo de Conclusión Generada

```markdown
## CONCLUSIONES DE LA SIMULACIÓN

### Configuración Utilizada
- Tipo de fuente: Video (frame de película)
- Resolución procesada: 64×64 RGB
- Modulación: 16-QAM
- SNR: 15 dB
- Canal: AWGN (sin desvanecimiento)
- Tasa de código: 0.5

### Resultados Obtenidos
| Métrica | Valor | Interpretación |
|---------|-------|----------------|
| BER | 0.000142 | Excelente (< 0.1%) |
| PSNR | 23.45 dB | Buena calidad visual |
| SSIM | 0.8234 | Alta similitud estructural |
| H(X) | 0.9156 bits | Alta diversidad de datos |
| I(X;Y) | 0.9001 bits | 98.3% información preservada |

### Observaciones
1. La imagen reconstruida mantiene los contornos principales
   y la estructura general claramente reconocibles.
2. Se observa ligera pérdida de detalles finos en áreas
   de alta frecuencia espacial.
3. Los colores principales se preservan bien, con ligera
   desaturación en tonos oscuros.

### Conclusiones Técnicas
1. Con SNR=15 dB y modulación 16-QAM, el sistema logra 
   un BER de 0.014%, lo cual es excelente para transmisión
   de video en tiempo real.
   
2. El PSNR de 23.45 dB indica calidad buena, donde ~3-4 dB
   corresponden a la compresión DCT base y ~1-2 dB a
   pequeños errores de transmisión.

3. La similitud estructural (SSIM=0.82) sugiere que los
   patrones visuales principales se preservan, siendo
   adecuado para la mayoría de aplicaciones de video.

### Recomendaciones
- Para mejorar calidad: Aumentar SNR a >20 dB o usar QPSK
- Para aumentar eficiencia: Usar 64-QAM si SNR > 20 dB
- Trade-off observado: Balanceado entre calidad y throughput
```

---

## 8. Comparación con Sistemas Reales

### 8.1 Simulador vs H.264/H.265

| Característica | Simulador | H.264 | H.265 |
|----------------|-----------|-------|-------|
| Compresión | Intra-frame | Inter + Intra | Inter + Intra |
| Transform | DCT 8×8 | DCT 4×4/8×8 | DCT 4×4 a 32×32 |
| Motion Est. | No | Sí | Sí (mejorado) |
| Bloques | Fijos 8×8 | Adaptativos | CTU adaptativos |
| Bitrate | ~98 kbps/frame | 1-50 Mbps | 0.5-30 Mbps |
| Calidad | Educativo | Producción | Producción |

### 8.2 Por Qué Usamos DCT Simplificado

1. **Propósito educativo**: Mostrar el concepto sin complejidad
2. **Transparencia**: Ver cada paso del proceso
3. **Tiempo de cómputo**: Simulación en segundos, no minutos
4. **Comprensibilidad**: Algoritmos que se pueden explicar

### 8.3 Limitaciones Conocidas

```
┌────────────────────────────────────────────────────────────┐
│ LIMITACIÓN                     │ IMPACTO                   │
├────────────────────────────────┼───────────────────────────┤
│ Sin compresión inter-frame     │ Cada frame independiente  │
│ Bloques 8×8 fijos              │ Posibles artefactos       │
│ Cuantización uniforme          │ No adaptativo a contenido │
│ Resolución 64×64               │ Pérdida de detalles       │
│ Sin entropy coding avanzado    │ Mayor bitrate             │
└────────────────────────────────┴───────────────────────────┘
```

---

## 9. Guía de Uso para Pruebas

### 9.1 Cómo Realizar Pruebas Sistemáticas

```
PASO 1: Preparar video de prueba
- Usar video de prueba estándar o propio
- Preferir resolución ≤ 1080p
- Tamaño recomendado < 10 MB

PASO 2: Establecer línea base
- Configurar SNR alto (25-30 dB)
- Canal AWGN
- Tasa 0.5, modulación QPSK
- Anotar PSNR y SSIM base

PASO 3: Variar un parámetro a la vez
- Mantener otros fijos
- Documentar cada resultado
- Capturar screenshot del frame

PASO 4: Registrar resultados
- Usar la plantilla de conclusiones
- Crear tabla comparativa
- Identificar tendencias

PASO 5: Generar conclusiones
- Basadas en datos observados
- Comparar con expectativas teóricas
- Identificar anomalías si las hay
```

### 9.2 Checklist de Documentación

```
☐ Screenshot de configuración
☐ Screenshot de frame original
☐ Screenshot de frame recibido
☐ Valores de todas las métricas
☐ Información del video (resolución, FPS)
☐ Número de bits procesados
☐ Tiempo de procesamiento (opcional)
☐ Conclusiones escritas
```

---

## 10. Preguntas Frecuentes (FAQ)

### ¿Por qué el frame se ve "pixelado" incluso con BER=0?

**Respuesta**: La compresión DCT es con pérdida (lossy). El BER=0 indica que los bits se transmitieron sin errores, pero esos bits ya representan una imagen comprimida. Esto es exactamente como funciona JPEG o H.264.

### ¿Por qué solo se simula un frame y no el video completo?

**Respuesta**: El propósito es educativo. Simular todo el video tomaría 10-25 minutos y perdería la interactividad. Con un frame puedes experimentar inmediatamente con diferentes parámetros.

### ¿Por qué el PSNR máximo es ~25 dB y no mayor?

**Respuesta**: Es el "piso" de calidad determinado por la cuantización DCT (factor /2). Para mayor PSNR necesitaríamos menos cuantización, lo cual generaría más bits y haría la simulación más lenta.

### ¿Por qué 64×64 y no la resolución original?

**Respuesta**: Por tiempo de cómputo. Un frame 1080p tendría 2 millones de píxeles × 24 bits = 48 millones de bits. Procesaríamos ~50 veces más datos, haciendo la simulación impráctica para educación.

### ¿Los resultados son representativos de sistemas reales?

**Respuesta**: Los conceptos sí, los valores exactos no. El simulador demuestra cómo funcionan las etapas de transmisión, pero sistemas reales (5G real) usan hardware dedicado, codecs más avanzados, y optimizaciones específicas.

---

## 11. Referencias Técnicas

### Estándares
- **H.264/AVC**: ISO/IEC 14496-10
- **H.265/HEVC**: ISO/IEC 23008-2
- **5G NR**: 3GPP TS 38.xxx

### Algoritmos
- **DCT**: Ahmed, Natarajan & Rao (1974)
- **LDPC**: Gallager (1962), MacKay (1996)
- **QAM**: Cimini (1985)

### Métricas
- **PSNR**: ITU-R BT.601
- **SSIM**: Wang et al., IEEE TIP 2004

---

*Documento generado para el Simulador 5G/6G*
*Versión 2.0 - Noviembre 2025*

# 📘 Manual del Simulador 5G/6G - Guía Completa

## Índice
1. [¿Cómo Funciona el Simulador?](#cómo-funciona-el-simulador)
2. [Explicación de Campos de Entrada](#explicación-de-campos-de-entrada)
3. [Diferencia entre SNR y Eb/N0](#diferencia-entre-snr-y-ebn0)
4. [¿Qué es la Tasa de Código?](#qué-es-la-tasa-de-código)
5. [Pipeline de 7 Etapas](#pipeline-de-7-etapas)
6. [Métricas Explicadas](#métricas-explicadas)
7. [Interpretación de Resultados](#interpretación-de-resultados)

---

## ¿Cómo Funciona el Simulador?

El simulador implementa un **sistema completo de comunicación digital** que reproduce cómo funcionan las redes 5G y 6G. Simula todo el proceso de transmisión desde que usted ingresa datos hasta que se reciben en el destino, pasando por todas las transformaciones que sufre la información.

### Proceso General

```
ENTRADA → Codificación → Canal con Ruido → Decodificación → SALIDA
```

**¿Por qué a veces la salida no es perfecta?**
En comunicaciones reales, el canal inalámbrico añade **ruido** y **desvanecimiento** (fading) que pueden corromper algunos bits. El simulador reproduce esto fielmente. A mayor ruido (SNR bajo), más errores. A menor ruido (SNR alto), mejor reconstrucción.

---

## Explicación de Campos de Entrada

### 1. **Tipo de Red**

Selecciona el estándar de comunicación a simular:

- **5G**: Red móvil de quinta generación
  - Usa codificación LDPC (Low-Density Parity-Check)
  - Soporta QPSK, 16-QAM, 64-QAM, 256-QAM
  - Diseñada para alta velocidad de datos
  
- **5G Avanzado (URLLC)**: Ultra-Reliable Low-Latency Communications
  - Misma tecnología que 5G pero optimizada para:
    - Ultra baja latencia (< 1 ms)
    - Ultra alta confiabilidad (99.999%)
  - Usado en: vehículos autónomos, cirugía remota, automatización industrial
  
- **6G (JSCC)**: Red de sexta generación (experimental)
  - Usa codificación conjunta fuente-canal (Joint Source-Channel Coding)
  - En el simulador es una versión simplificada
  - Representa el futuro de las comunicaciones

### 2. **Tipo de Fuente**

El tipo de información que desea transmitir:

- **Texto**: Mensajes de texto
  - Codificación: 8 bits por carácter (ASCII)
  - Ejemplo: "Hola Mundo 5G" = 104 bits (13 caracteres × 8 bits)
  
- **Imagen**: Archivos de imagen (PNG, JPG)
  - Codificación: DCT (Discrete Cosine Transform) similar a JPEG
  - Se divide en bloques de 8×8 píxeles
  - Se aplica transformada de frecuencia y cuantización
  
- **Audio**: Señales de audio sintéticas
  - Codificación: MDCT (Modified Discrete Cosine Transform) similar a AAC
  - Genera tonos de prueba a frecuencia específica
  
- **Video**: Frames de video
  - Codificación: Simplificación de H.265
  - Trata cada frame como imagen

### 3. **Esquema de Modulación**

Define cómo se convierten los bits en señales para transmitir:

| Modulación | Bits/Símbolo | Eficiencia | Robustez | Uso Típico |
|------------|--------------|------------|----------|------------|
| **QPSK** | 2 | Baja | Alta | Señales débiles, larga distancia |
| **16-QAM** | 4 | Media | Media | Balance velocidad/confiabilidad |
| **64-QAM** | 6 | Alta | Baja | Señal fuerte, corta distancia |
| **256-QAM** | 8 | Muy Alta | Muy Baja | Señal excelente, Wi-Fi |

**Trade-off**: Más bits por símbolo = más velocidad PERO más vulnerable al ruido.

**Ejemplo Visual**:
- QPSK: 4 puntos en el plano I/Q (fácil de distinguir con ruido)
- 256-QAM: 256 puntos muy juntos (difícil de distinguir con ruido)

### 4. **SNR (Signal-to-Noise Ratio)**

Relación Señal a Ruido en **decibelios (dB)**.

**¿Qué significa?**
- Mide la **potencia de la señal** versus la **potencia del ruido**
- SNR = 10 log₁₀(Potencia_Señal / Potencia_Ruido)

**Valores típicos**:
- **SNR < 0 dB**: Ruido más fuerte que la señal → Muchos errores
- **SNR = 10 dB**: Señal 10 veces más potente que ruido → Algunos errores
- **SNR = 20 dB**: Señal 100 veces más potente → Pocos errores
- **SNR > 30 dB**: Señal muy limpia → Casi sin errores

**En el simulador**:
- Rango: -10 a 30 dB
- Recomendado: 10-20 dB para ver comportamiento realista
- < 5 dB: Verá muchos errores (degradación evidente)
- > 25 dB: Verá transmisión casi perfecta

### 5. **Eb/N0 (Energy per Bit to Noise Density)**

Energía por bit dividida por la densidad espectral de ruido.

**¿Qué significa?**
- Similar a SNR pero **normalizado por bit**
- Más útil para comparar diferentes esquemas de modulación
- Eb/N0 = SNR × (Ancho_Banda / Tasa_Bits)

**Relación con SNR**:
```
Para QPSK (2 bits/símbolo):
Eb/N0 ≈ SNR - 3 dB

Para 16-QAM (4 bits/símbolo):
Eb/N0 ≈ SNR - 6 dB
```

**En el simulador**:
- Rango: -5 a 25 dB
- Se usa principalmente para cálculos internos
- El SNR es más intuitivo para el usuario

### 6. **Modelo de Desvanecimiento**

Simula cómo el canal inalámbrico afecta la señal:

- **AWGN (Additive White Gaussian Noise)**: Solo ruido
  - Canal ideal sin desvanecimiento
  - Ruido blanco gaussiano añadido
  - Mejor caso, usado como referencia
  - **Cuándo usarlo**: Para entender solo el efecto del ruido
  
- **Rayleigh (NLOS - Non-Line-of-Sight)**: Sin línea de vista
  - Entorno urbano con muchos obstáculos
  - La señal llega por múltiples caminos (reflexiones)
  - NO hay camino directo
  - **Peor caso**: Más errores que AWGN
  - **Cuándo usarlo**: Ciudad con edificios, interiores
  
- **Rician (LOS - Line-of-Sight)**: Con línea de vista
  - Hay un camino directo dominante
  - También hay reflexiones (multicamino)
  - Factor K controla la relación LOS/NLOS
  - **Mejor que Rayleigh, peor que AWGN**
  - **Cuándo usarlo**: Campo abierto, visión directa a antena

**Factor K (solo Rician)**:
- K = 0: Se comporta como Rayleigh (sin LOS)
- K = 10: Componente LOS 10 veces más fuerte que NLOS
- K = 20: Componente LOS muy dominante (casi AWGN)

### 7. **Tasa de Código (Code Rate)**

Este es un concepto MUY importante en comunicaciones.

**Definición Simple**:
- Proporción de bits de información respecto al total de bits transmitidos
- Tasa = Bits_Información / Bits_Totales

**¿Qué significa?**

Cuando transmitimos, añadimos **bits de redundancia** (bits extra) para proteger contra errores. La tasa de código indica cuánta redundancia añadimos.

**Ejemplo Práctico**:

```
Tasa 0.5 (50%):
- Tienes 100 bits de información
- Añades 100 bits de paridad (redundancia)
- Transmites 200 bits totales
- Tasa = 100/200 = 0.5
- Overhead = 100% (duplicas la cantidad de datos)

Tasa 0.9 (90%):
- Tienes 100 bits de información
- Añades 11 bits de paridad
- Transmites 111 bits totales
- Tasa = 100/111 = 0.9
- Overhead = 11% (muy poca redundancia)
```

**Trade-off**:

| Tasa de Código | Redundancia | Protección | Eficiencia | Uso |
|----------------|-------------|------------|------------|-----|
| **0.3** | Mucha (233%) | Excelente | Baja | Canal muy ruidoso |
| **0.5** | Media (100%) | Buena | Media | Balance |
| **0.7** | Poca (43%) | Regular | Alta | Canal limpio |
| **0.9** | Muy poca (11%) | Pobre | Muy Alta | Canal excelente |

**En el simulador**:
- Rango: 0.3 a 0.9
- Valor por defecto: 0.5 (balance)
- **Canal ruidoso (SNR bajo)**: Use 0.3-0.4 (más protección)
- **Canal limpio (SNR alto)**: Use 0.7-0.9 (más eficiencia)

**Analogía**:
Imagina enviar un paquete:
- Tasa 0.3: Empacas con MUCHO plástico de burbujas (llega intacto pero pesa más)
- Tasa 0.9: Empacas con POCO plástico (más liviano pero puede dañarse)

---

## Diferencia entre SNR y Eb/N0

Esta es una pregunta MUY común y válida. Ambos miden calidad del canal pero desde diferentes perspectivas.

### SNR (Signal-to-Noise Ratio)

**Qué mide**: Potencia total de la señal vs potencia total del ruido

**Fórmula**:
```
SNR = Potencia_Señal / Potencia_Ruido
SNR(dB) = 10 × log₁₀(SNR)
```

**Perspectiva**: A nivel de **símbolo** o **señal completa**

**Ejemplo**:
Si tu WiFi tiene SNR = 20 dB, significa que la señal es 100 veces más potente que el ruido.

### Eb/N0 (Energy per Bit to Noise Density)

**Qué mide**: Energía por **bit de información** vs densidad espectral de ruido

**Fórmula**:
```
Eb/N0 = (Potencia_Señal / Tasa_Bits) / Densidad_Ruido
Eb/N0 = SNR × (Ancho_Banda / Tasa_Bits)
```

**Perspectiva**: A nivel de **bit individual**

**Por qué es útil**:
- Permite comparar **sistemas diferentes** de manera justa
- Independiente del esquema de modulación usado
- Más relevante para calcular probabilidad de error de bit (BER)

### Relación entre SNR y Eb/N0

Depende del esquema de modulación:

```
Eb/N0 = SNR / (Bits_por_Símbolo)

Para QPSK (2 bits/símbolo):
Si SNR = 10 dB → Eb/N0 ≈ 7 dB

Para 16-QAM (4 bits/símbolo):
Si SNR = 10 dB → Eb/N0 ≈ 4 dB

Para 64-QAM (6 bits/símbolo):
Si SNR = 10 dB → Eb/N0 ≈ 1.76 dB
```

### ¿Cuál usar?

**Use SNR cuando**:
- Quiera medir calidad del canal en general
- Compare señales al mismo nivel de símbolo
- Analice sistemas de radio o WiFi

**Use Eb/N0 cuando**:
- Compare diferentes modulaciones
- Calcule BER (probabilidad de error)
- Diseñe sistemas de comunicación
- Compare con teoría de Shannon

### En el Simulador

**Ambos parámetros están disponibles** pero para simplicidad:
- **Ajuste el SNR** para controlar el ruido visible
- El Eb/N0 se calcula internamente
- A mayor SNR → mayor Eb/N0 → menos errores

**Recomendación**: Para experimentos educativos, enfóquese en el **SNR** que es más intuitivo.

---

## Pipeline de 7 Etapas

El simulador procesa la información en 7 etapas claramente definidas:

### Etapa 1: Codificación de Fuente

**Objetivo**: Comprimir la información, eliminar redundancia

**¿Qué hace?**
- Texto: Convierte caracteres a bits (8 bits/carácter en ASCII)
- Imagen: Aplica DCT (transforma espacial → frecuencia)
- Audio: Aplica MDCT (similar a AAC/MP3)
- Video: DCT + estimación de movimiento (H.265 simplificado)

**Salida**: Secuencia de bits (0s y 1s)

**Visualización**: Gráfico de bits en el tiempo

### Etapa 2: Codificación de Canal

**Objetivo**: Añadir redundancia controlada para proteger contra errores

**¿Qué hace?**
- Aplica código LDPC (Low-Density Parity-Check)
- Añade bits de paridad según la tasa de código
- Ejemplo: 100 bits → 200 bits (si tasa = 0.5)

**Salida**: Bits con redundancia añadida

**Visualización**: Muestra el overhead (bits añadidos)

### Etapa 3: Modulación

**Objetivo**: Convertir bits digitales en señales analógicas para transmitir

**¿Qué hace?**
- Agrupa bits según el esquema:
  - QPSK: 2 bits → 1 símbolo
  - 16-QAM: 4 bits → 1 símbolo
  - 64-QAM: 6 bits → 1 símbolo
  - 256-QAM: 8 bits → 1 símbolo
- Mapea a puntos en el plano complejo (I/Q)

**Salida**: Símbolos complejos (parte real + parte imaginaria)

**Visualización**: Diagrama de constelación I/Q
- Eje X: Componente en fase (I)
- Eje Y: Componente en cuadratura (Q)
- Puntos bien definidos = señal lista para transmitir

### Etapa 4: Canal Inalámbrico

**Objetivo**: Simular la transmisión por el aire con ruido y desvanecimiento

**¿Qué hace?**
- Añade ruido gaussiano (AWGN) según el SNR
- Aplica desvanecimiento si se selecciona:
  - Rayleigh: Multiplica por coeficiente aleatorio
  - Rician: Componente fija + componente aleatoria
- Formula: Señal_Recibida = h × Señal_Transmitida + Ruido

**Salida**: Símbolos recibidos (corrompidos por ruido)

**Visualización**: Constelación ruidosa
- Los puntos están "dispersos" alrededor de posiciones ideales
- Mayor dispersión = más ruido
- Rotación/atenuación = desvanecimiento

### Etapa 5: Demodulación

**Objetivo**: Extraer información de los símbolos recibidos

**¿Qué hace?**
- Calcula LLR (Log-Likelihood Ratio) para cada bit
- LLR mide la "confianza" en que un bit es 0 o 1
  - LLR > 0: Probablemente es 0
  - LLR < 0: Probablemente es 1
  - |LLR| grande: Alta confianza
  - |LLR| pequeño: Baja confianza (incertidumbre)

**Salida**: Valores LLR (números reales, no solo 0/1)

**Visualización**: Histograma de LLRs
- Picos alejados de 0: Alta confianza (buena señal)
- Valores cerca de 0: Incertidumbre (mala señal)

### Etapa 6: Decodificación de Canal

**Objetivo**: Usar la redundancia para corregir errores

**¿Qué hace?**
- Decodificador LDPC procesa los LLRs
- Usa la información de paridad para:
  - Detectar bits erróneos
  - Corregirlos si es posible
- Extrae los bits de información originales

**Salida**: Bits de información recuperados

**Visualización**: Muestra los bits decodificados

### Etapa 7: Decodificación de Fuente

**Objetivo**: Reconstruir la información original

**¿Qué hace?**
- Texto: Convierte bits a caracteres ASCII
- Imagen: IDCT (inversa de DCT) + reconstrucción
- Audio: IMDCT + overlap-add
- Video: IDCT + compensación de movimiento

**Salida**: Información reconstruida (texto, imagen, audio, video)

**Visualización**: Muestra el resultado final

---

## Métricas Explicadas

### Métricas de Teoría de la Información

#### H(X) - Entropía de Entrada

**¿Qué es?**
Mide la "cantidad de información" o "incertidumbre" en la entrada.

**Fórmula**:
```
H(X) = -Σ p(xᵢ) × log₂(p(xᵢ))
```

**Interpretación**:
- H(X) = 0 bits: Información totalmente predecible (ej: "AAAAA")
- H(X) = 1 bit: Máxima entropía binaria (ej: 50% de 0s y 50% de 1s)
- H(X) alto: Información muy variable (impredecible)

**Valores típicos**:
- Texto en español: 3-5 bits por carácter
- Bits aleatorios: ~1 bit
- Imagen natural: 6-8 bits por píxel

#### H(Y) - Entropía de Salida

Misma interpretación que H(X) pero para la señal recibida.

**Comparación**:
- Si H(Y) ≈ H(X): La salida tiene tanta información como la entrada (bueno)
- Si H(Y) >> H(X): Se añadió ruido/información extra (malo)
- Si H(Y) << H(X): Se perdió información (malo)

#### I(X;Y) - Información Mutua

**¿Qué es?**
Mide cuánta información sobre X se puede obtener observando Y.

**Fórmula**:
```
I(X;Y) = H(X) + H(Y) - H(X,Y)
```

**Interpretación**:
- I(X;Y) = H(X): Transmisión perfecta (toda la información se preservó)
- I(X;Y) < H(X): Se perdió información
- I(X;Y) = 0: X e Y son independientes (no hay relación)

**Valores típicos**:
- Canal perfecto: I(X;Y) = H(X)
- Canal con errores: I(X;Y) < H(X)
- Porcentaje de información preservada: I(X;Y)/H(X) × 100%

### Métricas de Integridad

#### BER (Bit Error Rate)

**¿Qué es?**
Proporción de bits erróneos en la transmisión.

**Fórmula**:
```
BER = (Número de bits erróneos) / (Número total de bits)
```

**Interpretación**:
- BER = 0: Sin errores (perfecto)
- BER = 0.001 (0.1%): 1 error cada 1000 bits (excelente)
- BER = 0.01 (1%): 1 error cada 100 bits (bueno)
- BER = 0.1 (10%): 1 error cada 10 bits (pobre)
- BER = 0.5 (50%): Aleatorio (no hay comunicación)

**Estándares típicos**:
- Voz (telefonía): BER < 10⁻³ (0.1%) aceptable
- Datos (internet): BER < 10⁻⁶ (0.0001%) requerido
- 5G URLLC: BER < 10⁻⁵ (0.001%)

#### PSNR (Peak Signal-to-Noise Ratio)

**Solo para imágenes/video**

**¿Qué es?**
Relación entre la señal máxima posible y el error cuadrático medio.

**Fórmula**:
```
MSE = (1/N) × Σ(Original - Reconstruida)²
PSNR = 10 × log₁₀(255² / MSE) dB
```

**Interpretación**:
- PSNR > 40 dB: Excelente (casi imperceptible)
- PSNR 30-40 dB: Buena calidad
- PSNR 20-30 dB: Calidad aceptable
- PSNR < 20 dB: Mala calidad (visible degradación)

#### SSIM (Structural Similarity Index)

**Solo para imágenes/video**

**¿Qué es?**
Mide similitud estructural (más perceptual que PSNR).

**Rango**: 0 a 1

**Interpretación**:
- SSIM = 1: Imágenes idénticas
- SSIM > 0.95: Excelente similitud
- SSIM 0.8-0.95: Buena similitud
- SSIM < 0.8: Diferencias visibles

**Ventaja sobre PSNR**:
SSIM correlaciona mejor con percepción humana.

---

## Interpretación de Resultados

### Caso 1: Transmisión Exitosa

```
Entrada: "Hola Mundo 5G"
Salida: "Hola Mundo 5G"
BER: 0.000000 (0%)
H(X): 4.52 bits
I(X;Y): 4.52 bits
```

**Interpretación**:
✅ Transmisión perfecta
✅ Sin errores de bit
✅ Toda la información se preservó (I(X;Y) = H(X))
✅ SNR suficientemente alto
✅ Codificación de canal funcionó

### Caso 2: Transmisión con Errores Leves

```
Entrada: "Hola Mundo 5G"
Salida: "Hola Mundo 5G" (algunos caracteres raros)
BER: 0.02 (2%)
H(X): 4.52 bits
I(X;Y): 4.43 bits
```

**Interpretación**:
⚠️ Algunos errores pero texto legible
⚠️ 2% de bits erróneos (aceptable para texto)
⚠️ Se perdió algo de información: 4.52 - 4.43 = 0.09 bits
💡 Sugerencia: Aumentar SNR o reducir tasa de código

### Caso 3: Transmisión Degradada

```
Entrada: "Hola Mundo 5G"
Salida: "H?l? M?nd? ?G"
BER: 0.15 (15%)
H(X): 4.52 bits
I(X;Y): 3.84 bits
```

**Interpretación**:
❌ Muchos errores
❌ 15% de bits erróneos (malo)
❌ Pérdida significativa de información: 0.68 bits (15%)
💡 Solución: 
   - Aumentar SNR (+10 dB)
   - Reducir tasa de código (0.3)
   - Usar QPSK en lugar de 64-QAM

### Caso 4: Canal Muy Ruidoso

```
Entrada: "Hola Mundo 5G"
Salida: "???????????????"
BER: 0.48 (48%)
H(X): 4.52 bits
I(X;Y): 0.23 bits
```

**Interpretación**:
❌ Transmisión fallida
❌ Casi 50% de errores (aleatorio)
❌ Pérdida casi total de información
💡 Solución:
   - Canal demasiado ruidoso
   - Aumentar SNR significativamente (+20 dB)
   - Usar tasa de código muy baja (0.3)
   - Usar QPSK (más robusto)

### Guía Rápida de Diagnóstico

| BER | I(X;Y)/H(X) | Diagnóstico | Acción |
|-----|-------------|-------------|--------|
| < 0.01 | > 95% | ✅ Excelente | Ninguna |
| 0.01-0.05 | 90-95% | ⚠️ Bueno | Considere mejorar SNR |
| 0.05-0.15 | 75-90% | ⚠️ Aceptable | Aumente SNR o reduzca tasa |
| > 0.15 | < 75% | ❌ Pobre | Configure mejor el sistema |

---

## Consejos Prácticos

### Para Experimentar

1. **Efecto del SNR**:
   - Configure todo igual
   - Varíe solo SNR: 0, 10, 20, 30 dB
   - Observe cómo mejora BER

2. **Efecto de la Modulación**:
   - SNR fijo = 15 dB
   - Pruebe: QPSK → 16-QAM → 64-QAM → 256-QAM
   - QPSK tendrá menor BER (más robusto)

3. **Efecto de la Tasa de Código**:
   - SNR bajo = 5 dB
   - Tasa 0.9 → muchos errores
   - Tasa 0.3 → menos errores (más protección)

### Configuraciones Recomendadas

**Para Texto Claro (legible)**:
```
Tipo de Red: 5G
Fuente: Texto
Modulación: QPSK o 16-QAM
SNR: 15-20 dB
Canal: AWGN
Tasa: 0.5
```

**Para Imágenes con Buena Calidad**:
```
Tipo de Red: 5G
Fuente: Imagen pequeña (< 200x200)
Modulación: 16-QAM
SNR: 20 dB
Canal: AWGN
Tasa: 0.5
```

**Para Mostrar Degradación por Ruido**:
```
Tipo de Red: 5G
Fuente: Texto
Modulación: 64-QAM
SNR: 5 dB (bajo)
Canal: Rayleigh
Tasa: 0.7
```

---

## Preguntas Frecuentes

### ¿Por qué el texto sale con caracteres raros?

**Causa**: BER alto (> 5%)
**Solución**: 
- Aumente SNR (> 15 dB)
- Use QPSK (más robusto)
- Reduzca tasa de código (0.3-0.4)

### ¿Cuál es el mejor esquema de modulación?

**No hay "el mejor"**, depende del canal:
- Canal limpio (SNR > 20 dB): 64-QAM o 256-QAM (más velocidad)
- Canal ruidoso (SNR < 10 dB): QPSK (más robusto)

### ¿Por qué hay dos parámetros de ruido (SNR y Eb/N0)?

Miden lo mismo desde perspectivas diferentes:
- **SNR**: A nivel de señal/símbolo (más intuitivo)
- **Eb/N0**: A nivel de bit (más técnico)

Para el usuario: **ajuste el SNR**. El Eb/N0 es interno.

### ¿Qué tasa de código debo usar?

Depende del SNR:
- **SNR alto (> 20 dB)**: 0.7-0.9 (poca redundancia, eficiente)
- **SNR medio (10-20 dB)**: 0.5 (balance)
- **SNR bajo (< 10 dB)**: 0.3-0.4 (mucha redundancia, robusto)

### ¿Cuándo usar Rayleigh vs Rician?

- **Rayleigh**: Ciudad, interiores, muchos obstáculos
- **Rician**: Campo abierto, visión directa
- **AWGN**: Referencia teórica (no realista pero útil)

---

## Glosario Técnico

- **LDPC**: Low-Density Parity-Check (código de corrección de errores)
- **QAM**: Quadrature Amplitude Modulation (modulación de amplitud en cuadratura)
- **QPSK**: Quadrature Phase Shift Keying (modulación por desplazamiento de fase)
- **DCT**: Discrete Cosine Transform (transformada discreta del coseno)
- **MDCT**: Modified DCT (DCT modificada para audio)
- **LLR**: Log-Likelihood Ratio (razón de verosimilitud logarítmica)
- **BER**: Bit Error Rate (tasa de error de bit)
- **SNR**: Signal-to-Noise Ratio (relación señal a ruido)
- **Eb/N0**: Energy per bit to noise density (energía por bit a densidad de ruido)
- **AWGN**: Additive White Gaussian Noise (ruido blanco gaussiano aditivo)
- **LOS**: Line-of-Sight (línea de vista)
- **NLOS**: Non-Line-of-Sight (sin línea de vista)

---

**Versión**: 1.0  
**Fecha**: Noviembre 2025  
**Para más información**: Consulte USER_GUIDE.md y TECHNICAL_DOCUMENTATION.md

# Soporte de Video en el Simulador 5G/6G

## Resumen de Cambios (Commit da01d96 + Nuevo)

El simulador ahora soporta la carga y procesamiento de archivos de video reales, además de la generación de frames sintéticos.

## Características Implementadas

### 1. Carga de Video Real

**Formatos Soportados:**
- MP4 (`.mp4`)
- AVI (`.avi`)
- MOV (`.mov`)
- MKV (`.mkv`)
- WebM (`.webm`)

**Funcionalidad:**
- Carga de archivos de video de hasta varios MB
- Extracción de información del video:
  - Resolución (ancho × alto)
  - Total de frames
  - FPS (frames por segundo)
  - Duración total
- Selección de frame específico para simular
- Visualización del frame seleccionado

### 2. Procesamiento de Frames

**Pipeline:**
1. **Carga**: El usuario sube un archivo de video
2. **Análisis**: Se extraen propiedades del video
3. **Selección**: Slider permite elegir cualquier frame
4. **Extracción**: Se extrae el frame seleccionado en formato RGB
5. **Simulación**: El frame pasa por el pipeline completo de 7 etapas
6. **Comparación**: Se muestran lado a lado el frame original y recibido

### 3. Frames Sintéticos

Para pruebas rápidas, sigue disponible la opción de generar frames sintéticos aleatorios de 64×64 píxeles.

## Uso del Simulador con Video

### Opción 1: Video Real

1. **Seleccione "Video" como Tipo de Fuente**
2. **Clic en "Browse files"** bajo "Cargar video"
3. **Seleccione un archivo de video** (recomendado: < 10 MB para carga rápida)
4. **Espere la carga** - verá:
   ```
   ✓ Video cargado: 1920x1080, 300 frames, 30.0 FPS
   ```
5. **Use el slider** para seleccionar el frame a simular
6. **Visualice el frame** seleccionado en la interfaz
7. **Clic en "🚀 Iniciar Simulación"**

### Opción 2: Frame Sintético

1. **Seleccione "Video" como Tipo de Fuente**
2. **Clic en "Generar Frame Sintético"**
3. **Clic en "🚀 Iniciar Simulación"**

## Ejemplos de Uso

### Caso 1: Video de Baja Resolución (Óptimo)

```
Entrada: video_test_640x480.mp4
Resolución: 640×480
Frames: 150
FPS: 30
Tamaño: 2.5 MB

Resultado:
- Carga instantánea
- Extracción rápida de frames
- Simulación completa en segundos
```

### Caso 2: Video HD (Funcional)

```
Entrada: video_hd_1920x1080.mp4
Resolución: 1920×1080
Frames: 900
FPS: 30
Tamaño: 8 MB

Resultado:
- Carga en 3-5 segundos
- Frame se redimensiona a 64×64 para procesamiento
- Métricas PSNR/SSIM comparables
```

### Caso 3: Video 4K (No Recomendado)

```
Entrada: video_4k.mp4
Resolución: 3840×2160
Tamaño: > 50 MB

Problema:
- Carga lenta en Streamlit
- Alto uso de memoria
- Recomendación: convertir a resolución menor primero
```

## Métricas para Video

Cuando se simula un frame de video, se calculan las siguientes métricas:

### Teoría de la Información
- **H(X)**: Entropía de entrada (bits)
- **H(Y)**: Entropía de salida (bits)
- **I(X;Y)**: Información mutua (bits)

### Integridad de Datos
- **BER**: Bit Error Rate (tasa de error de bits)
- **Tasa de Bits Correctos**: Porcentaje de bits sin errores

### Calidad de Imagen (PSNR y SSIM)
- **PSNR**: Peak Signal-to-Noise Ratio (dB)
  - > 30 dB: Excelente calidad
  - 20-30 dB: Buena calidad
  - < 20 dB: Calidad degradada
- **SSIM**: Structural Similarity Index
  - > 0.9: Muy similar al original
  - 0.7-0.9: Similar
  - < 0.7: Diferencias notables

### Información Adicional del Video
- Resolución original
- Número de frame actual / total
- FPS del video

## Tecnología Utilizada

### OpenCV (cv2)
- **Propósito**: Lectura y procesamiento de video
- **Versión**: >= 4.8.0
- **Funciones clave**:
  - `cv2.VideoCapture()`: Abre archivos de video
  - `cv2.VideoWriter()`: Crea archivos de video
  - `cap.get(cv2.CAP_PROP_*)`: Extrae propiedades
  - `cap.set(cv2.CAP_PROP_POS_FRAMES)`: Salta a frame específico
  - `cap.read()`: Lee frame actual

### Codificación de Video

El frame seleccionado se procesa usando codificación **H.265-like simplificada**:

1. **Conversión a escala de grises** (simplificación educativa)
2. **Transformada DCT en bloques 8×8**
3. **Cuantización con factor /2** (buena calidad)
4. **Conversión a bits** (8 bits por coeficiente)

### Decodificación de Video

1. **Conversión de bits a coeficientes**
2. **Dequantización** (multiplicación por 2)
3. **IDCT inversa** (reconstrucción espacial)
4. **Clipping** a rango [0, 255]

## Calidad Esperada

### Condiciones Perfectas (BER=0%, SNR alto)

```
PSNR: 20-25 dB
SSIM: 0.75-0.90
Calidad Visual: Buena (similar a video comprimido H.264)
```

**Nota**: La compresión DCT es **intencional** y simula codec de video real. Incluso con transmisión perfecta (BER=0%), habrá cierta pérdida por la compresión.

### Con Ruido de Canal (SNR moderado)

```
SNR 10 dB:
- PSNR: 15-18 dB
- SSIM: 0.60-0.75
- Degradación visible pero imagen reconocible

SNR 5 dB:
- PSNR: 10-15 dB
- SSIM: 0.40-0.60
- Degradación significativa, posible pixelación

SNR 0 dB:
- PSNR: < 10 dB
- SSIM: < 0.40
- Imagen muy degradada, difícil de reconocer
```

## Resolución de Problemas

### Problema: "OpenCV no instalado"

**Solución:**
```bash
pip install opencv-python>=4.8.0
```

### Problema: Video no se carga

**Causas posibles:**
1. Formato no soportado → Convertir a MP4/AVI
2. Archivo muy grande → Reducir tamaño/resolución
3. Codec no disponible → Reinstalar OpenCV

**Solución:**
```bash
# Convertir video con ffmpeg
ffmpeg -i input.mkv -vcodec libx264 -acodec aac output.mp4

# Reducir resolución
ffmpeg -i input.mp4 -vf scale=640:480 output_small.mp4
```

### Problema: Carga muy lenta

**Optimizaciones:**
1. Usar videos < 10 MB
2. Reducir resolución antes de cargar
3. Usar formatos comprimidos (MP4 con H.264)

### Problema: Frame no se extrae

**Verificación:**
```python
import cv2
cap = cv2.VideoCapture('video.mp4')
print(cap.isOpened())  # Debe ser True
print(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Total de frames
```

## Comparación: Antes vs Después

### Antes (Commit da01d96)

```
✗ Solo frames sintéticos aleatorios
✗ No se podían probar videos reales
✗ Resolución fija 64×64
✗ Sin información de video
✗ Limitado para demostraciones
```

### Después (Commit Actual)

```
✓ Carga de archivos de video reales
✓ Múltiples formatos soportados
✓ Extracción de cualquier frame
✓ Información completa del video
✓ Comparación lado a lado
✓ Métricas PSNR/SSIM para video
✓ Ideal para demostraciones educativas
```

## Ejemplo Completo de Simulación

### Configuración Recomendada

```
Tipo de Red: 5G
Tipo de Fuente: Video
Esquema de Modulación: 16-QAM
SNR: 15 dB
Eb/N0: 10 dB
Canal: AWGN (Sin desvanecimiento)
Tasa de Código: 0.7
```

### Flujo de Trabajo

1. **Cargar video**: `demo_640x480.mp4`
2. **Seleccionar frame**: Frame 45 (escena interesante)
3. **Iniciar simulación**
4. **Observar**:
   - Pipeline de 7 etapas visualizado
   - Frame original vs recibido lado a lado
   - Métricas: BER, PSNR, SSIM
   - Información del video

### Resultados Típicos

```
📊 RESULTADOS

Frame Original: [Mostrado a la izquierda]
Frame Recibido: [Mostrado a la derecha]

Teoría de la Información:
- H(X): 0.8234 bits
- H(Y): 0.8198 bits
- I(X;Y): 0.8150 bits

Integridad de Datos:
- BER: 0.002100 (0.21%)
- Tasa de Bits Correctos: 99.79%

Calidad de Video:
- PSNR: 22.45 dB
- SSIM: 0.8123

Información del Video:
- Resolución: 640×480
- Frame: 45/299
- FPS: 30.0
```

## Casos de Uso Educativos

### 1. Efecto del SNR en Calidad de Video

Comparar el mismo frame con diferentes SNR:
- SNR 20 dB: PSNR ~25 dB (excelente)
- SNR 10 dB: PSNR ~18 dB (bueno)
- SNR 5 dB: PSNR ~12 dB (pobre)

### 2. Comparación de Modulaciones

Mismo frame, diferentes modulaciones:
- QPSK: Más robusto, menor throughput
- 256-QAM: Más eficiente, más sensible al ruido

### 3. Efecto de Tasa de Código

- Tasa 0.3: Más redundancia, mejor calidad con ruido
- Tasa 0.9: Menos redundancia, más eficiente pero vulnerable

### 4. Canales con Desvanecimiento

- AWGN: Calidad consistente
- Rayleigh: Calidad variable (simula NLOS)
- Rician: Intermedio (simula LOS parcial)

## Limitaciones y Consideraciones

### Limitaciones Técnicas

1. **Procesamiento por Frame**
   - Solo se simula un frame a la vez
   - No se simulan múltiples frames consecutivos
   - No hay compresión inter-frame (como en video real)

2. **Resolución**
   - Frames se redimensionan a 64×64 para simulación
   - Pérdida de detalles en videos HD/4K

3. **Compresión Simplificada**
   - DCT básica, no H.265 completo
   - Sin motion estimation
   - Sin rate control

### Consideraciones de Rendimiento

1. **Tamaño de Archivo**
   - Óptimo: < 10 MB
   - Máximo recomendado: 20 MB
   - Muy grande (> 50 MB): Lento o error de memoria

2. **Resolución**
   - Óptimo: 640×480 o menor
   - Aceptable: 1920×1080
   - Problemático: 4K o superior

3. **Duración**
   - No afecta directamente (solo se usa 1 frame)
   - Pero más frames = archivo más grande

## Referencias

### Documentación OpenCV
- [VideoCapture Class](https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html)
- [Video Codec List](https://docs.opencv.org/4.x/dd/d9e/classcv_1_1VideoWriter.html)

### Estándares de Video
- **H.264/AVC**: ISO/IEC 14496-10
- **H.265/HEVC**: ISO/IEC 23008-2
- **VP9**: Google WebM Project

### Métricas de Calidad
- **PSNR**: Peak Signal-to-Noise Ratio (dB)
- **SSIM**: Structural Similarity Index (IEEE TIP 2004)
- **VMAF**: Video Multimethod Assessment Fusion (Netflix)

## Conclusión

El simulador ahora ofrece soporte completo para procesamiento de video real, permitiendo:
- ✅ Carga de archivos de video en múltiples formatos
- ✅ Selección flexible de frames
- ✅ Simulación realista del pipeline 5G/6G
- ✅ Métricas completas de calidad
- ✅ Comparación visual lado a lado
- ✅ Información detallada del video

Esto hace al simulador mucho más útil para demostraciones educativas y análisis de calidad de transmisión de video en redes móviles modernas.

# 🚀 Simulador de Técnicas de Codificación 5G/6G

## Resumen Ejecutivo

Este simulador educativo implementa el pipeline completo de comunicaciones digitales para redes 5G, 5G Avanzado y 6G, incluyendo:

- ✅ **Codificación de Fuente**: Huffman (texto), DCT (imagen), MDCT (audio), H.265 (video)
- ✅ **Codificación de Canal**: LDPC para 5G/5G-A
- ✅ **Modulación Digital**: QPSK, 16-QAM, 64-QAM, 256-QAM
- ✅ **Canal Inalámbrico**: AWGN, Rayleigh, Rician con ruido configurable
- ✅ **Demodulación Suave**: Cálculo de LLR (Log-Likelihood Ratio)
- ✅ **Métricas**: BER, PSNR, SSIM, Entropía, Información Mutua
- ✅ **Visualización**: Diagramas de constelación, LLR, flujos de bits
- ✅ **Interfaz Gráfica**: Streamlit fácil de usar

## 📁 Estructura del Proyecto

```
simulador-tecnicas-codificacion-python/
├── simulador.py                     # Aplicación principal (GUI)
├── modules/                         # Módulos del simulador
│   ├── __init__.py
│   ├── source_encoder.py           # Codificación de fuente
│   ├── channel_encoder.py          # LDPC
│   ├── modulator.py                # QPSK, QAM
│   ├── channel.py                  # Canal inalámbrico
│   ├── demodulator.py              # LLR
│   ├── channel_decoder.py          # Decodificación LDPC
│   ├── source_decoder.py           # Decodificación de fuente
│   ├── metrics.py                  # Métricas (BER, PSNR, Entropía)
│   └── visualizer.py               # Gráficos
├── requirements.txt                # Dependencias Python
├── CHANGELOG.md                    # Historial de cambios
├── USER_GUIDE.md                   # Guía del usuario (COMPLETA)
├── TECHNICAL_DOCUMENTATION.md      # Documentación técnica (COMPLETA)
├── TEST_CASES.md                   # Casos de prueba (COMPLETO)
├── test_modules.py                 # Script de prueba
└── README.md (original)            # Investigación teórica
```

## 🔧 Instalación Rápida

### Requisitos Previos
- Python 3.8 o superior
- pip

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/MAKEOUTHILL629/simulador-tecnicas-codificacion-python.git
cd simulador-tecnicas-codificacion-python
```

### Paso 2: Instalar dependencias

```bash
pip install -r requirements.txt
```

Dependencias necesarias:
- `numpy`: Operaciones numéricas
- `scipy`: Funciones científicas
- `matplotlib`: Visualización
- `streamlit`: Interfaz web interactiva
- `Pillow`: Procesamiento de imágenes
- `scikit-image`: Métricas de calidad (SSIM)

### Paso 3: Ejecutar el simulador

```bash
streamlit run simulador.py
```

El simulador se abrirá en su navegador en `http://localhost:8501`

## 🎯 Uso Rápido

### Ejemplo 1: Transmitir Texto

1. Abrir el simulador
2. Seleccionar **"5G"** como red
3. Seleccionar **"Texto"** como fuente
4. Ingresar texto: "Hola Mundo 5G"
5. Configurar SNR: 15 dB
6. Clic en **"🚀 Iniciar Simulación"**
7. Ver resultados en 7 etapas:
   - Codificación de fuente
   - Codificación de canal (LDPC)
   - Modulación (constelación)
   - Canal (ruido)
   - Demodulación (LLR)
   - Decodificación de canal
   - Salida reconstruida

### Ejemplo 2: Transmitir Imagen

1. Seleccionar **"Imagen"** como fuente
2. Cargar una imagen (PNG/JPG)
3. Configurar SNR: 20 dB
4. Modulación: 16-QAM
5. Iniciar simulación
6. Comparar imagen original vs recibida
7. Ver métricas: PSNR, SSIM

## 📊 Características Principales

### Pipeline de 7 Etapas

```
Entrada → Codificación Fuente → Codificación Canal → Modulación → 
Canal → Demodulación → Decodificación Canal → Decodificación Fuente → Salida
```

### Tipos de Red

- **5G**: Estándar con LDPC y modulación adaptativa
- **5G Avanzado (URLLC)**: Ultra-baja latencia, alta confiabilidad
- **6G (JSCC)**: Codificación conjunta fuente-canal

### Tipos de Fuente

- **Texto**: Codificación Huffman
- **Imagen**: Codificación DCT (similar a JPEG)
- **Audio**: Codificación MDCT (similar a AAC)
- **Video**: Codificación H.265 simplificada

### Modulaciones Soportadas

| Modulación | Bits/Símbolo | Robustez | Eficiencia |
|------------|--------------|----------|------------|
| QPSK       | 2            | Alta     | Baja       |
| 16-QAM     | 4            | Media    | Media      |
| 64-QAM     | 6            | Baja     | Alta       |
| 256-QAM    | 8            | Muy Baja | Muy Alta   |

### Modelos de Canal

- **AWGN**: Solo ruido blanco gaussiano
- **Rayleigh**: Desvanecimiento NLOS (sin línea de vista)
- **Rician**: Desvanecimiento LOS (con línea de vista)

### Métricas Calculadas

**Teoría de la Información:**
- H(X): Entropía de entrada
- H(Y): Entropía de salida
- I(X;Y): Información mutua

**Integridad:**
- BER: Bit Error Rate
- BLER: Block Error Rate

**Calidad de Imagen:**
- PSNR: Peak Signal-to-Noise Ratio
- SSIM: Structural Similarity Index

## 📚 Documentación

### Para Usuarios
- **[USER_GUIDE.md](USER_GUIDE.md)**: Guía completa de usuario
  - Instalación detallada
  - Configuración
  - Ejemplos paso a paso
  - Interpretación de resultados
  - Solución de problemas

### Para Desarrolladores
- **[TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md)**: Documentación técnica
  - Arquitectura del sistema
  - Fundamentos teóricos
  - Algoritmos implementados
  - APIs de módulos
  - Consideraciones de diseño

### Para Testing
- **[TEST_CASES.md](TEST_CASES.md)**: Casos de prueba
  - Casos funcionales
  - Casos de rendimiento
  - Casos de integración
  - Validación científica
  - Resultados esperados

### Control de Versiones
- **[CHANGELOG.md](CHANGELOG.md)**: Historial de cambios

## 🎓 Uso Educativo

### Para Presentaciones en Clase

El simulador es ideal para explicar:

1. **Teoría de la Información**
   - Entropía de Shannon
   - Capacidad del canal
   - Teorema de separación

2. **Técnicas de Codificación**
   - Códigos de compresión (Huffman, DCT)
   - Códigos de canal (LDPC)

3. **Modulación Digital**
   - Constelaciones I/Q
   - Trade-off robustez vs eficiencia

4. **Canales Inalámbricos**
   - Ruido AWGN
   - Desvanecimiento
   - Relación SNR vs calidad

### Ejemplos de Demostraciones

**Demo 1: Efecto del Ruido**
- Transmitir mismo texto con SNR=20dB, 10dB, 0dB
- Mostrar degradación progresiva del BER
- Explicar concepto de SNR

**Demo 2: Comparación de Modulaciones**
- Transmitir imagen con QPSK, 16-QAM, 64-QAM
- Comparar PSNR y constelaciones
- Explicar trade-off

**Demo 3: Protección de Canal**
- Transmitir con tasas de código 0.3, 0.5, 0.9
- Mostrar balance entre overhead y robustez
- Explicar codificación de canal

## 🔬 Fundamentos Teóricos

### Basado en Investigación IEEE

El simulador implementa técnicas descritas en:
- 3GPP TS 38.212 (LDPC para 5G)
- 3GPP TS 38.214 (Modulación y codificación)
- Papers de DeepJSCC (para 6G)

### Ecuaciones Clave Implementadas

**Capacidad de Shannon:**
```
C = B · log₂(1 + SNR)
```

**Entropía:**
```
H(X) = -Σ p(xᵢ) · log₂(p(xᵢ))
```

**PSNR:**
```
PSNR = 10 · log₁₀(MAX²/MSE)
```

**LLR:**
```
L(b|y) = log(P(b=0|y) / P(b=1|y))
```

## ⚠️ Limitaciones y Notas

### Simplificaciones Educativas

- LDPC usa codificación simplificada (no matrices 3GPP exactas)
- Sin rate matching completo
- Sin interleaving de bits
- 6G usa modulación base (no redes neuronales reales)
- Video es tratado como secuencia de imágenes

### Recomendaciones de Uso

- Usar textos cortos (< 100 caracteres)
- Usar imágenes pequeñas (< 128×128 píxeles)
- SNR recomendado: 10-20 dB para demos
- Para imágenes, usar SNR > 15 dB

## 🐛 Solución de Problemas

### Error: "Module not found"
```bash
pip install -r requirements.txt --upgrade
```

### Simulación muy lenta
- Reducir tamaño de entrada
- Usar textos más cortos
- Usar imágenes más pequeñas

### Interfaz no carga
```bash
streamlit cache clear
streamlit run simulador.py
```

## 🤝 Contribuciones

Este es un proyecto educativo. Para mejoras:
1. Fork el repositorio
2. Cree una rama para su feature
3. Commit sus cambios
4. Push a la rama
5. Abra un Pull Request

## 📄 Licencia

Proyecto educativo para propósitos académicos.

## 👨‍💻 Autor

Desarrollado como herramienta educativa para explicar técnicas de codificación en redes de comunicaciones móviles 5G y 6G.

## 📞 Soporte

Para problemas o preguntas:
- Abrir un issue en GitHub
- Revisar la documentación en USER_GUIDE.md
- Consultar casos de prueba en TEST_CASES.md

---

## 🚀 Inicio Rápido (TL;DR)

```bash
# 1. Clonar
git clone https://github.com/MAKEOUTHILL629/simulador-tecnicas-codificacion-python.git
cd simulador-tecnicas-codificacion-python

# 2. Instalar
pip install -r requirements.txt

# 3. Ejecutar
streamlit run simulador.py

# 4. Usar
# - Abrir http://localhost:8501
# - Seleccionar 5G + Texto
# - Ingresar "Hola Mundo"
# - Clic en Iniciar Simulación
# - Ver resultados!
```

---

**¡Disfrute explorando las técnicas de codificación de 5G y 6G!** 📡✨

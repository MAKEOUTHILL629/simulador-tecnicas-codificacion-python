# Guía de Usuario - Simulador 5G/6G

## 📋 Índice
1. [Introducción](#introducción)
2. [Requisitos del Sistema](#requisitos-del-sistema)
3. [Instalación](#instalación)
4. [Inicio Rápido](#inicio-rápido)
5. [Configuración](#configuración)
6. [Uso del Simulador](#uso-del-simulador)
7. [Interpretación de Resultados](#interpretación-de-resultados)
8. [Ejemplos de Uso](#ejemplos-de-uso)
9. [Solución de Problemas](#solución-de-problemas)

## Introducción

Bienvenido al Simulador de Técnicas de Codificación para Redes 5G, 5G Avanzado y 6G. Esta herramienta educativa permite simular el proceso completo de transmisión digital, desde la codificación de la fuente hasta la decodificación final, pasando por todas las etapas intermedias.

### ¿Qué puede hacer el simulador?

- Simular transmisión de **texto, imágenes, audio y video**
- Aplicar técnicas de **codificación de fuente** (Huffman, DCT, MDCT, H.265)
- Implementar **codificación de canal LDPC** para 5G/5G-A
- Utilizar diferentes esquemas de **modulación** (QPSK, 16-QAM, 64-QAM, 256-QAM)
- Simular **canales inalámbricos** con ruido y desvanecimiento
- Calcular **métricas de calidad** e integridad
- **Visualizar cada etapa** del proceso de transmisión

## Requisitos del Sistema

### Software Necesario
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Espacio en Disco
- Mínimo: 500 MB
- Recomendado: 1 GB

### RAM
- Mínimo: 4 GB
- Recomendado: 8 GB

## Instalación

### Paso 1: Clonar o descargar el repositorio

```bash
git clone https://github.com/MAKEOUTHILL629/simulador-tecnicas-codificacion-python.git
cd simulador-tecnicas-codificacion-python
```

### Paso 2: Instalar dependencias

```bash
pip install -r requirements.txt
```

Las dependencias incluyen:
- `numpy`: Operaciones numéricas
- `scipy`: Funciones científicas
- `matplotlib`: Visualización
- `streamlit`: Interfaz gráfica
- `Pillow`: Procesamiento de imágenes
- `scikit-image`: Métricas de calidad de imagen

### Paso 3: Verificar instalación

```bash
python -c "import streamlit; import numpy; import scipy; import matplotlib; import PIL; print('Instalación exitosa!')"
```

## Inicio Rápido

### Ejecutar el simulador

```bash
streamlit run simulador.py
```

El simulador se abrirá automáticamente en su navegador web en `http://localhost:8501`

### Primera simulación

1. Seleccione **"5G"** como tipo de red
2. Seleccione **"Texto"** como tipo de fuente
3. Escriba un texto corto: "Hola Mundo 5G"
4. Configure SNR en **10 dB**
5. Haga clic en **"🚀 Iniciar Simulación"**

¡Listo! Verá el proceso completo de transmisión visualizado paso a paso.

## Configuración

### Panel de Configuración (Barra Lateral)

#### 1. Tipo de Red
- **5G**: Estándar 5G con codificación LDPC
- **5G Avanzado (URLLC)**: Para aplicaciones de ultra-baja latencia
- **6G (JSCC)**: Modo experimental con codificación conjunta

#### 2. Tipo de Fuente
- **Texto**: Para mensajes de texto
- **Imagen**: Para archivos PNG, JPG, JPEG
- **Audio**: Señales de audio sintéticas
- **Video**: Frames de video (simplificado)

#### 3. Esquema de Modulación
Disponible según el tipo de red:
- **QPSK**: 2 bits/símbolo, más robusto
- **16-QAM**: 4 bits/símbolo
- **64-QAM**: 6 bits/símbolo
- **256-QAM**: 8 bits/símbolo, mayor capacidad

#### 4. Parámetros del Canal

**SNR (Relación Señal a Ruido)**
- Rango: -10 a 30 dB
- Recomendado para buena calidad: 10-20 dB
- Valores bajos (< 5 dB): mucho ruido
- Valores altos (> 20 dB): canal limpio

**Eb/N0 (Energía de bit a densidad de ruido)**
- Rango: -5 a 25 dB
- Similar al SNR pero normalizado por bit

**Modelo de Desvanecimiento**
- **AWGN**: Solo ruido blanco, sin desvanecimiento
- **Rayleigh (NLOS)**: Sin línea de vista directa
- **Rician (LOS)**: Con línea de vista directa
  - Factor K: Relación entre componente LOS y NLOS

#### 5. Tasa de Código (5G/5G-A)
- Rango: 0.3 a 0.9
- Valores bajos: más redundancia, más robusto
- Valores altos: menos redundancia, más eficiente

## Uso del Simulador

### Simulación de Texto

1. Seleccione **"Texto"** como fuente
2. Ingrese su mensaje en el área de texto
3. Configure los parámetros del canal
4. Haga clic en **"🚀 Iniciar Simulación"**

**Recomendaciones:**
- Use textos cortos (10-100 caracteres) para simulación rápida
- Pruebe diferentes SNR para ver el efecto del ruido

### Simulación de Imagen

1. Seleccione **"Imagen"** como fuente
2. Haga clic en **"Browse files"** para cargar una imagen
3. Formatos soportados: PNG, JPG, JPEG
4. Configure los parámetros
5. Inicie la simulación

**Recomendaciones:**
- Use imágenes pequeñas (< 500x500 px) para procesamiento rápido
- Las imágenes se convierten a escala de grises
- SNR alto (> 15 dB) para mejor calidad visual

### Simulación de Audio

1. Seleccione **"Audio"** como fuente
2. Configure duración y frecuencia de la señal sintética
3. Haga clic en **"Generar Audio"**
4. Configure parámetros del canal
5. Inicie la simulación

**Recomendaciones:**
- Duración corta (0.5-1 segundo) para simulación rápida
- Frecuencias de 300-1000 Hz son audibles y visibles

### Simulación de Video

1. Seleccione **"Video"** como fuente
2. Haga clic en **"Generar Frame"** (genera frame sintético)
3. Configure parámetros
4. Inicie la simulación

**Nota:** La simulación de video es simplificada y trata cada frame como una imagen.

## Interpretación de Resultados

### Pipeline de Procesamiento (7 Etapas)

#### 1️⃣ Codificación de Fuente
- **Visualización**: Flujo de bits de entrada
- **Qué observar**: Número de bits generados
- **Interpretación**: Más bits = mayor información

#### 2️⃣ Codificación de Canal (LDPC)
- **Visualización**: Bits con redundancia añadida
- **Qué observar**: Overhead (bits adicionales)
- **Interpretación**: Overhead alto = mayor protección contra errores

#### 3️⃣ Modulación
- **Visualización**: Diagrama de constelación
- **Qué observar**: Distribución de puntos I/Q
- **Interpretación**: 
  - Puntos bien definidos = buena modulación
  - Constelación más densa = mayor capacidad

#### 4️⃣ Canal Inalámbrico
- **Visualización**: Señal recibida con ruido
- **Qué observar**: "Nube" de ruido alrededor de los puntos
- **Interpretación**:
  - Nube pequeña = poco ruido, buena calidad
  - Nube grande = mucho ruido, canal deteriorado

#### 5️⃣ Demodulación (LLR)
- **Visualización**: Histograma de valores LLR
- **Qué observar**: Distribución de LLRs
- **Interpretación**:
  - LLR > 0: Bit probablemente es 0
  - LLR < 0: Bit probablemente es 1
  - |LLR| grande: Alta confianza
  - |LLR| pequeño: Baja confianza

#### 6️⃣ Decodificación de Canal
- **Visualización**: Bits recuperados
- **Qué observar**: Comparación con bits originales
- **Interpretación**: Similitud indica buena recuperación

#### 7️⃣ Decodificación de Fuente
- **Visualización**: Salida reconstruida
- **Qué observar**: Calidad de la reconstrucción
- **Interpretación**: 
  - Texto: Caracteres correctos vs incorrectos
  - Imagen: Similitud visual

### Métricas de Integridad

#### Teoría de la Información

**H(X) - Entropía de Entrada**
- Rango: 0 a log₂(alfabeto)
- Interpretación: Cantidad promedio de información
- Valor alto: Fuente muy variable (bueno)
- Valor bajo: Fuente predecible

**H(Y) - Entropía de Salida**
- Similar a H(X)
- Idealmente cercana a H(X)

**I(X;Y) - Información Mutua**
- Rango: 0 a H(X)
- Interpretación: Información compartida entre entrada y salida
- I(X;Y) ≈ H(X): Transmisión casi perfecta
- I(X;Y) << H(X): Mucha pérdida de información

#### Integridad de Datos

**BER (Bit Error Rate)**
- Rango: 0 a 1
- Interpretación: Proporción de bits erróneos
- BER < 0.001: Excelente
- BER < 0.01: Bueno
- BER > 0.1: Pobre

**Tasa de Bits Correctos**
- Rango: 0% a 100%
- Complemento del BER
- > 99%: Excelente
- 90-99%: Bueno
- < 90%: Pobre

#### Métricas de Imagen (si aplica)

**PSNR (Peak Signal-to-Noise Ratio)**
- Unidad: dB
- Interpretación: Calidad de reconstrucción
- PSNR > 40 dB: Excelente
- PSNR 30-40 dB: Bueno
- PSNR < 30 dB: Pobre

**SSIM (Structural Similarity Index)**
- Rango: 0 a 1
- Interpretación: Similitud estructural
- SSIM > 0.95: Excelente
- SSIM 0.8-0.95: Bueno
- SSIM < 0.8: Pobre

## Ejemplos de Uso

### Ejemplo 1: Comparación de Modulaciones

**Objetivo:** Ver cómo afecta el tipo de modulación a la calidad

1. Configure: 5G, Texto, SNR=15 dB
2. Ejecute con QPSK y anote el BER
3. Ejecute con 16-QAM y anote el BER
4. Ejecute con 64-QAM y anote el BER
5. Compare resultados

**Resultado esperado:** QPSK tendrá menor BER (más robusto)

### Ejemplo 2: Efecto del Ruido

**Objetivo:** Observar degradación con ruido

1. Configure: 5G, Imagen pequeña, QPSK
2. Ejecute con SNR=20 dB (anote PSNR)
3. Ejecute con SNR=10 dB (anote PSNR)
4. Ejecute con SNR=0 dB (anote PSNR)
5. Compare imágenes recibidas

**Resultado esperado:** Calidad disminuye con SNR bajo

### Ejemplo 3: Desvanecimiento

**Objetivo:** Comparar tipos de canal

1. Configure: 5G, Texto, QPSK, SNR=15 dB
2. Ejecute con AWGN (anote BER)
3. Ejecute con Rayleigh (anote BER)
4. Ejecute con Rician K=10 (anote BER)
5. Compare

**Resultado esperado:** Rayleigh tiene mayor BER que AWGN

### Ejemplo 4: Tasa de Código

**Objetivo:** Balance entre eficiencia y robustez

1. Configure: 5G, Texto, QPSK, SNR=10 dB
2. Ejecute con tasa=0.3 (mucha redundancia)
3. Ejecute con tasa=0.7 (poca redundancia)
4. Compare BER y overhead

**Resultado esperado:** Tasa baja = mayor overhead pero menor BER

## Solución de Problemas

### Error: "Module not found"
**Solución:** Reinstale las dependencias
```bash
pip install -r requirements.txt --upgrade
```

### La simulación es muy lenta
**Soluciones:**
- Use textos más cortos (< 50 caracteres)
- Use imágenes más pequeñas (< 128x128 px)
- Reduzca la duración del audio
- Cierre otras aplicaciones

### Los resultados no tienen sentido
**Verificaciones:**
- Asegúrese de que el SNR no sea extremadamente bajo (< -5 dB)
- Verifique que ingresó datos de entrada válidos
- Reinicie el simulador

### La interfaz no carga
**Solución:**
```bash
streamlit cache clear
streamlit run simulador.py
```

### Error de memoria
**Solución:**
- Reduzca el tamaño de los datos de entrada
- Cierre otras aplicaciones
- Reinicie el sistema

### Resultados inconsistentes
**Causa:** Naturaleza estocástica del ruido
**Solución:** Ejecute la simulación varias veces y tome el promedio

## Consejos para Presentaciones en Clase

1. **Prepare ejemplos simples**: Use textos cortos o imágenes pequeñas
2. **Compare escenarios**: Muestre el efecto de cambiar un parámetro
3. **Use visualizaciones**: Los diagramas de constelación son muy ilustrativos
4. **Explique las métricas**: BER, PSNR y SSIM son fáciles de entender
5. **Demuestre robustez**: Muestre cómo el código protege contra errores
6. **Tenga capturas de pantalla**: Por si hay problemas técnicos

## Contacto y Soporte

Para reportar errores o sugerir mejoras, por favor:
1. Abra un issue en el repositorio de GitHub
2. Incluya capturas de pantalla
3. Describa los pasos para reproducir el problema
4. Indique la versión de Python y dependencias

---

**¡Disfrute explorando las técnicas de codificación digital!** 📡

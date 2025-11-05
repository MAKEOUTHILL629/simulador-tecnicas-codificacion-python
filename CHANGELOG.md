# CHANGELOG

Todos los cambios notables de este proyecto serán documentados en este archivo.

## [1.0.0] - 2025-11-05

### Añadido
- Implementación inicial del simulador de técnicas de codificación 5G/6G
- Interfaz gráfica con Streamlit para facilidad de uso
- Módulo de codificación de fuente:
  - Codificación Huffman para texto
  - Codificación DCT para imágenes (similar a JPEG)
  - Codificación MDCT para audio (similar a AAC)
  - Codificación H.265 simplificada para video
- Módulo de codificación de canal:
  - Implementación LDPC simplificada para 5G y 5G Avanzado
  - Soporte para diferentes tasas de código (0.3 a 0.9)
- Módulo de modulación:
  - QPSK (4 símbolos, 2 bits/símbolo)
  - 16-QAM (16 símbolos, 4 bits/símbolo)
  - 64-QAM (64 símbolos, 6 bits/símbolo)
  - 256-QAM (256 símbolos, 8 bits/símbolo)
- Módulo de canal inalámbrico:
  - Canal AWGN (sin desvanecimiento)
  - Canal Rayleigh (NLOS)
  - Canal Rician (LOS) con factor K configurable
  - Parámetros configurables: SNR, Eb/N0
- Módulo de demodulación:
  - Demodulación suave con cálculo de LLR (Log-Likelihood Ratio)
  - Aproximación Max-Log-MAP para eficiencia computacional
- Módulo de decodificación de canal:
  - Decodificador LDPC simplificado con corrección de errores
  - Decisión dura sobre LLRs
- Módulo de decodificación de fuente:
  - Decodificadores inversos para cada tipo de fuente
  - Reconstrucción de texto, imágenes, audio y video
- Módulo de métricas:
  - Métricas de teoría de la información: Entropía H(X), Información Mutua I(X;Y)
  - Métricas de integridad: BER, BLER
  - Métricas de calidad para imágenes: PSNR, SSIM
- Módulo de visualización:
  - Gráficos de flujo de bits
  - Diagramas de constelación I/Q
  - Histogramas de LLR
  - Visualización de señales de audio
  - Comparación de imágenes
- Sistema de configuración inteligente:
  - Adaptación automática según tipo de red (5G, 5G-A, 6G)
  - Restricciones de modulación según tipo de red
  - Selección de parámetros optimizados
- Pipeline completo de simulación con 7 etapas:
  1. Codificación de fuente
  2. Codificación de canal
  3. Modulación
  4. Transmisión por canal
  5. Demodulación
  6. Decodificación de canal
  7. Decodificación de fuente
- Visualización de cada etapa del pipeline
- Cálculo y visualización de métricas de rendimiento
- Documentación completa:
  - Guía de usuario (USER_GUIDE.md)
  - Documentación técnica (TECHNICAL_DOCUMENTATION.md)
  - Casos de prueba (TEST_CASES.md)
- Archivo requirements.txt con dependencias necesarias

### Características
- Interfaz intuitiva y fácil de usar
- Simulación en tiempo real con barra de progreso
- Soporte para múltiples tipos de fuente: texto, imagen, audio, video
- Visualización detallada de cada etapa del proceso
- Cálculo exhaustivo de métricas de calidad
- Diseño modular y extensible
- Basado en investigación académica rigurosa (IEEE)

### Notas Técnicas
- La implementación LDPC es simplificada para propósitos educativos
- El modo 6G (JSCC/DeepJSCC) está preparado pero usa codificación básica
- Los codificadores de audio y video son versiones simplificadas de AAC y H.265
- La visualización se limita a los primeros 100 bits para mejor rendimiento

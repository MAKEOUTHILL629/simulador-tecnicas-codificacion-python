# Diseño del Simulador

Este documento describe el diseño de alto nivel del simulador de comunicaciones.

## Arquitectura

El simulador sigue una arquitectura de pipeline modular, donde cada etapa de la cadena de comunicación se implementa como un módulo de Python separado. Esto permite una visualización clara de la señal en cada paso y facilita la prueba y extensión de los módulos individuales.

### Módulos Principales (Versión 0.1.0)

1.  **Fuente (`main.py`):** Genera los datos de entrada leyendo un archivo de texto (`data/sample_text.txt`).
2.  **Codificador de Fuente (`src/huffman.py`):** Comprime el texto de origen utilizando la codificación Huffman.
3.  **Codificador de Canal (`src/channel_coding.py`):** Marcador de posición para la codificación de canal LDPC. Actualmente, pasa los datos sin modificarlos.
4.  **Modulador (`src/modulation.py`):** Mapea los bits codificados a símbolos complejos utilizando QPSK.
5.  **Canal (`src/channel.py`):** Simula un canal AWGN con un SNR configurable.
6.  **Demodulador (`src/modulation.py`):** Calcula las razones de verosimilitud logarítmica (LLR) a partir de los símbolos recibidos utilizando un demodulador max-log-MAP para QPSK.
7.  **Decodificador de Canal (`src/channel_coding.py`):** Marcador de posición para la decodificación de canal LDPC. Realiza una decodificación de decisión dura basada en los signos de los LLR.
8.  **Decodificador de Fuente (`src/huffman.py`):** Descomprime los datos utilizando el árbol de Huffman para reconstruir el texto original.
9.  **Visualización (`src/visualization.py`):** Genera gráficos de constelaciones utilizando `matplotlib`.

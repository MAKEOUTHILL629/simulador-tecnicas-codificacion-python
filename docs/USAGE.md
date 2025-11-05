# Cómo Usar el Simulador

Este documento explica cómo ejecutar el simulador del sistema de comunicaciones.

## Prerrequisitos

- Python 3.x
- `numpy`
- `matplotlib`
- `graphviz`
- `Pillow`

Puede instalar los paquetes de Python requeridos usando pip:

```bash
pip install numpy matplotlib graphviz Pillow
```

### Dependencia del Sistema: Graphviz

La visualización del árbol de Huffman requiere que Graphviz esté instalado en su sistema.

**En Debian/Ubuntu:**
```bash
sudo apt-get update
sudo apt-get install graphviz
```

**En macOS (usando Homebrew):**
```bash
brew install graphviz
```

**En Windows:**
Descargue e instale Graphviz desde el [sitio web oficial](https://graphviz.org/download/) y añada el directorio `bin` a su variable de entorno PATH.

## Ejecutando el Simulador

Para ejecutar la simulación, inicie la GUI ejecutando el script `main.py` desde el directorio raíz del proyecto:

```bash
python3 main.py
```

### Uso de la GUI

1.  **SNR (dB):** Ingrese la Relación Señal a Ruido deseada.
2.  **Select Input File:** Haga clic para seleccionar un archivo de texto de entrada.
3.  **Run Simulation:** Inicie la simulación. La interfaz permanecerá responsiva.
4.  **Resultados:** El texto original, el texto decodificado y las métricas (BER) se mostrarán en el área de texto.
5.  **Gráficos:** Los gráficos generados (constelaciones, histograma LLR, árbol de Huffman) se mostrarán en sus respectivas pestañas.

# Propuesta de Diseño para un Simulador Inteligente de Redes 5G, 5G Avanzado y 6G

> Experto Asignado: Dr. Elias Thorne, Experto en Codificación de Señal y Teoría de la Información. Ph.D. en Ingeniería Eléctrica, especializado en codificación de canal (LDPC, Polares) y compresión de fuentes (HEVC, DeepJSCC). Miembro Senior del IEEE y contribuyente a IEEE Transactions on Communications.

> Mi estilo es técnico, denso en ecuaciones y riguroso, enfocado en la derivación matemática y la viabilidad algorítmica para la implementación de sistemas.

## 1. Introducción y Arquitectura del Simulador

Este documento detalla la arquitectura teórica y el fundamento matemático para un simulador de capa física (PHY) de sistemas de comunicación inalámbrica 5G, 5G Avanzado y 6G. El propósito es establecer un marco de simulación que no solo implemente los estándares de codificación relevantes, sino que también opere de manera "inteligente", adaptando sus componentes algorítmicos basado en la selección del tipo de red y la fuente de datos.

La distinción fundamental en el simulador radica en el paradigma de codificación:

1.  **5G/5G Avanzado (SSCC - Codificación Separada de Fuente y Canal):** El simulador implementará la arquitectura clásica de Shannon donde la compresión de fuente (eliminación de redundancia) y la codificación de canal (adición de redundancia controlada) son procesos discretos y optimizados independientemente.¹
2.  **6G (JSCC - Codificación Conjunta Fuente-Canal):** El simulador implementará el paradigma emergente de Codificación Conjunta Fuente-Canal (JSCC), específicamente DeepJSCC (JSCC basada en Aprendizaje Profundo). Este enfoque abandona el principio de separación y entrena un mapeo neuronal de extremo a extremo, desde la fuente (p.ej., píxeles de imagen) directamente a los símbolos del canal. Esto es teóricamente superior en escenarios prácticos de longitud de bloque finita, baja latencia y complejidad limitada.¹

### 1.1. Flujo de Simulación (Pipeline)

El simulador se estructurará como una cadena de procesamiento modular, permitiendo la visualización de la señal en cada etapa (Requisito A).

**Flujo SSCC (5G/5G-A):**
$X \rightarrow [\text{Cod. Fuente}] \rightarrow B_{in} \rightarrow [\text{Cod. Canal}] \rightarrow B_{mod} \rightarrow [\text{Modulación}] \rightarrow S \rightarrow [\text{Canal}] \rightarrow R \rightarrow LLRs \rightarrow \hat{B}_{in} \rightarrow Y$

**Flujo JSCC (6G):**
$X \rightarrow Z \rightarrow [\text{Canal}] \rightarrow Y \rightarrow \hat{X}$

### 1.2. Lógica de Simulación Inteligente (Adaptativa)

El núcleo de la inteligencia del simulador residirá en un módulo de configuración que utiliza la selección del usuario para restringir los parámetros algorítmicos.

* **Selección de Red:**
    * **Si Red == "5G":** El simulador activa el flujo SSCC. La codificación de canal se restringe a LDPC (para datos) y Polar (para control). La modulación se limita a QPSK, 16-QAM, 64-QAM, 256-QAM.
    * **Si Red == "5G Avanzado":** Utiliza la misma base que 5G (SSCC, LDPC/Polar), pero introduce parámetros de enlace más estrictos para simular casos de uso como URLLC (Comunicaciones Ultra Confiables de Baja Latencia). Esto implica seleccionar tablas de Mapeo CQI-MCS (Modulation and Coding Scheme) que apunten a un BLER (Block Error Rate) objetivo mucho más bajo (p.ej., $10^{-5}$)^{7}$ en lugar del BLER estándar de eMBB (p.ej., $10^{-1}$ ).^{7}$
    * **Si Red == "6G":** El simulador desactiva el flujo SSCC y activa el flujo JSCC (DeepJSCC). La "codificación" y "modulación" se convierten en una única operación realizada por la red neuronal del codificador.
* **Selección de Fuente:**
    * **Si Fuente == "Texto":** Activa el codificador de fuente Huffman.
    * **Si Fuente == "Audio":** Activa el codificador de fuente basado en MDCT (similar a AAC).
    * **Si Fuente == "Imagen":** Activa el codificador de fuente basado en DCT y cuantización (similar a JPEG).11
    * **Si Fuente == "Video":** Activa el codificador de fuente HEVC (H.265) (Estimación de Movimiento, Residual, DCT, Cuantización). 13
* **Nota sobre 6G:** En el modo 6G (DeepJSCC), la selección de fuente cargará un modelo de autoencoder neuronal pre-entrenado específico para esa modalidad (p.ej., un autoencoder convolucional para imágenes 3, , un autoencoder basado en Transformer para texto ¹).

## 2. Generación de Fuente (Entrada $X$)

La entrada $X$ debe ser representada numéricamente.

* **Texto:** Una cadena de caracteres $X_{\text{txt}}$. Se convierte en una secuencia de símbolos $X$ basada en sus frecuencias de aparición (para Huffman).
* **Audio:** Una señal $X_{\text{audio}}(t)$. Muestreada a una frecuencia $f_s$ (p.ej., 44.1 kHz) para obtener un vector $X[n]$.
* **Imagen:** Una matriz 2D (escala de grises) o 3D (RGB) de valores de píxeles $X_{\text{img}}[i, j]$, típicamente enteros de 8 bits (0-255).
* **Video:** Una secuencia de tramas de imagen $X_{\text{video}}[i, j, t]$.

## 3. Módulo 1: Codificación de Fuente (SSCC - 5G/5G Avanzado)

Este módulo comprime $X$ en un flujo de bits $B_{in}$.

### 3.1. Texto: Codificación Huffman

Basado en las probabilidades de símbolo $p(x_i)$, se construye un árbol binario óptimo para asignar códigos de longitud variable (VLCs) a cada símbolo. El simulador debe:

1.  Calcular el histograma de $X_{\text{txt}}$.
2.  Construir el árbol de Huffman.
3.  Mapear $X_{\text{txt}}$ a $B_{in}$.

**Visualización:** El árbol de Huffman generado y el flujo de bits $B_{in}$ resultante.

### 3.2. Audio: Codificación AAC (MDCT)

El estándar AAC utiliza la Transformada de Coseno Discreta Modificada (MDCT) debido a su propiedad de superposición (overlap-add) que elimina el aliasing de bloque.

1.  **Ventaneo y Superposición:** La señal $X[n]$ se divide en bloques de longitud $2M$ que se superponen en un 50% (M muestras). 10
2.  **MDCT:** Para un bloque $x[n]$ (donde $n=0, \dots, 2M-1$), los coeficientes $X_k$ se calculan como:
    $$X_k = \sum_{n=0}^{2M-1} x[n] \cdot \cos\left[\frac{\pi}{M} \left(n + \frac{1}{2} + \frac{M}{2}\right) \left(k + \frac{1}{2}\right)\right]$$
    donde $k=0, \dots, M-1$.
3.  **Cuantización:** Los coeficientes $X_k$ se cuantifican (p.ej., cuantización uniforme $Q(X_k) = \text{round}(X_k/\Delta)$) y luego se codifican (p.ej., Huffman) para producir $B_{in}$.

**Visualización:** El espectrograma de $X[n]$ y la matriz de coeficientes MDCT cuantificados.

### 3.3. Imagen: Codificación JPEG (DCT y Cuantización)

1.  **Bloqueo:** La imagen $X_{\text{img}}$ se divide en bloques de $8 \times 8$ píxeles, $x_{ij}$.
2.  **Transformada (DCT-II):** Cada bloque se transforma al dominio de la frecuencia.11
    $$G_{uv} = \frac{1}{4} C(u) C(v) \sum_{i=0}^{7} \sum_{j=0}^{7} x_{ij} \cos\left[\frac{(2i+1)u\pi}{16}\right] \cos\left[\frac{(2j+1)v\pi}{16}\right]$$
    donde $C(k)=1/\sqrt{2}$ si $k=0$ y $C(k)=1$ si $k>0$.
3.  **Cuantización:** Los coeficientes DCT $G_{uv}$ se dividen (división por elementos) por una matriz de cuantización estándar $Q_{uv}$ y se redondean.
    $$G_Q[u,v] = \text{round}\left(\frac{G_{uv}}{Q_{uv}}\right)$$

**Visualización:** La matriz $G_Q$ (mostrando alta compresión en altas frecuencias) y el flujo de bits $B_{in}$ resultante (tras codificación de entropía, p.ej., Huffman).

### 3.4. Video: Codificación H.265/HEVC

HEVC (High Efficiency Video Coding) es significativamente más complejo. 13 El simulador implementará un modelo simplificado:

1.  **Estimación de Movimiento (Inter-predicción):** Para un bloque actual (Macroblock o Coding Unit) $C$, el simulador busca el bloque más similar $R$ en una trama de referencia (anterior) $F_{\text{ref}}$. La métrica de similitud estándar es la Suma de Diferencias Absolutas (SAD). 16
    $$\text{SAD (C, R)} = \sum_{i=0}^{N-1} \sum_{j=0}^{N-1} |C(i,j)-R(i,j)|$$
    El desplazamiento $(dx, dy)$ que minimiza el SAD es el Vector de Movimiento (MV).
2.  **Cálculo Residual:** Se calcula el bloque residual $E = C - R_{\text{best}}$. Este bloque de error tiene una entropía mucho menor que $C$.
3.  **Transformada y Cuantización:** El bloque residual $E$ se procesa de forma idéntica a la codificación de imagen (pasos 3.3.2 y 3.3.3): $E \xrightarrow{\text{DCT}} G_E \xrightarrow{\text{Quant}} G_{E,Q}$.
4.  **Codificación de Entropía:** Los MVs y los coeficientes $G_{E,Q}$ se codifican (p.ej., CABAC o Huffman) para generar $B_{in}$.

**Visualización:** El campo de vectores de movimiento, la imagen residual $E$ (debería parecer ruido de baja energía) y la imagen $G_{E,Q}$.

## 4. Módulo 2: Codificación y Modulación (SSCC - 5G/5G Avanzado)

Este módulo toma $B_{in}$ y lo prepara para el canal.

### 4.1. Codificación de Canal 5G NR

El simulador debe implementar LDPC (para datos) según 3GPP TS 38.212.5

1.  **Selección de Gráfico Base (BG):** 5G NR define dos gráficos base. 19 El simulador seleccionará:
    * **BG1:** Para bloques de datos grandes ($K>8448$) y tasas de código altas ($1/3$ a $8/9$). 20 Dimensiones: $46 \times 68$.19
    * **BG2:** Para bloques pequeños ($K \le 3840$) y tasas de código bajas (1/5 a 2/3). 20 Dimensiones: $42 \times 52$.21
2.  **Construcción de Matriz $H$ (Lifting):** La matriz de paridad $H$ real se genera mediante "lifting" del BG seleccionado.19 Cada entrada $(i, j)$ en el BG, que es un entero $V_{ij}$, se reemplaza por una matriz identidad $Z \times Z$ rotada cíclicamente $P_{ij}$ veces, donde $Z$ es el factor de "lifting" y $P_{ij} = V_{ij} \mod Z$.21 Si la entrada del BG es -1, se reemplaza por una matriz nula $Z \times Z$.23
3.  **Codificación:** La codificación LDPC es el proceso de encontrar una palabra código $C$ (que contiene $B_{in}$ y los bits de paridad $P$) tal que $H \cdot C^T = 0$. Dado que las matrices $H$ de 5G NR tienen una estructura cuasi-cíclica (QC-LDPC) y triangular 24, la codificación se puede realizar eficientemente mediante sustitución hacia adelante (back-substitution), evitando la multiplicación de matrices densas. 24
    La salida es el flujo de bits codificado $B_{mod}$.

### 4.2. Modulación Digital

El flujo $B_{mod}$ se agrupa en $k = \log_2(M)$ bits para mapear a un símbolo complejo $S$ de una constelación $M$-aria (QPSK, 16-QAM, 64-QAM, 256-QAM).6

* **QPSK ($M=4, k=2$):** Bits $[b_0, b_1] \rightarrow S = \frac{1}{\sqrt{2}} [(1-2b_0) + j(1-2b_1)]$
* **16-QAM ($M=16, k=4$):** Bits $[b_0, b_1, b_2, b_3]$.
    * Componente I (bits $b_0, b_2$): $I \in \{-3, -1, 1, 3\}$
    * Componente Q (bits $b_1, b_3$): $Q \in \{-3, -1, 1, 3\}$
    * $S = A \cdot (I + jQ)$ (donde $A$ es un factor de normalización de potencia).
* **64-QAM ($M=64, k=6$):** $I, Q \in \{-7, -5, -3, -1, 1, 3, 5, 7\}$
* **256-QAM ($M=256, k=8$):** $I, Q \in \{-15, -13, \dots, 13, 15\}$

**Visualización:** El diagrama de constelación (I/Q) de los símbolos $S$ transmitidos.

### 4.3. Adaptación Inteligente: Modulación y Codificación Adaptativa (AMC)

Este es el núcleo de la adaptación en 5G/5G-A. El simulador modelará el proceso de Adaptación de Enlace (Link Adaptation). 26

1.  **Feedback (CQI):** El receptor (simulado) estima la calidad del canal (p.ej., SINR) y la mapea a un Indice de Calidad del Canal (CQI) (0-15).
2.  **Mapeo (MCS):** La estación base (simulador) utiliza el CQI para seleccionar un Esquema de Modulación y Codificación (MCS) de una tabla 3GPP TS 38.214.6
3.  **Lógica del Simulador:** El simulador implementará esta tabla de consulta (LUT). Por ejemplo, según la Tabla 5.2.2.1-2 29:
    * **Si CQI = 1 o 2:** Selecciona QPSK, Tasa de Código baja (p.ej., 78/1024).29
    * **Si CQI = 7 o 8:** Selecciona 16-QAM, Tasa de Código media. 28
    * **Si CQI = 11 o 12:** Selecciona 64-QAM, Tasa de Código alta. 28
    * **Si CQI = 13, 14 o 15:** Selecciona 256-QAM, Tasa de Código muy alta.28
4.  **Adaptación 5G-A (URLLC):** Si se selecciona 5G-A (URLLC), el simulador utilizará las tablas de MCS de baja eficiencia espectral (Low SE) o las tablas CQI con un BLER objetivo de $10^{-5}$ (Tabla 3 en TS 38.214), forzando modulaciones más robustas (QPSK) y tasas de código más bajas (más redundancia) para la misma calidad de canal.

## 5. Módulo 3: Codificación/Modulación Conjunta (JSCC - 6G)

En el modo 6G, los Módulos 1 y 2 se reemplazan por un único bloque DeepJSCC, basado en un autoencoder.3

### 5.1. Arquitectura del Autoencoder

La arquitectura depende de la fuente 1:

* **Imagen/Video:** Redes Neuronales Convolucionales (CNNs).2
* **Texto:** Arquitecturas basadas en Transformer o RNN.

Tomando el caso de la imagen 2:

1.  **Codificador (Transmisor) $f_{\Theta_e}$:** Una CNN que mapea la imagen de entrada $X \in \mathbb{R}^{H \times W \times C}$ a un vector latente $Z \in \mathbb{C}^{k}$. $Z$ representa los símbolos complejos a transmitir.
    $$Z = f_{\Theta_e}(X)$$
    $f_{\Theta_e}$ consiste en capas convolucionales seguidas de downsampling (p.ej., Conv2D + ReLU) para comprimir la representación espacial.
    La capa final aplana y normaliza la salida para cumplir con la restricción de potencia de transmisión $P$.
2.  **Decodificador (Receptor) $g_{\Theta_d}$:** Una CNN que intenta reconstruir $\hat{X}$ desde la representación latente ruidosa $Y$.
    $$\hat{X} = g_{\Theta_d}(Y)$$
    $g_{\Theta_d}$ es una arquitectura espejo (p.ej., Convoluciones Transpuestas o ConvTranspose2D) que realiza upsampling para restaurar las dimensiones de la imagen original. 32

### 5.2. Proceso de Entrenamiento y Función de Pérdida

El simulador 6G debe cargar los pesos ($\Theta_e, \Theta_d$) de un modelo pre-entrenado. El entrenamiento (fuera del simulador) se define por la optimización de una función de pérdida $\mathcal{L}$ sobre un conjunto de datos $\mathcal{D}$.33
$$\min_{\Theta_e, \Theta_d} \mathbb{E}_{X \in \mathcal{D}, N \sim \mathcal{N}(0, \sigma^2)} [\mathcal{L}(X, \hat{X})]$$
La función de pérdida $\mathcal{L}$ es fundamental y debe equilibrar la distorsión de la fuente con las restricciones del canal 34:
$\mathcal{L} = \mathcal{L}_{\text{distorsión}} + \beta \cdot \mathcal{L}_{\text{potencia}}$

* $\mathcal{L}_{\text{distorsión}}$: Mide la diferencia entre $X$ y $\hat{X}$.
    * **MSE (Error Cuadrático Medio):** $\mathcal{L}_{\text{MSE}} = \frac{1}{N} \sum ||X - \hat{X}||^2$.33
    * **SSIM:** $\mathcal{L}_{\text{SSIM}} = 1 - \text{SSIM (X, \hat{X})}$.36
* $\mathcal{L}_{\text{potencia}}$: Restringe la potencia de transmisión de $Z$.
    $\mathcal{L}_{\text{potencia}} = \max(0, \mathbb{E}[||Z||^2] - P)$

**Visualización (6G):**

* **Salida del Codificador:** Visualización de $Z$ (la "constelación aprendida", que no será una cuadrícula limpia como QAM).
* **Salida del Canal:** $Y$ (la constelación ruidosa).
* **Salida del Decodificador:** La imagen reconstruida $\hat{X}$.

## 6. Módulo 4: El Canal Inalámbrico (Desvanecimiento y Ruido)

Este módulo simula la transmisión física de símbolos complejos ($S$ de 5G o $Z$ de 6G) para producir símbolos recibidos $R$ (o $Y$ en 6G).

### 6.1. Modelo Matemático del Canal

El modelo fundamental del canal es 38:
$$R = h \cdot S + N$$
donde:

* $S$: Símbolo complejo transmitido.
* $h$: Coeficiente de desvanecimiento del canal (complejo).
* $N$: Ruido Aditivo Blanco Gaussiano (AWGN) (complejo).
* $R$: Símbolo complejo recibido.

### 6.2. Ruido (AWGN)

$N$ es una variable aleatoria compleja $N = N_I + j N_Q$, donde $N_I$ y $N_Q$ son variables aleatorias Gaussianas i.i.d. con media cero y varianza $\sigma_n^2$.
La varianza $\sigma_n^2$ es la densidad espectral de potencia de ruido $N_0/2$.

* **Parámetros del Simulador (S/N y $E_b/N_0$):** El usuario configurará la calidad del canal usando $S/N$ (SNR) o $E_b/N_0$.
* **Relación:** La potencia de la señal $S$ es $E_s$. La potencia del ruido $N$ es $E[|N|^2] = N_O B$ (donde $B$ es el ancho de banda). La Tasa de bits $R_b$ está relacionada con la tasa de símbolos $R_s$ y $k$ bits/símbolo ($R_b = k R_s$).
    $S/N = \frac{P_S}{P_N} = \frac{E_s}{N_0 B/R_s}$
    $E_b/N_0 = \frac{P_S/R_b}{N_0} = \frac{P_S}{N_O B} \frac{B}{R_b} = (S/N) \cdot \frac{B}{R_b}$.40
    El simulador usará esta relación para calcular la varianza $\sigma_n^2$ necesaria para $N$ a partir del $E_b/N_0$ especificado.

### 6.3. Desvanecimiento (Generación de $h$)

* **Canal Rayleigh (NLOS):** Usado para escenarios sin línea de vista (Non-Line-of-Sight).42 El coeficiente $h$ se genera sumando dos variables Gaussianas i.i.d. $X \sim \mathcal{N}(0, \sigma^2)$ e $Y \sim \mathcal{N}(0, \sigma^2)$.
    $$h = X + jY$$
    La amplitud $|h| = \sqrt{X^2+Y^2}$ sigue una distribución de Rayleigh.
* **Canal Rician (LOS):** Usado cuando hay un componente de línea de vista (Line-of-Sight) dominante. 42 Se define por el factor $K$, la relación entre la potencia del camino dominante (LOS) y la potencia de los caminos difusos (NLOS). 45
    $$h = \sqrt{\frac{K}{K+1}} h_{\text{LOS}} + \sqrt{\frac{1}{K+1}} h_{\text{NLOS}}$$
    donde $h_{\text{LOS}}$ es un componente determinista (p.ej., $h_{\text{LOS}}=1$) y $h_{\text{NLOS}}$ se genera como un canal Rayleigh (ver arriba).

**Visualización:** El diagrama de constelación de $R$. Se observará la "nube" de ruido (de $N$) alrededor de los puntos de la constelación transmitida, y la rotación/atenuación (de $h$) de toda la constelación.

## 7. Módulo 5: Demodulación y Decodificación (Receptor SSCC)

Este módulo recupera $\hat{B}_{in}$ desde $R$.

### 7.1. Demodulación "Soft": Log-Likelihood Ratio (LLR)

En lugar de tomar una decisión "dura" (Hard-Decision) sobre $R$, el demodulador calcula la probabilidad logaritmica (LLR) para cada bit $b_i$ que componía el símbolo $S$.46 El LLR es la entrada requerida para los decodificadores modernos (LDPC, Polar, Turbo). 47

Definición de LLR para el bit $i$-ésimo, dado el símbolo recibido $R=y$:
$$L(b_i | y) = \log \left(\frac{P(b_i=0 | y)}{P(b_i=1 | y)} \right)$$
Asumiendo un canal AWGN ($y=x+n$, $p(y|x) \propto \exp(-|y-x|^2/N_O)$) y bits de entrada equiprobables 48:
$$L(b_i | y) = \log \left(\frac{\sum_{x \in \mathcal{X}_{i,0}} \exp\left(-\frac{|y-x|^2}{N_0}\right)}{\sum_{x \in \mathcal{X}_{i,1}} \exp\left(-\frac{|y-x|^2}{N_0}\right)} \right)$$
donde $\mathcal{X}_{i,0}$ y $\mathcal{X}_{i,1}$ son los subconjuntos de la constelación donde el bit $i$ es 0 y 1, respectivamente.49

* **Aproximación Max-Log-MAP:** El cálculo Log-MAP exacto es computacionalmente intensivo. Se utiliza la aproximación $\log(\sum_k e^{a_k}) \approx \max_k(a_k)$ 51:
    $$L(b_i | y) \approx \max_{x \in \mathcal{X}_{i,0}} \left\{-\frac{|y-x|^2}{N_0} \right\} - \max_{x \in \mathcal{X}_{i,1}} \left\{-\frac{|y-x|^2}{N_0} \right\}$$
    Esto simplifica a encontrar el símbolo $x$ más cercano en cada subconjunto (el Mínimo Error Cuadrático) 53:
    $$L(b_i | y) \approx \frac{1}{N_0} \left(\min_{x \in \mathcal{X}_{i,1}} |y-x|^2 - \min_{x \in \mathcal{X}_{i,0}} |y-x|^2 \right)$$

**Visualización:** Un histograma de los valores LLR. Valores fuertemente positivos indican alta confianza en '0', fuertemente negativos indican alta confianza en '1', y valores cercanos a 0 indican incertidumbre.

### 7.2. Decodificación de Canal: LDPC (Sum-Product Algorithm)

El decodificador LDPC es un algoritmo iterativo de paso de mensajes (Belief Propagation) en el grafo de Tanner de la matriz $H$.54 Opera en el dominio LLR.55

1.  **Inicialización:** Los Nodos Variables (VNs, bits $v_i$) se inicializan con los LLRs del canal: $L(v_i) = L(b_i | y)$ de la Ecuación Max-Log-MAP.
2.  **Paso 1 (VN a CN):** Cada Nodo Variable $v_i$ envía un mensaje LLR (su "creencia") $L_{v \to c}$ a cada Nodo de Chequeo (CNs, ecuaciones $c_j$) conectado a él. Es la suma de todas las otras creencias que $v_i$ ha recibido, excluyendo la del destinatario $c_j$ 58:
    $$L_{v_i \to c_j} = L(v_i) + \sum_{c' \in \mathcal{N}(v_i) \setminus \{c_j\}} L_{c' \to v_i}$$
    (En la primera iteración, $L_{v_i \to c_j} = L(v_i)$).
3.  **Paso 2 (CN a VN):** Cada Nodo de Chequeo $c_j$ calcula un mensaje $L_{c \to v}$ para $v_i$. El nodo de chequeo impone la restricción de paridad (la suma XOR de sus entradas debe ser 0). El mensaje LLR resultante es 55:
    $$L_{c_j \to v_i} = 2\cdot \text{atanh} \left(\prod_{v' \in \mathcal{M}(c_j) \setminus \{v_i\}} \tanh \left(\frac{L_{v' \to c_j}}{2} \right) \right)$$
4.  **Aproximación Min-Sum:** La Ecuación del Paso 2 es compleja. El simulador puede usar la aproximación Min-Sum, que es robusta y más simple 59:
    $$L_{c_j \to v_i} \approx \left(\prod_{v' \in \mathcal{M}(c_j) \setminus \{v_i\}} \text{sign}(L_{v' \to c_j}) \right)\cdot \min_{v' \in \mathcal{M}(c_j) \setminus \{v_i\}} |L_{v' \to c_j}|$$
5.  **Decisión y Parada:** Después de cada iteración, se calcula el LLR a posteriori (APP) total para cada bit:
    $$L(v_i | Y) = L(v_i) + \sum_{c \in \mathcal{N}(v_i)} L_{c \to v_i}$$
    Se toma una decisión dura $\hat{B}_{in}(i) = (L(v_i|Y) < 0)$. El algoritmo se detiene si $H \cdot \hat{B}_{in}^T = 0$ o si se alcanza un número máximo de iteraciones.

### 7.3. Decodificación de Canal: Códigos Polares (Successive Cancellation)

Para los canales de control 5G, se usa la decodificación por Cancelación Sucesiva (SC).61 Es un algoritmo recursivo.62 Dado un LLR $L_N^{(i)}$ del canal, el decodificador calcula recursivamente los LLRs $L_1^{(i)}$ de los bits de información $u_i$.

La recursión fundamental utiliza dos operaciones (basadas en el grafo mariposa del código polar):

* $L_N^{(i)}(y_1^N, u_1^{i-1}) = f(L_{N/2}^{(i)}(y_1^{N/2}, u_1^{i-1, \text{par}}), L_{N/2}^{(i+N/2)}(y_{N/2+1}^N, u_1^{i-1, \text{impar}} \oplus u_1^{i-1, \text{par}}))$
    La función $f$ es (similar al nodo de chequeo LDPC): $L_a \boxplus L_b \approx \text{sign}(L_a)\text{sign}(L_b) \min(|L_a|, |L_b|)$
* $L_N^{(i+N/2)}(y_1^N, u_1^{i-1}) = g(L_{N/2}^{(i)}(y_1^{N/2}, u_1^{i-1, \text{par}}), L_{N/2}^{(i+N/2)}(y_{N/2+1}^N, u_1^{i-1, \text{impar}} \oplus u_1^{i-1, \text{par}}), \hat{u}_i)$
    La función $g$ es (similar al nodo variable LDPC): $L_b + (-1)^{\hat{u}_i} L_a$

El decodificador estima $\hat{u}_i$ secuencialmente. Si $i$ es un indice de bit "congelado" (frozen), $\hat{u}_i = 0$. Si $i$ es un indice de bit de "información", $\hat{u}_i = (L_1^{(i)} < 0)$. Esta decisión $\hat{u}_i$ se retroalimenta inmediatamente para decodificar $u_{i+1}$.⁶

## 8. Módulo 6: Decodificación de Fuente y Métricas de Rendimiento (Salida $Y$)

### 8.1. Decodificación de Fuente

El receptor realiza la operación inversa del Módulo 1 sobre el flujo de bits recuperado $\hat{B}_{in}$.

* **Texto:** Decodificación Huffman (recorrido del árbol).
* **Audio:** Decodificación de entropía, De-cuantización, IMDCT y Overlap-Add. 10
    $$y[n] = \sum_{k=0}^{M-1} \hat{X}_k \cdot \cos\left[\frac{\pi}{M} \left(n + \frac{1}{2} + \frac{M}{2}\right) \left(k + \frac{1}{2}\right)\right]$$
* **Imagen/Video:** Decodificación de entropía, De-cuantización ($G_{uv} = \hat{G}_Q[u,v] \cdot Q_{uv}$), IDCT (Transformada Inversa).¹¹
* **Video (Adicional):** Compensación de Movimiento (sumar el residual $\hat{E}$ al bloque $R_{\text{best}}$ apuntado por el MV recuperado).

### 8.2. Cálculo de Métricas de Integridad (Req. B y D)

El simulador debe comparar la entrada $X$ con la salida $Y$ (o $\hat{X}$ en 6G).

* **BER (Bit Error Rate):** Métrica a nivel de canal. Compara $B_{in}$ (bits de fuente) con $\hat{B}_{in}$ (bits de fuente decodificados).
    $$\text{BER} = \frac{\text{# bits erróneos}}{\text{# bits totales}}$$
* **BLER (Block Error Rate):** Métrica de capa de enlace.
    $$\text{BLER} = \frac{\text{# bloques (p.ej., tramas) con } \ge 1 \text{ error}}{\text{# bloques totales}}$$
* **PSNR (Peak Signal-to-Noise Ratio):** Métrica de fidelidad para Imagen/Video.36
    $$\text{MSE} = \frac{1}{H \cdot W} \sum_{i=0}^{H-1} \sum_{j=0}^{W-1} [X(i,j) - Y(i,j)]^2$$
    $$\text{PSNR} = 10 \cdot \log_{10} \left(\frac{\text{MAX}_I^2}{\text{MSE}} \right)$$
    (donde $\text{MAX}_I$ es 255 para imágenes de 8 bits).
* **SSIM (Structural Similarity Index):** Métrica perceptual para Imagen/Video.36
    $$\text{SSIM}(X, Y) = \frac{(2\mu_X\mu_Y + C_1)(2\sigma_{XY} + C_2)}{(\mu_X^2 + \mu_Y^2 + C_1)(\sigma_X^2 + \sigma_Y^2 + C_2)}$$
    (donde $\mu$ es la media local, $\sigma^2$ la varianza local, $\sigma_{XY}$ la covarianza local, y $C_1, C_2$ constantes de estabilización).

### 8.3. Métricas de Teoría de la Información (Req. C)

Estas métricas cuantifican la información transmitida.

* **Cantidad de Información (Auto-información):** $I(x_i) = -\log_2(p(x_i))$.⁶⁶
* **Cantidad Promedio de Información (Entropía de Fuente):** $H(X) = E[I(X)] = -\sum_i p(x_i) \log_2(p(x_i))$.67
    * **Simulación:** $p(x_i)$ se estima a partir del histograma normalizado de la fuente $X$.
* **Información Mutua (Entrada $X$ vs. Salida $Y$):** Mide la información sobre $X$ que se obtiene observando $Y$. Es la métrica de fidelidad teórica fundamental.68
    $$I(X;Y) = H(X) + H(Y) - H(X,Y)$$
* **Algoritmo de Cálculo (para Imágenes):**
    1.  Calcular $H(X)$ y $H(Y)$ usando sus respectivos histogramas de intensidad (p.ej., 256 bins).
    2.  Calcular la Entropía Conjunta $H(X,Y)$. Esto requiere la construcción de un Histograma 2D (o matriz de co-ocurrencia) de tamaño $256 \times 256$.68 La celda $(i, j)$ en este histograma cuenta la frecuencia de píxeles $(m,n)$ tales que $X(m,n)=i$ y $Y(m,n)=j$.
    3.  Normalizar el histograma 2D para obtener la distribución de probabilidad conjunta $p(x,y)$.
    4.  $H(X,Y) = -\sum_{i=0}^{255} \sum_{j=0}^{255} p(i,j) \log_2(p(i,j))$.69
    5.  Calcular $I(X;Y)$. Un valor de $I(X;Y)$ cercano a $H(X)$ indica una transmisión casi perfecta.

## 9. Conclusión de la Propuesta

El simulador propuesto proporciona un marco unificado para la evaluación comparativa de los paradigmas SSCC (5G/5G-A) y JSCC (6G). La arquitectura "inteligente" permite una configuración paramétrica cohesiva que refleja las decisiones de diseño del mundo real (p.ej., la adaptación de enlace vía CQI/MCS) y las arquitecturas emergentes (DeepJSCC). La inclusión de visualización en cada etapa y un conjunto robusto de métricas (desde BER hasta Información Mutua) permitirá un análisis exhaustivo del rendimiento, la fidelidad perceptual y la eficiencia teórica de la información de cada sistema bajo condiciones de canal variables.

---

## Obras citadas

1.  Articulo 1.pdf
2.  Deep Joint Source-Channel Coding for Wireless Image Transmission - UCL Discovery - University College London, fecha de acceso: noviembre 4, 2025, https://discovery.ucl.ac.uk/id/eprint/10089480/1/FINAL%20VERSION.pdf
3.  DeepJSCC-f: Deep Joint Source-Channel Coding of Images with Feedback - Imperial College London, fecha de acceso: noviembre 4, 2025, https://www.imperial.ac.uk/media/imperial-college/research-centres-and-groups/ipc-lab/KurkaGunduz-deepJSCC-f.pdf
4.  Demystifying 5G Polar and LDPC Codes: A Comprehensive Review and Foundations, fecha de acceso: noviembre 4, 2025, https://arxiv.org/html/2502.11053v2
5.  Demystifying 5G Polar and LDPC Codes: A Comprehensive Review and Foundations, fecha de acceso: noviembre 4, 2025, https://arxiv.org/html/2502.11053v1
6.  5G Modulation and Coding Scheme | 5G MCS - Techplayon, fecha de acceso: noviembre 4, 2025, https://www.techplayon.com/5g-nr-modulation-and-coding-scheme-modulation-and-code-rate/
7.  [5G URLLC] CQI & MCS. CQI (Channel Quality Indicator) & MCS... | by Jessica Chuang, fecha de acceso: noviembre 4, 2025, https://medium.com/@jessica.chchuang/5g-urllc-cqi-mcs-fb3e3ad994cf
8.  Comprimiendo datos - el algoritmo de Huffman en Python - Bit y Byte, fecha de acceso: noviembre 4, 2025, https://bitybyte.github.io/Huffman-coding/
9.  MX2011000366A - Codificador y decodificador de audio para codificar y decodificar muestras de audio. - Google Patents, fecha de acceso: noviembre 4, 2025, https://patents.google.com/patent/MX2011000366A/es
10. TESIS: DISEÑO E IMPLEMENTACIÓN DE UN CODIFICADOR DECODIFICADOR PERCEPTUAL DE AUDIO DIGITAL - UNAM, fecha de acceso: noviembre 4, 2025, https://tesiunamdocumentos.dgb.unam.mx/ptd2016/noviembre/0752493/0752493.pdf
11. Marca de agua digital basada en DWT-DCT para imágenes de documentos manuscritos: optimización contra ataques de compresión JPEG. - Redalyc, fecha de acceso: noviembre 4, 2025, https://www.redalyc.org/journal/3783/378365831003/html/
12. Transformada de coseno discreta - Wikipedia, la enciclopedia libre, fecha de acceso: noviembre 4, 2025, https://es.wikipedia.org/wiki/Transformada_de_coseno_discreta
13. Codificación de video en HEVC/H.265 utilizando FFMPEG - SciELO Cuba, fecha de acceso: noviembre 4, 2025, http://scielo.sld.cu/scielo.php?script=sci_arttext&pid=S1815-59282019000200022
14. Codificación de video en HEVC/H.265 utilizando FFMPEG - ResearchGate, fecha de acceso: noviembre 4, 2025, https://www.researchgate.net/publication/332877529_Codificacion_de_video_en_HEVCH265_utilizando_FFMPEG
15. Redes neuronales profundas preentrenadas - MATLAB & Simulink - MathWorks, fecha de acceso: noviembre 4, 2025, https://la.mathworks.com/help/deeplearning/ug/pretrained-convolutional-neural-networks.html
16. Sum of absolute differences - Wikipedia, fecha de acceso: noviembre 4, 2025, https://en.wikipedia.org/wiki/Sum_of_absolute_differences
17. Codificación de video en HEVC/H.265 utilizando FFMPEG - Dialnet, fecha de acceso: noviembre 4, 2025, https://dialnet.unirioja.es/descarga/articulo/9513852.pdf
18. TS 138 212 - V17.8.0 - 5G; NR; Multiplexing and channel coding (3GPP TS 38.212 version 17.8.0 Release 17) - ETSI, fecha de acceso: noviembre 4, 2025, https://www.etsi.org/deliver/etsi_ts/138200_138299/138212/17.08.00_60/ts_138212v170800p.pdf
19. LDPC in NR - 5G | Share Technote, fecha de acceso: noviembre 4, 2025, https://www.sharetechnote.com/html/5G/5G_LDPC.html
20. análisis e implementación de una nueva codificación Idpc en sistemas de comunicaciones por satélite - ADDI, fecha de acceso: noviembre 4, 2025, https://addi.ehu.es/bitstream/10810/29194/1/TFG_JonMaseda.pdf
21. TS 138 212 - V15.2.0-5G; NR; Multiplexing and channel coding (3GPP TS 38.212 version 15.2.0 Release 15) - ETSI, fecha de acceso: noviembre 4, 2025, https://www.etsi.org/deliver/etsi_ts/138200_138299/138212/15.02.00_60/ts_138212v150200p.pdf
22. Structure diagram of base matrix for standard 5G LDPC codes. - ResearchGate, fecha de acceso: noviembre 4, 2025, https://www.researchgate.net/figure/Structure-diagram-of-base-matrix-for-standard-5G-LDPC-codes_fig2_327489753
23. WO2010089444A1 - Codificar y decodificar usando códigos cuasi-cíclicos Idpc, fecha de acceso: noviembre 4, 2025, https://patents.google.com/patent/WO2010089444A1/es
24. Diseño e implementación de un codificador LDPC para sistema de navegación por satélite., fecha de acceso: noviembre 4, 2025, https://es.globals.ieice.org/en/publications/elex/10.1587/elex.21.20240322/f
25. CD 12378.pdf - ESCUELA POLITÉCNICA NACIONAL, fecha de acceso: noviembre 4, 2025, https://bibdigital.epn.edu.ec/bitstream/15000/22922/1/CD%2012378.pdf
26. How Link Adaptation Uses CQI, MCS, and AMC in Wireless Systems - Patsnap Eureka, fecha de acceso: noviembre 4, 2025, https://eureka.patsnap.com/article/how-link-adaptation-uses-cqi-mcs-and-amc-in-wireless-systems
27. Link adaptation in 5G Networks: Reinforcement Learning framework based approach - DiVA portal, fecha de acceso: noviembre 4, 2025, https://www.diva-portal.org/smash/get/diva2:1710474/FULLTEXT01.pdf
28. 5G NR mapping CQI to MCS - telecomHall Forum, fecha de acceso: noviembre 4, 2025, https://www.telecomhall.net/t/5g-nr-mapping-cqi-to-mcs/31287
29. TS 138 214-V15.2.0-5G; NR; Physical layer procedures for data (3GPP TS 38.214 version 15.2.0 Release 15) - ETSI, fecha de acceso: noviembre 4, 2025, https://www.etsi.org/deliver/etsi_ts/138200_138299/138214/15.02.00_60/ts_138214v150200p.pdf
30. 5G NR Downlink CSI Reporting - MATLAB & Simulink - MathWorks, fecha de acceso: noviembre 4, 2025, https://www.mathworks.com/help/5g/ug/5g-nr-downlink-csi-reporting.html
31. CSI Report - 5G | ShareTechnote, fecha de acceso: noviembre 4, 2025, https://www.sharetechnote.com/html/5G/5G_CSI_Report.html
32. ¿Qué son las redes neuronales convolucionales? - MATLAB & Simulink - MathWorks, fecha de acceso: noviembre 4, 2025, https://la.mathworks.com/discovery/convolutional-neural-network.html
33. Loss Functions in Simple Autoencoders: MSE vs. L1 Loss | by Bhipanshu Dhupar - Medium, fecha de acceso: noviembre 4, 2025, https://medium.com/@bhipanshudhupar/loss-functions-in-simple-autoencoders-mse-vs-l1-loss-4e838ae425b9
34. ¿Qué es la función de pérdida? - IBM, fecha de acceso: noviembre 4, 2025, https://www.ibm.com/es-es/think/topics/loss-function
35. ¿Qué es la función de pérdida? - IBM, fecha de acceso: noviembre 4, 2025, https://www.ibm.com/mx-es/think/topics/loss-function
36. Evaluación y Comparación de Métricas Objetivas PSNR, SSIM y LPIPS para el Análisis de Calidad de Video | Revista Tecnológica - ESPOL, fecha de acceso: noviembre 4, 2025, https://www.rte.espol.edu.ec/index.php/tecnologica/es/article/view/1317
37. Impact of loss functions on the performance of a deep neural network designed to restore low-dose digital mammography - PubMed Central, fecha de acceso: noviembre 4, 2025, https://pmc.ncbi.nlm.nih.gov/articles/PMC10267506/
38. Aplicación de Teoría de Matrices Aleatorias en Comunicación Inalámbrica - Sistemas MIMO - Cimat, fecha de acceso: noviembre 4, 2025, https://www.cimat.mx/~pabreu/Presentacion.pdf
39. Modelamiento matemático de canal inalámbrico Multitrayecto - YouTube, fecha de acceso: noviembre 4, 2025, https://www.youtube.com/watch?v=a5EOPtjpIW8
40. ¿Cómo simular Eb/NO (dB)?: r/DSP - Reddit, fecha de acceso: noviembre 4, 2025, https://www.reddit.com/r/DSP/comments/z697zc/how_to_simulate_ebn0_db/?tl=es-419
41. Cociente de Energía de Señal por Bit (Eb/NO) - Aula Virtual, fecha de acceso: noviembre 4, 2025, https://aulavirtual.fio.unam.edu.ar/mod/resource/view.php?id=59752
42. Modelos de canal de desvanecimiento para comunicaciones Millimeter-Wave - Dialnet, fecha de acceso: noviembre 4, 2025, https://dialnet.unirioja.es/descarga/articulo/7741842.pdf
43. Modelos de canal de desvanecimiento para comunicaciones Millimeter-Wave, fecha de acceso: noviembre 4, 2025, https://riti.es/index.php/riti/article/view/71/557
44. Conceptos básicos del desvanecimiento y tipos de desvanecimiento en las comunicaciones inalámbricas - RF Miso, fecha de acceso: noviembre 4, 2025, http://es.rf-miso.com/news/fading-basics-and-types-of-fading-in-wireless-communication-2/
45. 2.5. MODELOS DE SIMULACION PARA CANALES DE DESVANECIMIENTO MULTICAMINO. 2.5.1. Introducción. Como ya hemos dicho en la mayoría, fecha de acceso: noviembre 4, 2025, https://biblus.us.es/bibing/proyectos/use/abreproy/10390/fichero/10jun01_2.PDF
46. "Machine LLRning": Learning to Softly Demodulate - arXiv, fecha de acceso: noviembre 4, 2025, https://arxiv.org/pdf/1907.01512
47. Log-Likelihood Ratio (LLR) Demodulation - MATLAB & Simulink - MathWorks, fecha de acceso: noviembre 4, 2025, https://www.mathworks.com/help/comm/ug/log-likelihood-ratio-llr-demodulation.html
48. Exercise 4.2: Channel Log Likelihood Ratio at AWGN - LNTwww, fecha de acceso: noviembre 4, 2025, https://en.lntwww.de/Aufgaben:Exercise_4.2:_Channel_Log_Likelihood_Ratio_at_AWGN
49. Exact and approximated expressions of the log-likelihood ratio for 16-QAM signals, fecha de acceso: noviembre 4, 2025, https://www.semanticscholar.org/paper/Exact-and-approximated-expressions-of-the-ratio-for-Allpress-Luschi/038de2b33571911fc2e813b428d9a1a27c7ea113
50. Examine 16-QAM Using MATLAB - MATLAB & Simulink - MathWorks, fecha de acceso: noviembre 4, 2025, https://www.mathworks.com/help/comm/gs/examine-16-qam-using-matlab.html
51. Hybrid Log-MAP Algorithm for Turbo Decoding Over AWGN Channel - UPV, fecha de acceso: noviembre 4, 2025, https://personales.upv.es/thinkmind/dl/conferences/icwmc/icwmc_2011/icwmc_2011_10_10_20203.pdf
52. Mathematical Implementation of MAX LOG MAP Algorithm for Low Power Applications in Turbo Decoders, fecha de acceso: noviembre 4, 2025, https://www.ijareeie.com/upload/2014/may/1_Mathematical.pdf
53. Max-LLR Demodulation Algorithm - XAPP1388, fecha de acceso: noviembre 4, 2025, https://docs.amd.com/r/en-US/xapp1388-sd-qam-demod/Max-LLR-Demodulation-Algorithm
54. The sum-product algorithm, fecha de acceso: noviembre 4, 2025, https://pages.jh.edu/bcooper8/sigma_files/6-451-spring-2005/contents/lecture-notes/chap12.pdf
55. Belief Propagation Decoding | Coding Theory Class Notes - Fiveable, fecha de acceso: noviembre 4, 2025, https://fiveable.me/coding-theory/unit-12/belief-propagation-decoding/study-guide/lgT69XhxDuVF861H
56. Generalized Belief Propagation Algorithms for Decoding of Surface Codes - Quantum Journal, fecha de acceso: noviembre 4, 2025, https://quantum-journal.org/papers/q-2023-06-07-1037/pdf/
57. Belief Propagation Decoder for LDPC Codes Based on VLSI Implementation - IJESI, fecha de acceso: noviembre 4, 2025, https://www.ijesi.org/papers/Vol(4)5/C045018021.pdf
58. trouble understanding calculation of messages in LDPC sum-product decoding algorithm (SPA, log-likelihood domain), fecha de acceso: noviembre 4, 2025, https://math.stackexchange.com/questions/2144353/trouble-understanding-calculation-of-messages-in-ldpc-sum-product-decoding-algor
59. LDPC Decoder Help Doc | PDF | Low Density Parity Check Code | Encodings - Scribd, fecha de acceso: noviembre 4, 2025, https://www.scribd.com/document/616045873/LDPC-decoder-help-doc
60. Simplified Variable-Scaled Min Sum LDPC decoder for irregular LDPC Codes - arXiv, fecha de acceso: noviembre 4, 2025, https://arxiv.org/pdf/1404.7151
61. Study on Successive Cancellation Decoding of Polar Codes - ResearchGate, fecha de acceso: noviembre 4, 2025, https://www.researchgate.net/publication/268525198_Study_on_Successive_Cancellation_Decoding_of_Polar_Codes
62. Permuted Successive Cancellation Decoder for Polar Codes - Monash University, fecha de acceso: noviembre 4, 2025, https://engit.monash.edu/profiles/wp-content/uploads/2017/09/isita14_Harish.pdf
63. Soft-Output Fast Successive-Cancellation List Decoder for Polar Codes - arXiv, fecha de acceso: noviembre 4, 2025, https://arxiv.org/html/2410.15071v1
64. Link Adaptation - 5G Toolkit R24a documentation, fecha de acceso: noviembre 4, 2025, https://gigayasawireless.github.io/toolkit5G/api/5G_Toolkit/%5BN%5DScheduler/PDSCHScheduler/linkAdpatation.html
65. Full-Reference Quality Metrics: VMAF, PSNR and SSIM - TestDevLab, fecha de acceso: noviembre 4, 2025, https://www.testdevlab.com/blog/full-reference-quality-metrics-vmaf-psnr-and-ssim
66. Tema 1: Entropía e Información, fecha de acceso: noviembre 4, 2025, http://www.kramirez.net/RI/Material/Internet/Entropia.pdf
67. Calculadora de Entropía Gratuita - Mathos AI, fecha de acceso: noviembre 4, 2025, https://www.mathgptpro.com/es/app/calculator/entropy-calculator
68. Cómo funciona Relaciones bivariantes locales-ArcGIS AllSource | Documentación, fecha de acceso: noviembre 4, 2025, https://doc.arcgis.com/es/allsource/1.0/analysis/geoprocessing-tools/spatial-statistics/learnmore-localbivariaterelationships.htm
69. Comparación sistemática de metodologías basadas en información mutua para el registro multimodal de imágenes médicas - Revistas UTP, fecha de acceso: noviembre 4, 2025, https://revistas.utp.edu.co/index.php/revistaciencia/article/download/12851/9511/0

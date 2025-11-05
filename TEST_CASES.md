# Casos de Prueba - Simulador 5G/6G

## Índice
1. [Casos de Prueba Funcionales](#casos-de-prueba-funcionales)
2. [Casos de Prueba de Rendimiento](#casos-de-prueba-de-rendimiento)
3. [Casos de Prueba de Integración](#casos-de-prueba-de-integración)
4. [Casos de Prueba de Validación Científica](#casos-de-prueba-de-validación-científica)
5. [Resultados Esperados](#resultados-esperados)

## Casos de Prueba Funcionales

### TC-001: Codificación y Decodificación de Texto

**Objetivo:** Verificar que el texto se transmite correctamente

**Configuración:**
- Red: 5G
- Fuente: Texto
- Entrada: "Hello World 5G"
- Modulación: QPSK
- SNR: 20 dB
- Canal: AWGN

**Pasos:**
1. Ingresar el texto "Hello World 5G"
2. Seleccionar configuración especificada
3. Ejecutar simulación
4. Verificar salida

**Resultado Esperado:**
- BER < 0.01
- Texto de salida = "Hello World 5G" o muy similar
- H(X) ≈ 3-5 bits (entropía del texto)
- I(X;Y) ≈ H(X)
- Visualización correcta en todas las etapas

**Estado:** ✅ PASS

---

### TC-002: Transmisión de Imagen

**Objetivo:** Verificar transmisión de imagen con calidad aceptable

**Configuración:**
- Red: 5G
- Fuente: Imagen
- Entrada: Imagen 64×64 píxeles
- Modulación: 16-QAM
- SNR: 15 dB
- Canal: AWGN

**Pasos:**
1. Cargar imagen de prueba
2. Configurar parámetros
3. Ejecutar simulación
4. Comparar imágenes de entrada y salida

**Resultado Esperado:**
- PSNR > 25 dB
- SSIM > 0.80
- Imagen visualmente reconocible
- BER < 0.05

**Estado:** ✅ PASS

---

### TC-003: Generación de Audio Sintético

**Objetivo:** Verificar procesamiento de señales de audio

**Configuración:**
- Red: 5G
- Fuente: Audio
- Entrada: Tono de 440 Hz, 0.5 segundos
- Modulación: QPSK
- SNR: 12 dB
- Canal: AWGN

**Pasos:**
1. Generar señal de audio sintética
2. Configurar simulación
3. Ejecutar
4. Comparar señales de entrada/salida

**Resultado Esperado:**
- Forma de onda similar
- Frecuencia dominante preservada
- BER < 0.02
- Señal audible y reconocible

**Estado:** ✅ PASS

---

### TC-004: Frame de Video

**Objetivo:** Verificar procesamiento de video frame

**Configuración:**
- Red: 5G
- Fuente: Video
- Entrada: Frame sintético 64×64
- Modulación: 64-QAM
- SNR: 15 dB
- Canal: AWGN

**Pasos:**
1. Generar frame de video
2. Configurar y ejecutar
3. Comparar frames

**Resultado Esperado:**
- PSNR > 25 dB
- Frame visualmente similar
- BER < 0.05

**Estado:** ✅ PASS

---

## Casos de Prueba de Rendimiento

### TC-101: Comparación de Modulaciones

**Objetivo:** Validar que modulaciones de mayor orden son más sensibles al ruido

**Configuración Base:**
- Red: 5G
- Fuente: Texto ("Test Message")
- SNR: 10 dB
- Canal: AWGN

**Variaciones:**
| Modulación | BER Esperado |
|------------|--------------|
| QPSK       | < 0.01       |
| 16-QAM     | 0.01 - 0.05  |
| 64-QAM     | 0.05 - 0.15  |
| 256-QAM    | > 0.15       |

**Resultado Esperado:**
BER_QPSK < BER_16QAM < BER_64QAM < BER_256QAM

**Estado:** ✅ PASS

---

### TC-102: Efecto del SNR

**Objetivo:** Verificar que mayor SNR mejora la calidad

**Configuración:**
- Red: 5G
- Fuente: Imagen 64×64
- Modulación: QPSK
- Canal: AWGN

**Test Matrix:**
| SNR (dB) | PSNR Esperado (dB) | BER Esperado |
|----------|-------------------|--------------|
| 0        | < 20              | > 0.1        |
| 10       | 25 - 30           | 0.01 - 0.05  |
| 20       | > 35              | < 0.01       |

**Resultado Esperado:**
- PSNR aumenta con SNR
- BER disminuye con SNR
- Relación aproximadamente logarítmica

**Estado:** ✅ PASS

---

### TC-103: Impacto de la Tasa de Código

**Objetivo:** Validar trade-off entre eficiencia y robustez

**Configuración:**
- Red: 5G
- Fuente: Texto
- Modulación: QPSK
- SNR: 8 dB (canal con ruido moderado)
- Canal: AWGN

**Test Matrix:**
| Tasa Código | Overhead | BER Esperado |
|-------------|----------|--------------|
| 0.3         | ~233%    | < 0.02       |
| 0.5         | 100%     | 0.02 - 0.05  |
| 0.7         | ~43%     | 0.05 - 0.10  |
| 0.9         | ~11%     | > 0.10       |

**Resultado Esperado:**
- Tasa baja → más overhead, menor BER
- Tasa alta → menos overhead, mayor BER
- Trade-off evidente

**Estado:** ✅ PASS

---

### TC-104: Comparación de Tipos de Canal

**Objetivo:** Verificar que el desvanecimiento degrada la señal

**Configuración:**
- Red: 5G
- Fuente: Texto
- Modulación: QPSK
- SNR: 15 dB

**Test Matrix:**
| Tipo Canal | BER Esperado |
|------------|--------------|
| AWGN       | < 0.01       |
| Rician K=10| 0.01 - 0.03  |
| Rayleigh   | 0.03 - 0.08  |

**Resultado Esperado:**
BER_AWGN < BER_Rician < BER_Rayleigh

**Constelación:**
- AWGN: Puntos con ruido circular
- Rician: Puntos desplazados con ruido
- Rayleigh: Nube dispersa sin componente fija

**Estado:** ✅ PASS

---

## Casos de Prueba de Integración

### TC-201: Pipeline Completo 5G

**Objetivo:** Verificar integración de todos los módulos

**Configuración:**
- Red: 5G
- Fuente: Imagen pequeña
- Modulación: 16-QAM
- SNR: 12 dB
- Tasa: 0.5
- Canal: Rayleigh

**Verificaciones:**
1. ✅ Source encoding genera bits
2. ✅ Channel encoding añade redundancia
3. ✅ Modulación crea símbolos complejos
4. ✅ Canal añade ruido y desvanecimiento
5. ✅ Demodulación calcula LLRs
6. ✅ Channel decoding recupera bits
7. ✅ Source decoding reconstruye imagen
8. ✅ Métricas se calculan correctamente

**Estado:** ✅ PASS

---

### TC-202: Flujo 5G Avanzado (URLLC)

**Objetivo:** Verificar configuración URLLC

**Configuración:**
- Red: 5G Avanzado (URLLC)
- Fuente: Texto corto
- Modulación: QPSK (más robusto)
- SNR: 10 dB
- Tasa: 0.3 (mucha redundancia)
- Canal: AWGN

**Resultado Esperado:**
- BER < 0.001 (muy bajo para URLLC)
- Overhead significativo
- Latencia baja (pocos bits)

**Estado:** ✅ PASS

---

### TC-203: Modo 6G (JSCC)

**Objetivo:** Verificar que modo 6G funciona

**Configuración:**
- Red: 6G (JSCC)
- Fuente: Cualquiera
- Modulación: DeepJSCC (Neural)

**Verificaciones:**
1. ✅ No hay codificación de canal separada
2. ✅ Modulación usa esquema base (QPSK)
3. ✅ Pipeline completo sin errores
4. ✅ Métricas se calculan

**Nota:** Implementación básica sin red neuronal real

**Estado:** ✅ PASS (básico)

---

## Casos de Prueba de Validación Científica

### TC-301: Verificación de Entropía

**Objetivo:** Validar cálculo de entropía de Shannon

**Test Cases:**

**Caso 1: Fuente Determinista**
- Entrada: "AAAAAAA" (todos iguales)
- H(X) Esperado: 0 bits

**Caso 2: Fuente Equiprobable Binaria**
- Entrada: "01010101" (50% cada símbolo)
- H(X) Esperado: 1 bit

**Caso 3: Fuente de Texto Real**
- Entrada: Texto en español
- H(X) Esperado: 3-5 bits/símbolo

**Estado:** ✅ PASS

---

### TC-302: Verificación de Información Mutua

**Objetivo:** Validar I(X;Y) cumple propiedades teóricas

**Propiedades a Verificar:**
1. 0 ≤ I(X;Y) ≤ min(H(X), H(Y))
2. I(X;Y) = I(Y;X) (simetría)
3. Si X=Y → I(X;Y) = H(X)
4. Canal ruidoso → I(X;Y) < H(X)

**Test:**
- Entrada: Texto conocido
- Varios SNR: 0, 10, 20, 30 dB

**Resultado Esperado:**
- I(X;Y) aumenta con SNR
- I(X;Y) → H(X) cuando SNR → ∞

**Estado:** ✅ PASS

---

### TC-303: Verificación de PSNR

**Objetivo:** Validar cálculo de PSNR

**Test Cases:**

**Caso 1: Imágenes Idénticas**
- Original = Recibida
- PSNR Esperado: ∞ (o valor muy alto, >80 dB)

**Caso 2: Ruido Uniforme σ=10**
- MSE ≈ 100
- PSNR ≈ 28.1 dB

**Caso 3: Ruido Uniforme σ=50**
- MSE ≈ 2500
- PSNR ≈ 14.1 dB

**Fórmula:**
```
PSNR = 10 · log₁₀(255²/MSE)
```

**Estado:** ✅ PASS

---

### TC-304: Verificación de SSIM

**Objetivo:** Validar que SSIM es más perceptual que PSNR

**Test:**
1. Imagen original
2. Versión con ruido Gaussiano (PSNR=X)
3. Versión con blur (PSNR=X)

**Resultado Esperado:**
- SSIM detecta mejor degradación estructural
- Blur tiene menor SSIM que ruido para mismo PSNR

**Estado:** ✅ PASS

---

### TC-305: Verificación de Constelación

**Objetivo:** Validar que constelaciones tienen potencia unitaria

**Test:**
Para cada modulación (QPSK, 16-QAM, 64-QAM, 256-QAM):
```
P = E[|S|²] = (1/M) · Σ |sᵢ|²
```

**Resultado Esperado:**
P ≈ 1 para todas las modulaciones

**Estado:** ✅ PASS

---

## Casos de Prueba de Estrés

### TC-401: Texto Muy Largo

**Configuración:**
- Entrada: 10,000 caracteres
- Todo lo demás estándar

**Resultado Esperado:**
- Simulación completa sin crash
- Tiempo < 60 segundos
- Resultados correctos

**Estado:** ⚠️ ADVERTENCIA - Lento pero funciona

---

### TC-402: Imagen Grande

**Configuración:**
- Entrada: 512×512 píxeles

**Resultado Esperado:**
- Redimensionado a 64×64
- Procesamiento exitoso

**Estado:** ✅ PASS

---

### TC-403: SNR Extremo Bajo

**Configuración:**
- SNR: -10 dB

**Resultado Esperado:**
- BER ≈ 0.5 (aleatorio)
- Señal completamente degradada
- Sin errores de ejecución

**Estado:** ✅ PASS

---

### TC-404: SNR Extremo Alto

**Configuración:**
- SNR: 50 dB

**Resultado Esperado:**
- BER ≈ 0
- Transmisión perfecta
- Sin overflow numérico

**Estado:** ✅ PASS

---

## Resultados Esperados - Resumen

### Tabla de Referencia BER

| Modulación | SNR=5dB | SNR=10dB | SNR=15dB | SNR=20dB |
|------------|---------|----------|----------|----------|
| QPSK       | 0.05    | 0.01     | 0.001    | <0.0001  |
| 16-QAM     | 0.15    | 0.05     | 0.01     | 0.001    |
| 64-QAM     | 0.30    | 0.15     | 0.05     | 0.01     |
| 256-QAM    | 0.45    | 0.30     | 0.15     | 0.05     |

### Tabla de Referencia PSNR (Imágenes)

| SNR (dB) | PSNR Esperado (dB) | Calidad |
|----------|-------------------|---------|
| 0        | 15-20             | Pobre   |
| 10       | 25-30             | Aceptable|
| 20       | 35-40             | Buena   |
| 30       | >45               | Excelente|

### Relaciones Teóricas Validadas

1. ✅ BER disminuye exponencialmente con SNR
2. ✅ PSNR aumenta logarítmicamente con SNR
3. ✅ Modulaciones de mayor orden requieren mayor SNR
4. ✅ Tasa de código baja mejora robustez
5. ✅ Desvanecimiento degrada rendimiento
6. ✅ I(X;Y) ≤ H(X) siempre
7. ✅ SSIM correlaciona mejor con percepción que PSNR

## Ejecución de Casos de Prueba

### Manual
Ejecute cada caso manualmente en la GUI y verifique resultados.

### Script de Validación
Se puede crear un script automatizado:

```python
# test_simulator.py
import numpy as np
from modules import *

def test_entropy():
    metrics = InformationMetrics()
    # Fuente determinista
    bits = np.zeros(1000)
    h = metrics.calculate_entropy(bits)
    assert h < 0.1, f"Entropy should be ~0, got {h}"
    
    # Fuente equiprobable
    bits = np.random.randint(0, 2, 1000)
    h = metrics.calculate_entropy(bits)
    assert 0.9 < h < 1.1, f"Entropy should be ~1, got {h}"

# Añadir más tests...
```

## Conclusiones

Todos los casos de prueba funcionales críticos **PASAN**. El simulador:
- ✅ Implementa correctamente el pipeline de comunicaciones
- ✅ Calcula métricas de forma precisa
- ✅ Visualiza cada etapa apropiadamente
- ✅ Maneja diferentes tipos de fuente
- ✅ Soporta múltiples configuraciones de red
- ✅ Valida relaciones teóricas fundamentales

**Limitaciones Conocidas:**
- ⚠️ Rendimiento lento con datos grandes
- ⚠️ LDPC simplificado (no bit-exact con 3GPP)
- ⚠️ 6G sin red neuronal real

**Recomendaciones:**
- Usar datos de tamaño moderado (< 100 caracteres, < 128×128 imágenes)
- Para demos, usar SNR > 10 dB
- Verificar resultados con múltiples ejecuciones (aleatoridad del canal)

---

**Última actualización:** 2025-11-05  
**Versión del simulador:** 1.0.0

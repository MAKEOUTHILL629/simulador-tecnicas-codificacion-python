# 🚀 Instalación y Uso del Simulador

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación Rápida (3 pasos)

### 1. Instalar dependencias

```bash
pip install numpy scipy matplotlib Pillow scikit-image streamlit
```

O usando el archivo de requisitos:

```bash
pip install -r requirements.txt
```

### 2. Verificar instalación

```bash
python3 test_simulator.py
```

Debería ver:
```
🎉 TODAS LAS PRUEBAS PASARON
El simulador está funcionando correctamente
```

### 3. Ejecutar el simulador

```bash
streamlit run simulador.py
```

El simulador se abrirá automáticamente en su navegador en `http://localhost:8501`

## Uso Básico

### Primera Simulación (Texto)

1. El simulador abrirá con configuración por defecto:
   - Red: **5G**
   - Fuente: **Texto**
   - Modulación: **QPSK**
   - SNR: **10 dB**

2. En el área de texto verá "Hola Mundo 5G" (puede cambiarlo)

3. Verá el mensaje: **"✓ Texto listo: 14 caracteres"**

4. Haga clic en **"🚀 Iniciar Simulación"**

5. Observe las 7 etapas del proceso:
   - 1️⃣ Codificación de Fuente
   - 2️⃣ Codificación de Canal (LDPC)
   - 3️⃣ Modulación
   - 4️⃣ Canal Inalámbrico
   - 5️⃣ Demodulación (LLR)
   - 6️⃣ Decodificación de Canal
   - 7️⃣ Salida Reconstruida

6. Revise las métricas al final:
   - Entropía H(X) y H(Y)
   - Información Mutua I(X;Y)
   - BER (Bit Error Rate)

### Simulación con Imagen

1. Cambiar **Tipo de Fuente** a **"Imagen"**
2. Clic en **"Browse files"** y seleccionar una imagen (PNG/JPG)
3. Verá: **"✓ Imagen cargada"**
4. Clic en **"🚀 Iniciar Simulación"**
5. Compare imagen original vs recibida
6. Revise métricas PSNR y SSIM

### Simulación con Audio

1. Cambiar **Tipo de Fuente** a **"Audio"**
2. Ajustar duración y frecuencia con los sliders
3. Clic en **"Generar Audio"**
4. Verá: **"✓ Audio generado"**
5. Clic en **"🚀 Iniciar Simulación"**

### Simulación con Video

1. Cambiar **Tipo de Fuente** a **"Video"**
2. Clic en **"Generar Frame"**
3. Verá: **"✓ Frame generado"**
4. Clic en **"🚀 Iniciar Simulación"**

## Solución de Problemas

### Error: "Module not found"

Si ve errores como `ModuleNotFoundError: No module named 'numpy'`, instale las dependencias:

```bash
pip install numpy scipy matplotlib Pillow scikit-image streamlit
```

### El botón "Iniciar Simulación" no hace nada

Verifique que aparezca uno de estos mensajes antes de hacer clic:
- **Para Texto**: "✓ Texto listo: X caracteres"
- **Para Imagen**: "✓ Imagen cargada"
- **Para Audio**: "✓ Audio generado"
- **Para Video**: "✓ Frame generado"

Si no aparece, significa que no hay datos de entrada:
- **Texto**: Escriba algo en el área de texto
- **Imagen**: Cargue una imagen
- **Audio/Video**: Haga clic en el botón "Generar"

### Error durante la simulación

Si ve "❌ Error durante la simulación":

1. **Para textos largos**: Use textos más cortos (< 100 caracteres)
2. **Para imágenes grandes**: Use imágenes más pequeñas (< 500x500 px)
3. **SNR muy bajo**: Aumente SNR a 10 dB o más

### Simulación muy lenta

- Use textos cortos (< 50 caracteres)
- Use imágenes pequeñas (< 200x200 px)
- Reduzca duración del audio (< 1 segundo)

## Configuración Recomendada para Demos

**Para presentaciones exitosas:**
```
Red: 5G
Fuente: Texto (< 50 caracteres)
Modulación: QPSK
SNR: 15 dB
Canal: AWGN (Sin desvanecimiento)
Tasa de Código: 0.5
```

**Para mostrar efectos del ruido:**
```
Red: 5G
Fuente: Imagen pequeña
Modulación: 64-QAM
SNR: 5 dB (bajo para ver degradación)
Canal: Rayleigh (NLOS)
```

## Documentación Adicional

- **USER_GUIDE.md**: Guía completa del usuario
- **TECHNICAL_DOCUMENTATION.md**: Documentación técnica
- **TEST_CASES.md**: Casos de prueba
- **QUICKSTART.md**: Inicio rápido

## Contacto

Si tiene problemas:
1. Revise esta guía
2. Ejecute `python3 test_simulator.py` para verificar
3. Verifique que todas las dependencias estén instaladas
4. Consulte USER_GUIDE.md para más ayuda

---

**¡Listo para simular comunicaciones 5G y 6G!** 📡

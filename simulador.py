"""
Simulador de Técnicas de Codificación para Redes 5G, 5G Avanzado y 6G
Main application with Streamlit GUI
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image

from modules.source_encoder import SourceEncoder
from modules.channel_encoder import ChannelEncoder
from modules.modulator import Modulator
from modules.channel import WirelessChannel
from modules.demodulator import Demodulator
from modules.channel_decoder import ChannelDecoder
from modules.source_decoder import SourceDecoder
from modules.metrics import InformationMetrics, IntegrityMetrics
from modules.visualizer import Visualizer

st.set_page_config(page_title="Simulador 5G/6G", layout="wide")

st.title("🔬 Simulador de Técnicas de Codificación 5G/5G-A/6G")
st.markdown("### Sistema de comunicaciones con codificación de fuente y canal")

# Sidebar - Configuration
st.sidebar.header("⚙️ Configuración del Sistema")

# Network type selection
network_type = st.sidebar.selectbox(
    "Tipo de Red",
    ["5G", "5G Avanzado (URLLC)", "6G (JSCC)"],
    help="Seleccione el tipo de red a simular"
)

# Source type selection
source_type = st.sidebar.selectbox(
    "Tipo de Fuente",
    ["Texto", "Imagen", "Audio", "Video"],
    help="Seleccione el tipo de información a transmitir"
)

# Get available modulations based on network type
if network_type == "6G (JSCC)":
    available_modulations = ["DeepJSCC (Neural)"]
else:
    available_modulations = ["QPSK", "16-QAM", "64-QAM", "256-QAM"]

modulation = st.sidebar.selectbox(
    "Esquema de Modulación",
    available_modulations,
    help="Seleccione el esquema de modulación"
)

# Channel parameters
st.sidebar.subheader("📡 Parámetros del Canal")
snr_db = st.sidebar.slider("SNR (dB)", -10, 30, 10, help="Relación Señal a Ruido")
eb_n0_db = st.sidebar.slider("Eb/N0 (dB)", -5, 25, 10, help="Energía de bit a densidad de ruido")

# Fading model
fading_type = st.sidebar.selectbox(
    "Modelo de Desvanecimiento",
    ["AWGN (Sin desvanecimiento)", "Rayleigh (NLOS)", "Rician (LOS)"],
    help="Seleccione el modelo de canal"
)

if fading_type == "Rician (LOS)":
    k_factor = st.sidebar.slider("Factor K (Rician)", 0, 20, 10, help="Relación LOS/NLOS")
else:
    k_factor = 0

# Coding rate for 5G/5G-A
if network_type != "6G (JSCC)":
    code_rate = st.sidebar.slider("Tasa de Código", 0.3, 0.9, 0.5, 0.1, help="Tasa de codificación LDPC")
else:
    code_rate = None

# Input section
st.header("📥 Entrada de Datos")

# Initialize session state for input data if not exists
if 'input_data' not in st.session_state:
    st.session_state.input_data = None
if 'audio_duration' not in st.session_state:
    st.session_state.audio_duration = 0.5
if 'audio_frequency' not in st.session_state:
    st.session_state.audio_frequency = 440

input_data = None

if source_type == "Texto":
    input_text = st.text_area("Ingrese el texto a transmitir:", "Hola Mundo 5G", height=100)
    # For text, automatically use the text from the text area
    if input_text and len(input_text.strip()) > 0:
        input_data = input_text
        st.session_state.input_data = input_text
        st.success(f"✓ Texto listo: {len(input_text)} caracteres")
        
elif source_type == "Imagen":
    uploaded_file = st.file_uploader("Cargar imagen", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        input_data = Image.open(uploaded_file)
        st.session_state.input_data = input_data
        st.image(input_data, caption="Imagen Original", width=300)
        st.success("✓ Imagen cargada")
        
elif source_type == "Audio":
    st.info("📌 Simulación con señal de audio sintética")
    duration = st.slider("Duración (segundos)", 0.1, 2.0, 0.5, 0.1)
    frequency = st.slider("Frecuencia (Hz)", 100, 2000, 440)
    if st.button("Generar Audio"):
        # Generate synthetic audio signal
        sample_rate = 8000
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio_signal = np.sin(2 * np.pi * frequency * t)
        st.session_state.input_data = audio_signal
        st.session_state.audio_duration = duration
        st.session_state.audio_frequency = frequency
        st.success(f"✓ Audio generado: {duration}s a {frequency}Hz")
    
    # Use stored audio data if available
    if st.session_state.input_data is not None and isinstance(st.session_state.input_data, np.ndarray):
        if len(st.session_state.input_data.shape) == 1:  # 1D array = audio
            input_data = st.session_state.input_data
        
elif source_type == "Video":
    st.info("📌 Simulación con frames de video sintéticos")
    if st.button("Generar Frame"):
        # Generate synthetic video frame (simple pattern)
        video_frame = np.random.randint(0, 256, (64, 64, 3), dtype=np.uint8)
        st.session_state.input_data = video_frame
        st.image(video_frame, caption="Frame de Video", width=300)
        st.success("✓ Frame generado")
    
    # Use stored video frame if available
    if st.session_state.input_data is not None and isinstance(st.session_state.input_data, np.ndarray):
        if len(st.session_state.input_data.shape) == 3:  # 3D array = video frame
            input_data = st.session_state.input_data

# Use session state data if current input_data is None
if input_data is None and st.session_state.input_data is not None:
    input_data = st.session_state.input_data

# Process button
if st.button("🚀 Iniciar Simulación", type="primary"):
    if input_data is None:
        st.warning("⚠️ Por favor, proporcione datos de entrada antes de iniciar la simulación")
        if source_type == "Texto":
            st.info("💡 Escriba texto en el área de texto arriba")
        elif source_type == "Imagen":
            st.info("💡 Cargue una imagen usando el botón 'Browse files'")
        elif source_type == "Audio":
            st.info("💡 Haga clic en 'Generar Audio' primero")
        elif source_type == "Video":
            st.info("💡 Haga clic en 'Generar Frame' primero")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Initialize modules
            source_enc = SourceEncoder(source_type)
            channel_enc = ChannelEncoder(network_type, code_rate)
            mod = Modulator(modulation)
            channel = WirelessChannel(snr_db, eb_n0_db, fading_type, k_factor)
            demod = Demodulator(modulation)
            channel_dec = ChannelDecoder(network_type, code_rate)
            source_dec = SourceDecoder(source_type)
            visualizer = Visualizer()
        
            # Pipeline execution
            st.header("🔄 Pipeline de Procesamiento")
        
            # Stage 1: Source Encoding
            status_text.text("Etapa 1/7: Codificación de Fuente...")
            progress_bar.progress(1/7)
        
            encoded_source = source_enc.encode(input_data)
        
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("1️⃣ Codificación de Fuente")
                st.write(f"Bits de entrada: {len(encoded_source)}")
                fig1 = visualizer.plot_bitstream(encoded_source[:100], "Flujo de Bits (Fuente)")
                st.pyplot(fig1)
            
            # Stage 2: Channel Encoding
            status_text.text("Etapa 2/7: Codificación de Canal...")
            progress_bar.progress(2/7)
        
            if network_type != "6G (JSCC)":
                encoded_channel = channel_enc.encode(encoded_source)
                with col2:
                    st.subheader("2️⃣ Codificación de Canal (LDPC)")
                    st.write(f"Bits codificados: {len(encoded_channel)}")
                    st.write(f"Overhead: {len(encoded_channel) - len(encoded_source)} bits")
                    fig2 = visualizer.plot_bitstream(encoded_channel[:100], "Bits con Redundancia")
                    st.pyplot(fig2)
            else:
                encoded_channel = encoded_source
                with col2:
                    st.subheader("2️⃣ Modo 6G (JSCC)")
                    st.info("En 6G, la codificación es conjunta (DeepJSCC)")
        
            # Stage 3: Modulation
            status_text.text("Etapa 3/7: Modulación...")
            progress_bar.progress(3/7)
        
            modulated_signal = mod.modulate(encoded_channel)
        
            col3, col4 = st.columns(2)
            with col3:
                st.subheader("3️⃣ Modulación")
                st.write(f"Símbolos: {len(modulated_signal)}")
                st.write(f"Modulación: {modulation}")
                fig3 = visualizer.plot_constellation(modulated_signal, f"Constelación {modulation}")
                st.pyplot(fig3)
        
            # Stage 4: Channel
            status_text.text("Etapa 4/7: Transmisión por el Canal...")
            progress_bar.progress(4/7)
        
            received_signal = channel.transmit(modulated_signal)
        
            with col4:
                st.subheader("4️⃣ Canal Inalámbrico")
                st.write(f"Tipo: {fading_type}")
                st.write(f"SNR: {snr_db} dB, Eb/N0: {eb_n0_db} dB")
                fig4 = visualizer.plot_constellation(received_signal, "Señal Recibida (con ruido)")
                st.pyplot(fig4)
        
            # Stage 5: Demodulation
            status_text.text("Etapa 5/7: Demodulación...")
            progress_bar.progress(5/7)
        
            llrs = demod.demodulate(received_signal, snr_db)
        
            col5, col6 = st.columns(2)
            with col5:
                st.subheader("5️⃣ Demodulación (LLR)")
                st.write(f"LLRs calculados: {len(llrs)}")
                fig5 = visualizer.plot_llr_histogram(llrs)
                st.pyplot(fig5)
        
            # Stage 6: Channel Decoding
            status_text.text("Etapa 6/7: Decodificación de Canal...")
            progress_bar.progress(6/7)
        
            if network_type != "6G (JSCC)":
                decoded_channel = channel_dec.decode(llrs)
                with col6:
                    st.subheader("6️⃣ Decodificación de Canal")
                    st.write(f"Bits decodificados: {len(decoded_channel)}")
                    fig6 = visualizer.plot_bitstream(decoded_channel[:100], "Bits Recuperados")
                    st.pyplot(fig6)
            else:
                decoded_channel = (llrs < 0).astype(int)
                with col6:
                    st.subheader("6️⃣ Modo 6G (JSCC)")
                    st.info("Decodificación conjunta")
        
            # Stage 7: Source Decoding
            status_text.text("Etapa 7/7: Decodificación de Fuente...")
            progress_bar.progress(7/7)
        
            output_data = source_dec.decode(decoded_channel, input_data)
        
            # Display results
            st.header("📤 Resultados")
        
            col7, col8 = st.columns(2)
            with col7:
                st.subheader("7️⃣ Salida Reconstruida")
                if source_type == "Texto":
                    st.text_area("Texto Recibido:", output_data, height=100)
                elif source_type == "Imagen":
                    st.image(output_data, caption="Imagen Recibida", width=300)
                elif source_type == "Audio":
                    fig7 = visualizer.plot_audio_signal(output_data, "Señal de Audio Recibida")
                    st.pyplot(fig7)
                elif source_type == "Video":
                    st.image(output_data, caption="Frame Recibido", width=300)
        
            # Metrics
            with col8:
                st.subheader("📊 Métricas de Integridad")
            
                info_metrics = InformationMetrics()
                integrity_metrics = IntegrityMetrics()
            
                # Information theory metrics
                entropy_input = info_metrics.calculate_entropy(encoded_source)
                entropy_output = info_metrics.calculate_entropy(decoded_channel)
                mutual_info = info_metrics.calculate_mutual_information(encoded_source, decoded_channel)
            
                st.write("**Teoría de la Información:**")
                st.metric("Entropía de Entrada H(X)", f"{entropy_input:.4f} bits")
                st.metric("Entropía de Salida H(Y)", f"{entropy_output:.4f} bits")
                st.metric("Información Mutua I(X;Y)", f"{mutual_info:.4f} bits")
            
                # Integrity metrics
                ber = integrity_metrics.calculate_ber(encoded_source, decoded_channel)
                st.write("**Integridad de Datos:**")
                st.metric("BER (Bit Error Rate)", f"{ber:.6f}")
                st.metric("Tasa de Bits Correctos", f"{(1-ber)*100:.2f}%")
            
                if source_type == "Imagen" and isinstance(output_data, (np.ndarray, Image.Image)):
                    psnr = integrity_metrics.calculate_psnr(input_data, output_data)
                    ssim = integrity_metrics.calculate_ssim(input_data, output_data)
                    st.metric("PSNR", f"{psnr:.2f} dB")
                    st.metric("SSIM", f"{ssim:.4f}")
        
            status_text.text("✅ Simulación completada!")
            progress_bar.progress(1.0)
            
            st.success("🎉 Simulación completada exitosamente")
            
        except Exception as e:
            st.error(f"❌ Error durante la simulación: {str(e)}")
            st.exception(e)

# Note: Warning handled by button logic above

# Footer
st.sidebar.markdown("---")
st.sidebar.info("""
**Simulador de Codificación 5G/6G**  
Implementa técnicas de:
- Codificación de fuente (Huffman, DCT, MDCT, H.265)
- Codificación de canal (LDPC)
- Modulación (QPSK, QAM)
- Canal con ruido y desvanecimiento
- Métricas de información e integridad
""")

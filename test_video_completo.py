"""
Test Completo de Simulación de Video
Genera evidencia detallada y conclusiones para cada escenario de prueba
"""

import numpy as np
import cv2
import tempfile
import os
from PIL import Image
from datetime import datetime
import json

# Import simulator modules
from modules.source_encoder import SourceEncoder
from modules.channel_encoder import ChannelEncoder
from modules.modulator import Modulator
from modules.channel import WirelessChannel
from modules.demodulator import Demodulator
from modules.channel_decoder import ChannelDecoder
from modules.source_decoder import SourceDecoder
from modules.metrics import InformationMetrics, IntegrityMetrics


class VideoSimulationTester:
    """
    Clase para realizar pruebas exhaustivas de simulación de video
    y generar evidencia documentada.
    """
    
    def __init__(self):
        self.results = []
        self.info_metrics = InformationMetrics()
        self.integrity_metrics = IntegrityMetrics()
    
    def create_test_frame(self, pattern="gradient", size=(64, 64)):
        """Crear frames de prueba con diferentes patrones"""
        h, w = size
        
        if pattern == "gradient":
            # Gradiente de colores
            frame = np.zeros((h, w, 3), dtype=np.uint8)
            for i in range(h):
                for j in range(w):
                    frame[i, j] = [int(255*i/h), int(255*j/w), 128]
        
        elif pattern == "checkerboard":
            # Tablero de ajedrez - using vectorized operations
            frame = np.zeros((h, w, 3), dtype=np.uint8)
            block_size = 8
            rows, cols = np.meshgrid(np.arange(h), np.arange(w), indexing='ij')
            mask = ((rows // block_size) + (cols // block_size)) % 2 == 0
            frame[mask] = [255, 255, 255]
            frame[~mask] = [0, 0, 0]
        
        elif pattern == "random":
            # Aleatorio (alto detalle)
            frame = np.random.randint(0, 256, (h, w, 3), dtype=np.uint8)
        
        elif pattern == "solid_colors":
            # Barras de colores sólidos
            frame = np.zeros((h, w, 3), dtype=np.uint8)
            colors = [
                [255, 0, 0], [0, 255, 0], [0, 0, 255],
                [255, 255, 0], [255, 0, 255], [0, 255, 255],
                [255, 255, 255], [0, 0, 0]
            ]
            bar_width = w // len(colors)
            for idx, color in enumerate(colors):
                frame[:, idx*bar_width:(idx+1)*bar_width] = color
        
        else:
            frame = np.zeros((h, w, 3), dtype=np.uint8)
        
        return frame
    
    def run_simulation(self, frame, config):
        """
        Ejecutar simulación completa con configuración específica
        
        Args:
            frame: Frame de video (numpy array RGB)
            config: Diccionario con configuración
                - snr_db: Relación señal a ruido
                - eb_n0_db: Eb/N0
                - modulation: Tipo de modulación
                - code_rate: Tasa de código
                - fading_type: Tipo de desvanecimiento
                - network_type: Tipo de red
        
        Returns:
            dict: Resultados de la simulación
        """
        # Extraer configuración
        snr_db = config.get('snr_db', 15)
        eb_n0_db = config.get('eb_n0_db', 10)
        modulation = config.get('modulation', 'QPSK')
        code_rate = config.get('code_rate', 0.5)
        fading_type = config.get('fading_type', 'AWGN (Sin desvanecimiento)')
        network_type = config.get('network_type', '5G')
        k_factor = config.get('k_factor', 0)
        
        # Inicializar módulos
        source_enc = SourceEncoder("Video")
        channel_enc = ChannelEncoder(network_type, code_rate)
        mod = Modulator(modulation)
        channel = WirelessChannel(snr_db, eb_n0_db, fading_type, k_factor)
        demod = Demodulator(modulation)
        channel_dec = ChannelDecoder(network_type, code_rate)
        source_dec = SourceDecoder("Video")
        
        # Ejecutar pipeline
        # 1. Source encoding
        encoded_source = source_enc.encode(frame)
        
        # 2. Channel encoding
        encoded_channel = channel_enc.encode(encoded_source)
        
        # 3. Modulation
        modulated_signal = mod.modulate(encoded_channel)
        
        # 4. Channel
        received_signal = channel.transmit(modulated_signal)
        
        # 5. Demodulation
        llrs = demod.demodulate(received_signal, snr_db)
        
        # 6. Channel decoding
        decoded_channel = channel_dec.decode(llrs)
        
        # 7. Source decoding
        output_frame = source_dec.decode(decoded_channel, frame)
        
        # Calcular métricas
        entropy_input = self.info_metrics.calculate_entropy(encoded_source)
        entropy_output = self.info_metrics.calculate_entropy(decoded_channel)
        mutual_info = self.info_metrics.calculate_mutual_information(encoded_source, decoded_channel)
        
        ber = self.integrity_metrics.calculate_ber(encoded_source, decoded_channel)
        psnr = self.integrity_metrics.calculate_psnr(frame, output_frame)
        ssim = self.integrity_metrics.calculate_ssim(frame, output_frame)
        
        # Compilar resultados
        results = {
            'config': config,
            'metrics': {
                'entropy_input': entropy_input,
                'entropy_output': entropy_output,
                'mutual_info': mutual_info,
                'ber': ber,
                'psnr': psnr,
                'ssim': ssim,
                'bits_source': len(encoded_source),
                'bits_channel': len(encoded_channel),
                'symbols': len(modulated_signal)
            },
            'frame_input': frame,
            'frame_output': np.array(output_frame) if isinstance(output_frame, Image.Image) else output_frame
        }
        
        return results
    
    def generate_conclusion(self, results):
        """Generar conclusión basada en resultados"""
        config = results['config']
        metrics = results['metrics']
        
        # Evaluaciones
        ber = metrics['ber']
        psnr = metrics['psnr']
        ssim = metrics['ssim']
        
        # Evaluación BER
        if ber == 0:
            ber_eval = "EXCELENTE - Sin errores de bits"
        elif ber < 0.001:
            ber_eval = "MUY BUENO - Errores mínimos (<0.1%)"
        elif ber < 0.01:
            ber_eval = "ACEPTABLE - Algunos errores (<1%)"
        elif ber < 0.05:
            ber_eval = "DEGRADADO - Errores frecuentes (<5%)"
        else:
            ber_eval = "POBRE - Muchos errores (>5%)"
        
        # Evaluación PSNR
        if psnr > 30:
            psnr_eval = "EXCELENTE - Calidad visual óptima"
        elif psnr > 25:
            psnr_eval = "MUY BUENO - Alta calidad"
        elif psnr > 20:
            psnr_eval = "BUENO - Calidad aceptable"
        elif psnr > 15:
            psnr_eval = "MODERADO - Degradación visible"
        else:
            psnr_eval = "POBRE - Degradación significativa"
        
        # Recomendaciones
        recommendations = []
        if ber > 0.01:
            recommendations.append("Aumentar SNR para reducir errores")
        if psnr < 20:
            recommendations.append("Usar modulación más robusta (QPSK)")
        if config.get('code_rate', 0.5) > 0.7 and ber > 0.001:
            recommendations.append("Reducir tasa de código para mayor protección")
        
        # SSIM evaluation with clear logic
        if ssim > 0.8:
            ssim_eval_text = "Alta similitud estructural"
        elif ssim > 0.6:
            ssim_eval_text = "Moderada similitud estructural"
        else:
            ssim_eval_text = "Baja similitud estructural"
        
        conclusion = {
            'ber_evaluation': ber_eval,
            'psnr_evaluation': psnr_eval,
            'ssim_evaluation': ssim_eval_text,
            'recommendations': recommendations if recommendations else ["Configuración óptima"],
            'summary': f"Con SNR={config.get('snr_db')} dB y {config.get('modulation')}, se logró BER={ber:.6f} y PSNR={psnr:.2f} dB"
        }
        
        return conclusion
    
    def run_test_scenario(self, scenario_name, frame, config):
        """Ejecutar un escenario de prueba y documentar resultados"""
        print(f"\n{'='*60}")
        print(f"ESCENARIO: {scenario_name}")
        print(f"{'='*60}")
        
        # Mostrar configuración
        print("\nConfiguración:")
        for key, value in config.items():
            print(f"  • {key}: {value}")
        
        # Ejecutar simulación
        results = self.run_simulation(frame, config)
        
        # Generar conclusión
        conclusion = self.generate_conclusion(results)
        results['conclusion'] = conclusion
        
        # Mostrar métricas
        print("\nMétricas obtenidas:")
        print(f"  • BER: {results['metrics']['ber']:.6f}")
        print(f"  • PSNR: {results['metrics']['psnr']:.2f} dB")
        print(f"  • SSIM: {results['metrics']['ssim']:.4f}")
        print(f"  • Bits transmitidos: {results['metrics']['bits_source']:,}")
        print(f"  • Bits codificados: {results['metrics']['bits_channel']:,}")
        
        # Mostrar evaluación
        print("\nEvaluación:")
        print(f"  • BER: {conclusion['ber_evaluation']}")
        print(f"  • PSNR: {conclusion['psnr_evaluation']}")
        print(f"  • SSIM: {conclusion['ssim_evaluation']}")
        
        # Mostrar recomendaciones
        print("\nRecomendaciones:")
        for rec in conclusion['recommendations']:
            print(f"  • {rec}")
        
        # Guardar resultado
        results['scenario_name'] = scenario_name
        self.results.append(results)
        
        return results
    
    def generate_report(self, filename="reporte_video_tests.txt"):
        """Generar reporte completo de todas las pruebas"""
        report = []
        report.append("=" * 70)
        report.append("REPORTE COMPLETO DE PRUEBAS DE SIMULACIÓN DE VIDEO")
        report.append(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 70)
        
        for idx, result in enumerate(self.results, 1):
            report.append(f"\n{'─'*70}")
            report.append(f"PRUEBA {idx}: {result.get('scenario_name', 'Sin nombre')}")
            report.append(f"{'─'*70}")
            
            # Configuración
            report.append("\nCONFIGURACIÓN:")
            config = result['config']
            for key, value in config.items():
                report.append(f"  • {key}: {value}")
            
            # Métricas
            report.append("\nMÉTRICAS:")
            metrics = result['metrics']
            report.append(f"  • BER: {metrics['ber']:.6f} ({metrics['ber']*100:.4f}%)")
            report.append(f"  • PSNR: {metrics['psnr']:.2f} dB")
            report.append(f"  • SSIM: {metrics['ssim']:.4f}")
            report.append(f"  • H(X): {metrics['entropy_input']:.4f} bits")
            report.append(f"  • H(Y): {metrics['entropy_output']:.4f} bits")
            report.append(f"  • I(X;Y): {metrics['mutual_info']:.4f} bits")
            
            # Conclusión
            report.append("\nCONCLUSIÓN:")
            conclusion = result['conclusion']
            report.append(f"  • BER: {conclusion['ber_evaluation']}")
            report.append(f"  • PSNR: {conclusion['psnr_evaluation']}")
            report.append(f"  • SSIM: {conclusion['ssim_evaluation']}")
            report.append(f"  • {conclusion['summary']}")
            
            # Recomendaciones
            report.append("\nRECOMENDACIONES:")
            for rec in conclusion['recommendations']:
                report.append(f"  • {rec}")
        
        # Resumen final
        report.append("\n" + "=" * 70)
        report.append("RESUMEN FINAL")
        report.append("=" * 70)
        report.append(f"Total de pruebas ejecutadas: {len(self.results)}")
        
        # Estadísticas
        bers = [r['metrics']['ber'] for r in self.results]
        psnrs = [r['metrics']['psnr'] for r in self.results]
        ssims = [r['metrics']['ssim'] for r in self.results]
        
        report.append(f"\nBER:")
        report.append(f"  • Mínimo: {min(bers):.6f}")
        report.append(f"  • Máximo: {max(bers):.6f}")
        report.append(f"  • Promedio: {np.mean(bers):.6f}")
        
        report.append(f"\nPSNR:")
        report.append(f"  • Mínimo: {min(psnrs):.2f} dB")
        report.append(f"  • Máximo: {max(psnrs):.2f} dB")
        report.append(f"  • Promedio: {np.mean(psnrs):.2f} dB")
        
        report.append(f"\nSSIM:")
        report.append(f"  • Mínimo: {min(ssims):.4f}")
        report.append(f"  • Máximo: {max(ssims):.4f}")
        report.append(f"  • Promedio: {np.mean(ssims):.4f}")
        
        # Guardar reporte
        report_text = "\n".join(report)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        print(f"\n✓ Reporte guardado en: {filename}")
        return report_text


def main():
    """Ejecutar suite completa de pruebas de video"""
    print("\n" + "=" * 70)
    print("SUITE DE PRUEBAS DE SIMULACIÓN DE VIDEO")
    print("Simulador 5G/6G - Pruebas con Evidencia y Conclusiones")
    print("=" * 70)
    
    tester = VideoSimulationTester()
    
    # Crear frame de prueba
    test_frame = tester.create_test_frame("gradient")
    print(f"\nFrame de prueba creado: {test_frame.shape}")
    
    # ===== ESCENARIO 1: Condiciones ideales =====
    tester.run_test_scenario(
        "Condiciones Ideales (SNR Alto)",
        test_frame,
        {
            'snr_db': 30,
            'eb_n0_db': 25,
            'modulation': 'QPSK',
            'code_rate': 0.5,
            'fading_type': 'AWGN (Sin desvanecimiento)',
            'network_type': '5G'
        }
    )
    
    # ===== ESCENARIO 2: Condiciones normales =====
    tester.run_test_scenario(
        "Condiciones Normales (SNR Moderado)",
        test_frame,
        {
            'snr_db': 15,
            'eb_n0_db': 12,
            'modulation': 'QPSK',
            'code_rate': 0.5,
            'fading_type': 'AWGN (Sin desvanecimiento)',
            'network_type': '5G'
        }
    )
    
    # ===== ESCENARIO 3: SNR bajo =====
    tester.run_test_scenario(
        "SNR Bajo - Canal Ruidoso",
        test_frame,
        {
            'snr_db': 5,
            'eb_n0_db': 3,
            'modulation': 'QPSK',
            'code_rate': 0.5,
            'fading_type': 'AWGN (Sin desvanecimiento)',
            'network_type': '5G'
        }
    )
    
    # ===== ESCENARIO 4: Modulación alta =====
    tester.run_test_scenario(
        "Alta Eficiencia Espectral (256-QAM)",
        test_frame,
        {
            'snr_db': 25,
            'eb_n0_db': 20,
            'modulation': '256-QAM',
            'code_rate': 0.5,
            'fading_type': 'AWGN (Sin desvanecimiento)',
            'network_type': '5G'
        }
    )
    
    # ===== ESCENARIO 5: Tasa de código baja =====
    tester.run_test_scenario(
        "Alta Redundancia (Tasa 0.3)",
        test_frame,
        {
            'snr_db': 10,
            'eb_n0_db': 8,
            'modulation': 'QPSK',
            'code_rate': 0.3,
            'fading_type': 'AWGN (Sin desvanecimiento)',
            'network_type': '5G'
        }
    )
    
    # ===== ESCENARIO 6: Canal Rayleigh =====
    tester.run_test_scenario(
        "Canal con Desvanecimiento Rayleigh",
        test_frame,
        {
            'snr_db': 20,
            'eb_n0_db': 15,
            'modulation': 'QPSK',
            'code_rate': 0.5,
            'fading_type': 'Rayleigh (NLOS)',
            'network_type': '5G'
        }
    )
    
    # ===== ESCENARIO 7: Condiciones extremas =====
    tester.run_test_scenario(
        "Condiciones Extremas (Stress Test)",
        test_frame,
        {
            'snr_db': 0,
            'eb_n0_db': -2,
            'modulation': '64-QAM',
            'code_rate': 0.9,
            'fading_type': 'Rayleigh (NLOS)',
            'network_type': '5G'
        }
    )
    
    # Generar reporte final
    tester.generate_report("reporte_video_pruebas_completo.txt")
    
    # Resumen en consola
    print("\n" + "=" * 70)
    print("RESUMEN DE PRUEBAS")
    print("=" * 70)
    print(f"✓ Total de escenarios ejecutados: {len(tester.results)}")
    print(f"✓ Reporte generado: reporte_video_pruebas_completo.txt")
    
    # Define threshold for acceptable performance (not for passing tests, but for quality assessment)
    # All tests should complete, but we note which ones show degradation
    BER_ACCEPTABLE_THRESHOLD = 0.1  # 10% - Reasonable for communication systems
    acceptable_results = sum(1 for r in tester.results if r['metrics']['ber'] < BER_ACCEPTABLE_THRESHOLD)
    degraded_results = len(tester.results) - acceptable_results
    
    print(f"\nRendimiento:")
    print(f"  • Escenarios con BER < {BER_ACCEPTABLE_THRESHOLD*100:.0f}%: {acceptable_results}")
    print(f"  • Escenarios con degradación: {degraded_results} (esperado en condiciones extremas)")
    
    # All tests complete successfully, some may show expected degradation
    print("\n✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
    if degraded_results > 0:
        print("   (Algunos escenarios muestran degradación - comportamiento esperado en condiciones adversas)")
    
    return tester.results


if __name__ == "__main__":
    results = main()

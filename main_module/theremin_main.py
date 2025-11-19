#!/usr/bin/env python3
"""
Theremín Virtual con Video y Audio
Programa principal que integra el tracking de manos con síntesis de audio
"""

import cv2
import numpy as np
import time
import mediapipe as mp
import sys
import os
import argparse  
import tkinter as tk

# Agregar paths para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'video_module'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'audio_module'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from handPositionCalculator import HandPositionCalculator
from theremin_synthesizer import ThereminSynthesizer
from audio_video_integration import integrate_audio_with_tracking, draw_audio_info, draw_theremin_guide
from video_processor import VideoProcessor

from opencv_draw import cv_draw
from opencv_dynamic import AdvancedVisualizer

#Funcion para obtener resolucion de pantalla, usamos 1440x810 si falla
def get_screen_resolution():
    try:
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.destroy()
        return (width, height)
    except Exception as e:
        print(f"Advertencia: No se pudo obtener resolución de pantalla ({e})")
        print("Usando resolución por defecto: 1440x810")
        return (1440, 810)

# Funcion principal del theremin.
def theremin_virtual(source=0, size=get_screen_resolution(), wave_type='sine'):
    
    # Inicializar sintetizador de audio
    synthesizer = ThereminSynthesizer(
        sample_rate=44100,     #Frecuencia de muestreo, determina el numero de muestras de audio que se realizan por segundo
        min_frequency=200.0,   
        max_frequency=2000.0,  
        wave_type=wave_type,
        buffer_size=1024
    )
    
    # Iniciar audio
    if(synthesizer.start()):
        print("Synthesizer iniciado")
    wave_types = ['sine', 'square', 'saw', 'triangle']
    current_wave_idx = wave_types.index(wave_type)
    
    try:
        # Inicializar el procesador de video
        video_processor = VideoProcessor(source=source, size=size, save_video=False)
        if video_processor.is_opened():
            print("Procesador de video iniciado")
        
        # Inicializar visualizador avanzado
        advanced_viz = AdvancedVisualizer(frame_width=size[0], frame_height=size[1])
        print("Visualizador avanzado iniciado")

        last_pinch_state = False  # Estado anterior del pinch para detectar transiciones
        while video_processor.is_opened():
            frame, position_calculator, process_time = video_processor.process_frame()
            
            if frame is None:
                break
            
            # Integrar audio con video
            integrate_audio_with_tracking(position_calculator, synthesizer)
            
            # Obtener posiciones
            right_y = position_calculator.get_right_hand_y()
            left_x = position_calculator.get_left_hand_x()
            
            # Detectar gesto OK en mano izquierda para cambiar onda
            # El gesto OK se detecta en VideoProcessor, necesitamos acceder a los landmarks
            pinch_triggered = False
            if hasattr(video_processor, 'last_results') and video_processor.last_results.multi_hand_landmarks:
                for hand_idx, hand_landmarks in enumerate(video_processor.last_results.multi_hand_landmarks):
                    hand_label = video_processor.last_results.multi_handedness[hand_idx].classification[0].label
                    if hand_label == 'Left':
                        pinch_triggered = position_calculator.detect_ok_gesture(hand_landmarks, hand_label)
                        break
            
            # Cambiar tipo de onda si se detecta pinch
            if pinch_triggered and last_pinch_state == False:
                current_wave_idx = (current_wave_idx + 1) % len(wave_types)
                synthesizer.wave_type = wave_types[current_wave_idx]
                last_pinch_state = True
            elif not pinch_triggered:
                last_pinch_state = False

            
            # Calcular FPS para mostrarlos por pantalla
            fps_avg = video_processor.get_average_fps(process_time)
            
            #Bloque de dibujo en pantalla con open-cv -------------------------------------------------------------------------------
            # Dibujar guía del theremín
            draw_theremin_guide(frame)
            
            # ===== VISUALIZACIONES AVANZADAS =====
            info = synthesizer.get_info()
            current_frequency = info['frequency']
            current_volume = info['volume'] / 100.0  # Convertir a 0.0-1.0
            
            
            # Rastro de manos
            advanced_viz.draw_hand_trails(frame, left_hand_x=left_x, right_hand_y=right_y)
            
            # Colores dinámicos basados en frecuencia y volumen
            advanced_viz.draw_dynamic_colors(frame, current_frequency, current_volume, left_x, right_y)
            
            # ===== FIN VISUALIZACIONES AVANZADAS =====
            
            # Dibujar información de video
            cv_draw.draw_fps_info(frame, fps_avg, process_time, position=(50, 60))
            
            # Mostrar posiciones de las manos
            cv_draw.draw_hand_position(frame, right_y, left_x, position=(50, 200))
            
            # Dibujar información de audio
            draw_audio_info(frame, synthesizer, position=(50, 370))
            
            # Mostrar tipo de onda
            cv_draw.draw_wave_type(frame, synthesizer.wave_type, position=(50, 580))
            
            # Mostrar indicador de gesto
            cv_draw.draw_gesture_indicator(frame, gesture_active=pinch_triggered, position=(50, 650))
            #----------------------------------------------------------------------------------------------------------------------
            
            # Mostrar frame
            cv2.imshow('Theremin Virtual', frame)
            
            # Definimos controles de teclado, q=quit, s=switch wave
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                current_wave_idx = (current_wave_idx + 1) % len(wave_types)
                synthesizer.wave_type = wave_types[current_wave_idx]
                print(f"Tipo de onda cambiado a: {synthesizer.wave_type.upper()}")
        
        video_processor.cleanup()
    
    except KeyboardInterrupt:
        print("\n\nInterrupcion detectada...")
    
    finally:
        # Limpieza
        print("\nLimpiando recursos...")
        synthesizer.cleanup()
        cv2.destroyAllWindows()
        print("Programa terminado correctamente")
        print("="*60)


if __name__ == "__main__":
    
    theremin_virtual(0)

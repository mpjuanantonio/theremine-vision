

import cv2
import sys
import os

# Agregar paths para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'video_module'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'audio_module'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from theremin_synthesizer import ThereminSynthesizer
from opencv_draw import cv_draw


def integrate_audio_with_tracking(position_calculator, synthesizer):
    
    right_y = position_calculator.get_right_hand_y()
    left_x = position_calculator.get_left_hand_x()
    left_y = position_calculator.get_left_hand_y()
    
    # Obtener distancias de pinch para control de efectos
    right_pinch = position_calculator.get_right_hand_pinch()
    
    # Mapear pinch derecho a profundidad de vibrato
    # Rango pinch: ~0.0 (cerrado) a ~0.2 (abierto) -> Vibrato: 0.01 (min) a 0.1 (max)
    vibrato_depth = None
    if right_pinch is not None:
        # Normalizar pinch (asumiendo rango útil 0.02 - 0.15)
        norm_pinch = max(0.0, min(1.0, (right_pinch - 0.02) / (0.15 - 0.02)))
        # Invertir: más cerrado = más vibrato? O más abierto = más vibrato?
        # Usuario pidió: "normalizando la distancia... siendo 0.1 el vibrato maximo y 0.01 el minimo"
        # Asumiremos: Mayor distancia = Mayor vibrato (o al revés, ajustaremos según preferencia)
        # Vamos a hacer: Mayor distancia = Mayor vibrato (más expresivo al abrir la mano)
        vibrato_depth = 0.001 + (norm_pinch * 0.01) # Rango 0.001 a 0.011 (ajustado para sutileza)
        # Si el usuario quiere 0.01 a 0.1 es muy fuerte, probemos algo intermedio
        vibrato_depth = 0.001 + (norm_pinch * 0.02) 

    # Mapear altura mano izquierda (Eje Y) a tiempo de delay (Reverb)
    # Rango Y: 0.0 (arriba) a 1.0 (abajo) -> Delay: 0.1s a 0.8s
    delay_seconds = None
    if left_y is not None:
        # Invertimos: Arriba (0.0) = Más eco (0.8s), Abajo (1.0) = Menos eco (0.1s)
        # O al revés? Normalmente subir la mano = aumentar efecto
        # Vamos a hacer: Arriba (0.0) = 0.8s, Abajo (1.0) = 0.1s
        delay_seconds = 0.8 - (left_y * 0.7) # 0.8s a 0.1s

    # Actualizar sintetizador
    synthesizer.update_position(right_y, left_x)
    synthesizer.update_parameters(vibrato_depth=vibrato_depth, delay_seconds=delay_seconds)


def draw_audio_info(frame, synthesizer, position=(50, 370)):
    
    cv_draw.draw_audio_info(frame, synthesizer, position=position)


def draw_theremin_guide(frame):
    
    cv_draw.draw_theremin_guide(frame)




import cv2
import sys
import os

# Agregar paths para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'video_module'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'audio_module'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from theremin_synthesizer import ThereminSynthesizer
from opencv_draw import cv_draw

# ---------------CONSTANTES DE CONFIGURACIÓN ----------------------

# Volumen - Zona de control mano izquierda (eje X)
LEFT_ZONE_LIMIT = 0.5   #Restricción para que no se cruce la zona con la otra mano

# Vibrato
PINCH_MIN = 0.02        # Distancia minima para minimo vibrato
PINCH_MAX = 0.15        # Distancia maxima para maximo vibrato
VIBRATO_MIN = 0.001     # Profundidad minima de vibrato
VIBRATO_MAX = 0.02      # Profundidad maxima de vibrato

# Reverb 
REVERB_TOP = 0.30      # Posición Y para reverb máximo
REVERB_BOTTOM = 0.85   # Posición Y para reverb mínimo
DELAY_MAX = 0.8        # Segundos máx de reverb
DELAY_MIN = 0.1        # Segundos mín de reverb

#------------------------------- ----------------------


def integrate_audio_with_tracking(position_calculator, synthesizer):
    
    right_y = position_calculator.get_right_hand_y()
    left_x = position_calculator.get_left_hand_x()
    left_y = position_calculator.get_left_hand_y()
    
    # Mapear posición X mano izquierda a volumen
    mapped_left_x = None
    if left_x is not None:
        if left_x <= LEFT_ZONE_LIMIT:
            mapped_left_x = left_x / LEFT_ZONE_LIMIT
        else:
            mapped_left_x = 1.0
            
    
    right_pinch = position_calculator.get_right_hand_pinch()

    # CALCULO DEL VIBRATO
    vibrato_depth = None
    if right_pinch is not None:
        # Normalizar pinch y calculamos la profundidad del vibrato
        norm_pinch = max(0.0, min(1.0, (right_pinch - PINCH_MIN) / (PINCH_MAX - PINCH_MIN)))
        vibrato_depth = VIBRATO_MIN + (norm_pinch * VIBRATO_MAX) 

    # CALCULO DE LA REVERB
    delay_seconds = None
    if left_y is not None:
        # Normalizar al rango útil
        normalized_y = (left_y - REVERB_TOP) / (REVERB_BOTTOM - REVERB_TOP)
        normalized_y = max(0.0, min(1.0, normalized_y))  # Clamp entre 0 y 1
        
        # Invertimos: Arriba = Más rev, Abajo = Menos rev
        delay_seconds = DELAY_MAX - (normalized_y * (DELAY_MAX - DELAY_MIN))

    synthesizer.update_position(right_y, mapped_left_x)
    synthesizer.update_parameters(vibrato_depth=vibrato_depth, delay_seconds=delay_seconds)


def draw_audio_info(frame, synthesizer, position=(50, 370)):
    
    cv_draw.draw_audio_info(frame, synthesizer, position=position)


def draw_theremin_guide(frame):
    
    cv_draw.draw_theremin_guide(frame)


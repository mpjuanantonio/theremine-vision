"""
Integrador de Video y Audio para Theremín Virtual
Conecta el tracking de manos con el sintetizador de audio
"""

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
    """
    Función auxiliar que actualiza el sintetizador con las posiciones actuales.
    
    Args:
        position_calculator: Instancia de HandPositionCalculator
        synthesizer: Instancia de ThereminSynthesizer
    """
    right_y = position_calculator.get_right_hand_y()
    left_x = position_calculator.get_left_hand_x()
    
    # Actualizar sintetizador
    synthesizer.update_position(right_y, left_x)


def draw_audio_info(frame, synthesizer, position=(50, 370)):
    """
    Dibuja información del audio en el frame usando cv_draw.
    
    Args:
        frame: Frame de video
        synthesizer: Instancia de ThereminSynthesizer
        position: Posición (x, y) donde comenzar a dibujar
    """
    cv_draw.draw_audio_info(frame, synthesizer, position=position)


def draw_theremin_guide(frame):
    """
    Dibuja una guía visual del theremín en el frame usando cv_draw.
    
    Args:
        frame: Frame de video
    """
    cv_draw.draw_theremin_guide(frame)


"""
Módulo de visualización avanzada para el Theremín Virtual
Proporciona efectos visuales reactivos, espectrograma y rastro de mano
"""

import cv2
import numpy as np
from collections import deque

#Clase en la que se implementan las visualizaciones dinamicas 
class AdvancedVisualizer:
    
    # Constantes de colores (BGR)
    COLOR_BLACK = (0, 0, 0)
    COLOR_WHITE = (255, 255, 255)
    COLOR_RED = (0, 0, 255)
    COLOR_GREEN = (0, 255, 0)
    COLOR_BLUE = (255, 0, 0)
    COLOR_CYAN = (255, 255, 0)
    COLOR_MAGENTA = (255, 0, 255)
    COLOR_YELLOW = (0, 255, 255)
    COLOR_GRAY = (100, 100, 100)
    
    def __init__(self, frame_width=1440, frame_height=810):
        self.frame_width = frame_width
        self.frame_height = frame_height
        
        # Rastro de mano izquierda (para volumen)
        self.left_hand_trail = deque(maxlen=30)  # Últimas 30 posiciones
        
        # Rastro de mano derecha (para pitch)
        self.right_hand_trail = deque(maxlen=30)
        
        # Partículas reactivas
        self.particles = []
        self.max_particles = 50
        
        # Historial de frecuencias para efecto visual
        self.frequency_history = deque(maxlen=100)

    
    def draw_hand_trails(self, frame, left_hand_x=None, right_hand_y=None):
        # Rastro de mano izquierda (volumen, eje X inferior)
        if left_hand_x is not None:
            # Convertir a píxeles
            pixel_x = int(left_hand_x * self.frame_width)
            pixel_y = self.frame_height - 100  # Cerca del fondo
            
            self.left_hand_trail.append((pixel_x, pixel_y))
            
            # Dibujar línea del rastro
            if len(self.left_hand_trail) > 1:
                points = np.array(list(self.left_hand_trail), dtype=np.int32)
                # Dibujar con degradado de opacidad
                for i in range(len(points) - 1):
                    alpha = i / len(points)
                    color = (int(255 * alpha), int(255 * (1 - alpha)), 100)
                    cv2.line(frame, tuple(points[i]), tuple(points[i + 1]), color, 2)
            
            # Círculo en posición actual
            cv2.circle(frame, (pixel_x, pixel_y), 8, self.COLOR_CYAN, -1)
        
        # Rastro de mano derecha (pitch, eje Y derecho)
        if right_hand_y is not None:
            # Convertir a píxeles
            pixel_x = self.frame_width - 100  # Cerca de la derecha
            pixel_y = int(right_hand_y * self.frame_height)
            
            self.right_hand_trail.append((pixel_x, pixel_y))
            
            # Dibujar línea del rastro
            if len(self.right_hand_trail) > 1:
                points = np.array(list(self.right_hand_trail), dtype=np.int32)
                # Dibujar con degradado de opacidad
                for i in range(len(points) - 1):
                    alpha = i / len(points)
                    color = (100, int(255 * alpha), int(255 * (1 - alpha)))
                    cv2.line(frame, tuple(points[i]), tuple(points[i + 1]), color, 2)
            
            # Círculo en posición actual
            cv2.circle(frame, (pixel_x, pixel_y), 8, self.COLOR_MAGENTA, -1)
    
    def draw_dynamic_colors(self, frame, frequency, volume, left_hand_x=None, right_hand_y=None):
        # Color basado en frecuencia
        color = self._get_color_from_frequency(frequency)
        
        # Grosor basado en volumen
        thickness = max(2, int(volume * 10))
        
        # Borde animado en los costados
        if right_hand_y is not None:
            # Línea vertical derecha
            start_y = int(right_hand_y * self.frame_height)
            cv2.line(frame, (self.frame_width - 10, start_y - 50),
                    (self.frame_width - 10, start_y + 50), color, thickness)
        
        if left_hand_x is not None:
            # Línea vertical izquierda
            start_x = int(left_hand_x * self.frame_width)
            cv2.line(frame, (start_x - 30, self.frame_height - 10),
                    (start_x + 30, self.frame_height - 10), color, thickness)
   
    
    def _get_color_from_frequency(self, frequency, min_freq=200, max_freq=2000, alpha=1.0):
        # Normalizar frecuencia
        normalized = (frequency - min_freq) / (max_freq - min_freq)
        normalized = np.clip(normalized, 0, 1)
        
        # Mapear a color: Rojo -> Amarillo -> Verde -> Cyan -> Azul
        if normalized < 0.25:
            # Rojo a Amarillo
            r = 255
            g = int(255 * (normalized / 0.25))
            b = 0
        elif normalized < 0.5:
            # Amarillo a Verde
            r = int(255 * (1 - (normalized - 0.25) / 0.25))
            g = 255
            b = 0
        elif normalized < 0.75:
            # Verde a Cyan
            r = 0
            g = 255
            b = int(255 * ((normalized - 0.5) / 0.25))
        else:
            # Cyan a Azul
            r = 0
            g = int(255 * (1 - (normalized - 0.75) / 0.25))
            b = 255
        
        return (int(b * alpha), int(g * alpha), int(r * alpha))
    


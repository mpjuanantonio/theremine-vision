"""
Módulo de utilidades para dibujo con OpenCV
Centraliza todas las funciones de dibujo para el Theremín Virtual
"""

import cv2
import numpy as np


class cv_draw:
    """Clase que contiene todas las funciones de dibujo con OpenCV para el Theremín Virtual."""
    
    # Fuente del texto
    FONT = cv2.FONT_HERSHEY_DUPLEX
    FONT_THICKNESS = 2
    TEXT_PADDING = 20
    
    # Constantes de colores (BGR)
    COLOR_WHITE = (255, 255, 255)
    COLOR_BLACK = (0, 0, 0)
    COLOR_GREEN = (0, 255, 0)
    COLOR_GRAY = (100, 100, 100)
    COLOR_CYAN = (255, 255, 0)
    COLOR_MAGENTA = (255, 0, 255)
    COLOR_RED = (0, 0, 255)
    COLOR_BLUE = (255, 0, 0)
    COLOR_YELLOW = (0, 255, 255)
    COLOR_PINK = (230, 66, 245)
    COLOR_LIGHT_CYAN = (66, 245, 230)
    COLOR_LIGHT_ORANGE = (250, 150, 50)
    COLOR_LIGHT_PURPLE = (150, 50, 250)
    COLOR_LIGHT_BLUE = (50, 150, 250)
    
    @staticmethod
    # Dibuja un cuadro de texto rectangular en pantalla
    def draw_text_with_bg(frame, text, pos, font_scale=0.6, text_color=COLOR_WHITE, bg_color=COLOR_BLACK):
    
        thickness = cv_draw.FONT_THICKNESS
        padding = cv_draw.TEXT_PADDING
        
        # Calculamos el tamaño que ocupará el texto dado el font_scale y grosor
        (text_width, text_height), baseline = cv2.getTextSize(text, cv_draw.FONT, font_scale, thickness)

        # Calculamos las dimensiones del rectángulo de fondo para que cubra todo el texto 
        rect_width = text_width + 2 * padding
        rect_height = text_height + baseline + 2 * padding
        
        x, y = pos
        rect_x1 = x
        rect_y1 = y - text_height
        rect_x2 = rect_x1 + rect_width
        rect_y2 = rect_y1 + rect_height
        
        # Dibujar rectángulo de fondo
        cv2.rectangle(frame, (rect_x1, rect_y1), (rect_x2, rect_y2), bg_color, -1)
        
        # Dibujar texto, en este orden para que quede encima del rectángulo
        text_x = rect_x1 + padding
        text_y = rect_y1 + padding + text_height
        cv2.putText(frame, text, (text_x, text_y), cv_draw.FONT, font_scale, text_color, thickness)
    
    @staticmethod
    # Dibuja la etiqueta de la mano en el frame, izq o der junto a la mano
    def draw_hand_label(frame, hand_landmarks, hand_label):
        altura, ancho, _ = frame.shape
        wrist = hand_landmarks.landmark[0]
        #Obtenemos las posiciones de la muñeca para usarla como posicion de la etiqueta
        wrist_x, wrist_y = int(wrist.x * ancho), int(wrist.y * altura)
        posicion=(wrist_x - 30, wrist_y - 20)
        cv2.putText(frame, hand_label, posicion, cv_draw.FONT, 0.7, cv_draw.COLOR_GREEN, 2)

    @staticmethod
    #Dibuja información del audio (frecuencia, nota, volumen)
    def draw_audio_info(frame, synthesizer, position=(50, 370)):
        #posición (x, y) donde comenzar a dibujar
        info = synthesizer.get_info()
        x, y = position
        
        # Dibujar información de frecuencia
        cv_draw.draw_text_with_bg(frame,f'Frequency: {info["frequency"]:.2f} Hz',(x, y), bg_color=cv_draw.COLOR_LIGHT_BLUE,font_scale=1.0       )
        
        # Dibujar información de nota
        cv_draw.draw_text_with_bg(frame, f'Note: {info["note"]}', (x, y + 70), bg_color=cv_draw.COLOR_LIGHT_PURPLE, font_scale=1.0)
        
        # Dibujar información de volumen
        cv_draw.draw_text_with_bg(frame, f'Volume: {info["volume"]:.1f}%', (x, y + 140), bg_color=cv_draw.COLOR_LIGHT_ORANGE,font_scale=1.0)
        
        # Indicador visual de si está sonando
        if info['volume'] > 0:
            cv2.circle(frame, (x + 400, y + 50), 15, cv_draw.COLOR_GREEN, -1)
            cv2.putText(frame, 'PLAYING', (x + 420, y + 60), cv_draw.FONT, 0.7, cv_draw.COLOR_GREEN, 2)
        else:
            cv2.circle(frame, (x + 400, y + 50), 15, cv_draw.COLOR_GRAY, -1)
            cv2.putText(frame, 'SILENT', (x + 420, y + 60), cv_draw.FONT, 0.7, cv_draw.COLOR_GRAY, 2)
    
    @staticmethod
    # Dubuja una guía visual del theremín en el frame para que sea mas intuitivo para el usuario
    def draw_theremin_guide(frame):
    
        altura, ancho, _ = frame.shape
        
        # Línea vertical para el tono (derecha) - mano derecha
        cv2.line(frame, (ancho- 100, 100), (ancho- 100, altura- 100), cv_draw.COLOR_PINK, 3)
        cv2.putText(frame, 'PITCH', (ancho- 150, 80), cv_draw.FONT, 0.6, cv_draw.COLOR_PINK, 2)
        cv2.putText(frame, 'HIGH', (ancho- 150, 120), cv_draw.FONT, 0.5, cv_draw.COLOR_PINK, 1)
        cv2.putText(frame, 'LOW', (ancho- 150, altura- 110), cv_draw.FONT, 0.5, cv_draw.COLOR_PINK, 1)
        
        # Línea horizontal para el volumen (izquierda) - mano izquierda
        cv2.line(frame, (100, altura- 100), (400, altura- 100), cv_draw.COLOR_LIGHT_CYAN, 3)
        cv2.putText(frame, 'VOLUME', (100, altura- 110), cv_draw.FONT, 0.6, cv_draw.COLOR_LIGHT_CYAN, 2)
        cv2.putText(frame, 'OFF', (80, altura- 70), cv_draw.FONT, 0.5, cv_draw.COLOR_LIGHT_CYAN, 1)
        cv2.putText(frame, 'MAX', (380, altura- 70), cv_draw.FONT, 0.5, cv_draw.COLOR_LIGHT_CYAN, 1)
    
    @staticmethod
    # Dibuja los fps y tiempo de procesamiento en el frame
    def draw_fps_info(frame, fps, process_time, position=(50, 60)):
        x, y = position
        cv_draw.draw_text_with_bg(frame, f'FPS: {int(fps)}', (x, y), bg_color=(0, 200, 100), font_scale=1.0)
        cv_draw.draw_text_with_bg(frame, f'Time: {process_time * 1000:.1f}ms', (x, y + 70), bg_color=(0, 200, 100), font_scale=1.0)
    
    @staticmethod
    # Dibuja las posiciones de las manos
    def draw_hand_position(frame, right_y, left_x, position=(50, 200)):
        x, y = position
        
        # Posición mano derecha (Y)
        if right_y is not None:
            cv_draw.draw_text_with_bg(
                frame,
                f'Right Hand Y: {right_y:.4f}',
                (x, y),
                bg_color=cv_draw.COLOR_PINK,
                font_scale=0.9
            )
        else:
            cv_draw.draw_text_with_bg(frame,f'Right Hand Y: N/A',(x, y), bg_color=cv_draw.COLOR_GRAY,font_scale=0.9)
        
        # Posición mano izquierda (X)
        if left_x is not None:
            cv_draw.draw_text_with_bg(
                frame,
                f'Left Hand X: {left_x:.4f}',
                (x, y + 70),
                bg_color=cv_draw.COLOR_LIGHT_CYAN,
                font_scale=0.9
            )
        else:
            cv_draw.draw_text_with_bg(frame, f'Left Hand X: N/A', (x, y + 70), bg_color=cv_draw.COLOR_GRAY, font_scale=0.9)
    
    @staticmethod
    #Dibuja el tipo de onda que esta sonando
    def draw_wave_type(frame, wave_type, position=(50, 580)):
        cv_draw.draw_text_with_bg(frame, f'Wave: {wave_type.upper()}',position, bg_color=(200, 100, 200), font_scale=0.9)

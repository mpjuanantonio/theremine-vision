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
    
        thickness = 1 # Reducido para un look más limpio
        padding = 8   # Reducido padding
        
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
        
        # Dibujar rectángulo de fondo con transparencia (simulada)
        overlay = frame.copy()
        cv2.rectangle(overlay, (rect_x1, rect_y1), (rect_x2, rect_y2), bg_color, -1)
        alpha = 0.7  # Transparencia
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        
        # Dibujar texto, en este orden para que quede encima del rectángulo
        text_x = rect_x1 + padding
        text_y = rect_y1 + padding + text_height
        cv2.putText(frame, text, (text_x, text_y), cv_draw.FONT, font_scale, text_color, thickness, cv2.LINE_AA)
    
    @staticmethod
    # Dibuja una barra de progreso simple
    def draw_progress_bar(frame, value, max_value, pos, width=150, height=10, color=COLOR_GREEN, label=None):
        x, y = pos
        
        # Fondo de la barra
        cv2.rectangle(frame, (x, y), (x + width, y + height), (50, 50, 50), -1)
        
        # Barra de progreso
        progress_width = int((value / max_value) * width)
        progress_width = max(0, min(width, progress_width))
        cv2.rectangle(frame, (x, y), (x + progress_width, y + height), color, -1)
        
        # Borde
        cv2.rectangle(frame, (x, y), (x + width, y + height), (200, 200, 200), 1)
        
        if label:
            cv2.putText(frame, label, (x, y - 5), cv_draw.FONT, 0.4, (200, 200, 200), 1, cv2.LINE_AA)

    @staticmethod
    # Dibuja la etiqueta de la mano en el frame, izq o der junto a la mano
    def draw_hand_label(frame, hand_landmarks, hand_label):
        altura, ancho, _ = frame.shape
        wrist = hand_landmarks.landmark[0]
        #Obtenemos las posiciones de la muñeca para usarla como posicion de la etiqueta
        wrist_x, wrist_y = int(wrist.x * ancho), int(wrist.y * altura)
        posicion=(wrist_x - 30, wrist_y - 20)
        cv2.putText(frame, hand_label, posicion, cv_draw.FONT, 0.5, cv_draw.COLOR_GREEN, 1, cv2.LINE_AA)

    @staticmethod
    #Dibuja información del audio (frecuencia, nota, volumen)
    def draw_audio_info(frame, synthesizer, position=(20, 20)):
        #posición (x, y) donde comenzar a dibujar
        info = synthesizer.get_info()
        x, y = position
        
        # Panel de fondo semitransparente para toda la info
        panel_width = 220
        panel_height = 230
        overlay = frame.copy()
        cv2.rectangle(overlay, (x-10, y-10), (x + panel_width, y + panel_height), (30, 30, 30), -1)
        cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
        
        # Título
        cv2.putText(frame, "THEREMIN STATUS", (x, y + 15), cv_draw.FONT, 0.5, cv_draw.COLOR_WHITE, 1, cv2.LINE_AA)
        
        current_y = y + 45
        spacing = 40
        
        # 1. Nota y Frecuencia
        note_text = f"{info['note']}"
        freq_text = f"{info['frequency']:.1f} Hz"
        cv2.putText(frame, "NOTE / FREQ", (x, current_y - 5), cv_draw.FONT, 0.4, cv_draw.COLOR_GRAY, 1, cv2.LINE_AA)
        cv2.putText(frame, f"{note_text}  |  {freq_text}", (x, current_y + 15), cv_draw.FONT, 0.6, cv_draw.COLOR_CYAN, 1, cv2.LINE_AA)
        
        current_y += spacing + 10
        
        # 2. Volumen
        cv_draw.draw_progress_bar(frame, info['volume'], 100, (x, current_y), width=180, color=cv_draw.COLOR_LIGHT_ORANGE, label="VOLUME")
        
        current_y += spacing
        
        # 3. Vibrato (Mapeado 0.0 - 0.1 aprox a 0-100 visual)
        vibrato_pct = (info['vibrato_depth'] / 0.02) * 100 # Escala aproximada para visualización
        cv_draw.draw_progress_bar(frame, vibrato_pct, 100, (x, current_y), width=180, color=cv_draw.COLOR_LIGHT_PURPLE, label="VIBRATO DEPTH")
        
        current_y += spacing
        
        # 4. Reverb (Delay) (Mapeado 0.1s - 0.8s a 0-100 visual)
        # El delay va de 0.1s (mínimo) a 0.8s (máximo), normalizamos a ese rango
        delay_min = 0.1
        delay_max = 0.8
        reverb_pct = ((info['delay_seconds'] - delay_min) / (delay_max - delay_min)) * 100
        reverb_pct = max(0, min(100, reverb_pct))  # Clamp entre 0 y 100
        cv_draw.draw_progress_bar(frame, reverb_pct, 100, (x, current_y), width=180, color=cv_draw.COLOR_LIGHT_BLUE, label="REVERB (DELAY)")
        
        # Indicador de estado (Play/Pause) pequeño en la esquina del panel
        status_color = cv_draw.COLOR_GREEN if info['volume'] > 0 else cv_draw.COLOR_RED
        cv2.circle(frame, (x + panel_width - 20, y + 10), 6, status_color, -1)
    
    @staticmethod
    # Dubuja una guía visual del theremín en el frame para que sea mas intuitivo para el usuario
    def draw_theremin_guide(frame):
    
        altura, ancho, _ = frame.shape
        
        # Definir límites de zonas
        left_zone_limit = int(ancho * 0.5)   # Zona izquierda ampliada al 50%
        right_zone_start = int(ancho * 0.75) # Zona derecha reducida (empieza al 75%)
        
        # --- ZONA DERECHA (PITCH) ---
        # Dibujar área semitransparente para la zona derecha
        overlay = frame.copy()
        cv2.rectangle(overlay, (right_zone_start, 0), (ancho, altura), (50, 0, 50), -1)
        cv2.addWeighted(overlay, 0.1, frame, 0.9, 0, frame)
        
        # Línea vertical guía (centrada en la zona derecha)
        pitch_guide_x = right_zone_start + (ancho - right_zone_start) // 2
        cv2.line(frame, (pitch_guide_x, 50), (pitch_guide_x, altura - 50), cv_draw.COLOR_PINK, 2)
        
        # Etiquetas
        cv2.putText(frame, 'PITCH ZONE', (right_zone_start + 20, 40), cv_draw.FONT, 0.6, cv_draw.COLOR_PINK, 1, cv2.LINE_AA)
        cv2.putText(frame, 'HIGH', (pitch_guide_x + 10, 80), cv_draw.FONT, 0.5, cv_draw.COLOR_PINK, 1, cv2.LINE_AA)
        cv2.putText(frame, 'LOW', (pitch_guide_x + 10, altura - 80), cv_draw.FONT, 0.5, cv_draw.COLOR_PINK, 1, cv2.LINE_AA)
        
        # --- ZONA IZQUIERDA (VOLUMEN / REVERB) ---
        # Dibujar área semitransparente para la zona izquierda
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (left_zone_limit, altura), (50, 50, 0), -1)
        cv2.addWeighted(overlay, 0.1, frame, 0.9, 0, frame)
        
        # Línea límite vertical
        cv2.line(frame, (left_zone_limit, 0), (left_zone_limit, altura), (100, 100, 100), 1, cv2.LINE_AA)
        
        # Guía Volumen (Horizontal)
        cv2.line(frame, (20, altura - 50), (left_zone_limit - 20, altura - 50), cv_draw.COLOR_LIGHT_CYAN, 2)
        cv2.putText(frame, 'VOLUME ZONE', (20, 40), cv_draw.FONT, 0.6, cv_draw.COLOR_LIGHT_CYAN, 1, cv2.LINE_AA)
        cv2.putText(frame, 'MIN', (20, altura - 60), cv_draw.FONT, 0.4, cv_draw.COLOR_LIGHT_CYAN, 1, cv2.LINE_AA)
        cv2.putText(frame, 'MAX', (left_zone_limit - 50, altura - 60), cv_draw.FONT, 0.4, cv_draw.COLOR_LIGHT_CYAN, 1, cv2.LINE_AA)
        
        # Guía Reverb (Vertical en zona izquierda)
        # Ajustado al rango útil: 30% - 85% de la altura
        reverb_top = int(altura * 0.30)      # Donde empieza el máximo reverb
        reverb_bottom = int(altura * 0.85)   # Donde termina el mínimo reverb
        
        cv2.line(frame, (20, reverb_top), (20, reverb_bottom), cv_draw.COLOR_LIGHT_BLUE, 2)
        cv2.putText(frame, '+', (10, reverb_top - 10), cv_draw.FONT, 0.8, cv_draw.COLOR_LIGHT_BLUE, 1, cv2.LINE_AA)
        cv2.putText(frame, '-', (10, reverb_bottom + 20), cv_draw.FONT, 0.8, cv_draw.COLOR_LIGHT_BLUE, 1, cv2.LINE_AA)
    
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
    
    @staticmethod
    # Dibuja indicador de gesto detectado
    def draw_gesture_indicator(frame, gesture_active=False, position=(50, 650)):
        if gesture_active:
            cv_draw.draw_text_with_bg(frame, 'PINCH DETECTED', position, bg_color=(0, 255, 0), font_scale=0.8, text_color=(0, 0, 0))
        else:
            cv_draw.draw_text_with_bg(frame, 'Pinch left hand to change wave', position, bg_color=(100, 100, 100), font_scale=0.6)

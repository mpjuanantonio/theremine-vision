import cv2
import numpy as np
import time
import mediapipe as mp
import sys
import os
import handPositionCalculator

# Agregar path para importar módulos de utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from opencv_draw import cv_draw

# Clase encargada de procesar video y realizar hand tracking
class VideoProcessor:
    
    def __init__(self, source=0, size=(1440, 810), save_video=False):
        self.source = source
        self.size = size
        self.save_video = save_video
        self.avg_fps = []
        self.video_writer = None
        self.last_results = None  # Almacenar resultados de MediaPipe para gestos
        
        # Inicializar MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Inicializar captura de video
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise RuntimeError(f"No se pudo abrir la fuente de video: {source}")
        
        # Obtener parámetros del video
        frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        
        # Inicializar video writer si es necesario
        if self.save_video:
            self.video_writer = cv2.VideoWriter(
                "hand-tracking.avi",
                cv2.VideoWriter_fourcc(*"mp4v"),
                fps if fps > 0 else 30,
                self.size
            )
        
        # Inicializar calculador de posiciones
        self.position_calculator = handPositionCalculator.HandPositionCalculator(
            self.size[0], self.size[1]
        )
    # procesa un frame (instante) del video
    def process_frame(self):
        ret, frame = self.cap.read()
        
        if not ret:
            return None, None, None
        
        frame = cv2.resize(frame, self.size)
        frame = cv2.flip(frame, 1)  # Efecto espejo
        
        start_time = time.time()
        
        # Convertir BGR a RGB para MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Procesar frame con MediaPipe Hands 
        results = self.hands.process(frame_rgb)
        
        # Almacenar resultados para acceso externo (para gestos)
        self.last_results = results

        
        process_time = time.time() - start_time
        
        # Resetear posiciones antes de actualizar
        self.position_calculator.reset()
        
        # Procesar landmarks de las manos
        if results.multi_hand_landmarks:
            for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                hand_label = results.multi_handedness[hand_idx].classification[0].label
                
                # Actualizar posición en el calculador
                self.position_calculator.update_hand_position(hand_landmarks, hand_label)
                
                # Dibujar las conexiones y puntos de la mano
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
                
                # Dibujar línea de vibrato (entre pulgar e índice) solo para mano derecha
                h, w, _ = frame.shape
                if hand_label == 'Right':
                    thumb_tip = hand_landmarks.landmark[4]
                    index_tip = hand_landmarks.landmark[8]
                    
                    thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
                    index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)
                    
                    # Dibujar línea
                    cv2.line(frame, (thumb_x, thumb_y), (index_x, index_y), (255, 0, 255), 2)
                    # Dibujar puntos en los extremos
                    cv2.circle(frame, (thumb_x, thumb_y), 4, (255, 0, 255), -1)
                    cv2.circle(frame, (index_x, index_y), 4, (255, 0, 255), -1)
                
                # Dibujar etiqueta de la mano
                wrist = hand_landmarks.landmark[0]
                wrist_x, wrist_y = int(wrist.x * w), int(wrist.y * h)
                cv2.putText(frame, hand_label, (wrist_x - 30, wrist_y - 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Guardar frame si es necesario
        if self.video_writer:
            self.video_writer.write(frame)

        # Returns:   Tupla (frame_processed, position_calculator, process_time) o (None, None, None) si no hay frame
        return frame, self.position_calculator, process_time
    
    def get_average_fps(self, process_time):
        if process_time > 0:
            fps = 1.0 / process_time
            self.avg_fps.append(fps)
            return sum(self.avg_fps) / len(self.avg_fps)
        return 0
    
    def cleanup(self):
        self.cap.release()
        if self.video_writer:
            self.video_writer.release()
        cv2.destroyAllWindows()
        self.hands.close()
    
    def is_opened(self):
        return self.cap.isOpened()


# Ejemplo de uso de la clase VideoProcessor, no usado para el main
def hand_tracking(source=0, size=(1440, 810)):
    try:
        # Usar la clase VideoProcessor
        video_processor = VideoProcessor(source=source, size=size, save_video=True)
        
        while video_processor.is_opened():
            frame, position_calculator, process_time = video_processor.process_frame()
            
            if frame is None:
                break
            
            # Obtener posiciones de las manos
            right_y = position_calculator.get_right_hand_y()
            left_x = position_calculator.get_left_hand_x()
            
            # Calcular FPS promedio
            fps_avg = video_processor.get_average_fps(process_time)
            
            # Mostrar información en pantalla
            cv_draw.draw_fps_info(frame, fps_avg, process_time, position=(50, 60))
            
            # Mostrar posiciones de las manos
            cv_draw.draw_hand_position(frame, right_y, left_x, position=(50, 200))
            
            cv2.imshow('Hand Tracking', frame)
            
            # Salir con 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        video_processor.cleanup()
        
    except RuntimeError as e:
        print(f"Error: {e}")


if __name__ == "__main__":

    hand_tracking(0)  # Hand tracking con camara default
    #hand_tracking("video.mp4")  # Hand tracking con video de archivo

'''
Puntos de referencia de la mano (21 landmarks por mano):
        0: muñeca
        1: base del pulgar
        2: articulación media del pulgar
        3: punta del pulgar
        4: punta del pulgar
        5: base del índice
        6: articulación media del índice
        7: articulación distal del índice
        8: punta del índice
        9: base del dedo medio
        10: articulación media del dedo medio
        11: articulación distal del dedo medio
        12: punta del dedo medio
        13: base del anular
        14: articulación media del anular
        15: articulación distal del anular
        16: punta del anular
        17: base del meñique
        18: articulación media del meñique
        19: articulación distal del meñique
        20: punta del meñique
'''
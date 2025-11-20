
from kalman_filter import KalmanFilter


class HandPositionCalculator:

    
    def __init__(self, frame_width, frame_height):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.right_hand_y = None  # Posición Y de la mano derecha (0.0 - 1.0)
        self.left_hand_x = None   # Posición X de la mano izquierda (0.0 - 1.0)
        self.left_hand_y = None   # Posición Y de la mano izquierda (0.0 - 1.0)
        
        self.right_hand_pinch = None # Distancia pinch mano derecha
        self.left_hand_pinch = None  # Distancia pinch mano izquierda
        
        # Gesture detection
        # Distancia máxima entre pulgar e índice para detectar pinch
        # Este valor lo podemos variar para ajustar la sensibilidad del gesto, el unico problema es que si estas muy cerca puede haber muchos falsos negativos y si esta alejado falsos positivos
        self.pinch_threshold = 0.03  
        self.pinch_detected = False 
        
        # Filtros de Kalman para suavizado de posiciones
        # process_variance=0.0001: El filtro es bastante restrictivo (suavizado fuerte)
        # measurement_variance=0.001: Confiamos bastante en las mediciones de MediaPipe
        self.kalman_x = KalmanFilter(initial_value=0.5, process_variance=0.0001, measurement_variance=0.001)
        self.kalman_y = KalmanFilter(initial_value=0.5, process_variance=0.0001, measurement_variance=0.001)
        self.kalman_left_y = KalmanFilter(initial_value=0.5, process_variance=0.0001, measurement_variance=0.001)
    
    def update_hand_position(self, hand_landmarks, hand_label):
        
        # Índices de los puntos de referencia clave
        key_points = [
            0,   # muñeca
            4,   # punta del pulgar
            8,   # punta del índice
            12,  # punta del dedo medio
            16,  # punta del anular
            20   # punta del meñique
        ]
        
        # Calcular la posición media de todos los puntos clave, tomamos las puntas de los dedos y la muñeca
        avg_x = sum(hand_landmarks.landmark[i].x for i in key_points) / len(key_points)
        avg_y = sum(hand_landmarks.landmark[i].y for i in key_points) / len(key_points)
        
        # Calcular distancia de pinch (pulgar a índice)
        thumb = hand_landmarks.landmark[4]
        index = hand_landmarks.landmark[8]
        pinch_dist = ((thumb.x - index.x)**2 + (thumb.y - index.y)**2)**0.5
        
        if hand_label == 'Right':
            # Mano derecha controla el eje Y (invertido para que arriba = 0.0, abajo = 1.0)
            # Aplicar Filtro de Kalman para suavizar la posición
            self.right_hand_y = self.kalman_y.filter(float(avg_y))
            self.right_hand_pinch = pinch_dist
        elif hand_label == 'Left':
            # Mano izquierda controla el eje X
            # Aplicar Filtro de Kalman para suavizar la posición
            self.left_hand_x = self.kalman_x.filter(float(avg_x))
            self.left_hand_y = self.kalman_left_y.filter(float(avg_y))
            self.left_hand_pinch = pinch_dist
    
    def get_right_hand_y(self):
        return self.right_hand_y
    
    def get_left_hand_x(self):
        return self.left_hand_x
        
    def get_left_hand_y(self):
        return self.left_hand_y
        
    def get_right_hand_pinch(self):
        return self.right_hand_pinch
        
    def get_left_hand_pinch(self):
        return self.left_hand_pinch
    
    # Detecta un gesto de ok (pulgar e índice juntos mientras otros dedos están extendidos).
    def detect_ok_gesture(self, hand_landmarks, hand_label):
            


        if hand_landmarks is None:
            self.pinch_detected = False
            return False
        
        # Landmarks para cada dedo (punta):
        # 4: Thumb tip, 8: Index tip, 12: Middle tip, 16: Ring tip, 20: Pinky tip
        thumb = hand_landmarks.landmark[4]
        index = hand_landmarks.landmark[8]
        middle = hand_landmarks.landmark[12]
        ring = hand_landmarks.landmark[16]
        pinky = hand_landmarks.landmark[20]
        
        # Distancia entre pulgar e índice (deben estar juntos)
        thumb_index_distance = ((thumb.x - index.x)**2 + (thumb.y - index.y)**2)**0.5
        
        # Comprobamos que indice y pulgar están juntos
        thumb_index_close = thumb_index_distance < self.pinch_threshold  # 0.05
        
        # Comprobamos que los otros dedos están algo extendidos para evitar falsos positivos como cerrar el puño
        thumb_middle_distance = ((thumb.x - middle.x)**2 + (thumb.y - middle.y)**2)**0.5
        thumb_ring_distance = ((thumb.x - ring.x)**2 + (thumb.y - ring.y)**2)**0.5
        thumb_pinky_distance = ((thumb.x - pinky.x)**2 + (thumb.y - pinky.y)**2)**0.5
        other_fingers_open = (thumb_middle_distance > 0.08 and 
                              thumb_ring_distance > 0.08 and 
                              thumb_pinky_distance > 0.08)
        
        
        self.pinch_detected = thumb_index_close and other_fingers_open
        return self.pinch_detected
    
    def reset(self):
        # Resetea las posiciones cuando no se detectan manos.
        self.right_hand_y = None
        self.left_hand_x = None
        self.left_hand_y = None
        self.right_hand_pinch = None
        self.left_hand_pinch = None
        self.pinch_detected = False

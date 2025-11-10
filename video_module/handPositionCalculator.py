
class HandPositionCalculator:
    """
    Clase para calcular las posiciones normalizadas de las manos.
    Mano Derecha: Controla el eje Y (altura)
    Mano Izquierda: Controla el eje X (anchura)
    """
    
    def __init__(self, frame_width, frame_height):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.right_hand_y = None  # Posición Y de la mano derecha (0.0 - 1.0)
        self.left_hand_x = None   # Posición X de la mano izquierda (0.0 - 1.0)
    
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
        
        if hand_label == 'Right':
            # Mano derecha controla el eje Y (invertido para que arriba = 0.0, abajo = 1.0)
            self.right_hand_y = float(avg_y)
        elif hand_label == 'Left':
            # Mano izquierda controla el eje X
            self.left_hand_x = float(avg_x)
    
    def get_right_hand_y(self):
        return self.right_hand_y
    
    def get_left_hand_x(self):
        return self.left_hand_x
    
    def reset(self):
        # Resetea las posiciones cuando no se detectan manos.
        self.right_hand_y = None
        self.left_hand_x = None

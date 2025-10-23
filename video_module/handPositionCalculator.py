
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
        """
        Actualiza la posición de la mano según su etiqueta.
        Calcula la posición media usando múltiples puntos de referencia:
        - Muñeca (landmark 0)
        - Punta del pulgar (landmark 4)
        - Punta del índice (landmark 8)
        - Punta del dedo medio (landmark 12)
        - Punta del anular (landmark 16)
        - Punta del meñique (landmark 20)
        
        Args:
            hand_landmarks: Los landmarks de MediaPipe para la mano
            hand_label: 'Left' o 'Right' indicando qué mano es
        """
        # Índices de los puntos de referencia clave
        key_points = [
            0,   # WRIST (muñeca)
            4,   # THUMB_TIP (punta del pulgar)
            8,   # INDEX_FINGER_TIP (punta del índice)
            12,  # MIDDLE_FINGER_TIP (punta del dedo medio)
            16,  # RING_FINGER_TIP (punta del anular)
            20   # PINKY_TIP (punta del meñique)
        ]
        
        # Calcular la posición media de todos los puntos clave
        avg_x = sum(hand_landmarks.landmark[i].x for i in key_points) / len(key_points)
        avg_y = sum(hand_landmarks.landmark[i].y for i in key_points) / len(key_points)
        
        if hand_label == 'Right':
            # Mano derecha controla el eje Y (invertido para que arriba = 0.0, abajo = 1.0)
            self.right_hand_y = float(avg_y)
        elif hand_label == 'Left':
            # Mano izquierda controla el eje X
            self.left_hand_x = float(avg_x)
    
    def get_right_hand_y(self):
        """
        Obtiene la posición Y normalizada de la mano derecha.
        
        Returns:
            float: Valor entre 0.0 (arriba) y 1.0 (abajo), o None si no se detecta la mano
        """
        return self.right_hand_y
    
    def get_left_hand_x(self):
        """
        Obtiene la posición X normalizada de la mano izquierda.
        
        Returns:
            float: Valor entre 0.0 (izquierda) y 1.0 (derecha), o None si no se detecta la mano
        """
        return self.left_hand_x
    
    def reset(self):
        """Resetea las posiciones cuando no se detectan manos."""
        self.right_hand_y = None
        self.left_hand_x = None

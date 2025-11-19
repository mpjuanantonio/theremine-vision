

import numpy as np


class KalmanFilter:
    """
    Filtro de Kalman 1D para suavizado de posiciones.
    
    Reduce el jitter y ruido en las detecciones de MediaPipe,
    proporcionando movimientos más suaves y predecibles.
    
    Parámetros:
        - initial_value: Posición inicial (0.0-1.0)
        - process_variance: Cuánto esperamos que cambie la posición (mayor = más sensible a cambios rápidos)
        - measurement_variance: Cuánto confiamos en las mediciones de MediaPipe (menor = más confianza)
    """
    
    def __init__(self, initial_value=0.5, process_variance=0.0001, measurement_variance=0.001):

        # Estado: posición estimada
        self.x = np.array([[initial_value], [0.0]])  # [posición, velocidad]
        
        # Matriz de transición de estado (F)
        # Predice el siguiente estado basado en el actual
        self.F = np.array([[1.0, 1.0],   # posición_siguiente = posición + velocidad
                          [0.0, 1.0]])   # velocidad_siguiente = velocidad
        
        # Matriz de medición (H)
        # Solo medimos posición, no velocidad
        self.H = np.array([[1.0, 0.0]])
        
        # Matriz de covarianza de error (P)
        # Estimamos cuánto de error hay en nuestro estado
        self.P = np.array([[1.0, 0.0],
                          [0.0, 1.0]])
        
        # Varianza del proceso (Q)
        # Cuánto esperamos que cambie el modelo entre frames
        self.Q = np.array([[process_variance, 0.0],
                          [0.0, process_variance]])
        
        # Varianza de medición (R)
        # Cuánto ruido esperamos en las mediciones de MediaPipe
        self.R = np.array([[measurement_variance]])
        
        # Ganancia de Kalman (K)
        # Se calcula dinámicamente en cada actualización
        self.K = None
    
    def predict(self):
        # Predecir estado: x = F * x
        self.x = self.F @ self.x
        
        # Predecir covarianza de error: P = F * P * F^T + Q
        self.P = self.F @ self.P @ self.F.T + self.Q
    
    def update(self, measurement):
        
        # Asegurar que la medición está en rango válido
        measurement = np.clip(measurement, 0.0, 1.0)
        
        # Calcular ganancia de Kalman: K = P * H^T / (H * P * H^T + R)
        S = self.H @ self.P @ self.H.T + self.R  # Innovación
        self.K = self.P @ self.H.T @ np.linalg.inv(S)
        
        # Actualizar estado: x = x + K * (z - H * x)
        y = np.array([[measurement]])  # Medición como matriz
        innovation = y - self.H @ self.x
        self.x = self.x + self.K @ innovation
        
        # Actualizar covarianza: P = (I - K * H) * P
        I = np.eye(2)
        self.P = (I - self.K @ self.H) @ self.P
    
    def filter(self, measurement):
       
        self.predict()
        self.update(measurement)
        
        # Retornar posición estimada (primer elemento del vector de estado)
        estimated_position = float(self.x[0, 0])
        
        # Asegurar que está en rango válido
        return np.clip(estimated_position, 0.0, 1.0)
    
    def get_state(self):
       
        return float(self.x[0, 0]), float(self.x[1, 0])
    
    def set_state(self, position, velocity=0.0):
       
        self.x = np.array([[position], [velocity]])


class KalmanFilterPair:
   
    
    def __init__(self, initial_x=0.5, initial_y=0.5, process_variance=0.0001, measurement_variance=0.001):
        
        self.filter_x = KalmanFilter(initial_x, process_variance, measurement_variance)
        self.filter_y = KalmanFilter(initial_y, process_variance, measurement_variance)
    
    def filter(self, x, y):
       
        filtered_x = self.filter_x.filter(x) if x is not None else None
        filtered_y = self.filter_y.filter(y) if y is not None else None
        
        return filtered_x, filtered_y
    
    def get_state(self):
        
        x_pos, x_vel = self.filter_x.get_state()
        y_pos, y_vel = self.filter_y.get_state()
        
        return {
            'x_position': x_pos,
            'x_velocity': x_vel,
            'y_position': y_pos,
            'y_velocity': y_vel
        }
    
    def set_state(self, x_position=None, y_position=None, x_velocity=0.0, y_velocity=0.0):
        
        if x_position is not None:
            self.filter_x.set_state(x_position, x_velocity)
        if y_position is not None:
            self.filter_y.set_state(y_position, y_velocity)

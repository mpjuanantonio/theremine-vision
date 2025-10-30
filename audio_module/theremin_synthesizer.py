"""
Módulo de síntesis de audio para el Theremín Virtual
Genera audio en tiempo real basado en las posiciones de las manos
"""

import numpy as np
import pyaudio
import threading
from collections import deque


class ThereminSynthesizer:
    """
    Sintetizador de theremín que genera audio basado en posiciones de manos. 
    Genera sonido en base al eje x, que asociamos al volumen, y el eje y, que asociamos al tono (pitch).
    La mano derecha controla el tono (eje Y) y la mano izquierda controla el volumen (eje X).
    """
    
    def __init__(self, 
                 sample_rate=44100,
                 min_frequency=200.0,
                 max_frequency=2000.0,
                 wave_type='sine',
                 buffer_size=1024):
        # Frecuencia de muestreo. Define cuantas muestras de audio se generan por segundo.
        #  44100 Hz es estándar para audio de alta calidad. Se podria reducir para mejorar la latencia aunque perdiendo calidad.
        self.sample_rate = sample_rate 
        self.min_frequency = min_frequency # Frecuencia mínima
        self.max_frequency = max_frequency # Frecuencia máxima
        self.wave_type = wave_type # Tipo de onda
        self.buffer_size = buffer_size # Tamaño del buffer

        # Estado actual, con el que empieza la aplicación
        self.current_frequency = 440.0  # A4 por defecto
        self.current_volume = 0.0  # Silencio por defecto
        self.is_playing = False
        
        # Para suavizado de transiciones
        self.frequency_history = deque(maxlen=5)
        self.volume_history = deque(maxlen=3)
        
        # PyAudio
        self.pyaudio = pyaudio.PyAudio()
        self.stream = None
        self.phase = 0.0
        
        # Thread control
        self.lock = threading.Lock()
        
    def start(self):
        # Comienza el stream de audio si no está ya iniciado.
        if self.stream is None:
            self.stream = self.pyaudio.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=self.sample_rate,
                output=True,
                frames_per_buffer=self.buffer_size,
                stream_callback=self._audio_callback
            )
            self.is_playing = True
            self.stream.start_stream()
            print("Sintetizador de theremín iniciado")
    
    def stop(self):
        # Detiene el stream de audio si está activo.
        self.is_playing = False
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        print("Sintetizador detenido")
    
    def cleanup(self):
        # Limpia los recursos de PyAudio
        self.stop()
        self.pyaudio.terminate()
    
    
    # Actualiza la posición de las manos para modificar frecuencia y volumen de salida del audio
    def update_position(self, right_hand_y, left_hand_x):
        
        with self.lock:
            # Actualizar frecuencia basada en mano derecha (Eje Y)
            if right_hand_y is not None:
                # Invertir: Y cercano a 0 = agudo, Y cercano a 1 = grave
                frequency = self._calculate_frequency(1.0 - right_hand_y)
                self.frequency_history.append(frequency)
                # Suavizado
                self.current_frequency = np.mean(self.frequency_history)
            else:
                # Sin mano derecha detectada, mantener frecuencia actual
                pass
            
            # Actualizar volumen basado en mano izquierda (Eje X)
            if left_hand_x is not None:
                # X cercano a 0 = silencio, X cercano a 1 = volumen máximo
                volume = self._calculate_volume(left_hand_x)
                self.volume_history.append(volume)
                # Suavizado
                self.current_volume = np.mean(self.volume_history)
            else:
                # Sin mano izquierda detectada, silencio
                self.current_volume = 0.0
                self.volume_history.clear()
    
    
    # Calcula la frecuencia basada en la posición normalizada.
    def _calculate_frequency(self, normalized_pitch):
        
        # Escala logarítmica para una mejor progresión musical
        log_min = np.log(self.min_frequency)
        log_max = np.log(self.max_frequency)
        log_freq = log_min + normalized_pitch * (log_max - log_min)
        return np.exp(log_freq)
    
    
    # Calcula el volumen basado en la posición normalizada.
    def _calculate_volume(self, normalized_volume):
        
        # Curva suave de volumen
        return normalized_volume ** 1.5
    

    # Genera la onda de audio según el tipo seleccionado. Tenemos varias formas de onda comunes: sine, square, saw, triangle.
    def _generate_wave(self, frequency, num_samples):
        
        # Calcular el incremento de fase
        phase_increment = 2 * np.pi * frequency / self.sample_rate
        
        # Generar índices de fase
        phases = self.phase + np.arange(num_samples) * phase_increment
        
        # Actualizar fase para continuidad
        self.phase = phases[-1] % (2 * np.pi)
        
        # Generar onda según el tipo
        if self.wave_type == 'sine':
            wave = np.sin(phases)
        elif self.wave_type == 'square':
            wave = np.sign(np.sin(phases))
        elif self.wave_type == 'saw':
            wave = 2 * (phases / (2 * np.pi) - np.floor(phases / (2 * np.pi) + 0.5))
        elif self.wave_type == 'triangle':
            wave = 2 * np.abs(2 * (phases / (2 * np.pi) - np.floor(phases / (2 * np.pi) + 0.5))) - 1
        else:
            wave = np.sin(phases)  # Default a sine
        
        return wave
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        # Usamos un lock para evitar que otro hilo modifique los valores mientras generamos audio
        with self.lock:
            frequency = self.current_frequency
            volume = self.current_volume
        
        # Generar onda
        wave = self._generate_wave(frequency, frame_count)
        
        # Aplicar volumen
        audio_data = (wave * volume * 0.3).astype(np.float32)  # 0.3 para evitar clipping
        
        return (audio_data.tobytes(), pyaudio.paContinue)
    
    def get_current_note_name(self):
        # Nombres de notas
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        # A4 = 440 Hz es la referencia
        a4_freq = 440.0
        
        # Calcular número de semitonos desde A4
        if self.current_frequency > 0:
            semitones_from_a4 = 12 * np.log2(self.current_frequency / a4_freq)
            note_number = int(round(semitones_from_a4))
            
            # A4 es la nota 9 de la octava 4
            note_index = (9 + note_number) % 12
            octave = 4 + (9 + note_number) // 12
            
            return f"{note_names[note_index]}{octave}"
        
        return "N/A"
    
    # Información del estado actual del sintetizador, usado para mostrar en pantalla
    def get_info(self):
      
        return {
            'frequency': self.current_frequency,
            'volume': self.current_volume * 100,  # En porcentaje
            'note': self.get_current_note_name(),
            'is_playing': self.is_playing
        }

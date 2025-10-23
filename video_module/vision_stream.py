import cv2
import numpy as np
import time
import mediapipe as mp
import handPositionCalculator

avg_fps = []
video_writer = None



def draw_text_with_bg(img, text, pos, font_scale=0.6, text_color=(255, 255, 255), bg_color=(0, 0, 0)):
    font = cv2.FONT_HERSHEY_SIMPLEX
    thickness = 2
    padding = 20
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    rect_width = text_width + 2 * padding
    rect_height = text_height + baseline + 2 * padding
    x, y = pos
    rect_x1 = x
    rect_y1 = y - text_height
    rect_x2 = rect_x1 + rect_width
    rect_y2 = rect_y1 + rect_height
    cv2.rectangle(img, (rect_x1, rect_y1), (rect_x2, rect_y2), bg_color, -1)  # Draw background rectangle
    text_x = rect_x1 + padding  # Center text in rectangle with equal padding
    text_y = rect_y1 + padding + text_height  # Properly centered vertically
    cv2.putText(img, text, (text_x, text_y), font, font_scale, text_color, thickness)


def hand_tracking(source=0, size=(1440, 810)):
    # Inicializar MediaPipe Hands
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    cap = cv2.VideoCapture(source)

    _, _, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
    video_writer = cv2.VideoWriter("hand-tracking.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, size)

    # Inicializar el calculador de posiciones
    position_calculator = handPositionCalculator.HandPositionCalculator(size[0], size[1])

    while cap.isOpened():
        ret, frame = cap.read()

        # ret es un booleano que indica si se ha leído correctamente el frame
        if not ret:
            break

        frame = cv2.resize(frame, size)
        frame = cv2.flip(frame, 1)  # Efecto espejo
        
        start_time = time.time()
        
        # Convertir BGR a RGB para MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        
        process_time = time.time() - start_time

        # Resetear posiciones antes de actualizar
        position_calculator.reset()

        # Dibujar landmarks de las manos y calcular su posición
        if results.multi_hand_landmarks:
            for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                # Obtener información de la mano (izquierda o derecha)
                hand_label = results.multi_handedness[hand_idx].classification[0].label
                
                # Actualizar posición en el calculador
                position_calculator.update_hand_position(hand_landmarks, hand_label)
                
                # Dibujar las conexiones y puntos de la mano
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )
                
                # Dibujar etiqueta de la mano (Left/Right)
                h, w, _ = frame.shape
                wrist = hand_landmarks.landmark[0]
                wrist_x, wrist_y = int(wrist.x * w), int(wrist.y * h)
                cv2.putText(frame, hand_label, (wrist_x - 30, wrist_y - 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Obtener y mostrar las posiciones de las manos
        right_y = position_calculator.get_right_hand_y()
        left_x = position_calculator.get_left_hand_x()

        # Calculo de fps y escritura en pantalla
        fps = 1.0 / process_time if process_time > 0 else 0
        avg_fps.append(fps)
        fps = sum(avg_fps) / len(avg_fps)
        draw_text_with_bg(frame, f'Hand Tracking FPS: {int(fps)}', (50, 60), bg_color=(0, 200, 100), font_scale=1.2)
        draw_text_with_bg(frame, f'Time: {process_time * 1000:.1f}ms', (50, 145), bg_color=(0, 200, 100),
                          font_scale=1.2)
        
        # Mostrar posiciones de las manos
        if right_y is not None:
            draw_text_with_bg(frame, f'Right Hand Y: {right_y:.4f}', (50, 230), 
                            bg_color=(230, 66, 245), font_scale=1.0)
        else:
            draw_text_with_bg(frame, f'Right Hand Y: N/A', (50, 230), 
                            bg_color=(100, 100, 100), font_scale=1.0)
        
        if left_x is not None:
            draw_text_with_bg(frame, f'Left Hand X: {left_x:.4f}', (50, 300), 
                            bg_color=(66, 245, 230), font_scale=1.0)
        else:
            draw_text_with_bg(frame, f'Left Hand X: N/A', (50, 300), 
                            bg_color=(100, 100, 100), font_scale=1.0)

        cv2.imshow('Hand Tracking', frame)
        video_writer.write(frame)
        # Salir con 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()
    hands.close()


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
import sys
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import os

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
my_drawing_specs = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1)

def classify_face_shape(face_landmarks):
    points = face_landmarks.landmark
    
    forehead_top = points[10]  # Approximate
    chin_bottom = points[152]  # Approximate

    face_height = np.linalg.norm(np.array([forehead_top.x, forehead_top.y]) - np.array([chin_bottom.x, chin_bottom.y]))
    jaw_width = np.linalg.norm(np.array([points[0].x, points[0].y]) - np.array([points[16].x, points[16].y]))

    if face_height == 0:
        return "Undefined"

    ratio = jaw_width / face_height
    
    if ratio > 1.3:
        return "Round"
    elif ratio < 0.75:
        return "Oval"
    else:
        return "Square"

def process_face_shape(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not load image. Check the file path.")
        exit()

    resize_scale = 0.5
    image = cv2.resize(image, (0, 0), fx=resize_scale, fy=resize_scale)
    
    results = []
    with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as face_mesh:
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_mesh_results = face_mesh.process(image_rgb)
        
        if face_mesh_results.multi_face_landmarks:
            for face_landmarks in face_mesh_results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_tesselation_style()
                )
                
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=my_drawing_specs
                )
                
                face_shape = classify_face_shape(face_landmarks)
                cv2.putText(image, f"Face Shape: {face_shape}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                results.append({
                    'SerialNumber': len(results) + 1,
                    'FaceShape': face_shape
                })
        
        cv2.imshow("Image Face Mesh", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    results_df = pd.DataFrame(results)
    output_file_path = r'C:\Users\Aswin\OneDrive\Documents\Learning\face_shape_results.csv'

    if not os.path.isfile(output_file_path):
        next_serial_number = 1
    else:
        existing_df = pd.read_csv(output_file_path)
        next_serial_number = len(existing_df) + 1

    for i in range(len(results_df)):
        results_df.loc[i, 'SerialNumber'] = next_serial_number + i

    if not os.path.isfile(output_file_path):
        results_df.to_csv(output_file_path, index=False)
    else:
        results_df.to_csv(output_file_path, mode='a', header=False, index=False)

    print("Face shape results saved to face_shape_results.csv")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    process_face_shape(image_path)

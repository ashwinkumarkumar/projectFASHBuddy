import sys
import pandas as pd
import cv2
import mediapipe as mp
import numpy as np
import os

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def classify_lengths(shoulder_length, waist_length):
    if shoulder_length > 0.6:
        shoulder_type = "Broad"
    elif shoulder_length < 0.4:
        shoulder_type = "Narrow"
    else:
        shoulder_type = "Balanced"
    
    if waist_length > 0.5:
        waist_type = "High"
    elif waist_length < 0.2:
        waist_type = "Low"
    elif waist_length < 0.4:
        waist_type = "Natural"
    else:
        waist_type = "Dropped"
    
    return shoulder_type, waist_type

def calculate_lengths(landmarks):
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    shoulder_length = np.linalg.norm(np.array([left_shoulder.x, left_shoulder.y]) - np.array([right_shoulder.x, right_shoulder.y]))
    
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
    waist_length = np.linalg.norm(np.array([left_hip.x, left_hip.y]) - np.array([right_hip.x, right_hip.y]))
    
    return shoulder_length, waist_length

def process_pose_estimation(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not load image. Check the file path.")
        exit()
    
    resize_scale = 0.9
    image = cv2.resize(image, (0, 0), fx=resize_scale, fy=resize_scale)
    
    output_file_path = r'C:\Users\Aswin\OneDrive\Documents\Learning\pose_estimation_data.csv'
    
    if os.path.isfile(output_file_path):
        output_df = pd.read_csv(output_file_path)
    else:
        output_df = pd.DataFrame(columns=['SerialNumber', 'ShoulderLength', 'WaistLength', 'ShoulderType', 'WaistType'])

    if not output_df.empty:
        next_serial_number = output_df['SerialNumber'].max() + 1
    else:
        next_serial_number = 1
    
    with mp_pose.Pose(static_image_mode=True, model_complexity=2, enable_segmentation=True, min_detection_confidence=0.5) as pose:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)
        
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            shoulder_length, waist_length = calculate_lengths(results.pose_landmarks.landmark)
            shoulder_type, waist_type = classify_lengths(shoulder_length, waist_length)
            
            cv2.putText(image, f"Shoulder Length: {shoulder_length:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(image, f"Waist Length: {waist_length:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(image, f"Shoulder Type: {shoulder_type}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(image, f"Waist Type: {waist_type}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            
            new_data = pd.DataFrame([{
                'SerialNumber': next_serial_number,
                'ShoulderLength': shoulder_length,
                'WaistLength': waist_length,
                'ShoulderType': shoulder_type,
                'WaistType': waist_type
            }])
            
            output_df = pd.concat([output_df, new_data], ignore_index=True)
            output_df.to_csv(output_file_path, index=False)
        
        cv2.imshow("Pose Estimation", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    print(f"Output data saved to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    process_pose_estimation(image_path)

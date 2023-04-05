import cv2
import mediapipe as mp
import numpy as np
import csv
import os
import glob

# MediaPipe를 이용해 관절 추적을 위한 객체 초기화
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def process_video(input_video):
    # 관절 움직임 추적을 위한 변수 초기화
    joint_movement_counts = {mp_pose.PoseLandmark(i).name: 0 for i in range(len(mp_pose.PoseLandmark))}

    cap = cv2.VideoCapture(input_video)

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        prev_frame_landmarks = None

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            # BGR to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # 관절 추적
            results = pose.process(image)

            if results.pose_landmarks:
                if prev_frame_landmarks:
                    for i, landmark in enumerate(results.pose_landmarks.landmark):
                        prev_landmark = prev_frame_landmarks.landmark[i]
                        distance = np.sqrt((landmark.x - prev_landmark.x) ** 2 + (landmark.y - prev_landmark.y) ** 2)

                        if distance > 0.001:
                            joint_name = mp_pose.PoseLandmark(i).name
                            joint_movement_counts[joint_name] += 1

                prev_frame_landmarks = results.pose_landmarks

                # 관절 시각화 (선택 사항)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Display frame (선택 사항)
            cv2.imshow("Frame", image)
            if cv2.waitKey(1) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()

    return joint_movement_counts

# 디렉토리 내의 모든 동영상 파일 처리
video_directory = "video"
video_files = glob.glob(os.path.join(video_directory, "*.mp4"))

for video_file in video_files:
    joint_movements = process_video(video_file)
    video_name = os.path.splitext(os.path.basename(video_file))[0]
    csv_file = f"{video_name}_result.csv"

    # 결과를 CSV 파일로 저장
    with open(csv_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Joint Name", "Movements"])
        for joint_name, movement_count in joint_movements.items():
            writer.writerow([joint_name, movement_count])

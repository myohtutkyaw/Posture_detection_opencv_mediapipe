import cv2 as cv
import mediapipe as mp
import numpy as np
import math
from collections import deque

mp_pose = mp.solutions.pose

# geometry helpers 
def angle_between(v1, v2):
    v1 = np.array(v1, dtype=np.float32)
    v2 = np.array(v2, dtype=np.float32)
    n1 = np.linalg.norm(v1); n2 = np.linalg.norm(v2)
    if n1 == 0 or n2 == 0:
        return 0.0
    c = np.clip(np.dot(v1, v2) / (n1*n2), -1, 1)
    return math.degrees(math.acos(c))
#coverts input into float array and compute angle between 2 vectors using dot-product formula
def angle_from_vertical(vec):
    return angle_between(vec, (0, -1))  # เทียบกับแกน Y (แนวดิ่งขึ้น)
# opencv + goes to downward so -1 y axis
def lmk_xy(landmark, w, h):
    return np.array([landmark.x * w, landmark.y * h], dtype=np.float32)
#convert landmark to pixel coordinate using current frame width/height
def pick_side(lm, w, h):
    L = {
        "SH": lm[mp_pose.PoseLandmark.LEFT_SHOULDER],
        "HP": lm[mp_pose.PoseLandmark.LEFT_HIP],
        "EA": lm[mp_pose.PoseLandmark.LEFT_EAR],
    }
    R = {
        "SH": lm[mp_pose.PoseLandmark.RIGHT_SHOULDER],
        "HP": lm[mp_pose.PoseLandmark.RIGHT_HIP],
        "EA": lm[mp_pose.PoseLandmark.RIGHT_EAR],
    }
    L_score = L["SH"].visibility + L["HP"].visibility + L["EA"].visibility
    R_score = R["SH"].visibility + R["HP"].visibility + R["EA"].visibility
    side = L if L_score >= R_score else R
    name = "LEFT" if L_score >= R_score else "RIGHT"
    return {k: lmk_xy(side[k], w, h) for k in side}, name
#visiblitiy score(0-1) pick the side that has better total visibility (left or right)

# -- posture levels --
def severity_from_angles(trunk_ang, neck_ang):
    if neck_ang >= 40 or trunk_ang >= 14 or fhd_ratio >=0.3 :
        return 4  # Severe slouch
    elif neck_ang >= 30 or trunk_ang >= 12 or fhd_ratio >=0.2 :
        return 3  # Moderate slouch
    elif neck_ang >= 15 or trunk_ang >= 9.7 or fhd_ratio >=0.1 :
        return 2  # Mild slouch
    else:
        return 1  # Normal posture
#threshold for slouching severity 

def level_label(lv):
    return {
        1: "Normal posture",
        2: "Mild slouch ",
        3: "Moderate slouch ",
        4: "Severe slouch "
    }.get(lv, "Unknown")

def level_color(lv):
    return {
        1: (0,255,0),
        2: (0,255,255),
        3: (0,165,255),
        4: (0,0,255)
    }.get(lv, (255,255,255)) 
#text label and BGR color to draw for each level

# -- main --
cap = cv.VideoCapture(0)
levels = deque(maxlen=10)
MIRROR = True

# ขนาดหน้าจอ
target_width, target_height = 1500, 940

#levels keeps the most recent 10 classification to smooth out noise later

with mp_pose.Pose(static_image_mode=False, model_complexity=1,
                  enable_segmentation=False, min_detection_confidence=0.6,
                  min_tracking_confidence=0.6) as pose:
#static_image_mode = Flase: for video
#model complexity = 1 (medium)
#confidence threshold=0.6 for detection and tracking
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if MIRROR:
            frame = cv.flip(frame, 1)

        h, w = frame.shape[:2]
        rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        res = pose.process(rgb)
#mirror and covert from BGR TO RGB

        trunk_ang = neck_ang = back_bend = fhd_ratio = 0.0
        side_used_disp = "N/A"
#default if no one is detected

        if res.pose_landmarks:
            lm = res.pose_landmarks.landmark
            side_pts, side_used_body = pick_side(lm, w, h)
            side_used_disp = "RIGHT" if (MIRROR and side_used_body=="LEFT") else \
                             "LEFT" if (MIRROR and side_used_body=="RIGHT") else side_used_body

            SH = side_pts["SH"]
            HP = side_pts["HP"]
            EA = side_pts["EA"]
#picks the best visible side and mirror to no true left and no true right
            # -- Trunk angle --
            trunk_vec = SH - HP   # จาก สะโพก ไป ไหล่
            trunk_ang = angle_from_vertical(trunk_vec)
#trunk angle is how much the line from hip to shoulder tilts away from straight-up

            # -- Neck angle --
            neck_vec = EA - SH    # จาก ไหล่ ไป หู
            neck_ang = angle_between(neck_vec, SH - HP)
#relative bend between neck segment and trunk segment
            # -- FHD ratio --
            torso_len = np.linalg.norm(trunk_vec)
            fhd_ratio = abs(EA[0] - SH[0]) / torso_len if torso_len > 0 else 0
#measure how far ear is horizontally un front of or behind the shoulder
            # -- Back bend --
            back_bend = trunk_ang  # ใช้ trunk angle เป็นตัวแทนองศาเอนหลัง

            # -- Level classification --
            level = severity_from_angles(trunk_ang, neck_ang)
            levels.append(level)
#frame level to 10frame buffer
            # -- Draw skeleton --
            SHi, HPi, EAi = tuple(SH.astype(int)), tuple(HP.astype(int)), tuple(EA.astype(int))
            cv.line(frame, HPi, SHi, (0,255,0), 2)
            cv.line(frame, SHi, EAi, (255,255,0), 2)
        else:
            levels.append(1)
#if no person, default to normal
        debounced_level = int(np.median(levels)) if levels else 1
        label_txt = level_label(debounced_level)
        label_col = level_color(debounced_level)
#median of last 10 frame (reduce flicker)
        # -- HUD --
        y0 = 30
        cv.putText(frame, f"Side: {side_used_disp}", (10,y0), cv.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)
        cv.putText(frame, f"Trunk angle: {trunk_ang:.1f}degree", (10,y0+30), cv.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),2)
        cv.putText(frame, f"Neck angle: {neck_ang:.1f}degree", (10,y0+60), cv.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)
        cv.putText(frame, f"Back bend: {back_bend:.1f}degree", (10,y0+90), cv.FONT_HERSHEY_SIMPLEX,0.6,(255,200,0),2)
        cv.putText(frame, f"FHD ratio: {fhd_ratio:.2f}", (10,y0+120), cv.FONT_HERSHEY_SIMPLEX,0.6,(0,255,255),2)
        cv.putText(frame, f"Posture Level: {label_txt}", (10,h-30), cv.FONT_HERSHEY_SIMPLEX,0.8,label_col,2)
#on screen display of all metrics and debounced posture level in its color

        # --Resize to 1500x940 --
        resized = cv.resize(frame, (target_width, target_height))
        cv.imshow("Posture (Side View) - 1500x940", resized)
#resize frame (doesn't affect anything)
        if cv.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv.destroyAllWindows()
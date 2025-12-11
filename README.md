🧍‍♂️ Slouch Detection System
Digital Image Processing Mini Project

📌 Overview

This project implements an intelligent slouch detection system using MediaPipe Pose, OpenCV, and geometric angle analysis. The system monitors human posture in real time using a webcam and classifies posture into Good, Mild, Moderate, or Severe slouching based on neck angle, trunk angle, and forward head displacement.
(See page 1 for project cover) 

Final presentation images _comp…

📚 Table of Contents

Problem Statement

Objectives

Proposed Method

Experiment

Results

Conclusion

Future Work

References

🚨 Problem Statement

Manual posture monitoring is inefficient, inconsistent, and error-prone. Poor posture, especially slouching, contributes to long-term musculoskeletal problems.
This project aims to develop an automated image-processing system that can identify:

Sitting posture

Standing posture

Different levels of slouching
(Page 3) 

Final presentation images _comp…

🎯 Objectives

(Page 4) 

Final presentation images _comp…

Automate slouching posture detection

Classify slouch severity accurately

Promote ergonomic awareness and healthier sitting habits

🧠 Proposed Method
1. Input Acquisition

Webcam captures real-time video frames.

Images processed as BGR frames in OpenCV.
(Page 5) 

Final presentation images _comp…

2. Pose Estimation (MediaPipe Pose)

Detects 33 anatomical key points.

Automatically selects the most visible body side (left/right).
(Page 5) 

Final presentation images _comp…

3. Geometry Computation

Convert keypoints into measurable posture indicators:

Trunk Angle – angle relative to vertical Y-axis.

Neck Angle – tilt between neck and torso.

FHD Ratio (Forward Head Displacement) – horizontal head deviation relative to neck length.
(Page 6) 

Final presentation images _comp…

Severity Classification:

Level	Conditions
Severe	neck ≥ 40°, trunk ≥ 14°, FHD ≥ 0.3
Moderate	neck ≥ 30°, trunk ≥ 12°, FHD ≥ 0.2
Mild	neck ≥ 15°, trunk ≥ 9.7°, FHD ≥ 0.1
Normal	else

References acknowledged in slides:

Antonelli-Incalzi: thoracic curvature > 40°

Kenneth Hansraj: text-neck effects on spine load
(Page 6) 

Final presentation images _comp…

4. Visualization & Output

System displays:

Trunk angle

Neck angle

FHD ratio

Side detection

Posture level (Color-coded: green → red)
(Page 7) 

Final presentation images _comp…

🧪 Experiment
Real-Time Testing

Implemented using Python + MediaPipe Pose.

Overlays: lines, labels, angle values updated per frame.

Classified four posture levels.
(Example frames on page 8) 

Final presentation images _comp…

Validation with Medical Goniometer

Collected ground-truth measurements of neck and trunk angles.
(Page 9) 

Final presentation images _comp…

📊 Results
Comparison of Goniometer vs Image Processing

(Complete table on page 10) 

Final presentation images _comp…

Mean Difference

Total bias = +1.4 degrees, meaning the system’s angle predictions closely match medical measurements.
(Page 11) 

Final presentation images _comp…

Correlation

Charts on page 12 show:

R² = 0.9462 (Medical Tool)

R² = 0.9277 (Image Processing)

98% correlation between methods
These confirm high accuracy of pose-based estimation.


Final presentation images _comp…

🏁 Conclusion

This project successfully developed an intelligent, real-time posture monitoring system using a fixed camera.
MediaPipe Pose and geometric computation allowed accurate classification of:

Good posture

Mild slouch

Moderate slouch

Severe slouch

The system helps automate posture analysis and promotes better ergonomic habits.
(Page 13) 

Final presentation images _comp…

🚀 Future Work

(Page 14) 

Final presentation images _comp…

3D Posture Estimation using depth cameras (e.g., OAK-D)

Multi-Angle Detection for front & side views

Real-Time Alerts (sound, vibration, LED feedback)

📖 References

(Page 15) 

Final presentation images _comp…


Includes academic papers, IEEE references, MediaPipe documentation, and medical studies.

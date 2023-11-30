from ultralytics import YOLO
import numpy as np
model = YOLO("yolov8n-pose.pt",task="pose")
SOL_OMUZ = 5
SAG_OMUZ = 6
SAG_BILEK = 16
SOL_BILEK = 15
SOL_BEL = 11
SAG_BEL = 12
SOL_DIRSEK = 7
SAG_DIRSEK = 8
SOL_EL = 9
SAG_EL = 10
SOL_DIZ = 13
SAG_DIZ = 14
import math
def comelme_hesapla(sol_bilek,sol_diz,sol_bel):
    p1 = math.dist(sol_bilek,sol_diz)
    p2 = math.dist(sol_diz,sol_bel)
    p3 = math.dist(sol_bel,sol_bilek)
    aci = math.degrees(math.acos((p1*p1+p2*p2-p3*p3)/(2*p1*p2)))
    if aci<90:
        return True
    else:
        return False

def yatma_hesapla(sol_dirsek,sol_omuz,sol_bel):
    p1 = math.dist(sol_dirsek,sol_omuz)
    p2 = math.dist(sol_omuz,sol_bel)
    p3 = math.dist(sol_bel,sol_dirsek)
    aci = math.degrees(math.acos((p1*p1+p2*p2-p3*p3)/(2*p1*p2)))
    if aci>30:
        return True
    else:
        return False
def kosma_hesapla(sol_el,sol_dirsek,sol_omuz):
    p1 = math.dist(sol_el,sol_dirsek)
    p2 = math.dist(sol_dirsek,sol_omuz)
    p3 = math.dist(sol_omuz,sol_el)
    aci = math.degrees(math.acos((p1*p1+p2*p2-p3*p3)/(2*p1*p2)))
    if aci<90:
        return True
    else:
        return False
from collections import defaultdict

import cv2
import numpy as np

from ultralytics import YOLO

# Load the YOLOv8 model

# Open the video file
video_path = r"fainting_videos\Denmark official faints during Covid-19 conference.mp4"
cap = cv2.VideoCapture(video_path)
writer = cv2.VideoWriter("test1.mp4",-1,30,(int(cap.get(3)),int(cap.get(4))),True)
# Store the track history
track_history = defaultdict(lambda: [])
frame_count = 0
frame_count_last = {}
frame_count_first = {}

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        try:    
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
            results = model.track(frame, persist=True)

        # Get the boxes and track IDs
            boxes = results[0].boxes.xywh.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            keypoints = results[0].keypoints.xy.cpu()
            
        # Visualize the results on the frame
            annotated_frame = results[0].plot()
            if len(track_ids):
                for i,trk_id in enumerate(track_ids):
                    if trk_id not in frame_count_first:
                        frame_count_last[trk_id] = frame_count
                        frame_count_first[trk_id] = frame_count
                    if frame_count_last[trk_id]>frame_count_first[trk_id]:
                        frame_count_last[trk_id] = frame_count
                    else:
                        frame_count_first[trk_id] = frame_count
        # Plot the tracks
            for box, track_id,keypoint in zip(boxes, track_ids,keypoints):
                x, y, w, h = box
                track = track_history[track_id]
                track.append((float(x), float(y)))  # x, y center point
                #if len(track) > 30:  # retain 90 tracks for 90 frames
                #    track.pop(0)
                sol_bel = keypoint.xy.cpu()[0][SOL_BEL]
                sol_diz = keypoint.xy.cpu()[0][SOL_DIZ]
                sol_bilek = keypoint.xy.cpu()[0][SOL_BILEK]
                sol_el = keypoint.xy.cpu()[0][SOL_EL]
                sol_dirsek= keypoint.xy.cpu()[0][SOL_DIRSEK]
                sol_omuz = keypoint.xy.cpu()[0][SOL_OMUZ]
                if comelme_hesapla(sol_bilek=sol_bilek,sol_diz=sol_diz,sol_bel=sol_bel):
                    cv2.putText(annotated_frame,"comelme",(int(x),int(y+20)),cv2.FONT_HERSHEY_COMPLEX,1,(230,230,230),1)
                elif kosma_hesapla(sol_el=sol_el,sol_dirsek=sol_dirsek,sol_omuz=sol_omuz):
                    cv2.putText(annotated_frame,"kosma",(int(x),int(y+20)),cv2.FONT_HERSHEY_COMPLEX,1,(230,230,230),1)
                elif yatma_hesapla(sol_dirsek=sol_dirsek,sol_omuz=sol_omuz,sol_bel=sol_bel):
                    cv2.putText(annotated_frame,"yatma",(int(x),int(y+20)),cv2.FONT_HERSHEY_COMPLEX,1,(230,230,230),1)
                else:
                    cv2.putText(annotated_frame,"hicbirsey yapmiyor.",(int(x),int(y+20)),cv2.FONT_HERSHEY_COMPLEX,1,(230,230,230),1)
            # Draw the tracking lines
                duration = (frame_count_first[track_id]-frame_count_last[track_id])/30
                cv2.putText(annotated_frame,f"duration: {round(duration)}",(int(x),int(y+10)),cv2.FONT_HERSHEY_COMPLEX,1,(230,230,230),1)

        # Display the annotated frame
            cv2.imshow("YOLOv8 Tracking", annotated_frame)
            writer.write(annotated_frame)

        # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        except (AttributeError):
            continue
        frame_count+=1
    else:
        # Break the loop if the end of the video is reached
        break
    

# Release the video capture object and close the display window
cap.release()
writer.release()
cv2.destroyAllWindows()
from ultralytics import YOLO
import numpy as np
from collections import defaultdict
import cv2
from utils import comelme_hesapla,kosma_hesapla,yatma_hesapla \
    ,SOL_BEL,SAG_BEL,SAG_BILEK,SAG_DIRSEK,SAG_DIZ,SAG_EL,SAG_OMUZ,SOL_BILEK,SOL_DIRSEK,SOL_DIZ,SOL_EL,SOL_OMUZ


class PoseEstimator:
    def __init__(self,model = 'yolov8n-pose',task = 'pose'):
        self.model = YOLO(model,task=task)
        self.track_history = defaultdict(lambda: [])
    def detect_image(self,img):
        results = self.model(img)
        keypoints = results[0].keypoints.xy.cpu()
        boxes = results[0].boxes.xywh.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()
        annotated_frame = results[0].plot()
        for box, track_id,keypoint in zip(boxes, track_ids,keypoints):
            x, y, w, h = box
            track = self.track_history[track_id]
            track.append((float(x), float(y)))  # x, y center point
            #if len(track) > 30:  # retain 90 tracks for 90 frames
            #    track.pop(0)
            sol_bel = keypoint.xy.cpu()[0][SOL_BEL]
            sol_diz = keypoint.xy.cpu()[0][SOL_DIZ]
            sol_bilek = keypoint.xy.cpu()[0][SOL_BILEK]
            sol_el = keypoint.xy.cpu()[0][SOL_EL]
            sol_dirsek= keypoint.xy.cpu()[0][SOL_DIRSEK]
            sol_omuz = keypoint.xy.cpu()[0][SOL_OMUZ]
            sag_bel = keypoint.xy.cpu()[0][SAG_BEL]
            sag_diz = keypoint.xy.cpu()[0][SAG_DIZ]
            sag_bilek = keypoint.xy.cpu()[0][SAG_BILEK]
            sag_el = keypoint.xy.cpu()[0][SAG_EL]
            sag_dirsek = keypoint.xy.cpu()[0][SAG_DIRSEK]
            sag_omuz = keypoint.xy.cpu()[0][SAG_OMUZ]
            if comelme_hesapla(sol_bilek=sol_bilek,sol_diz=sol_diz,sol_bel=sol_bel,sag_bilek=sag_bilek,sag_bel=sag_bel,sag_diz=sag_diz,sag_omuz=sag_omuz,sol_omuz=sol_omuz):
                cv2.putText(annotated_frame,"comelme",(int(x),int(y+20)),cv2.FONT_HERSHEY_COMPLEX,1,(230,230,230),1)
            elif kosma_hesapla(sol_el=sol_el,sol_dirsek=sol_dirsek,sol_omuz=sol_omuz,sag_bel=sag_bel,sag_bilek=sag_bilek,sag_dirsek=sag_dirsek,sag_diz=sag_diz,sag_el=sag_el,sag_omuz=sag_omuz,sol_bel=sol_bel,sol_bilek=sol_bilek,sol_diz=sol_diz):
                cv2.putText(annotated_frame,"kosma",(int(x),int(y+20)),cv2.FONT_HERSHEY_COMPLEX,1,(230,230,230),1)
            elif yatma_hesapla(sol_dirsek=sol_dirsek,sol_omuz=sol_omuz,sol_bel=sol_bel,sag_bel=sag_bel,sag_bilek=sag_bilek,sag_dirsek=sag_dirsek,sag_diz=sag_diz,sag_omuz=sag_omuz,sol_bilek=sol_bilek,sol_diz=sol_diz):
                cv2.putText(annotated_frame,"yatma",(int(x),int(y+20)),cv2.FONT_HERSHEY_COMPLEX,1,(230,230,230),1)
            else:
                cv2.putText(annotated_frame,"hicbirsey yapmiyor.",(int(x),int(y+20)),cv2.FONT_HERSHEY_COMPLEX,1,(230,230,230),1)
        return annotated_frame
    def show_img(img):
        cv2.imshow('annotated frame',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    def detect_video(self,video_path,save = True,output_path = "output.mp4"):
        cap = cv2.VideoCapture(video_path)
        if save:
            writer = cv2.VideoWriter(output_path,-1,30,(int(cap.get(3)),int(cap.get(4))),True)
        frame_count = 0
        frame_count_last = {}
        frame_count_first = {}
        while cap.isOpened():
            success, frame = cap.read()
            if success:
                try:
                    results = self.model.track(frame, persist=True)
                    boxes = results[0].boxes.xywh.cpu()
                    track_ids = results[0].boxes.id.int().cpu().tolist()
                    keypoints = results[0].keypoints.cpu()
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
                    for box, track_id, keypoint in zip(boxes, track_ids,keypoints):
                        x, y, w, h = box
                        track = self.track_history[track_id]
                        track.append((float(x), float(y)))
                        if len(track) > 30:
                            track.pop(0)
                        sol_bel = keypoint.xy.cpu()[0][SOL_BEL]
                        sol_diz = keypoint.xy.cpu()[0][SOL_DIZ]
                        sol_bilek = keypoint.xy.cpu()[0][SOL_BILEK]
                        sol_el = keypoint.xy.cpu()[0][SOL_EL]
                        sol_dirsek= keypoint.xy.cpu()[0][SOL_DIRSEK]
                        sol_omuz = keypoint.xy.cpu()[0][SOL_OMUZ]
                        sag_bel = keypoint.xy.cpu()[0][SAG_BEL]
                        sag_diz = keypoint.xy.cpu()[0][SAG_DIZ]
                        sag_bilek = keypoint.xy.cpu()[0][SAG_BILEK]
                        sag_el = keypoint.xy.cpu()[0][SAG_EL]
                        sag_dirsek = keypoint.xy.cpu()[0][SAG_DIRSEK]
                        sag_omuz = keypoint.xy.cpu()[0][SAG_OMUZ]
                        if comelme_hesapla(sol_bilek=sol_bilek,sol_diz=sol_diz,sol_bel=sol_bel,sag_bilek=sag_bilek,sag_bel=sag_bel,sag_diz=sag_diz,sol_omuz=sol_omuz,sag_omuz=sag_omuz):
                            cv2.putText(annotated_frame,"comelme",(int(x),int(y+20)),cv2.FONT_HERSHEY_COMPLEX,1,(230,230,230),1)
                        elif kosma_hesapla(sol_el=sol_el,sol_dirsek=sol_dirsek,sol_omuz=sol_omuz,sag_bel=sag_bel,sag_bilek=sag_bilek,sag_dirsek=sag_dirsek,sag_diz=sag_diz,sag_el=sag_el,sag_omuz=sag_omuz,sol_bel=sol_bel,sol_bilek=sol_bilek,sol_diz=sol_diz):
                            cv2.putText(annotated_frame,"kosma",(int(x),int(y+20)),cv2.FONT_HERSHEY_COMPLEX,1,(230,230,230),1)
                        elif yatma_hesapla(sol_dirsek=sol_dirsek,sol_omuz=sol_omuz,sol_bel=sol_bel,sag_bel=sag_bel,sag_bilek=sag_bilek,sag_dirsek=sag_dirsek,sag_diz=sag_diz,sag_omuz=sag_omuz,sol_bilek=sol_bilek,sol_diz=sol_diz):
                            cv2.putText(annotated_frame,"yatma",(int(x),int(y+20)),cv2.FONT_HERSHEY_COMPLEX,1,(230,230,230),1)
                        else:
                            cv2.putText(annotated_frame,"hicbirsey yapmiyor.",(int(x),int(y+20)),cv2.FONT_HERSHEY_COMPLEX,1,(230,230,230),1)
                        duration = (frame_count_first[track_id]-frame_count_last[track_id])/30
                        cv2.putText(annotated_frame,f"duration: {round(duration)}",(int(x-50),int(y)),cv2.FONT_HERSHEY_COMPLEX,1,(230,230,230),1)

                    cv2.imshow("YOLOv8 Tracking", annotated_frame)
                    if save:
                        writer.write(annotated_frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                except (AttributeError):
                    continue
                frame_count+=1
            else:
                break
        cap.release()
        if save:
            writer.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    pose_estimator = PoseEstimator()
    video_path = r"fainting_videos\Denmark official faints during Covid-19 conference.mp4"
    pose_estimator.detect_video(video_path=video_path)
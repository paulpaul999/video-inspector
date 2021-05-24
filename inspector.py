from functools import partial
import numpy as np
import cv2

import json

from sys import exit

# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html

def load_project(json_path):
    with open(project_file, 'rb') as f:
        infos = json.load(f)
    return infos['start'], infos['videos']

def split_sbs_frame(frame):
    """returns left and right frame as a tuple (L,R)"""
    boundary = (frame.shape[1]//2)
    return frame[:,:boundary], frame[:,boundary:]

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Tool for video resolution/quality comparison.')
    parser.add_argument('-p', '--project', required=False, type=str, help='Project file in JSON format.', metavar='FILE')
    args = parser.parse_args()
    # ------------------------------
    
    project_file = args.project if args.project else 'project.json'
    start_frame, in_video_infos = load_project(project_file)
    
    for video_info in in_video_infos:
        path = video_info['path']
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            print("Cannot open file "+path)
            exit()
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame+video_info['offset'])
        #cap.set(cv2.CAP_PROP_POS_MSEC, 1000*30)
        video_info['capture'] = cap

    selected_video_idx = 0
    zoom_level = 1
    running = True
    while running:
        for video_info in in_video_infos:
            cap = video_info['capture']
            #cap.set(cv2.CAP_PROP_POS_FRAMES, int(selected_frame_num))
            ret, frame = cap.read()
        
            # Processing
            #frame = background.copy()
            frame = split_sbs_frame(frame)[0]
            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            video_info['frame'] = frame
        
        while True:
            # local transformations
            video_info = in_video_infos[selected_video_idx]
            frame = video_info['frame']
            if not zoom_level == 1:
                _scale = 1/zoom_level
                
                dst = np.float64([[0,0],[frame.shape[0],0],[0,frame.shape[1]]])
                center_point = np.float64(((frame.shape[0]-1)/2, (frame.shape[1]-1)/2))
                src = np.float64( center_point+_scale*(dst-center_point) )
                
                M = cv2.getAffineTransform(np.float32(src),np.float32(dst))
                frame = cv2.warpAffine(frame,M,frame.shape[:2])
            
            cv2.putText(frame, video_info['note'], (100,500), cv2.FONT_HERSHEY_SIMPLEX, 5, 255, 16)
            
            # Show and save
            cv2.namedWindow('image', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('image', 800,800)
            cv2.imshow('image', frame)
    
            key = chr(cv2.waitKey(delay=0) & 0xFF)
            if key == 'q':
                running = False
                break
            elif key == 'd':
                selected_video_idx = (selected_video_idx+1) % len(in_video_infos)
            elif key == 'a':
                selected_video_idx = (selected_video_idx-1) % len(in_video_infos)
            elif key == 'e':
                print("### Next frame ###")
                break
            elif key == 'w':
                zoom_level = max(1,zoom_level+1)
            elif key == 's':
                zoom_level = max(1,zoom_level-1)
    
    for video_info in in_video_infos:
        video_info['capture'].release()
    
    cv2.destroyAllWindows()

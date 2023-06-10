# encodeing = big-5
import cv2
from pathlib import Path
import numpy as np
from utils.tracker import *
import time
from datetime import datetime
import os
import shutil
import sys
import openpyxl
from openpyxl.workbook import Workbook
# from control_pi import OSIsoftPy
from PIL import ImageFont, ImageDraw, Image


class Detector(object):

    def smoke_detection():
        output_file_name = time.strftime("%Y_%m_%d", time.localtime())
        print(output_file_name)
        
        # Create tracker object
        tracker = EuclideanDistTracker()
        
        cap = cv2.VideoCapture("smoke.mp4")
        # cap = cv2.VideoCapture("rtsp://root:FCFA@<cctv　の　ip>")

        output_dir = output_file_name+"_output"
        if os.path.isdir(output_dir):
            # shutil.rmtree(output_dir)
            print('ディレクトリはすでに存在します!')
        else:
            os.makedirs(output_dir+"/with smoke", exist_ok=True)
            os.makedirs(output_dir+"/no smoke", exist_ok=True)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file_name + '_output.mp4', fourcc, 30.0, (1344, 756)) # new
        
        number_of_smoke_events_per_minute = 40
        
        current_time_hour = int(time.strftime("%H", time.localtime()))
        
        if (current_time_hour > 5) and (current_time_hour < 18):
            object_detector = cv2.createBackgroundSubtractorMOG2(history=25, varThreshold=3,detectShadows = False)
        else:
            object_detector = cv2.createBackgroundSubtractorMOG2(history=25, varThreshold=3,detectShadows = False)
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        
        x_scale = 0.7
        y_scale = 0.7
        roi_x1 = int(0*x_scale)
        roi_x2 = int(1200*x_scale)
        roi_y1 = int(0*y_scale)
        roi_y2 = int(750*y_scale)

        dark_left_roi_x1 = int(100 * x_scale)
        dark_left_roi_x2 = int(300 * x_scale)
        dark_left_roi_y1 = int(700 * y_scale)
        dark_left_roi_y2 = int(900 * y_scale)

        dark_right_roi_x1 = int(1650 * x_scale)
        dark_right_roi_x2 = int(1850 * x_scale)
        dark_right_roi_y1 = int(700 * y_scale)
        dark_right_roi_y2 = int(900 * y_scale)

        s_up_roi_x1 = int(500 * x_scale)
        s_up_roi_x2 = int(700 * x_scale)
        s_up_roi_y1 = int(200 * y_scale)
        s_up_roi_y2 = int(400 * y_scale)

        s_right_roi_x1 = int(700 * x_scale)
        s_right_roi_x2 = int(850 * x_scale)
        s_right_roi_y1 = int(200 * y_scale)
        s_right_roi_y2 = int(600 * y_scale)

        s_left_roi_x1 = int(350 * x_scale)
        s_left_roi_x2 = int(500 * x_scale)
        s_left_roi_y1 = int(200 * y_scale)
        s_left_roi_y2 = int(600 * y_scale)

        # normal part

        region_all = []
        n_layer = 14
        
        for i in range(n_layer):
            region_all.append([(340-i*25,260-i*20),(340-i*25,500),(350-i*25,500),(350-i*25,270-i*20),(490+i*25,270-i*20),(490+i*25,500),(500+i*25,500),(500+i*25,260-i*20)])

        region_all_time_a = []
        region_all_time_b = []
        smoke_flag = []
        smoke_initial_time = []
        time_diff_all = []
        x_dis = []
        y_dis = []
        
        for i in range(len(region_all)):
            region_all_time_a.append({})
            region_all_time_b.append({})
        
        for i in range(len(region_all) - 1):
            smoke_flag.append(False)
            smoke_initial_time.append(0)
            time_diff_all.append(0)
            x_dis.append(0)
            y_dis.append(0)

        # horizontal_down part

        region_all_horizontal_down = []
        n_layer_horizontal_down = 25

        for i in range(n_layer_horizontal_down):
            region_all_horizontal_down.append([(250, 240 + i * 10), (580, 240 + i * 10), (580, 245 + i * 10), (250, 245 + i * 10)])

        region_all_time_a_horizontal_down = []
        region_all_time_b_horizontal_down = []
        smoke_flag_horizontal_down = []
        smoke_initial_time_horizontal_down = []
        time_diff_all_horizontal_down = []
        x_dis_horizontal_down = []
        y_dis_horizontal_down = []

        for i in range(len(region_all_horizontal_down)):
            region_all_time_a_horizontal_down.append({})
            region_all_time_b_horizontal_down.append({})

        for i in range(len(region_all_horizontal_down) - 1):
            smoke_flag_horizontal_down.append(False)
            smoke_initial_time_horizontal_down.append(0)
            time_diff_all_horizontal_down.append(0)
            x_dis_horizontal_down.append(0)
            y_dis_horizontal_down.append(0)

        # horizontal_up part

        region_all_horizontal_up = []
        n_layer_horizontal_up = 50

        for i in range(n_layer_horizontal_up):
            region_all_horizontal_up.append([(250, 300 - i * 4), (580, 300 - i * 4), (580, 302 - i * 4), (250, 302 - i * 4)])

        region_all_time_a_horizontal_up = []
        region_all_time_b_horizontal_up = []
        smoke_flag_horizontal_up = []
        smoke_initial_time_horizontal_up = []
        time_diff_all_horizontal_up = []
        x_dis_horizontal_up = []
        y_dis_horizontal_up = []

        for i in range(len(region_all_horizontal_up)):
            region_all_time_a_horizontal_up.append({})
            region_all_time_b_horizontal_up.append({})

        for i in range(len(region_all_horizontal_up) - 1):
            smoke_flag_horizontal_up.append(False)
            smoke_initial_time_horizontal_up.append(0)
            time_diff_all_horizontal_up.append(0)
            x_dis_horizontal_up.append(0)
            y_dis_horizontal_up.append(0)

        def motion(region_a, region_b, x, y, w, h, id,region_all_time_a, region_all_time_b):
        
            inside_region_a = cv2.pointPolygonTest(np.array(region_a), (int(x + w / 2), int(y + h / 2)), False)
            if inside_region_a >= 0:
                region_all_time_a[id] = time.time()
        
            if id in region_all_time_a:
                inside_region_b = cv2.pointPolygonTest(np.array(region_b), (int(x + w / 2), int(y + h / 2)), False)
                if inside_region_b >= 0:
                    if id not in region_all_time_b:
                        region_all_time_b[id] = time.time()
                        #print("here: ", region_all_time_b[id] - region_all_time_a[id], " ",id)
                        time_diff = region_all_time_b[id] - region_all_time_a[id]
                        if time_diff > 0 and time_diff < 0.8:
        
                            cv2.putText(roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 1)
                            cv2.circle(roi, (int(x + w / 2), int(y + h / 2)), 3, (0, 0, 255), 6)
                            return time.time(), True, time_diff, x, y
        
        count =1
        temp_time_diff = []
        temp_x_dis = []
        temp_y_dis = []

        count_horizontal_down =1
        temp_time_diff_horizontal_down = []
        temp_x_dis_horizontal_down = []
        temp_y_dis_horizontal_down = []

        count_horizontal_up =1
        temp_time_diff_horizontal_up = []
        temp_x_dis_horizontal_up = []
        temp_y_dis_horizontal_up = []

        frame_count = 1
        n_alarm_400_frames = []
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        temp_date_hour_minute = ''
        count_n_smoke = 0
        
        while True:
            cap.grab()
            ret, frame = cap.retrieve()
            if not ret:
                print("ライブストリームが中断されました: ",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                break
        
            rows, cols=frame.shape[:2]
            size=(int(cols*x_scale), int(rows*y_scale))
            frame = cv2.resize(frame,size)
    #        frame = cv2.rectangle(frame, (roi_x1, roi_y1),(roi_x2, roi_y2),(0,255,0),3)
            roi = frame[roi_y1: roi_y2, roi_x1: roi_x2]
            median_value = np.median(roi)
    #        print(median_value)

            dark_left_roi = frame[dark_left_roi_y1: dark_left_roi_y2, dark_left_roi_x1: dark_left_roi_x2]
            dark_left_median_value = np.median(dark_left_roi)
    #        print('dark_left: ',dark_left_median_value)
    #        frame = cv2.rectangle(frame, (dark_left_roi_x1, dark_left_roi_y1), (dark_left_roi_x2, dark_left_roi_y2), (0, 255, 0), 3)
            dark_right_roi = frame[dark_right_roi_y1: dark_right_roi_y2, dark_right_roi_x1: dark_right_roi_x2]
            dark_right_median_value = np.median(dark_right_roi)
    #        print('dark_right: ',dark_right_median_value)
    #        frame = cv2.rectangle(frame, (dark_right_roi_x1, dark_right_roi_y1), (dark_right_roi_x2, dark_right_roi_y2), (0, 255, 0), 3)
            s_up_roi = frame[s_up_roi_y1: s_up_roi_y2, s_up_roi_x1: s_up_roi_x2]
            s_up_median_value = np.median(s_up_roi)
    #        print('s_up: ', s_up_median_value)
    #        frame = cv2.rectangle(frame, (s_up_roi_x1, s_up_roi_y1), (s_up_roi_x2, s_up_roi_y2), (0, 255, 0), 3)
            s_right_roi = frame[s_right_roi_y1: s_right_roi_y2, s_right_roi_x1: s_right_roi_x2]
            s_right_median_value = np.median(s_right_roi)
    #        print('s_right: ',s_right_median_value)
    #        frame = cv2.rectangle(frame, (s_right_roi_x1, s_right_roi_y1), (s_right_roi_x2, s_right_roi_y2), (0, 255, 0), 3)
            s_left_roi = frame[s_left_roi_y1: s_left_roi_y2, s_left_roi_x1: s_left_roi_x2]
            s_left_median_value = np.median(s_left_roi)
    #        print('s_left: ',s_left_median_value)
    #        frame = cv2.rectangle(frame, (s_left_roi_x1, s_left_roi_y1), (s_left_roi_x2, s_left_roi_y2), (0, 255, 0), 3)

            if median_value < 50 or (95 < median_value and median_value < 145):
                area_threshold = 100
            else:
                area_threshold = 60
                object_detector.setHistory(30)
        
            # 1. Object Detection
            mask = object_detector.apply(roi)
            _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            detections = []
            for cnt in contours:
                # Calculate area and remove small elements
                area = cv2.contourArea(cnt)
                if area > area_threshold:
                    #cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
                    x, y, w, h = cv2.boundingRect(cnt)
        
                    detections.append([x, y, w, h])
        
            # 2. Object Tracking
            boxes_ids = tracker.update(detections)
        
            for box_id in boxes_ids:
                x, y, w, h, id = box_id
                # cv2.putText(roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                # cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)
                # cv2.circle(roi, (int(x+w/2),int(y+h/2)) , 2 , (255,255,255),6)
        
                for i in range(len(region_all) - 1):
                    dummy = None
                    if i <= (len(region_all) - 2):
                        dummy = motion(region_all[i], region_all[i+1], x, y, w, h, id, region_all_time_a[i], region_all_time_b[i])
                    if dummy is not None:
                        smoke_initial_time[i] = dummy[0]
                        smoke_flag[i] = dummy[1]
                        time_diff_all[i] = dummy[2]
                        x_dis[i] = dummy[3]
                        y_dis[i] = dummy[4]

                for i in range(len(region_all_horizontal_down) - 1):
                    dummy_horizontal_down = None
                    if i <= (len(region_all_horizontal_down) - 2):
                        dummy_horizontal_down = motion(region_all_horizontal_down[i], region_all_horizontal_down[i+1], x, y, w, h, id, region_all_time_a_horizontal_down[i], region_all_time_b_horizontal_down[i])
                    if dummy_horizontal_down is not None:
                        smoke_initial_time_horizontal_down[i] = dummy_horizontal_down[0]
                        smoke_flag_horizontal_down[i] = dummy_horizontal_down[1]
                        time_diff_all_horizontal_down[i] = dummy_horizontal_down[2]
                        x_dis_horizontal_down[i] = dummy_horizontal_down[3]
                        y_dis_horizontal_down[i] = dummy_horizontal_down[4]

                for i in range(len(region_all_horizontal_up) - 1):
                    dummy_horizontal_up = None
                    if i <= (len(region_all_horizontal_up) - 2):
                        dummy_horizontal_up = motion(region_all_horizontal_up[i], region_all_horizontal_up[i+1], x, y, w, h, id, region_all_time_a_horizontal_up[i], region_all_time_b_horizontal_up[i])
                    if dummy_horizontal_up is not None:
                        smoke_initial_time_horizontal_up[i] = dummy_horizontal_up[0]
                        smoke_flag_horizontal_up[i] = dummy_horizontal_up[1]
                        time_diff_all_horizontal_up[i] = dummy_horizontal_up[2]
                        x_dis_horizontal_up[i] = dummy_horizontal_up[3]
                        y_dis_horizontal_up[i] = dummy_horizontal_up[4]

            duration = 3.0

            alarm_per_frame = []
            if count > 100000:
                count = 1
        
            for i in range((len(region_all) - 1)):
                if((time.time() - smoke_initial_time[i] < duration and smoke_flag[i])):
                    if count <= 6:
                        temp_time_diff.append(time_diff_all[i])
                        temp_x_dis.append(x_dis[i])
                        temp_y_dis.append(y_dis[i])
                    else:
                        temp_time_diff.pop(0)
                        temp_time_diff.append(time_diff_all[i])
                        temp_x_dis.pop(0)
                        temp_x_dis.append(x_dis[i])
                        temp_y_dis.pop(0)
                        temp_y_dis.append(y_dis[i])
        
                    #print(count,temp_time_diff,len(set(temp_time_diff)),sep=" ") 
                    if len(set(temp_time_diff)) >= 5 and np.std(temp_x_dis) > 20 and np.std(temp_x_dis) < 240 and np.std(temp_y_dis) > 20:
                        alarm_per_frame.append(1)
        
                    count += 1
        
                if(time.time() - smoke_initial_time[i]) > duration:
                    smoke_flag[i] = False


            alarm_per_frame_horizontal_down = []
            if count_horizontal_down > 100000:
                count_horizontal_down = 1

            for i in range((len(region_all_horizontal_down) - 1)):
                if ((time.time() - smoke_initial_time_horizontal_down[i] < duration and smoke_flag_horizontal_down[i])):
                    #print("time now: ",timestamp,"time diff: ",time_diff_all_horizontal_down[i],sep="  ")
                    if count_horizontal_down <= 6:
                        temp_time_diff_horizontal_down.append(time_diff_all_horizontal_down[i])
                        temp_x_dis_horizontal_down.append(x_dis_horizontal_down[i])
                        temp_y_dis_horizontal_down.append(y_dis_horizontal_down[i])
                    else:
                        temp_time_diff_horizontal_down.pop(0)
                        temp_time_diff_horizontal_down.append(time_diff_all_horizontal_down[i])
                        temp_x_dis_horizontal_down.pop(0)
                        temp_x_dis_horizontal_down.append(x_dis_horizontal_down[i])
                        temp_y_dis_horizontal_down.pop(0)
                        temp_y_dis_horizontal_down.append(y_dis_horizontal_down[i])

                    #print(count_horizontal_down,temp_time_diff_horizontal_down,len(set(temp_time_diff_horizontal_down)),sep=" ")
                    if len(set(temp_time_diff_horizontal_down)) >= 5:
                        alarm_per_frame_horizontal_down.append(1)

                    count_horizontal_down += 1

                if (time.time() - smoke_initial_time_horizontal_down[i]) > duration:
                    smoke_flag_horizontal_down[i] = False


            alarm_per_frame_horizontal_up = []
            if count_horizontal_up > 100000:
                count_horizontal_up = 1

            for i in range((len(region_all_horizontal_up) - 1)):
                if ((time.time() - smoke_initial_time_horizontal_up[i] < duration and smoke_flag_horizontal_up[i])):
                    #print("time now: ",timestamp,"time diff: ",time_diff_all_horizontal_up[i],sep="  ")
                    if count_horizontal_up <= 6:
                        temp_time_diff_horizontal_up.append(time_diff_all_horizontal_up[i])
                        temp_x_dis_horizontal_up.append(x_dis_horizontal_up[i])
                        temp_y_dis_horizontal_up.append(y_dis_horizontal_up[i])
                    else:
                        temp_time_diff_horizontal_up.pop(0)
                        temp_time_diff_horizontal_up.append(time_diff_all_horizontal_up[i])
                        temp_x_dis_horizontal_up.pop(0)
                        temp_x_dis_horizontal_up.append(x_dis_horizontal_up[i])
                        temp_y_dis_horizontal_up.pop(0)
                        temp_y_dis_horizontal_up.append(y_dis_horizontal_up[i])

                    #print(count_horizontal_up,temp_time_diff_horizontal_up,len(set(temp_time_diff_horizontal_up)),sep=" ")
                    if len(set(temp_time_diff_horizontal_up)) >= 5:
                        alarm_per_frame_horizontal_up.append(1)

                    count_horizontal_up += 1

                if (time.time() - smoke_initial_time_horizontal_up[i]) > duration:
                    smoke_flag_horizontal_up[i] = False


            if frame_count > 100000:
                frame_count = 1

            if frame_count <= 400:
                if (len(alarm_per_frame) >= 12 or len(alarm_per_frame_horizontal_down) >= 12 or len(alarm_per_frame_horizontal_up) >= 15) and n_alarm_400_frames.count(0) > 50:
                    n_alarm_400_frames.append(0)
                else:
                    n_alarm_400_frames.append(len(alarm_per_frame) + len(alarm_per_frame_horizontal_down) + len(alarm_per_frame_horizontal_up))
            else:
                n_alarm_400_frames.pop(0)
                if (len(alarm_per_frame) >= 12 or len(alarm_per_frame_horizontal_down) >= 12 or len(alarm_per_frame_horizontal_up) >= 15) and n_alarm_400_frames.count(0) > 300:
                    n_alarm_400_frames.append(0)
                else:
                    n_alarm_400_frames.append(len(alarm_per_frame) + len(alarm_per_frame_horizontal_down) + len(alarm_per_frame_horizontal_up))

            frame_count += 1

            smoke_alarm_special = False
            if (dark_left_median_value < 80 and dark_right_median_value < 80) and (s_left_median_value > 100 or s_up_median_value > 100 or s_right_median_value > 100):
                smoke_alarm_special = True

            smoke_alarm = False
            if sum(n_alarm_400_frames) >= 700 or smoke_alarm_special:
                smoke_alarm = True

            if smoke_alarm:
                cv2.putText(frame,'Kemuri ga arimasu', (150, 650), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 8)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if localtime != timestamp:
                date_hour_minute = str(timestamp[:-3])
                if smoke_alarm:
                    if temp_date_hour_minute == date_hour_minute:
                        count_n_smoke += 1
                    else:
                        count_n_smoke = 0

                temp_date_hour_minute = date_hour_minute
                end_of_min = int(datetime.now().strftime("%S"))

                if end_of_min == 59:
                    if smoke_alarm:
                        cv2.imwrite(output_dir + "/with smoke" + "/" + str(
                            datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")[:-3]) + ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
                    else:
                        cv2.imwrite(output_dir + "/no smoke" + "/" + str(
                            datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")[:-3]) + ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])

            localtime = timestamp


    #        for i in range(len(region_all)):
    #            cv2.polylines(frame, [np.array(region_all[i])], True, (0, 255, 0), 1)
    #            cv2.fillPoly(frame, [np.array(region_all[i])], (0, 255, 0) )
    #            cv2.putText(frame, str(i+1), (488+i*25, 520), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)

    #        for i in range(len(region_all_horizontal_down)):
    #            cv2.polylines(frame, [np.array(region_all_horizontal_down[i])], True, (255, 0, 0), 1)
    #            cv2.putText(frame, str(i + 1), (590, 245 + i * 10), cv2.FONT_HERSHEY_PLAIN, 0.7, (0, 0, 255), 1)

    #        for i in range(len(region_all_horizontal_up)):
    #            cv2.polylines(frame, [np.array(region_all_horizontal_up[i])], True, (255, 0, 0), 1)
    #            cv2.putText(frame, str(i + 1), (590, 305 - i * 4), cv2.FONT_HERSHEY_PLAIN, 0.6, (0, 255, 255), 1)

            frame = cv2.rectangle(frame, (365, 285),(473,400),(0,255,0),2)
        
            #mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
            #cv2.imshow("Mask", mask)
            cv2.imshow("Frame", frame)
        
            out.write(frame)

            global switch
            switch = True
            key = cv2.waitKey(1) # for live stream
            #key = cv2.waitKey(5) #for video fps 30
            #key = cv2.waitKey(20) #for video fps 10
            if key == 27:
                switch = False
                break
            if key == ord('p'):
                cv2.waitKey(-1)

            global index
            close_and_restart_time = time.strftime("%H%M", time.localtime())
            if close_and_restart_time == '2359' and index == 0:
                index = 1
                break
        
        cap.release()
        cv2.destroyAllWindows()
        


        return switch



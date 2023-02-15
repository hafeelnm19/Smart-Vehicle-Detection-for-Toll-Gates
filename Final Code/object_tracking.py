import cv2
import os
from object_detection import ObjectDetection
import math
# Initialize Object Detection
from collections import defaultdict

# Defining a dict
od = ObjectDetection()

FILE_OUTPUT = 'output4.avi'
if os.path.isfile(FILE_OUTPUT):
    os.remove(FILE_OUTPUT)
# fourcc = cv2.VideoWriter_fourcc(*"mp4v")
# out = cv2.VideoWriter("output.mp4", fourcc, 20.0, (640,480))
cap = cv2.VideoCapture("frame13.mp4")
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

out = cv2.VideoWriter(FILE_OUTPUT, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                      10, (frame_width, frame_height))

#def track(cap):
    # Initialize count
object_exists = defaultdict(list)
count = 0
center_points_prev_frame = []
id=[]

tracking_objects = {}
frame={}
track_id = 0
#fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # you can use other codecs as well
#out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))


while True:
    ret, frame = cap.read()
    count += 1
    if not ret:
        break

    # Point current frame
    curr_time=0
    center_points_cur_frame = []

    # Detect objects on frame
    (class_ids, scores, boxes) = od.detect(frame)
    boxes_refine=[]
    for i in range(len(class_ids)):
        if class_ids[i]  in [1,2,3,4,5,6,7]:
            boxes_refine.append(boxes[i])
    for box in boxes_refine:
        (x, y, w, h) = box
        cx = int((x + x + w) / 2)
        cy = int((y + y + h) / 2)
        center_points_cur_frame.append((cx, cy))
        #print("FRAME N°", count, " ", x, y, w, h)

        # cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Only at the beginning we compare previous and current frame
    if count <= 2:
        for pt in center_points_cur_frame:
            for pt2 in center_points_prev_frame:
                distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])

                if distance < 200:
                    tracking_objects[track_id] = pt
                    track_id += 1
    else:

        tracking_objects_copy = tracking_objects.copy()
        center_points_cur_frame_copy = center_points_cur_frame.copy()

        for object_id, pt2 in tracking_objects_copy.items():
            object_exists[object_id].append("False")
            for pt in center_points_cur_frame_copy:
                distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])

                # Update IDs position
                if distance < 200:
                    tracking_objects[object_id] = pt
                    #print(id)
                    object_exists[object_id].append("True")
                    if pt in center_points_cur_frame:
                        center_points_cur_frame.remove(pt)
                    continue

            # Remove IDs lost
            if (len(object_exists[object_id]) >=10) and (
                    object_exists[object_id][-1] == "False" and object_exists[object_id][-2] == "False" and
                    object_exists[object_id][-3] == "False" and object_exists[object_id][-4] == "False" and
                    object_exists[object_id][-5] == "False" and object_exists[object_id][-6]=="False" and object_exists[object_id][-7] and object_exists[object_id][-8]== "False"):
                tracking_objects.pop(object_id)

        # Add new IDs found
        for pt in center_points_cur_frame:
            tracking_objects[track_id] = pt
            track_id += 1

    for object_id, pt in tracking_objects.items():
        cv2.circle(frame, pt, 5, (0, 0, 255), -1)
        cv2.putText(frame, str(object_id), (pt[0], pt[1] - 7), 0, 1, (0, 0, 255), 2)
        #if (350 < pt[0] < 450) and (150 < pt[1] < 250) and (object_id not in id):
        if (590< pt[0] < 950) and (150 < pt[1] < 550)and (object_id not in id):
            id.append(object_id)
            #gray=cv2.cvtColor(frame[y:y + h, x:x + w], cv2.COLOR_BGR2GRAY)
            cv2.imwrite('./data13/frame' + str(object_id) + '.jpg', frame[y:y + h, x:x + w])

    print("Tracking objects")
    print(tracking_objects)
    #print("CUR FRAME LEFT PTS")
    #print(center_points_cur_frame)
    out.write(frame)
    cv2.imshow("Frame", frame)
    #yield frame
    # Make a copy of the points
    center_points_prev_frame = center_points_cur_frame.copy()

    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
out.release()
cv2.destroyAllWindows()
"""if __name__ == "__main__":
    cap = cv2.VideoCapture("exit2.mp4")
    track(cap)
    cap.release()
    cv2.destroyAllWindows()"""

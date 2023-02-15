from time import sleep

from flask import Flask, render_template, Response, stream_with_context, jsonify
import cv2
from object_detection import ObjectDetection
import math
# Initialize Object Detection
from collections import defaultdict

app = Flask(__name__)
od = ObjectDetection()
cap = cv2.VideoCapture("exit2.mp4")


def track(cap):
    global data
    dictt = {}
    # Initialize count
    object_exists = defaultdict(list)
    count = 0
    center_points_prev_frame = []
    id = []

    tracking_objects = {}
    frame = {}
    track_id = 0
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # you can use other codecs as well
    # out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))

    while True:
        ret, frame = cap.read()
        count += 1
        if not ret:
            break

        # Point current frame
        curr_time = 0
        center_points_cur_frame = []

        # Detect objects on frame
        (class_ids, scores, boxes) = od.detect(frame)
        boxes_refine = []
        for i in range(len(class_ids)):
            if class_ids[i] in [1, 2, 3, 4, 5, 6, 7]:
                boxes_refine.append(boxes[i])
        for box in boxes_refine:
            (x, y, w, h) = box
            cx = int((x + x + w) / 2)
            cy = int((y + y + h) / 2)
            center_points_cur_frame.append((cx, cy))
            # print("FRAME N°", count, " ", x, y, w, h)

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
                        # print(id)
                        object_exists[object_id].append("True")
                        if pt in center_points_cur_frame:
                            center_points_cur_frame.remove(pt)
                        continue

                # Remove IDs lost
                if (len(object_exists[object_id]) >= 5) and (
                        object_exists[object_id][-1] == "False" and object_exists[object_id][-2] == "False" and
                        object_exists[object_id][-3] == "False" and object_exists[object_id][-4] == "False" and
                        object_exists[object_id][-5] == "False"):
                    tracking_objects.pop(object_id)

            # Add new IDs found
            for pt in center_points_cur_frame:
                tracking_objects[track_id] = pt
                track_id += 1

        for object_id, pt in tracking_objects.items():
            cv2.circle(frame, pt, 5, (0, 0, 255), -1)
            cv2.putText(frame, str(object_id), (pt[0], pt[1] - 7), 0, 1, (0, 0, 255), 2)
            if (350 < pt[0] < 500) and (100 < pt[1] < 200) and (object_id not in id):
                # if (900 < pt[0] < 950) and (400 < pt[1] < 480) and (object_id not in id):
                id.append(object_id)
                # gray=cv2.cvtColor(frame[y:y + h, x:x + w], cv2.COLOR_BGR2GRAY)
                cv2.imwrite('./data/frame' + str(object_id) + '.jpg', frame[y:y + h, x:x + w])
                dictt["exit"] = object_id
                dictt["entrance"] = 10
                dictt["result"] = "Matched"
                data.append(dictt)

        print("Tracking objects")
        print(tracking_objects)
        # return tracking_objects
        print("CUR FRAME LEFT PTS")
        print(center_points_cur_frame)
        # out.write(frame)
        cv2.imshow("Frame", frame)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        # Make a copy of the points
        center_points_prev_frame = center_points_cur_frame.copy()

        key = cv2.waitKey(1)
        if key == 27:
            break
    # out.release()

def var():
    new = [{"exit": -1, "entrance": -1, "result": "Matched"},]
    global data

    if data[-1] != new[-1]:
        new.append(data[-1])

    yield f"{new[-1]}"



data = [
    {"exit": 0, "entrance": 10, "result": "Matched"},
{"exit": 0, "entrance": 10, "result": "Matched"},
{"exit": 0, "entrance": 10, "result": "Matched"},
{"exit": 0, "entrance": 10, "result": "Matched"}
]


@app.route('/')
def home():  # put application's code here
    global cap
    global data
    # frame=track(cap)

    # global data
    return render_template('home.html')


@app.route('/video')
def video():
    global cap
    # global data
    # x=track(cap)
    # data.append(x)
    return Response(track(cap), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/dataa')
def dataa():
    return Response(stream_with_context(var()), mimetype='text')


if __name__ == '__main__':
    app.run(debug=True)

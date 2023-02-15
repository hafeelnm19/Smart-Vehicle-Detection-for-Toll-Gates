import os
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import Model
import numpy as np
import cv2
from collections import defaultdict
import math
from object_detection import ObjectDetection

model = VGG16()
# restructure the model
model = Model(inputs=model.inputs, outputs=model.layers[-2].output)

features = {}
# directory = '/content/download.jpg'
# for image in os.listdir(directory):
# directory = "/content/drive/MyDrive/Images"
directory = "./data"
for images in os.listdir(directory):
    image_path = directory + "/" + str(images)

    img = load_img(image_path, target_size=(224, 224))
    # cv2_imshow(immm)
    # convert pixel to numpy array
    img = img_to_array(img)
    # reshape the image for the model
    img = img.reshape((1, img.shape[0], img.shape[1], img.shape[2]))
    # preprocess the image
    img = preprocess_input(img)
    # extract features
    feature = model.predict(img, verbose=0)
    # store feature
    features[image_path] = feature
    if len(features) == 50:
        break

print(features)

od = ObjectDetection()
cap = cv2.VideoCapture("exit2.mp4")
# Initialize count
object_exists = defaultdict(list)
count = 0
center_points_prev_frame = []
id=[]

tracking_objects = {}
frame={}
track_id = 0


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
            if (len(object_exists[object_id]) >= 5) and (
                    object_exists[object_id][-1] == "False" and object_exists[object_id][-2] == "False" and
                    object_exists[object_id][-3] == "False" and object_exists[object_id][-4] == "False" and
                    object_exists[object_id][-5] == "False"):
                tracking_objects.pop(object_id)

        # Add new IDs found
        for pt in center_points_cur_frame:
            tracking_objects[track_id] = pt
            track_id += 1
    distance={}
    for object_id, pt in tracking_objects.items():
        cv2.circle(frame, pt, 5, (0, 0, 255), -1)
        cv2.putText(frame, str(object_id), (pt[0], pt[1] - 7), 0, 1, (0, 0, 255), 2)
        if (350 < pt[0] < 400) and (150 < pt[1] < 200) and (object_id not in id):
        #if (900 < pt[0] < 950) and (400 < pt[1] < 480) and (object_id not in id):
            id.append(object_id)
            #gray=cv2.cvtColor(frame[y:y + h, x:x + w], cv2.COLOR_BGR2GRAY)
            img2=frame[y:y + h, x:x + w]
            path='/content/drive/MyDrive/data2' + str(object_id) + '.jpg'
            #cv2.imwrite('/content/drive/MyDrive/data2' + str(object_id) + '.jpg', frame[y:y + h, x:x + w])
            img2 = load_img(path, target_size=(224, 224))
            print(img2)
            img2 = img_to_array(img2)
            img2 = img2.reshape((1, img2.shape[0], img2.shape[1], img2.shape[2]))
            img2 = preprocess_input(img2)
            feature2 = model.predict(img2, verbose=0)
            for img1 in features:
              d=np.linalg.norm(np.array(features[img1])-np.array(feature2))
              print(img1)
              print(d)
              distance[img1]=d
            print(distance)
    center_points_prev_frame = center_points_cur_frame.copy()





    print("Tracking objects")
    print(tracking_objects)
    print("CUR FRAME LEFT PTS")
    print(center_points_cur_frame)
    #cv2.imshow("Frame", frame)

    # Make a copy of the points
    # center_points_prev_frame = center_points_cur_frame.copy()

    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
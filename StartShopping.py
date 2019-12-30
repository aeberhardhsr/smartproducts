# Written by: Andreas Eberhard
# Find motioned frames (movement detection) and detect it (object detection), analyze results (predictions) and store it to database
# Last Updated: 27.12.2019
# PART 1 is based on intel detection algorithmus, found here:
# https://software.intel.com/en-us/node/754940


import os
import sys
import time
import shutil
import glob
import time
import csv
import argparse
import webbrowser
import subprocess
import numpy as np
from cv2 import cv2
import pymysql
from tkinter import messagebox
from tkinter import Tk
from operator import itemgetter



########## Begin of Functions ##########

## Part 1 ##
def open_folder():
    #open systems file browser to view images folder
    cwd = os.getcwd()
    webbrowser.open(cwd)

def distMap(frame1, frame2):
    #outputs pythagorean distance between two frames
    frame1_32 = np.float32(frame1)
    frame2_32 = np.float32(frame2)
    diff32 = frame1_32 - frame2_32

    norm32 = np.sqrt(diff32[:, :, 0]**2 + diff32[:, :, 1]**2 + diff32[:, :, 2]
                     **2)/np.sqrt(255**2 + 255**2 + 255**2)

    dist = np.uint8(norm32*255)
    return dist

def print_date_time():
    #Updates current date and time and keys info on to video
    current_time = time.asctime()

    cv2.putText(frame2, str(current_time), (280, 24),
                font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

## Part 2 ##
class Output:

    def __init__(self, classes):
        self.colors = np.random.uniform(0, 255, size=(len(classes), 3))
        self.classes = classes

    def draw_prediction(self, image, class_id, confidence, x1, y1, x2, y2):
        image_height, image_width, _ = image.shape
        fontSize = round(image_height / 1024)
        label = (str(self.classes[class_id]) + " " + str(round(confidence * 100)) + "%").upper()
        color = self.colors[class_id]
        x1 = max(x1, 0)
        y1 = max(y1, 0)
        cv2.rectangle(image, (x1, y1), (x2, y2), color, fontSize)
        (textWidth, textHeight), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, fontSize, fontSize)
        if y1 - textHeight <= 0:
            y1 = y1 + textHeight
            cv2.rectangle(image, (x1, y1), (x1 + textWidth, y1 - textHeight), color, -1)
            cv2.putText(image, label, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, fontSize, (0, 0, 0), fontSize)
        else:
            cv2.rectangle(image, (x1, y1), (x1 + textWidth, y1 - textHeight), color, -1)
            cv2.putText(image, label, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, fontSize, (0, 0, 0), fontSize)

class YoloObjectDetector:

    def __init__(self, modelSize):
        if modelSize == "tiny":
            self.modelSize = 416
            #set the paths to the YoloV3-Tiny files
            self.model = cv2.dnn.readNet(tiny_weights_folder, tiny_cfg_folder)
        
            
        else:
            self.modelSize = int(modelSize)
            self.model = cv2.dnn.readNet(yolo_weights_folder, yolo_cfg_folder)
        
        #open the .txt file with all the label names
        with open(label_folder, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]

        self.output = Output(self.classes)
        #scale is 0.00392 for YOLO as it does not use 0..255 but 0..1 as range (0.00392 = 1/255)
        self.scale = 0.00392

    def processImage(self, image):
        if image is None:
            print("Ignoring image")
            return

        image_height, image_width, _ = image.shape
        blob = cv2.dnn.blobFromImage(image, self.scale, (self.modelSize, self.modelSize), (0, 0, 0), True, crop=False)
        self.model.setInput(blob)
        retval = self.model.forward(self.get_output_layers(self.model))
        class_ids = []
        confidences = []
        boxes = []
        conf_threshold = 0.5
        nms_threshold = 0.4

        for out in retval:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > conf_threshold:
                    center_x = int(detection[0] * image_width)
                    center_y = int(detection[1] * image_height)
                    w = int(detection[2] * image_width)
                    h = int(detection[3] * image_height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])
        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

        if len(indices) == 0:
            return

        for i in indices:
            i = i[0]
            box = boxes[i]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            #draw the rectangle with id and prediction value on the image
            self.output.draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))
            #open the result.txt file and write the id and prediction value
            f = open(res_dec_folder, "a+")
            f.write("%d %f\n" % (class_ids[i], confidences[i]))
            f.close
        return image


    def get_output_layers(self, net):
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        return output_layers

########## End of Functions ##########

################################## PART 0, Working Directories and Paths ##################################
#File directory for labels (prediction name)
label_folder = (r"C:\Users\Andy\Desktop\SP_Software_V1.0\NeuralNetwork\yolov3.txt")

#Folder for the Yolov3-TINY .weights file
tiny_weights_folder = (r"C:\Users\Andy\Desktop\SP_Software_V1.0\NeuralNetwork\yolov3-tiny.weights")

#Folder for the Yolov3-TINY .cfg file
tiny_cfg_folder = (r"C:\Users\Andy\Desktop\SP_Software_V1.0\NeuralNetwork\yolov3-tiny.cfg")

#Folder for Yolo .weights file
yolo_weights_folder = (r"C:\Users\Andy\Desktop\SmartShoppingCart_Software\objectDetection\models\yolo\yolov3.weights")

#Folder for Yolo .cfg file
yolo_cfg_folder = (r"C:\Users\Andy\Desktop\SmartShoppingCart_Software\objectDetection\models\yolo\yolov3.cfg")

#Folder for saving frames from the MovementDetector
mov_dec_folder = (r"C:\Users\Andy\Desktop\SP_Software_V1.0\MovementDetection")

#Folder for predicted frames. Frames come from MovementDetector
pro_dec_folder = (r"C:\Users\Andy\Desktop\SP_Software_V1.0\ProductDetection")

#Folder for the results from the predicted frames. Results come from the ProductDetector
res_dec_folder = (r"C:\Users\Andy\Desktop\SP_Software_V1.0\result.txt")


################################## PART 1, MOTION DETECTOR ################################## 
##### Settings for the Movement Detector
root = Tk()
motion_detect = 1
md_switch = 'ON'

#Check if folder already exists
check_folder = os.path.isdir(mov_dec_folder)

#If folder doesn't exist, then create it.
if not check_folder:
    os.makedirs(mov_dec_folder)

#Make that folder current dir.
os.chdir(mov_dec_folder)

#Change sdthresh (sensitivty) to suit camera and conditions,
#10-15 is usually within the threshold range.
sdThresh = 25

#Used to count individualy named frames as jpgs.
img_index = 0

#Use this cv2 font.
font = cv2.FONT_HERSHEY_SIMPLEX

#Capture video stream.
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
_, frame1 = cap.read()
_, frame2 = cap.read()

##### Main Code for the Movement Detector
while img_index < 15:

    # Report error if camera not found.
    try:
        _, frame3 = cap.read()
        rows, cols, _ = np.shape(frame3)
        dist = distMap(frame1, frame3)
    except:
        print('Camera not found.')
        exit(0)
    frame1 = frame2
    frame2 = frame3
    keyPress = cv2.waitKey(20)

    # Apply Gaussian smoothing.
    mod = cv2.GaussianBlur(dist, (9, 9), 0)

    # Apply thresholding.
    _, thresh = cv2.threshold(mod, 100, 255, 0)

    # Calculate st dev test.
    _, stDev = cv2.meanStdDev(mod)

    # If motion is dectected.
    if stDev > sdThresh:
        
        # Motion is detected.
        cv2.putText(frame2, 'MD-Frame '+str(img_index),
                    (0, 20), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        

        # Save a timestamped jpg if motion detected.
        if motion_detect == 1:
            frame_name = (str(img_index)+str('.jpg'))
            cv2.imwrite(frame_name, frame2)
            img_index += 1

    print_date_time()
    cv2.imshow('Live video', frame2)

# Close down the Movement Detector
cap.release()
cv2.destroyAllWindows()

################################## PART 2, IMAGE DETECTOR ################################## 

#delete result.txt to avoid false prediction value in database
if os.path.exists(res_dec_folder):
    os.remove(res_dec_folder)
else:
    print("The file 'result.txt' does not exist, but will be created")

##### Settings for the Image Detector #####
#To use the YoloV3-Tiny 
modelSize = "tiny"

#Apply the Settings and load the neural Network
detector = YoloObjectDetector(modelSize)

#The Software should recreate the folder every time to prevent massive storage usage
if os.path.exists(pro_dec_folder):
    shutil.rmtree(pro_dec_folder)

#Create the storage folder for predicted images
os.mkdir(pro_dec_folder)
files = glob.glob(mov_dec_folder + "/**/*.jpg", recursive=True) #Load all Images from Movement Detector
numberFiles = len(files)
for idx, filename in enumerate(files):
    if os.path.isfile(filename):  #filter dirs
        image = cv2.imread(filename) #Load the image into OpenCV 
        image = detector.processImage(image) #Process the image through the neural Network
        if image is not None:
            output = os.path.join(pro_dec_folder, os.path.basename(filename)) #If the image is successfully processed, save it to the Folder
            cv2.imwrite(output, image)


################################## PART 3, ANALYZE PREDICTIONS AND PROBABILITIES ##################################

#If products were detected on the images go ahead. If not, the program will exit at this point.
if os.listdir(pro_dec_folder) == []:
    print("No products were detected on the images. The script will exit. Please start again to detect your products.")
    exit(0)
else:
    print("Products were detected.")

#Empty List to store all the prediction Indexes from the images
problist = []

#Open and read the result.txt file with all the predictions inside
reader = csv.reader(open(res_dec_folder, encoding='utf-8'), delimiter=" ") #Replace the encoding if the OS is Mac or Linux




#Sort the lines by the second column (predicted values)
for line in sorted(reader, key=itemgetter(1), reverse=False):
    problist.extend(line) #extend the list with a value

#find the Product ID with the max prediction value
max_tuple = line

#strip the prediction Value and use only the product ID for further processing
predicted_id = line[0][:2]

################################## PART 4, WRITE PREDICTIONS INTO DATABASE ##################################
conn = pymysql.connect('localhost', 'spuser', 'spuser', 'smartproducts')
 
with conn:
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO records (p_id) VALUES (%s)""", (predicted_id))
    conn.commit()
    cursor.close()

print("Productinformation is stored in the Database. Go to the website and watch them.")


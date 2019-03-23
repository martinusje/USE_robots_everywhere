import cv2
import numpy as np
import serial, time

arduino = serial.Serial('COM3', 9600, timeout=.1)
time.sleep(1) #give the connection a second to settle

framewidth = 720
frameheight = 600

def get_output_layers(net):
    
    layer_names = net.getLayerNames()
    
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers

def __draw_label(img, scale, text, pos, bg_color):
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    color = (0, 0, 0)
    thickness = cv2.FILLED
    margin = 2

    txt_size = cv2.getTextSize(text, font_face, scale, thickness)

    end_x = pos[0] + txt_size[0][0] + margin
    end_y = pos[1] - txt_size[0][1] - margin

    cv2.rectangle(img, pos, (end_x, end_y), bg_color, thickness)
    cv2.putText(img, text, pos, font_face, scale, color, 1, cv2.LINE_AA)

def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):

    label = str(classes[class_id])

    if(label == 'banana'):
        #Banana detected
        print(label + " detected")
        # draw the label in the frame
        threshold = 0.15
        if(x_plus_w > (framewidth*(1-threshold))):
            __draw_label(img, 1, '>>>', (framewidth - 40,frameheight/2), (255,0,0))
            arduino.write("right")
        if(x < (framewidth*threshold)):
            __draw_label(img, 1, '<<<', (40,frameheight/2), (255,0,0))
            arduino.write("left")
        if(y_plus_h > (frameheight*(1-threshold))):
            __draw_label(img, 1, 'Down', (framewidth/2,frameheight - 40), (255,0,0))
        if(y < (frameheight*threshold)):
            __draw_label(img, 1, 'UP', (framewidth/2,40), (255,0,0))

    color = COLORS[class_id]

    cv2.rectangle(img, (int(x), int(y)), (int(x_plus_w),int(y_plus_h)), color, 2)

    cv2.putText(img, label, (np.round(x-10).astype("int"),np.round(y-10).astype("int")), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (11,255,255), 2, cv2.LINE_AA)

winName = 'Deep learning object detection in OpenCV'
cv2.namedWindow(winName, cv2.WINDOW_NORMAL)

# get external camera attached to usb
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0) # turn the autofocus off
cap.set(3, framewidth) # set the Horizontal resolution
cap.set(4, frameheight) # Set the Vertical resolution

net = cv2.dnn.readNet('yolov3_320.weights', 'yolov3.cfg')
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

while 1:
    hasFrame, image = cap.read()

    if image is not None:
        #Flip image for rotated camera
        image = cv2.flip(image, -1)

        Width = image.shape[1]
        Height = image.shape[0]
        scale = 0.00392

        classes = None

        with open('classes.names', 'r') as f:
            classes = [line.strip() for line in f.readlines()]

        COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

        blob = cv2.dnn.blobFromImage(image, scale, (320,320), (0,0,0), True, crop=False)

        net.setInput(blob)

        outs = net.forward(get_output_layers(net))

        class_ids = []
        confidences = []
        boxes = []
        conf_threshold = 0.5
        nms_threshold = 0.4

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * Width)
                    center_y = int(detection[1] * Height)
                    w = int(detection[2] * Width)
                    h = int(detection[3] * Height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

        for i in indices:
            i = i[0]
            box = boxes[i]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))

        cv2.imshow(winName, image)
    else:
        print("Camera stream not loaded properly")

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

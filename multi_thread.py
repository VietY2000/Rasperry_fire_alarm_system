import threading
import cv2
from my_yolov6 import my_yolov6

yolov6_model = my_yolov6("runs/train/exp/weights/yolov6n_ckpt.pt","0","data/Train_val_yolov6.yaml", 640, False)

def playcamera(cam,cam_name):
    cap = cv2.VideoCapture(cam)
    while True:
        success, frame = cap.read()
        frame = cv2.resize(frame, (640,480))
        frame, det = yolov6_model.infer(frame, conf_thres=0.6, iou_thres=0.45)
        cv2.imshow('{}'.format(cam_name),frame)

        if cv2.waitKey(1) & 0xFF == ord('e'):
            break
    cap.release()
    cv2.destroyAllWIndows()

t1 = threading.Thread(target=playcamera, args = (0,"camera1"))
t1.start()
t2 = threading.Thread(target=playcamera,args = (1,"camera2"))
t2.start()

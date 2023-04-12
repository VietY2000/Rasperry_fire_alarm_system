# khai báo các thư viện
from my_yolov6 import my_yolov6
import cv2
from twilio.rest import Client
import playsound
import serial
from gmail import email

# Load model đã train
yolov6_model = my_yolov6("/home/pi/Desktop/PROJECT/YOLOv6/runs/train/exp/weights/fire_smoke.pt", "0" \
                         , "/home/pi/Desktop/PROJECT/YOLOv6/data/Train_val_yolov6.yaml", 640, False)
# Client của Twilio
client = Client("AC623056caa8d2a05393987afe310*****", "0bc11d0bc0fe08bd62fab6f7549*****")

# Turn on serial gate
ser = serial.Serial('/dev/ttyS0', 9600)
# Turn off ECHO
ser.write('ATE0\r\n'.encode())

# Read video from camera
cap = cv2.VideoCapture(0)

# condition don't spam message
mes = 0
frame_count = 0

while True:
    success, frame = cap.read()
    frame = cv2.resize(frame, (1080, 720))
    frame, det = yolov6_model.infer(frame, conf_thres=0.65, iou_thres=0.45)

    if det != 0:
        if frame_count == 0 or frame_count == 16:
            playsound.playsound('/home/pi/Desktop/PROJECT/project.mp3', True)
            frame_count = 1

            if mes == 0:
                # funcition send message and make a telephone
                message = client.messages.create(body="phát hiện cháy", from_="Twilio_number",
                                                 to="Your_number")
                ser.write('ATD0398972640;\r\n'.encode())
                cv2.imwrite('fire_img.jpg', frame)
                email.send_mail("/home/pi/Desktop/PROJECT/YOLOv6/fire_img.jpg", "receive_email")
                mes = 1

        frame_count = frame_count + 1
    if det == 0:
        mes = 0
        frame_count = 0

    # hiển thị từng frame
    cv2.imshow('frame', frame)

    # khi bấm phím e sẽ dừng vòng lặp và chương trình sẽ dừng
    if cv2.waitKey(1) & 0xFF == ord('e'):
        break

# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()



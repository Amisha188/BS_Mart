import cv2
detector=cv2.QRCodeDetector()
reval,point,s_qr=detector.detectAndDecode(cv2.imread('first.png'))
print(reval)

# [10:40 AM, 3/10/2022] Diya: pip3 install opencv-python
# [10:41 AM, 3/10/2022] Diya: pip install qrcode
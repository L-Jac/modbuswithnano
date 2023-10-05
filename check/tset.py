import cv2
import numpy as np

# 初始化视频流
cap = cv2.VideoCapture(0)

# 初始化帧
_, frame = cap.read()
old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

while True:
    # 读取新的帧
    _, frame = cap.read()
    new_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 计算帧差异
    frame_diff = cv2.absdiff(old_gray, new_gray)

    # 应用阈值来获得二值图像，以便我们可以找到轮廓
    threshold = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)[1]
    threshold = cv2.dilate(threshold, None, iterations=2)

    # 找到轮廓
    contours, _ = cv2.findContours(
        threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    for contour in contours:
        if cv2.contourArea(contour) > 500:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # 显示结果
    cv2.imshow("Motion Detection", frame)

    old_gray = new_gray

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

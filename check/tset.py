import cv2
from loguru import logger
import keyboard
import time

# 定义blur、erode和dilate运算的核的大小
BLUR_RADIUS = 21
erode_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
dilate_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
some = 25
area = []

cap = cv2.VideoCapture(1)
# 设置分辨率为 640x480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

_, frame = cap.read()
gray_background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# 对其进行高斯模糊
gray_background = cv2.GaussianBlur(gray_background,
                                   (BLUR_RADIUS, BLUR_RADIUS), 0)

success, frame = cap.read()
while success:
    # 对每一帧的都进行灰度转换和高斯模糊
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame,
                                  (BLUR_RADIUS, BLUR_RADIUS), 0)

    # 分离出运动目标，也就是前景
    # 比较背景帧和当前帧
    diff = cv2.absdiff(gray_background, gray_frame)
    # 阈值化处理
    _, thresh = cv2.threshold(diff, some, 255, cv2.THRESH_BINARY)
    # cv2.erode 和 cv2.dilate 函数对二值图像进行形态学处理，以去除噪声并填补空洞。
    # 使用cv2.erode和cv2.dilate函数对二值图像进行腐蚀和膨胀操作
    # 第三个参数是输出图像，第四个参数是迭代次数
    # 腐蚀操作可以去除小的白色噪点，而膨胀操作可以填补小的黑色空洞
    cv2.erode(thresh, erode_kernel, thresh, iterations=2)
    cv2.dilate(thresh, dilate_kernel, thresh, iterations=2)

    # 使用cv2.findContours 函数来在二值图像 thresh 中查找轮廓。
    # cv2.RETR_EXTERNAL 参数表示只检测最外层的轮廓
    # cv2.CHAIN_APPROX_SIMPLE 参数表示使用简单的轮廓近似方法来压缩水平、垂直和对角方向的轮廓。
    contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                      cv2.CHAIN_APPROX_SIMPLE)
    # contours 是一个列表，其中包含了图像中所有轮廓的坐标点。
    # hier 是一个数组，其中包含了轮廓之间的层次关系信息。

    for c in contours:
        # cv2.contourArea 函数计算每个轮廓的面积
        if 15000 > cv2.contourArea(c) > 0:
            a = cv2.contourArea(c)
            # cv2.boundingRect 函数计算该轮廓的外接矩形
            x, y, w, h = cv2.boundingRect(c)
            # 画矩形
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
            area.append(a)
    if len(area) > 0:
        logger.info(f"areas: {area}")
        area.clear()
    # diff 窗口显示的是当前帧与背景帧之间的差异图像
    cv2.imshow('diff', diff)
    # thresh 窗口显示的是经过阈值化处理后的二值图像
    # 白色的部分表示前景，黑色的部分表示背景。
    cv2.imshow('thresh', thresh)
    cv2.imshow('detection', frame)

    _ = cv2.waitKey(1)

    if keyboard.is_pressed('a'):
        time.sleep(0.5)
        some += 1
        logger.info(f"low: {some}")
    elif keyboard.is_pressed('d'):
        time.sleep(0.5)
        some -= 1
        logger.info(f"high: {some}")
    elif keyboard.is_pressed('r'):
        time.sleep(0.5)
        _, frame = cap.read()
        gray_background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 对其进行高斯模糊
        gray_background = cv2.GaussianBlur(gray_background,
                                           (BLUR_RADIUS, BLUR_RADIUS), 0)
        logger.info("reset")
    elif keyboard.is_pressed('q'):
        time.sleep(0.5)  # Escape
        break

    success, frame = cap.read()

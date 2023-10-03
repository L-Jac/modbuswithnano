import cv2
import numpy as np
import math
import time
import RPi.GPIO as GPIO
import os
import csv

OPENCV_MAJOR_VERSION = int(cv2.__version__.split('.')[0])


class Hog_descriptor():

    def __init__(self, img, cell_size=16, bin_size=8):
        self.img = img
        self.img = np.sqrt(img / np.max(img))
        self.img = img * 255
        self.cell_size = cell_size
        self.bin_size = bin_size
        self.angle_unit = 360 / self.bin_size

    def extract(self):

        height, width = self.img.shape

        gradient_magnitude, gradient_angle = self.global_gradient()
        gradient_magnitude = abs(gradient_magnitude)

        cell_gradient_vector = np.zeros((int(height / self.cell_size), int(width / self.cell_size), self.bin_size))
        height_cell, width_cell, _ = np.shape(cell_gradient_vector)

        for i in range(height_cell):
            for j in range(width_cell):
                cell_magnitude = gradient_magnitude[i * self.cell_size:(i + 1) * self.cell_size,
                                 j * self.cell_size:(j + 1) * self.cell_size]

                cell_angle = gradient_angle[i * self.cell_size:(i + 1) * self.cell_size,
                             j * self.cell_size:(j + 1) * self.cell_size]

                cell_gradient_vector[i][j] = self.cell_gradient(cell_magnitude, cell_angle)

        hog_image = self.render_gradient(np.zeros([height, width]), cell_gradient_vector)
        hog_vector = []

        for i in range(height_cell - 1):
            for j in range(width_cell - 1):
                block_vector = []
                block_vector.extend(cell_gradient_vector[i][j])
                block_vector.extend(cell_gradient_vector[i][j + 1])
                block_vector.extend(cell_gradient_vector[i + 1][j])
                block_vector.extend(cell_gradient_vector[i + 1][j + 1])
                mag = lambda vector: math.sqrt(sum(i ** 2 for i in vector))
                magnitude = mag(block_vector)
                if magnitude != 0:
                    normalize = lambda block_vector, magnitude: [element / magnitude for element in block_vector]
                    block_vector = normalize(block_vector, magnitude)
                hog_vector.append(block_vector)
        return hog_vector, hog_image

    def global_gradient(self):
        gradient_values_x = cv2.Sobel(self.img, cv2.CV_64F, 1, 0, ksize=5)
        gradient_values_y = cv2.Sobel(self.img, cv2.CV_64F, 0, 1, ksize=5)
        gradient_magnitude = cv2.addWeighted(gradient_values_x, 0.5, gradient_values_y, 0.5, 0)
        gradient_angle = cv2.phase(gradient_values_x, gradient_values_y, angleInDegrees=True)
        return gradient_magnitude, gradient_angle

    def cell_gradient(self, cell_magnitude, cell_angle):
        orientation_centers = [0] * self.bin_size
        for i in range(cell_magnitude.shape[0]):
            for j in range(cell_magnitude.shape[1]):
                gradient_strength = cell_magnitude[i][j]
                gradient_angle = cell_angle[i][j]
                min_angle, max_angle, mod = self.get_closest_bins(gradient_angle)
                orientation_centers[min_angle] += (gradient_strength * (1 - (mod / self.angle_unit)))
                orientation_centers[max_angle] += (gradient_strength * (mod / self.angle_unit))
        return orientation_centers

    def get_closest_bins(self, gradient_angle):
        idx = int(gradient_angle / self.angle_unit)
        mod = gradient_angle % self.angle_unit
        return idx, (idx + 1) % self.bin_size, mod

    def render_gradient(self, image, cell_gradient):
        cell_width = self.cell_size / 2
        max_mag = np.array(cell_gradient).max()
        for x in range(cell_gradient.shape[0]):
            for y in range(cell_gradient.shape[1]):
                cell_grad = cell_gradient[x][y]
                cell_grad /= max_mag
                angle = 0
                angle_gap = self.angle_unit
                for magnitude in cell_grad:
                    angle_radian = math.radians(angle)
                    x1 = int(x * self.cell_size + magnitude * cell_width * math.cos(angle_radian))
                    y1 = int(y * self.cell_size + magnitude * cell_width * math.sin(angle_radian))
                    x2 = int(x * self.cell_size - magnitude * cell_width * math.cos(angle_radian))
                    y2 = int(y * self.cell_size - magnitude * cell_width * math.sin(angle_radian))
                    cv2.line(image, (y1, x1), (y2, x2), int(255 * math.sqrt(magnitude)))
                    angle += angle_gap
        return image


def main():
    judge_person_x = 65
    judge_person_y = 40
    judge_person_w = 90
    judge_person_h = 35

    EXTRACT_FOLDER = 'testOriginalImage'  # 存放帧图片的位置
    index = 1

    cap = cv2.VideoCapture(0)

    PIN_NUM_IN = 12
    PIN_NUM_OUT = 7
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(PIN_NUM_IN, GPIO.IN)
    GPIO.setup(PIN_NUM_OUT, GPIO.OUT)

    GPIO.output(PIN_NUM_OUT, False)

    while True:
        if GPIO.input(PIN_NUM_IN) == 1:
            #  print("person_in")
            success, frame = cap.read()
            moving_object_flag = 0
            difference_hog = 0
            frame_index = 0

            while success:
                if GPIO.input(PIN_NUM_IN) == 0:
                    #  print("person_out")
                    break

                if moving_object_flag == 0:
                    frame = cv2.resize(frame, (160, 120), interpolation=cv2.INTER_LINEAR)

                    judge_person_area = frame[judge_person_y:judge_person_y + judge_person_h,
                                        judge_person_x:judge_person_x + judge_person_w]

                    judge_person_area = cv2.cvtColor(judge_person_area, cv2.COLOR_BGR2GRAY)

                    hog1 = Hog_descriptor(judge_person_area, cell_size=10, bin_size=6)
                    vector1, image1 = hog1.extract()
                    v1 = np.array(vector1)
                    moving_object_flag = 1

                if moving_object_flag == 1:
                    frame = cv2.resize(frame, (160, 120), interpolation=cv2.INTER_LINEAR)

                    cv2.rectangle(frame, (judge_person_x, judge_person_y),
                                  (judge_person_x + judge_person_w, judge_person_y + judge_person_h), (0, 255, 255), 2)
                    judge_person_area = frame[judge_person_y:judge_person_y + judge_person_h,
                                        judge_person_x:judge_person_x + judge_person_w]

                    judge_person_area = cv2.cvtColor(judge_person_area, cv2.COLOR_BGR2GRAY)
                    hog2 = Hog_descriptor(judge_person_area, cell_size=10, bin_size=6)
                    vector2, image2 = hog2.extract()
                    v2 = np.array(vector2)
                    v = [abs(v1[i] - v2[i]) for i in range(len(v1))]
                    difference_hog = sum(map(sum, v))

                if difference_hog > 30:
                    GPIO.output(PIN_NUM_OUT, True)
                    save_path = "{}/{:>03d}.jpg".format(EXTRACT_FOLDER, index)
                    index += 1  # 保存图片数＋1
                    #  cv2.imwrite(save_path,frame)
                    print(index)
                success, frame = cap.read()

        else:
            GPIO.output(PIN_NUM_OUT, False)
        # print("person_out")


if __name__ == "__main__":
    main()

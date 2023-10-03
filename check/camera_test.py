import cv2


def main():
    # 打开摄像头
    cap = cv2.VideoCapture(0)

    while True:
        # 逐帧捕获
        ret, frame = cap.read()

        # 显示结果帧
        cv2.imshow('frame', frame)

        # 如果按下 'q' 键，就退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 完成所有操作后，释放捕获
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

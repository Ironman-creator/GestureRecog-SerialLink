# -*- coding:utf-8 -*-
# 第二部分：Main类相关代码
# 这部分代码定义了一个名为Main的类，用于调用HandDetector类来实现手势识别功能，并在摄像头获取的视频流中实时检测和识别手势，根据识别结果在图像上添加相应的文字标注。

# 类的初始化方法 __init__：
# 创建一个摄像头对象self.camera，并设置摄像头的分辨率为1280x720。

# Gesture_recognition方法：
# 首先创建一个HandDetector类的实例self.detector。
# 然后进入一个无限循环，在每次循环中：
# 通过摄像头读取一帧图像img，并使用self.detector.findHands方法在图像上检测手部并可选择是否绘制检测结果。
# 接着使用self.detector.findPosition方法获取手部地标位置和边界框信息。
# 如果成功获取到手部地标位置（lmList不为空），则进一步获取手部边界框的坐标以及通过self.detector.fingersUp方法获取每根手指的竖起状态。
# 根据手指的竖起状态判断当前的手势，如两根手指竖起（食指和中指）、三根手指竖起等不同情况，并在图像上对应的位置使用cv2.putText方法添加相应的文字标注，如"2_TWO"、"3_THREE"等。
# 最后通过cv2.imshow显示处理后的图像，并根据窗口的可见性以及等待按键事件来决定是否退出循环。如果窗口不可见或者按下了特定按键（这里原本有通过cv2.waitKey(1) & 0xFF == ord("q")判断是否按下q键退出的逻辑，但被注释掉了，现在是根据窗口可见性判断），则退出循环。

import cv2
from HandTrackingModule import HandDetector

class Main:
    def __init__(self):
        self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.camera.set(3, 1280)
        self.camera.set(4, 720)

    def Gesture_recognition(self):
        self.detector = HandDetector()
        while True:
            frame, img = self.camera.read()
            img = self.detector.findHands(img)
            lmList, bbox = self.detector.findPosition(img)

            if lmList:
                x_1, y_1 = bbox["bbox"][0], bbox["bbox"][1]
                x1, x2, x3, x4, x5 = self.detector.fingersUp()

                if (x2 == 1 and x3 == 1) and (x4 == 0 and x5 == 0 and x1 == 0):
                    cv2.putText(img, "2_TWO", (x_1, y_1), cv2.FONT_HERSHEY_PLAIN, 3,
                                (0, 0, 255), 3)
                elif (x2 == 1 and x3 == 1 and x4 == 1) and (x1 == 0 and x5 == 0):
                    cv2.putText(img, "3_THREE", (x_1, y_1), cv2.FONT_HERSHEY_PLAIN, 3,
                                (0, 0, 255), 3)
                elif (x2 == 1 and x3 == 1 and x4 == 1 and x5 == 1) and (x1 == 0):
                    cv2.putText(img, "4_FOUR", (x_1, y_1), cv2.FONT_HERSHEY_PLAIN, 3,
                                (0, 0, 255), 3)
                elif x1 == 1 and x2 == 1 and x3 == 1 and x4 == 1 and x5 == 1:
                    cv2.putText(img, "5_FIVE", (x_1, y_1), cv2.FONT_HERSHEY_PLAIN, 3,
                                (0, 0, 255), 3)
                elif x2 == 1 and (x1 == 0, x3 == 0, x4 == 0, x5 == 0):
                    cv2.putText(img, "1_ONE", (x_1, y_1), cv2.FONT_HERSHEY_PLAIN, 3,
                                (0, 0, 255), 3)
                elif x1 and (x2 == 0, x3 == 0, x4 == 0, x5 == 0):
                    cv2.putText(img, "GOOD!", (x_1, y_1), cv2.FONT_HERSHEY_PLAIN, 3,
                                (0, 0, 255), 3)
            cv2.imshow("camera", img)
            if cv2.getWindowProperty('camera', cv2.WND_PROP_VISIBLE) < 1:
                break
            cv2.waitKey(1)
            # if cv2.waitKey(1) & 0xFF == ord("q"):
            #     break


if __name__ == '__main__':
    Solution = Main()
    Solution.Gesture_recognition()

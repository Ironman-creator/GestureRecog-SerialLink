# -*- coding:utf-8 -*-
# 第一部分：HandDetector类相关代码
# 定义了一个名为HandDetector的类，用于使用mediapipe库来检测和分析手部信息，包括手部位置、手指状态等。

# 类的初始化方法 __init__：
# 接受参数mode（是否为静态模式）、maxHands（要检测的最大手数）、detectionCon（最小检测置信度）和minTrackCon（最小跟踪置信度）。
# 设置类的属性，包括初始化mediapipe的手部识别模型self.hands以及绘图工具self.mpDraw，同时定义了指尖的索引列表self.tipIds，以及用于存储手指状态和手部地标位置的列表self.fingers和self.lmList。

# findHands方法：
# 接受参数img（要检测手部的图像）和draw（是否在图像上绘制检测结果的标志）。
# 首先将输入的图像从BGR模式转换为RGB模式，因为mediapipe库要求输入图像为RGB格式。
# 然后使用初始化的手部识别模型self.hands对转换后的图像进行处理，得到手部地标等检测结果。
# 如果检测到多只手的地标，并且draw为True，则使用绘图工具self.mpDraw在原始图像上绘制出手部的地标连接情况。
# 最后返回处理后的图像（带或不带绘制的图形，取决于draw参数）。

# findPosition方法：
# 接受参数img（要查找手部位置的图像）、handNo（如果检测到多只手时的手部编号）和draw（是否在图像上绘制相关信息的标志）。
# 初始化一些用于存储手部地标位置坐标的列表（xList、yList）以及用于存储手部边界框信息的变量（bbox、bboxInfo）。
# 如果检测到多只手的地标，根据指定的手部编号获取对应的手部地标信息，将地标位置转换为像素坐标并存储在self.lmList列表中，同时更新xList和yList。
# 根据xList和yList中的坐标信息计算出手部的边界框（bbox）以及边界框的中心坐标，并将相关信息整理成字典bboxInfo。
# 如果draw为True，则在原始图像上绘制出表示手部边界框的矩形。
# 最后返回手部地标位置列表self.lmList和手部边界框信息bboxInfo。

# fingersUp方法：
# 用于判断每根手指是否竖起。
# 如果检测到多只手的地标，首先通过handType方法确定手部是左手还是右手。
# 然后针对拇指和其他四根手指分别进行判断：对于拇指，根据手部是左手还是右手，比较拇指指尖与相邻关节的横坐标关系来确定拇指是否竖起；对于其他四根手指，比较指尖与相邻关节的纵坐标关系来判断是否竖起。
# 将每根手指的竖起状态（0 或 1）存储在fingers列表中并返回。

# handType方法：
# 用于判断检测到的手部是左手还是右手。
# 如果检测到多只手的地标，通过比较手部特定地标（索引为 17 和 5）的横坐标关系来确定手部类型，返回"Right"或"Left"。
import cv2
import mediapipe as mp

class HandDetector:
    """
    使用mediapipe库查找手。导出地标像素格式。添加了额外的功能。
    如查找方式，许多手指向上或两个手指之间的距离。而且提供找到的手的边界框信息。
    """
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, minTrackCon = 0.5):
        """
        :param mode: 在静态模式下，对每个图像进行检测
        :param maxHands: 要检测的最大手数
        :param detectionCon: 最小检测置信度
        :param minTrackCon: 最小跟踪置信度
        """
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = False
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon

        # 初始化手部识别模型
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex,
                                        self.detectionCon, self.minTrackCon)
        self.mpDraw = mp.solutions.drawing_utils	# 初始化绘图器
        self.tipIds = [4, 8, 12, 16, 20]			# 指尖列表
        self.fingers = []
        self.lmList = []

    def findHands(self, img, draw=True):
        """
        从图像(BRG)中找到手部。
        :param img: 用于查找手的图像。
        :param draw: 在图像上绘制输出的标志。
        :return: 带或不带图形的图像
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # 将传入的图像由BGR模式转标准的Opencv模式——RGB模式，
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        """
        查找单手的地标并将其放入列表中像素格式。还可以返回手部周围的边界框。
        :param img: 要查找的主图像
        :param handNo: 如果检测到多只手，则为手部id
        :param draw: 在图像上绘制输出的标志。(默认绘制矩形框)
        :return: 像素格式的手部关节位置列表；手部边界框
        """

        xList = []
        yList = []
        bbox = []
        bboxInfo =[]
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                px, py = int(lm.x * w), int(lm.y * h)
                xList.append(px)
                yList.append(py)
                self.lmList.append([px, py])
                if draw:
                    cv2.circle(img, (px, py), 5, (255, 0, 255), cv2.FILLED)
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            boxW, boxH = xmax - xmin, ymax - ymin
            bbox = xmin, ymin, boxW, boxH
            cx, cy = bbox[0] + (bbox[2] // 2), \
                     bbox[1] + (bbox[3] // 2)
            bboxInfo = {"id": id, "bbox": bbox,"center": (cx, cy)}

            if draw:
                cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                              (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                              (0, 255, 0), 2)

        return self.lmList, bboxInfo

    def fingersUp(self):
        """
        查找列表中打开并返回的手指数。会分别考虑左手和右手
        ：return：竖起手指的列表
        """
        if self.results.multi_hand_landmarks:
            myHandType = self.handType()
            fingers = []
            # Thumb
            if myHandType == "Right":
                if self.lmList[self.tipIds[0]][0] > self.lmList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if self.lmList[self.tipIds[0]][0] < self.lmList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            # 4 Fingers
            for id in range(1, 5):
                if self.lmList[self.tipIds[id]][1] < self.lmList[self.tipIds[id] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers

    def handType(self):
        """
        检查传入的手部是左还是右
        ：return: "Right" 或 "Left"
        """
        if self.results.multi_hand_landmarks:
            if self.lmList[17][0] < self.lmList[5][0]:
                return "Right"
            else:
                return "Left"

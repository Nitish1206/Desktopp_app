from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QGridLayout

import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import pyautogui
from preprocessing_utils import  pad_to_size
from scipy import ndimage
import os
from datetime import datetime
import threading

swidth, sheight = pyautogui.size()
seperator = os.sep

global button_name ,first_start
button_name = ""
first_start="True"

drawing = False
global x1, y1, x2, y2, num, h, w, windowRegion
x1, y1, x2, y2, h, w = 0, 0, 0, 0, 0, 0
windowRegion = (0, 0, swidth//2, sheight)
num = 0



class VideoWidget(QtWidgets.QWidget):
    def __init__(self, user_data,maximum_threshold ,parent=None):
        super().__init__(parent)
        self.video_widget_data = {}
        for user_keys in user_data.keys():
            self.create_data_dir(user_data[user_keys][0], user_data[user_keys][1], user_data[user_keys][2], user_data[user_keys][3])

        self.face_detection_widget = FaceDetectionWidget(self.video_widget_data, maximum_threshold)
        self.exit_button_window = False
        self.record_video = RecordVideo()
        image_data_slot = self.face_detection_widget.image_data_slot
        self.record_video.image_data.connect(image_data_slot)
        self.layout = QtWidgets.QVBoxLayout()
        button_layout = QtWidgets.QHBoxLayout()
        self.run_button = QtWidgets.QPushButton('Start')
        self.pause_button = QtWidgets.QPushButton('Pause')
        self.restart_button = QtWidgets.QPushButton('Restart')
        self.exit_button = QtWidgets.QPushButton('Exit')
        self.end_button = QtWidgets.QPushButton('End')
        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.restart_button)
        button_layout.addWidget(self.exit_button)
        button_layout.addWidget(self.end_button)
        self.layout.addLayout(button_layout)


        self.run_button.clicked.connect(lambda: self.button_clicked("start"))
        self.pause_button.clicked.connect(lambda: self.button_clicked("pause"))
        self.restart_button.clicked.connect(lambda: self.button_clicked("restart"))
        self.exit_button.clicked.connect(lambda: self.button_clicked("exit"))
        self.end_button.clicked.connect(lambda: self.button_clicked("END"))

        self.layout.insertWidget(0, self.face_detection_widget)
        self.layout.addWidget(self.record_video.start_recording())
        self.setLayout(self.layout)

    def create_data_dir(self, model, label, accuracy_t, n_images):
        # creating folder to save image
        created_date = str(datetime.now().strftime("%d%m%Y"))
        created_time = str(datetime.now().strftime("%H%M%S"))
        data_dir = "Data"
        isdatadir = os.path.isdir(data_dir)
        if isdatadir == False:
            os.mkdir(data_dir)

        label_dir = data_dir + seperator + label + "_" + str(accuracy_t.text()) + "%" + "_" + created_date + "_" + created_time
        islabeldir = os.path.isdir(label_dir)
        if islabeldir == False:
            os.mkdir(label_dir)

        image_dir = label_dir + seperator + "Image"
        isvideos_dir = os.path.isdir(image_dir)
        if isvideos_dir == False:
            os.mkdir(image_dir)

        videos_dir = label_dir + seperator + "Videos"
        isvideos_dir = os.path.isdir(videos_dir)
        if isvideos_dir == False:
            os.mkdir(videos_dir)

        size = (940, 900)

        video_obj = cv2.VideoWriter(videos_dir + seperator + str(label)+"_"+str(accuracy_t.text())+"%"+created_date+"_"+created_time+".avi",
                                          cv2.VideoWriter_fourcc(*'MJPG'),
                                          10, size)

        self.video_widget_data[label] = [model, label, accuracy_t, n_images, image_dir, video_obj]

    def window_crop(self):

        self.MainWindow = QMainWindow()
        self.ui = UI_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()


    def button_clicked(self, button_mode):
        global first_start

        if first_start == "True" and button_mode =="start":
            self.window_crop()

        else:
            global button_name
            button_name = button_mode

class FaceDetectionWidget(QtWidgets.QWidget):
    def __init__(self, video_widget_data,maximum_threshold, parent=None):
        super().__init__(parent)

        self.input_size = [224, 224, 3]
        self.label_num = 0
        self.is_v_sign = True
        self.sign = ""
        self.data_from_user = video_widget_data
        self.video_write_status = 0
        self.text_pos = (40, 800)
        self.preogress_bar_pos = (40, 840)
        self.victory_status = False
        global button_name
        self.info_status = True
        self.button_modoe1 = button_name
        self.bar_increment_value = 0
        self.intialize_flag = True
        self.data_visualize = {}
        self.counter_check=0
        self.image = QtGui.QImage()
        self._red = (0, 0, 255)
        self._width = 2
        self._min_size = (940, 900)
        self.victory_countr = 0
        self.selection_area = False
        self.maxthreshold=maximum_threshold

    def image_data_slot(self, image_data):

        frame = np.array(image_data)
        ration = float(self.input_size[0]) / max(frame.shape)
        scale = [ration, ration, 1]
        result_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        video_frame = result_frame.copy()
        imageframe = result_frame.copy()

        if self.info_status==True:
            all_classifier = [labelkey for labelkey in self.data_from_user.keys()]
            text_msg = ""
            for labels in all_classifier:
                text_msg += "\n"+str(labels)

            msg = QMessageBox()
            msg.setWindowTitle("selection detail")

            msg.setText("selected classifier:  "+ text_msg)
            z = msg.exec_()
            self.info_status = False

        if button_name == "start":
            self.action_to_perform = "classify_the_object"

        elif button_name == "pause":
            self.action_to_perform = "pause_classification"
        elif button_name == "restart":
            self.action_to_perform = "restart_classification"
        elif button_name == "exit":
            self.action_to_perform = None
            global first_start, windowRegion
            first_start = "True"
            windowRegion = (0, 0, swidth // 2, sheight)

        elif button_name == "END":
            self.action_to_perform=None
            for j,labelkey in enumerate(self.data_from_user.keys()):
                self.data_visualize[labelkey] = [self.data_from_user[labelkey][1] + ": {}".format(0),
                                             self.data_from_user[labelkey][1] + "  Progressbar: " + str(0) + "%",self.label_num]

        else:
            self.action_to_perform = None

        if self.action_to_perform == None:
            result_frame = result_frame.copy()

        if self.action_to_perform == "exit_app":
            for j, labelkey in enumerate(self.data_from_user.keys()):
                self.data_from_user[labelkey][5].release()
            self.action_to_perform=None

        self.counter_check+=1

        if self.action_to_perform == "classify_the_object" or self.action_to_perform == "pause_classification":
            scaled_img = ndimage.zoom(result_frame, scale, order=1)
            padded_image, padding = pad_to_size(scaled_img, self.input_size)
            imagep = np.expand_dims(padded_image, 0)

            for j, labelkey in enumerate(self.data_from_user.keys()):
                if labelkey not in self.data_visualize.keys():
                    self.data_visualize[labelkey] = [self.data_from_user[labelkey][1] + ": {}".format(0),
                                                     self.data_from_user[labelkey][1] + "  Progressbar: " + str(
                                                         0) + "%",
                                                     self.label_num]
                threading.Thread(target=self.predict_, args=(labelkey, imagep, imageframe, result_frame, video_frame, j)). start()


        if self.action_to_perform == "restart_classification":
            self.victory_status = False
            for j,labelkey in enumerate(self.data_from_user.keys()):
                self.data_visualize[labelkey] = [self.data_from_user[labelkey][1] + ": {}".format(0),
                                             self.data_from_user[labelkey][1] + "  Progressbar: " + str(0) + "%",self.label_num]

                y_put = 910 - 70 * (j + 1)
                cv2.putText(result_frame, self.data_visualize[labelkey][0], (30, y_put+35), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 3)
                cv2.putText(result_frame, self.data_visualize[labelkey][1], (30, y_put),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

        self.image = self.get_qimage(result_frame)

        if self.image.size() != self.size():
            self.setFixedSize(self.image.size())

        self.update()

    def predict_(self, labelkey, imagep, imageframe, result_frame, video_frame, j):

        prediction = self.data_from_user[labelkey][0].predict(imagep).squeeze() * 100
        if prediction >= int(self.data_from_user[labelkey][2].text()) and \
                prediction <= self.maxthreshold and \
                self.action_to_perform == "classify_the_object" and \
                int(self.data_from_user[labelkey][3].text()) > self.data_visualize[labelkey][2]:
            self.data_visualize[labelkey][2] = self.data_visualize[labelkey][2] + 1
            text = self.data_from_user[labelkey][1] + ": {}".format(self.data_visualize[labelkey][2])
            bar_increment_value = int(
                (self.data_visualize[labelkey][2] / int(self.data_from_user[labelkey][3].text())) * 100)
            preogress_bar_text = self.data_from_user[labelkey][1] + "  Progressbar: " + str(bar_increment_value) + "%"
            self.data_visualize[labelkey] = [text, preogress_bar_text, self.data_visualize[labelkey][2]]

            cv2.putText(imageframe, str(int(prediction)) + "%", (50, 800), cv2.FONT_HERSHEY_SIMPLEX, 1.25,
                        (0, 255, 0), 5)

            cv2.imwrite(self.data_from_user[labelkey][4] + seperator + str(int(prediction)) + "p" +
                        str(self.data_visualize[labelkey][2]) + ".jpg", imageframe)

        if int(self.data_from_user[labelkey][3].text()) == self.data_visualize[labelkey][2]:
            self.data_visualize[labelkey][2] += 1
            self.victory_countr += 1
            if self.victory_countr == len(self.data_from_user.keys()):
                self.victory_status = True

        y_put = 910 - 70 * (j + 1)

        cv2.putText(result_frame, self.data_visualize[labelkey][0], (30, y_put + 35), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), 3)
        cv2.putText(result_frame, self.data_visualize[labelkey][1], (30, y_put), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 0, 0), 3)

        if self.victory_status == True:
            cv2.putText(result_frame, "V", (400, 700), cv2.FONT_HERSHEY_DUPLEX, 8, (0, 255, 0), 20, cv2.LINE_AA)

        cv2.putText(video_frame, str(int(prediction)) + "%", (50, 800), cv2.FONT_HERSHEY_SIMPLEX, 1.25, (0, 255, 0),
                    5)

        self.video_write_status += 1
        self.data_from_user[labelkey][5].write(video_frame)

    def get_qimage(self, image: np.ndarray):
        height, width, colors = image.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage

        image = QImage(image.data,
                       width,
                       height,
                       bytesPerLine,
                       QImage.Format_RGB888)

        image = image.rgbSwapped()
        return image

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()



class RecordVideo(QtCore.QObject):
    image_data = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, camera_port=0, parent=None):
        super().__init__(parent)
        self.timer = QtCore.QBasicTimer()

    def start_recording(self):
        self.timer.start(0, self)

    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            return
        global first_start
        print(first_start)
        im = pyautogui.screenshot(region=windowRegion)
        frame = np.array(im)
        frame = cv2.resize(frame, (940, 900))
        self.image_data.emit(frame)


class UI_MainWindow(object):
    def setupUi(self, MainWindow):

        self.windw=MainWindow
        MainWindow.setObjectName("MainWindow")
        sizeObject = QtWidgets.QDesktopWidget().screenGeometry(-1)
        H = (sizeObject.height())
        W = (sizeObject.width())

        self.W = W
        self.H = H
        MainWindow.resize(W // 8, H // 10)
        MainWindow.setMinimumSize(QtCore.QSize(W // 5, H // 7))
        MainWindow.setAcceptDrops(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.radioButton1 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton1.setObjectName("radioButton1")
        self.gridLayout.addWidget(self.radioButton1, 2, 0, 1, 1)

        self.radioButton2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton2.setObjectName("radioButton")
        self.gridLayout.addWidget(self.radioButton2, 3, 0, 1, 1)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 23))
        self.pushButton.setIconSize(QtCore.QSize(16, 25))
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 4, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.clicked = False
        self.pushButton.clicked.connect(self.takeSnapNow)
        self.radioButton1.toggled.connect(self.setcustomStatus)
        self.radioButton2.toggled.connect(self.defaultStatus)
        self.th = {}
        self.cap = ""
        self.custom = False
        self.default = False
        self.st = 0
        self.arguments = ''
        self.process = None


    def setcustomStatus(self):
        if self.custom == False:
            self.custom = True
        else:
            self.custom = False

    def defaultStatus(self):
        if self.default == False:
            self.default = True
        else:
            self.default = False


    def draw_rect(self, event, x, y, flags, param):
        global x1, y1, drawing, num, img, img2, x2, y2
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            x1, y1 = x, y
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing == True:
                a, b = x, y
                if a != x & b != y:
                    img = img2.copy()

                    cv2.rectangle(img, (x1, y1), (x, y), (0, 255, 0), 2)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            num += 1
            font = cv2.FONT_HERSHEY_SIMPLEX
            x2 = x
            y2 = y

    def takeSnap(self):
        global x1, y1, drawing, num, img, img2, x2, y2, h, w
        global windowRegion

        if self.custom == True:
            key = ord('a')

            im1 = pyautogui.screenshot()
            im1.save(r"monitor-1.png")

            img = cv2.imread('monitor-1.png')  # reading image
            try:
                os.remove('monitor-1.png')
            except:
                pass
            cv2.putText(img, "Click and select the Region, Press w to confirm selection ", (self.W // 8, self.H // 2),
                        cv2.FONT_HERSHEY_TRIPLEX, 1.3, (20, 255, 0), 2, cv2.LINE_AA)

            img2 = img.copy()
            cv2.namedWindow("main", cv2.WINDOW_NORMAL)
            cv2.setMouseCallback("main", self.draw_rect)
            cv2.setWindowProperty("main", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

            while key != ord('w'):
                cv2.imshow("main", img)
                key = cv2.waitKey(1) & 0xFF
            (h, w) = ((y2 - y1), (x2 - x1))
            if key == ord('w'):
                cv2.destroyAllWindows()


        elif self.default ==True:

            x1, y1, w, h = (0, 0, swidth//2, sheight)
        if w % 2 == 0:
            pass
        else:
            w = w + 1
        if h % 2 == 0:
            pass
        else:
            h = h + 1
        windowRegion = (x1, y1, w, h)
        return x1, y1, w, h

    def takeSnapNow(self):
        x1, y1, w, h = self.takeSnap()
        global windowRegion
        self.window_selection=windowRegion
        self.windw.close()
        global button_name
        button_name = "start"
        global first_start
        first_start = "False"

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Virtuozus Video Recorder"))
        self.radioButton1.setText(_translate("MainWindow", "Custom Screen"))
        self.radioButton2.setText(_translate("MainWindow", "Default Screen"))
        self.pushButton.setText(_translate("MainWindow", "Start Recording"))
        self.pushButton.setShortcut(_translate("MainWindow", "Ctrl+r"))
        self.actionNew.setText(_translate("MainWindow", "New"))

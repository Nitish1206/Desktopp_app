from PyQt5.QtCore import Qt
from main_window import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QGridLayout
import sys
from datetime import datetime
import os
import pyautogui
import pygetwindow as gw
from keras.models import load_model
from efficientnet_model import Swish, swish
from training_metrics import *
import getpass
from second_window import VideoWidget
from PyQt5 import QtCore
import shutil

# ######################  init static values  ##################################################

swidth, sheight = pyautogui.size()
seperator = os.sep
networks_dir = "best_networks"
custom_objects = {'swish': Swish(swish), 'recall_m': recall_m, 'precision_m': precision_m}
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
user_name = getpass.getuser()
#
# #################################################################################################
# ########################### load model ##########################################################
# start = datetime.now()


all_31_model = load_model(
    networks_dir + seperator + "all_31" + seperator + "epoch_056-loss0.176_model.hdf5",
    custom_objects)
long_21_model = load_model(
    networks_dir + seperator + "long_21" + seperator + "epoch_054-loss0.225_model.hdf5",
    custom_objects)
lt_long_23_model = load_model(
    networks_dir + seperator + "lt_long_23" + seperator + "epoch_073-loss0.091_model.hdf5",
    custom_objects)
lt_short_26_model = load_model(
    networks_dir + seperator + "lt_short_26" + seperator + "epoch_062-loss0.002_model.hdf5",
    custom_objects)
rt_long_25_model = load_model(
    networks_dir + seperator + "rt_long_25" + seperator + "epoch_091-loss0.060_model.hdf5",
    custom_objects)
rt_short_27_model = load_model(
    networks_dir + seperator + "rt_short_27" + seperator + "epoch_059-loss0.093_model.hdf5",
    custom_objects)
short_29 = load_model(
    networks_dir + seperator + "short_29" + seperator + "epoch_059-loss0.079_model.hdf5",
    custom_objects)

# t_delta = datetime.now()-start
# minute_diff = t_delta.total_seconds()/60
# print("[!] Number send is blocked!", minute_diff)

# #############################################################################################################
# ############################### Start Zoom APP ##############################################################
#
# # os.startfile("C:\\Users\\" + user_name + "\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe")
# # time.sleep(15)
# #
# # hwnd = gw.getWindowsWithTitle('zoom')
# # if hwnd:
# #     print("got window...")
# #     zoomwindow = gw.getWindowsWithTitle('zoom')[0]
# #     zoomwindow.moveTo(0, 0)
# #     try:
# #         zoomwindow.activate()
# #     except Exception as e:
# #         pass
# #     zoomwindow.resizeTo(int(swidth / 2), int(sheight))
# # else:
# #     print('Window not found!')
# #     exit()
#
# ###################################################################################################
# #####################################  MAIN APP  ###################################################
class MainAPP(QMainWindow):
    def __init__(self):
        super(MainAPP, self).__init__()
        self.main_window = Ui_MainWindow()
        self.main_window.setupUi(self)
        self.setWindowTitle("Classifier")
        self.user_selection = False
        self.user_input_data = {}
        self.trigger_to_second_window = True
        self.max_threshold = 98

        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.main_window.maxthresholdlineedit.textChanged.connect(lambda : self.set_theshold())
        self.main_window.singlecb.stateChanged.connect(lambda : self.set_input(self.main_window.single_acc_lineedit,
                                                                               self.main_window.single_nimage_lineedit))

        #buttons from main window on which we called function on click
        self.main_window.all_cb.stateChanged.connect(lambda: self.get_input(all_31_model, "all_31",
                                                                            self.main_window.all_31_acc_lineedit,
                                                                            self.main_window.all_31_nimage_lineedit))
        #
        self.main_window.long_21cb.stateChanged.connect(lambda: self.get_input(long_21_model, "long_21",
                                                                                  self.main_window.long21_acc_lineedit,
                                                                                  self.main_window.long21_nimage_lineedit))

        self.main_window.long_23cb.stateChanged.connect(lambda: self.get_input(lt_long_23_model, "lt_long_23",
                                                                                self.main_window.lt_long_23_acc_lineedit,
                                                                                self.main_window.lt_long_23_nimage_lineedit))

        self.main_window.long_25cb.stateChanged.connect(lambda: self.get_input(lt_short_26_model, "lt_short_26",
                                                                                self.main_window.rt_long_25_acc_lineedit,
                                                                                self.main_window.rt_long_25_nimage_lineedit))

        self.main_window.short_26cb.stateChanged.connect(lambda: self.get_input(rt_long_25_model, "rt_long_25",
                                                                                self.main_window.lt_short_26_acc_lineedit,
                                                                                self.main_window.lt_short_26_nimage_lineedit))

        self.main_window.short_27cb.stateChanged.connect(lambda: self.get_input(rt_short_27_model, "rt_short_27",
                                                                                self.main_window.rt_short_27_acc_lineedit,
                                                                                self.main_window.rt_short_27_nimage_lineedit))

        self.main_window.short_29cb.stateChanged.connect(lambda: self.get_input(short_29, "short_29",
                                                                                self.main_window.short29_acc_lineedit,
                                                                                self.main_window.short29_nimage_lineedit))
        self.main_window.start_button.clicked.connect(lambda: self.openWindow())
        self.show()
        classifierwindow = gw.getWindowsWithTitle('Classifier')[0]
        try:
            classifierwindow.moveTo(int(swidth / 2), 0)
        except Exception as e:
            pass


    def openWindow(self):

        self.validate_data()

        if self.trigger_to_second_window == True:
            self.close()
            self.window = QMainWindow()
            self.window.setGeometry(QtCore.QRect(940, 30, 900, 950))
            self.window.setWindowTitle("Run window")
            self.ui = VideoWidget(self.user_input_data, self.max_threshold)
            self.window.setCentralWidget(self.ui)
            self.ui.exit_button.clicked.connect(lambda : self.openPrimary(self.window))
            self.window.show()

    def reset_checkbox(self):
        if self.main_window.all_cb.isChecked() : self.main_window.all_cb.setChecked(False)
        if self.main_window.long_21cb.isChecked() : self.main_window.long_21cb.setChecked(False)
        if self.main_window.long_23cb.isChecked() : self.main_window.long_23cb.setChecked(False)
        if self.main_window.long_25cb.isChecked() : self.main_window.long_25cb.setChecked(False)
        if self.main_window.short_26cb.isChecked() : self.main_window.short_26cb.setChecked(False)
        if self.main_window.short_27cb.isChecked() : self.main_window.short_27cb.setChecked(False)
        if self.main_window.short_29cb.isChecked() : self.main_window.short_29cb.setChecked(False)

    def openPrimary(self, window):
        self.reset_checkbox()
        if self.main_window.singlecb.isChecked() : self.main_window.singlecb.setChecked(False)
        self.main_window.maxthresholdlineedit.clear()
        window.close()

        created_date = str(datetime.now().strftime("%d%m%Y"))
        created_time = str(datetime.now().strftime("%H%M%S"))

        data_dir = "TopRatedData"
        isdatadir = os.path.isdir(data_dir)
        if isdatadir == False:
            os.mkdir(data_dir)
        current_run_dir=data_dir+seperator+created_date+"_"+created_time
        iscurrentrundir = os.path.isdir(current_run_dir)
        if iscurrentrundir == False:
            os.mkdir(current_run_dir)

        for key in self.ui.video_widget_data.keys():
            image_data_dir = self.ui.video_widget_data[key][4]
            current_folder_name = image_data_dir.split(seperator)[1]
            sorted_list = sorted(os.listdir(image_data_dir))[:10]
            key_dir = current_run_dir+seperator+current_folder_name
            os.mkdir(key_dir)
            for file in sorted_list:
                shutil.copy(image_data_dir+seperator+file,key_dir)
        try:
            os.system(f'start {os.path.realpath(current_run_dir)}')
        except Exception as e:
            print("got error while dir open..",e)
            pass
        self.show()

    def set_theshold(self):
        if self.main_window.maxthresholdlineedit.text() != "":
            self.max_threshold = int(self.main_window.maxthresholdlineedit.text())
        else:
            self.max_threshold = 98

    def set_input(self,linedit,imgedit):

        if linedit.isEnabled() == False:
            linedit.setEnabled(True)
            imgedit.setEnabled(True)
            self.user_selection = True

        elif linedit.isEnabled() == True:
            linedit.clear()
            imgedit.clear()
            linedit.setEnabled(False)
            imgedit.setEnabled(False)
            self.user_selection = False
            self.reset_checkbox()

    def get_input(self, model, label, linedit, nimagedit):
        if linedit.isEnabled() == True:
            linedit.clear()
            nimagedit.clear()
            if label in self.user_input_data.keys(): del self.user_input_data[label]
            linedit.setEnabled(False)
            nimagedit.setEnabled(False)
        elif linedit.isEnabled() == False:
            linedit.setEnabled(True)
            nimagedit.setEnabled(True)
            if self.user_selection==True:
                nimagedit.setText(self.main_window.single_acc_lineedit.text())
                linedit.setText(self.main_window.single_nimage_lineedit.text())
            self.user_input_data[label] = [model, label, linedit, nimagedit]

    def validate_data(self):
        for keys in self.user_input_data.keys():
            if self.user_input_data[keys][2].text() == "":
                self.trigger_to_second_window = False
                QMessageBox.warning(self, 'Info', "Please enter Accuracy for:  "+ self.user_input_data[keys][1])
            if self.user_input_data[keys][3].text() == "":
                self.trigger_to_second_window = False
                QMessageBox.warning(self, 'Info', "Please enter number of Images for:  "+ self.user_input_data[keys][1])
            elif self.user_input_data[keys][2].text() != "" and self.user_input_data[keys][3].text() != "":
                self.trigger_to_second_window = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    style = """
            QWidget{
                background: #262D37;
            }
            QLabel{

                font-size: 11pt;
                color: #fff;
                border-radius: 0px;
            }

            QLabel#infolabel{
                background: #0577a8;
                font-size: 18pt;
                color: #fff;
                border-radius: 5px;
            }

            QPushButton
            {
                color: white;
                background: #0577a8;
                border: 1px #DADADA solid;
                padding: 5px 10px;
                border-radius: 2px;
                font-weight: bold;
                font-size: 9pt;
                outline: none;
            }
            QPushButton:hover{
                border: 1px #C6C6C6 solid;
                color: #fff;
                background: #0892D0;
            }
            QCheckBox:hover{
                border: 1px #C6C6C6 solid;
                color: #fff;
                background: #0892D0;
            }
            QLineEdit {

                color: #fff;
                border-style: solid;
                border: 2px solid #fff;
                border-radius: 5px;

            }
            QCheckBox#singlecb
            {
                color: white;
                border: 1px #DADADA solid;
                padding: 5px 10px;
                border-radius: 2px;
                font-weight: bold;
                font-size: 9pt;
                outline: none;
            }


            QCheckBox
            {
                color: white;
                background: #0577a8;
                border: 1px #DADADA solid;
                padding: 5px 10px;
                border-radius: 2px;
                font-weight: bold;
                font-size: 9pt;
                outline: none;
            }
    """
    app.setStyleSheet(style)

    screen = app.primaryScreen()
    main_app = MainAPP()
    main_app.setStyleSheet(style)
    app.exec_()

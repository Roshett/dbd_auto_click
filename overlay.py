import sys

from PyQt5 import QtGui, QtCore, uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLabel
from PyQt5.QtCore import QThread, QObject, pyqtSignal as Signal, pyqtSlot as Slot
import time
from cv_handler import CVHandler


class Worker(QObject):
    progress = Signal(int)
    completed = Signal(int)

    @Slot(int)
    def cv_work(self):
        cv_handler = CVHandler(self)

class MainWindow(QMainWindow):
    work_requested = Signal(int)

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
        )
        self.setGeometry(
            QtWidgets.QStyle.alignedRect(
                QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter,
                QtCore.QSize(100, 32),
                QtWidgets.qApp.desktop().availableGeometry()
        ))

        # set background transparent
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.move(0, 0)

        # write text
        self.label = QLabel(self)
        self.label.setText("DBD Auto Clicker")
        self.label.setFont(QtGui.QFont("Arial", 20))
        self.label.setStyleSheet("color:  #00FF00")
        self.label.move(5, 5)

        self.worker = Worker()
        self.worker_thread = QThread()

        self.worker.progress.connect(self.update_fps)

        self.work_requested.connect(self.worker.cv_work)

        # move worker to the worker thread
        self.worker.moveToThread(self.worker_thread)

        # start the thread
        self.worker_thread.start()
        self.work_requested.emit(1)

    def mousePressEvent(self, event):
        QtWidgets.qApp.quit()
    
    # function set text
    def setText(self, text):
        self.label.setText(text)
    
    def update_fps(self, fps):
        self.label.setText(str(fps))
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MainWindow()
    mywindow.show()
    mywindow.setText("60")
    app.exec_()
    print("exit")
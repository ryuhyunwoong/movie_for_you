import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_window = uic.loadUiType('./calculator.ui')[0]
class Exam(QWidget, form_window):           ## 상속해서 다 가지게 된다. # 클래스를 만든 것
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())           ## 윈도우를 계속 유지시켜주는 함수

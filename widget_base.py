############ 위젯 베이스 복붙용 ##############

import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_window = uic.loadUiType('./cat_and_dog.ui')[0] #Qt디자인에서 만든ui 불러오는 코드

class Exam(QWidget, form_window):
## 클래스 작성
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__=='__main__':
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())   #프로그램종료
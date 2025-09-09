from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class CheckBox(QCheckBox):

    def __init__(self, name, text, parent=None):
        super(CheckBox, self).__init__(parent)
        self.setObjectName(name)
        self._parent = parent
        self.setText(text)
        self.setStyleSheet('''
            QCheckBox {
                color: #aaa;
                font-size: 14px;
                font-family: 'Roboto', sans-serif;
                padding: 5px 0 5px 0;
            }
        ''')
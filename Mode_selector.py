from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDialog
from PyQt5.QtCore import Qt

from Confirmation_dialog import ConfirmationDialog

class Mode_selector:
    _modes = ['compare', 'show']
    _currect_mode = None

    def __init__(self, main_window):
        self._main_window = main_window

    def selector_widget(self):
        widget = QWidget()
        widget.setFixedSize(400, 200)

        # compare button
        compare_button = QPushButton("Compare")
        compare_button.clicked.connect(lambda: self.set_mode("compare"))
        compare_button.setFixedSize(400, 50)

        # show button
        show_button = QPushButton("Show")
        show_button.setFixedSize(400, 50)
        show_button.clicked.connect(lambda: self.set_mode("show"))

        # widget layout
        layout = QVBoxLayout(widget)
        layout.addWidget(compare_button, stretch=1, alignment=Qt.AlignCenter)
        layout.addWidget(show_button, stretch=1, alignment=Qt.AlignCenter)
        widget.setLayout(layout)

        return widget

    def set_mode(self, mode):

        dialog = ConfirmationDialog()
        dialog.exec_()

        if dialog.result() == QDialog.Accepted:
            self._currect_mode = mode
            self._main_window.set_mode(mode)
        else:
            pass



    def get_mode(self):
        return self._currect_mode
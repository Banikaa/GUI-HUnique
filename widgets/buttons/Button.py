from PyQt5.QtWidgets import QPushButton, QFileDialog

# button class initialisation
class Button(QPushButton):



    '''
     parent: QLabel = the widget that will be affected by the button
     button_name: str
     button_text: str
     action_class: class =  where the action will be performed / viewed
     action: str = to select the type of action to be performed
    '''
    def __init__(self, parent, button_name, button_text, action_class = None, action = None):
        super(Button, self).__init__()
        self._parent = parent
        self._action_class = action_class
        self._button_text = button_text
        self._button_name = button_name
        self._photo_dir = ''
        self.setAcceptDrops(True)
        self.setFixedHeight(50)
        self.setText(self._button_text)
        self.setObjectName(self._button_name)
        self.setStyleSheet("border: 1px solid grey; background-color: grey; border-radius: 15px")

        if action:
            if action == 'insert_photo':
                self._photo_dir = '/Users/banika/Desktop/images'
            if 'insert_photo' in action:
                self.clicked.connect(self.open_photo_dir)


    # open photo directory
    def open_photo_dir(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Select Photo',
                                                  self._photo_dir,
                                                  'Images (*.png *.jpg)')
        if filename == '':
            return
        self._parent.input_photo(filename)  # set image to the parent label




from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QHBoxLayout, QPushButton

# class to show the confirmation dialog after the user selects either show or compare
class ConfirmationDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Set dialog title
        self.setWindowTitle("Confirmation")

        # Create a vertical layout for the dialog
        layout = QVBoxLayout()

        # Add a label to display the message and center it
        label = QLabel("Are you sure?")
        label.setAlignment(Qt.AlignCenter)  # Center the label
        layout.addWidget(label)

        # Create a spacer item to center content vertically
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()

        # Create Yes and No buttons
        yes_button = QPushButton("Yes")
        no_button = QPushButton("No")

        # Connect buttons to their respective functions
        yes_button.clicked.connect(self.accept)  # Close the dialog and return Accepted
        no_button.clicked.connect(self.reject)    # Close the dialog and return Rejected

        # Add buttons to the horizontal layout
        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)

        # Center the buttons in the horizontal layout
        button_layout.setAlignment(Qt.AlignCenter)

        # Add button layout to the main layout
        layout.addLayout(button_layout)

        # Create another spacer to ensure the layout is vertically centered
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Set the layout for the dialog
        self.setLayout(layout)

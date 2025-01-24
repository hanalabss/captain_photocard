from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap, QGuiApplication
import os
import sys

class ProcessScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.showFullScreen()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        
        # 배경 이미지 설정
        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        process_image_path = os.path.join( "assets", "printing_process.jpg")
        process_image = QImage(process_image_path)
        
        if not process_image.isNull():
            process_image = process_image.scaled(
                QGuiApplication.primaryScreen().geometry().width(),
                QGuiApplication.primaryScreen().geometry().height(),
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            label = QLabel(self)
            label.setPixmap(QPixmap.fromImage(process_image))
            layout.addWidget(label)

        # 3초 후 완료 화면으로 이동
        QTimer.singleShot(3000, self.go_to_complete_screen)

    def go_to_complete_screen(self):
        """완료 화면으로 이동"""
        from .complete import CompleteScreen
        self.parent().setCentralWidget(CompleteScreen(self.parent()))

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap, QGuiApplication
import os
import sys

class CompleteScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        print("CompleteScreen initialized")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.showFullScreen()
        self.initUI()

    def initUI(self):
        print("Initializing CompleteScreen UI")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        
        # 배경 이미지 설정
        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        complete_image_path = os.path.join(application_path, "assets", "printing_complete.jpg")
        print(f"Complete image path: {complete_image_path}")
        
        complete_image = QImage(complete_image_path)
        
        if not complete_image.isNull():
            print("Complete image loaded successfully")
            complete_image = complete_image.scaled(
                QGuiApplication.primaryScreen().geometry().width(),
                QGuiApplication.primaryScreen().geometry().height(),
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            label = QLabel(self)
            label.setPixmap(QPixmap.fromImage(complete_image))
            layout.addWidget(label)
        else:
            print("Error: Complete image failed to load")

        # 4초 후 메인 화면으로 이동
        QTimer.singleShot(4000, self.go_to_main)

    def go_to_main(self):
        """메인 화면(MainWindow)으로 이동"""
        print("Attempting to go to MainWindow")
        try:
            if self.parent():
                main_window = self.parent()
                # 현재 화면 제거
                self.hide()
                self.deleteLater()
                
                # MainWindow 초기화
                main_window.clear_central_widget()
                main_window.initUI()
                main_window.configure_event_filter(enable=True)
                
                print("Successfully returned to MainWindow")
            else:
                print("Error: No parent window found")
                
        except Exception as e:
            print(f"Error during transition to MainWindow: {e}")
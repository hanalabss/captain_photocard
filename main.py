from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPalette, QBrush, QGuiApplication
import sys
from screens.second_screen import SecondScreen
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("캡틴 아메리카: 브레이브 뉴 월드 포토카드")
        self.setFixedSize(1920, 1080)
        self.showFullScreen()

        # 배경 설정
        if getattr(sys, 'frozen', False):
            # PyInstaller로 빌드된 경우
            application_path = sys._MEIPASS
        else:
            # 일반 Python 스크립트로 실행된 경우
            application_path = os.path.dirname(os.path.abspath(__file__))
            
        background_path = os.path.join(application_path, "assets", "background.jpg")
        self.set_background(background_path)

        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # 이벤트 필터 설정
        self.configure_event_filter(enable=True)
        
    def set_background(self, image_path):
        try:
            background = QImage(image_path)
            if background.isNull():
                raise Exception("배경 이미지를 불러올 수 없습니다")

            # 화면 크기 가져오기
            screen_geometry = QGuiApplication.primaryScreen().geometry()
            screen_width = screen_geometry.width()
            screen_height = screen_geometry.height()

            # 비율 유지 없이 화면 크기에 맞게 이미지 크기 조정
            background = background.scaled(
                screen_width, 
                screen_height, 
                Qt.AspectRatioMode.IgnoreAspectRatio,  # 비율 무시
                Qt.TransformationMode.SmoothTransformation  # 부드러운 스케일링
            )

            palette = self.palette()
            palette.setBrush(QPalette.ColorRole.Window, QBrush(background))
            self.setPalette(palette)
        except Exception as e:
            print(f"배경 이미지 로딩 실패: {e}")
            self.setStyleSheet("background-color: #000B1D;")

    
    def configure_event_filter(self, enable=True):
        if enable:
            self.installEventFilter(self)
        else:
            self.removeEventFilter(self)

    def clear_central_widget(self):
        old_widget = self.centralWidget()
        if old_widget:
            old_widget.deleteLater()
        self.setPalette(QPalette())  # 배경 초기화

    def eventFilter(self, obj, event):
        if event.type() == event.Type.MouseButtonPress:
            admin_mode = event.modifiers() & Qt.KeyboardModifier.ControlModifier
            self.show_second_screen(admin_mode)
            return True
        return super().eventFilter(obj, event)
    
    def show_second_screen(self, admin_mode=False):
        # 중앙 위젯 정리
        self.clear_central_widget()

        # 이벤트 필터 제거
        self.configure_event_filter(enable=False)

        # 두 번째 화면 표시
        self.second_screen = SecondScreen(self, admin_mode)
        self.setCentralWidget(self.second_screen)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

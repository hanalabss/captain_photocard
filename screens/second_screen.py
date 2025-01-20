from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit,QLabel
from PyQt6.QtCore import Qt,QPropertyAnimation
from PyQt6.QtGui import QImage, QPainter, QGuiApplication, QPixmap
from screens.virtual_keyboard import VirtualKeyboard
import os
import sys

class SecondScreen(QWidget):
    def __init__(self, parent=None, admin_mode=False):
        super().__init__(parent)
        self.admin_mode = admin_mode
        QGuiApplication.instance().installEventFilter(self)
        self.click_count = 0
        self.coordinates = []
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.showFullScreen()
        self.initUI()
        
    def eventFilter(self, source, event):
        if isinstance(source, VirtualKeyboard):
            if event.type() == event.Type.FocusOut:
                # print("VirtualKeyboard lost focus via eventFilter, restoring...")
                source.raise_()
                source.activateWindow()
                return True
        return super().eventFilter(source, event)

    
    def mousePressEvent(self, event):
        if hasattr(self, 'keyboard'):
            # 클릭된 위치 가져오기
            click_pos = event.pos()
            
            # 키보드의 geometry 가져오기
            keyboard_rect = self.keyboard.geometry()
            
            # 디버깅을 위한 좌표 출력
            print(f"클릭 위치: ({click_pos.x()}, {click_pos.y()})")
            print(f"키보드 영역: {keyboard_rect.left()}, {keyboard_rect.top()}, {keyboard_rect.width()}, {keyboard_rect.height()}")
            print(f"키보드 활성화 상태: {self.keyboard.isActiveWindow()}")
            
            # 클릭된 위치가 키보드 영역 안인지 확인
            if keyboard_rect.contains(click_pos):
                print("키보드 영역 내부 클릭")
                # 키보드 영역 내부 클릭인 경우 이벤트 처리
                if not self.keyboard.isActiveWindow():
                    self.keyboard.raise_()
                    self.keyboard.activateWindow()
            else:
                print("키보드 영역 외부 클릭")
                # 키보드 영역 외부 클릭인 경우 이벤트 무시
                event.ignore()
                
            # 키보드를 항상 최상단에 유지
            self.keyboard.raise_()
            self.keyboard.activateWindow()
    
        if self.click_count < 2:
            x = event.position().x()
            y = event.position().y()
            self.coordinates.append((x, y))
            self.click_count += 1
            
            if self.click_count == 2:
                x1, y1 = self.coordinates[0]
                x2, y2 = self.coordinates[1]
                
                # 바탕화면 경로 가져오기
                desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
                file_path = os.path.join(desktop_path, 'keyboard_coordinates.txt')
                
                # 좌표 정보를 파일로 저장
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(f"키보드 영역 좌표:\n")
                        f.write(f"좌상단: ({x1}, {y1})\n")
                        f.write(f"우하단: ({x2}, {y2})\n")
                        f.write(f"너비: {x2 - x1}\n")
                        f.write(f"높이: {y2 - y1}\n")
                        f.write(f"\n화면 크기: {self.screen_width} x {self.screen_height}")
                except Exception as e:
                    # 파일 저장 실패시 임시 경로에 저장 시도
                    temp_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keyboard_coordinates.txt')
                    with open(temp_path, 'w', encoding='utf-8') as f:
                        f.write(f"키보드 영역 좌표:\n")
                        f.write(f"좌상단: ({x1}, {y1})\n")
                        f.write(f"우하단: ({x2}, {y2})\n")
                        f.write(f"너비: {x2 - x1}\n")
                        f.write(f"높이: {y2 - y1}\n")
                        f.write(f"\n화면 크기: {self.screen_width} x {self.screen_height}")
        
    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        
        screen = QGuiApplication.primaryScreen().geometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()
        
        self.load_background()
        
        # 입력 필드 생성
        self.input_field = QLineEdit(self)
        self.input_field.setGeometry(118, 925, 839, 131)
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: rgba(27, 40, 56, 0.8);
                color: #00FFC2;
                border: 2px solid #00FFC2;
                border-radius: 5px;
                padding: 10px;
                font-size: 72px;
            }
        """)
        
        # 가상 키보드 설정
        KEYBOARD_COORDS = {
            'left': 106.0,
            'top': 1141.0,
            'width': 864.0,
            'height': 441.0
        }
        
        scale_x = self.screen_width / 1080
        scale_y = self.screen_height / 1920
        
        keyboard_left = int(KEYBOARD_COORDS['left'] * scale_x)
        keyboard_top = int(KEYBOARD_COORDS['top'] * scale_y)
        keyboard_width = int(KEYBOARD_COORDS['width'] * scale_x)
        keyboard_height = int(KEYBOARD_COORDS['height'] * scale_y)
        
        self.keyboard = VirtualKeyboard(self.input_field, second_screen=self)
        self.keyboard.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.keyboard.setGeometry(
            keyboard_left,
            keyboard_top,
            keyboard_width,
            keyboard_height
        )
        
        self.keyboard.show()

        self.ensure_widget_visibility()
        
        
    def ensure_widget_visibility(self):
        """모든 위젯이 보이도록 설정"""
        # self.live_label.setVisible(True)
        self.input_field.setVisible(True)
        
    
    def paintEvent(self, event):
        if self.background:
            painter = QPainter(self)
            painter.drawImage(0, 0, self.background)
        
        # 모든 위젯을 최상위로 올림
        self.input_field.raise_()
        # self.live_label.raise_()
        if hasattr(self, 'keyboard'):
            self.keyboard.raise_()
            
        self.ensure_widget_visibility()
        
    def load_background(self):
        try:
            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS
            else:
                application_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            image_path = os.path.join(application_path, "assets", "input_screen_steps.jpg")
            self.background = QImage(image_path)
            
            if self.background.isNull():
                raise Exception("Failed to load the input screen steps image")
                
            self.background = self.background.scaled(
                self.screen_width,
                self.screen_height,
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.background = None
              
    def focusOutEvent(self, event):
        print("VirtualKeyboard lost focus, restoring...")
        self.raise_()  # 다시 최상위로 올리기
        self.activateWindow()  # 포커스를 다시 잡기
        event.accept()  # 이벤트를 처리했음을 알림
        super().focusOutEvent(event)

    def hide_with_animation(self, widgets):
        for widget in widgets:
            animation = QPropertyAnimation(widget, b"windowOpacity")
            animation.setDuration(300)  # 300ms 애니메이션
            animation.setStartValue(1.0)  # 시작 투명도
            animation.setEndValue(0.0)  # 끝 투명도
            animation.start()
            animation.finished.connect(widget.hide)  # 애니메이션 후 hide 호출
            

    def print_input(self):
        """가상 키보드에서 입력된 텍스트를 프린트"""
        from .print_manager import PrintManager
        from .process_screen import ProcessScreen

        text = self.input_field.text()
        if text:
            # 입력 필드 및 키보드 제거
            self.input_field.deleteLater()  # 입력 필드를 삭제
            self.keyboard.deleteLater()  # 가상 키보드를 삭제
            
            # 프린트 작업 실행
            printer = PrintManager()
            printer.direct_print(text, x=102, y=155)  # 좌표값 수정 필요
            
            # 프로세스 화면으로 전환
            self.parent().setCentralWidget(ProcessScreen(self.parent()))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            # print("ESC Key Pressed: Closing application from SecondScreen")  # 디버그 출력
            QGuiApplication.quit()  # 애플리케이션 종료
        else:
            super().keyPressEvent(event)  # 기본 동작 처리
            
    def closeEvent(self, event):
        # print("SecondScreen closed: Exiting application")
        QGuiApplication.quit()  # 애플리케이션 종료
        super().closeEvent(event)
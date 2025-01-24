from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton
from PyQt6.QtCore import Qt, QPropertyAnimation
from PyQt6.QtGui import QImage, QPainter, QGuiApplication
from screens.virtual_keyboard import VirtualKeyboard
import os
import sys
from wcwidth import wcwidth

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
        self.add_exit_button()

    def add_exit_button(self, x_offset=50, y_offset=10):
        self.exit_button = QPushButton("X", self)
        self.exit_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                font-size: 18px;
                border: none;
                border-radius: 10px;
                padding: 5px;
                width: 30px;
                height: 30px;
                z-index: 999;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        self.exit_button.setFixedSize(40, 40)
        
        screen = QGuiApplication.primaryScreen().geometry()
        self.exit_button.move(screen.width() - x_offset, y_offset)
        self.exit_button.raise_()
        self.exit_button.clicked.connect(QGuiApplication.quit)
        self.exit_button.setVisible(True)
        
    def showEvent(self, event):
        super().showEvent(event)
        if hasattr(self, 'exit_button'):
            self.exit_button.raise_()
            
    def eventFilter(self, source, event):
        if isinstance(source, VirtualKeyboard):
            if event.type() == event.Type.FocusOut:
                source.raise_()
                source.activateWindow()
                return True
        return super().eventFilter(source, event)
    
    def mousePressEvent(self, event):
        if hasattr(self, 'keyboard'):
            click_pos = event.pos()
            keyboard_rect = self.keyboard.geometry()
            input_field_rect = self.input_field.geometry()
            exit_button_rect = self.exit_button.geometry()
            
            if keyboard_rect.contains(click_pos):
                self.keyboard.raise_()
                self.keyboard.activateWindow()
                event.accept()
            elif input_field_rect.contains(click_pos):
                self.input_field.setFocus()
                self.keyboard.raise_()
                self.keyboard.activateWindow()
                event.accept()
            elif exit_button_rect.contains(click_pos):
                event.accept()
            else:
                event.accept()
                return
        
        if self.admin_mode and self.click_count < 2:
            x = event.position().x()
            y = event.position().y()
            self.coordinates.append((x, y))
            self.click_count += 1
            
            if self.click_count == 2:
                x1, y1 = self.coordinates[0]
                x2, y2 = self.coordinates[1]
                
                # desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
                # file_path = os.path.join(desktop_path, 'keyboard_coordinates.txt')
                
                # try:
                #     with open(file_path, 'w', encoding='utf-8') as f:
                #         f.write(f"키보드 영역 좌표:\n")
                #         f.write(f"좌상단: ({x1}, {y1})\n")
                #         f.write(f"우하단: ({x2}, {y2})\n")
                #         f.write(f"너비: {x2 - x1}\n")
                #         f.write(f"높이: {y2 - y1}\n")
                #         f.write(f"\n화면 크기: {self.screen_width} x {self.screen_height}")
                # except Exception as e:
                #     temp_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keyboard_coordinates.txt')
                #     with open(temp_path, 'w', encoding='utf-8') as f:
                #         f.write(f"키보드 영역 좌표:\n")
                #         f.write(f"좌상단: ({x1}, {y1})\n")
                #         f.write(f"우하단: ({x2}, {y2})\n")
                #         f.write(f"너비: {x2 - x1}\n")
                #         f.write(f"높이: {y2 - y1}\n")
                #         f.write(f"\n화면 크기: {self.screen_width} x {self.screen_height}")
    
    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        
        screen = QGuiApplication.primaryScreen().geometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()
        
        self.load_background()
        
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
        self.input_field.setVisible(True)
    
    def paintEvent(self, event):
        if self.background:
            painter = QPainter(self)
            painter.drawImage(0, 0, self.background)
        
        self.input_field.raise_()
        if hasattr(self, 'keyboard'):
            self.keyboard.raise_()
            
        self.ensure_widget_visibility()
        
    def load_background(self):
        try:
            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS
            else:
                application_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            image_path = os.path.join("assets", "input_screen_steps.jpg")
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
            self.background = None
              
    def focusOutEvent(self, event):
        self.raise_()
        self.activateWindow()
        event.accept()
        super().focusOutEvent(event)

    def hide_with_animation(self, widgets):
        for widget in widgets:
            animation = QPropertyAnimation(widget, b"windowOpacity")
            animation.setDuration(300)
            animation.setStartValue(1.0)
            animation.setEndValue(0.0)
            animation.start()
            animation.finished.connect(widget.hide)

    def print_input(self):
        from .print_manager import PrintManager
        from .process_screen import ProcessScreen
        from .config_handler import load_print_coordinates

        text = self.input_field.text()
        if text:
            text = self.visual_center(text.strip(), 8, ' ')
            self.input_field.deleteLater()
            self.keyboard.deleteLater()
            
            x, y = load_print_coordinates()
            printer = PrintManager()
            printer.direct_print(text, x=x, y=y)
            
            self.parent().setCentralWidget(ProcessScreen(self.parent()))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            QGuiApplication.quit()
        else:
            super().keyPressEvent(event)
            
    def closeEvent(self, event):
        QGuiApplication.quit()
        super().closeEvent(event)

    def visual_center(self, text, width, fillchar=' '):
        # 문자열의 시각적 너비 계산
        text_width = sum(wcwidth(char) for char in text)  # 각 문자별로 너비 계산
        
        # 필요한 패딩 계산
        padding = width - text_width
        if padding <= 0:
            return text
        
        # 왼쪽과 오른쪽 패딩 계산
        left_padding = padding // 2
        right_padding = padding - left_padding
        
        # 중앙 정렬된 문자열 반환
        return (fillchar * left_padding) + text + (fillchar * right_padding)
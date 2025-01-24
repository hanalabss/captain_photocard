from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
                             QHBoxLayout, QSlider)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPalette, QBrush, QGuiApplication
import sys
import os
import pygame
from screens.second_screen import SecondScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.audio_available = False  # 오디오 사용 가능 여부 플래그
        self.setup_pygame()  # pygame 초기화 시도
        self.initUI()
        
    def setup_pygame(self):
        """Pygame 오디오 초기화"""
        try:
            # 여러 가지 설정으로 초기화 시도
            try:
                pygame.mixer.init(44100, -16, 2, 2048)
                self.audio_available = True
            except:
                try:
                    pygame.mixer.init(44100, 16, 2, 2048)
                    self.audio_available = True
                except:
                    try:
                        pygame.mixer.init()
                        self.audio_available = True
                    except:
                        print("오디오 장치를 찾을 수 없습니다.")
                        self.audio_available = False
                        return
                        
            if not self.audio_available:
                return
                        
            # BGM 파일 경로 설정
            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
                
            bgm_path = os.path.join("assets", "bgm", "background_music.mp3")
            
            # 파일 존재 확인
            if not os.path.exists(bgm_path):
                print(f"BGM 파일을 찾을 수 없습니다: {bgm_path}")
                self.audio_available = False
                return
                
            # BGM 로드 및 재생
            pygame.mixer.music.load(bgm_path)
            pygame.mixer.music.set_volume(0.5)  # 기본 볼륨 50%
            pygame.mixer.music.play(-1)  # -1은 무한 반복
            
        except Exception as e:
            print(f"BGM 설정 중 오류 발생: {str(e)}")
            self.audio_available = False
            
    def initUI(self):
        self.setWindowTitle("캡틴 아메리카: 브레이브 뉴 월드 포토카드")
        self.setFixedSize(1920, 1080)
        self.showFullScreen()

        # 배경 설정
        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
            
        background_path = os.path.join( "assets", "background.jpg")
        self.set_background(background_path)

        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # 종료 버튼 추가
        self.add_exit_button(central_widget)

        # 오디오 컨트롤 추가 (if available)
        if self.audio_available:
            self.setup_audio_controls()
        
        # 이벤트 필터 설정
        self.configure_event_filter(enable=True)

    def setup_audio_controls(self):
        """오디오 컨트롤 위젯 설정 - New Captain Challenge 테마"""
        # 컨트롤 컨테이너 생성
        self.audio_controls = QWidget(self)
        layout = QHBoxLayout(self.audio_controls)
        layout.setSpacing(15)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # BGM On/Off 버튼
        self.bgm_button = QPushButton("🔊", self.audio_controls)
        self.bgm_button.setCheckable(True)
        self.bgm_button.setChecked(True)
        self.bgm_button.clicked.connect(self.toggle_bgm)
        self.bgm_button.setFixedSize(40, 40)
        self.bgm_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 #4A4A4A, stop:0.5 #3A3A3A, stop:1 #2A2A2A);
                color: white;
                border: 1px solid #666666;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
                box-shadow: 0 0 10px #0066CC;
            }
            QPushButton:checked {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 #0066CC, stop:0.5 #0055AA, stop:1 #004488);
                border: 1px solid #0088FF;
                box-shadow: 0 0 15px #00AAFF;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 #5A5A5A, stop:0.5 #4A4A4A, stop:1 #3A3A3A);
                border: 1px solid #888888;
            }
        """)
        
        # 볼륨 슬라이더
        self.volume_slider = QSlider(Qt.Orientation.Horizontal, self.audio_controls)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.change_volume)
        self.volume_slider.setFixedSize(120, 20)
        self.volume_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #666666;
                height: 6px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 #2A2A2A, stop:1 #1A1A1A);
                margin: 0px;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 #DEDEDE, stop:0.5 #C0C0C0, stop:1 #A0A0A0);
                border: 1px solid #666666;
                width: 18px;
                height: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 #0088FF, stop:1 #0066CC);
                border-radius: 3px;
            }
            QSlider::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 #FFFFFF, stop:0.5 #DEDEDE, stop:1 #C0C0C0);
                border: 1px solid #888888;
            }
        """)
        
        # 컨트롤 배치
        layout.addWidget(self.bgm_button)
        layout.addWidget(self.volume_slider)
        
        # 전체 컨테이너에 배경과 글로우 효과 추가
        self.audio_controls.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 rgba(30, 30, 30, 0.9),
                                        stop:1 rgba(20, 20, 20, 0.9));
                border: 1px solid #444444;
                border-radius: 25px;
            }
        """)
        
        # 컨트롤 위치 설정 (왼쪽 상단)
        self.audio_controls.setGeometry(20, 20, 200, 50)
        self.audio_controls.raise_()
        self.audio_controls.show()
        
    def toggle_bgm(self, checked):
        """BGM 켜기/끄기"""
        if checked:
            pygame.mixer.music.unpause()
            self.bgm_button.setText("🔊")
        else:
            pygame.mixer.music.pause()
            self.bgm_button.setText("🔇")
            
    def change_volume(self, value):
        """볼륨 조절"""
        volume = value / 100
        pygame.mixer.music.set_volume(volume)
            
    def set_background(self, image_path):
        try:
            background = QImage(image_path)
            if background.isNull():
                raise Exception("배경 이미지를 불러올 수 없습니다")

            screen_geometry = QGuiApplication.primaryScreen().geometry()
            screen_width = screen_geometry.width()
            screen_height = screen_geometry.height()

            background = background.scaled(
                screen_width, 
                screen_height, 
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            palette = self.palette()
            palette.setBrush(QPalette.ColorRole.Window, QBrush(background))
            self.setPalette(palette)
        except Exception as e:
            print(f"배경 이미지 로딩 실패: {e}")
            self.setStyleSheet("background-color: #000B1D;")

    def add_exit_button(self, parent_widget, x_offset=50, y_offset=10):
        """부모 위젯의 오른쪽 위에 종료 버튼 추가"""
        exit_button = QPushButton("X", parent_widget)
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                font-size: 18px;
                border: none;
                border-radius: 10px;
                padding: 5px;
                width: 30px;
                height: 30px;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        exit_button.setFixedSize(40, 40)

        def adjust_position():
            exit_button.move(parent_widget.width() - x_offset, y_offset)

        adjust_position()
        parent_widget.resizeEvent = lambda event: adjust_position()
        parent_widget.showEvent = lambda event: exit_button.raise_()
        exit_button.clicked.connect(self.close)

    def configure_event_filter(self, enable=True):
        if enable:
            self.installEventFilter(self)
        else:
            self.removeEventFilter(self)

    def clear_central_widget(self):
        old_widget = self.centralWidget()
        if old_widget:
            old_widget.deleteLater()
        self.setPalette(QPalette())

    def eventFilter(self, obj, event):
        if event.type() == event.Type.MouseButtonPress:
            admin_mode = event.modifiers() & Qt.KeyboardModifier.ControlModifier
            self.show_second_screen(admin_mode)
            return True
        return super().eventFilter(obj, event)
    
    def show_second_screen(self, admin_mode=False):
        self.clear_central_widget()
        self.configure_event_filter(enable=False)
        self.second_screen = SecondScreen(self, admin_mode)
        self.setCentralWidget(self.second_screen)
        self.add_exit_button(self.second_screen)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
            
    def closeEvent(self, event):
        """앱 종료 시 BGM 정지"""
        if self.audio_available:
            try:
                if pygame.mixer.get_init():
                    pygame.mixer.music.stop()
                    pygame.mixer.quit()
            except:
                pass
        event.accept()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtGui import QPainter, QFont, QColor, QImage, QFontDatabase
from PyQt6.QtCore import Qt, QRectF
import os
import sys
import traceback

class PrintManager:
    def __init__(self):
        try:
            print("PrintManager 초기화 시작")
            self.printer = QPrinter()
            print("QPrinter 초기화 완료")
            
            # 경로 설정
            if getattr(sys, 'frozen', False):
                self.application_path = sys._MEIPASS
                print(f"Frozen 모드 경로: {self.application_path}")
            else:
                self.application_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                print(f"개발 모드 경로: {self.application_path}")
                
            self.font_path = os.path.join(self.application_path, "assets", "fonts", "A시월구일1.TTF")
            self.image_path = os.path.join(self.application_path, "assets", "input_image.jpg")
            
            print(f"폰트 경로: {self.font_path}")
            print(f"이미지 경로: {self.image_path}")
            
            # 폰트 존재 확인
            if os.path.exists(self.font_path):
                print("폰트 파일 존재함")
            else:
                print("폰트 파일이 없음!")
            
            # 이미지 존재 확인
            if os.path.exists(self.image_path):
                print("이미지 파일 존재함")
            else:
                print("이미지 파일이 없음!")
            
            # 폰트 등록
            self.font_id = QFontDatabase.addApplicationFont(self.font_path)
            if self.font_id == -1:
                print(f"폰트 등록 실패: {self.font_path}")
            else:
                self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
                print(f"폰트 등록 성공: {self.font_family}")
                
        except Exception as e:
            print(f"PrintManager 초기화 중 오류: {str(e)}")
            print("상세 오류:")
            print(traceback.format_exc())
            
    def print_text(self, text, x, y):
        print(f"프린트 시작: text='{text}', x={x}, y={y}")
        try:
            painter = QPainter()
            if painter.begin(self.printer):
                try:
                    # 배경 이미지 로드
                    print("배경 이미지 로드 시도")
                    background = QImage(self.image_path)
                    if not background.isNull():
                        print("배경 이미지 로드 성공")
                        target_rect = QRectF(0, 0, self.printer.width(), self.printer.height())
                        painter.drawImage(target_rect, background)
                    else:
                        print("배경 이미지 로드 실패!")
                    
                    # 폰트 설정
                    font = QFont()
                    if self.font_id != -1:
                        font.setFamily(self.font_family)
                        print(f"설정된 폰트: {self.font_family}")
                    else:
                        font.setFamily("Arial")
                        print("기본 폰트(Arial) 사용")
                    
                    font.setPointSizeF(9.6)
                    painter.setFont(font)
                    
                    # 텍스트 색상 설정
                    painter.setPen(QColor(255, 0, 0))
                    
                    # 텍스트 그리기
                    print(f"텍스트 그리기: {text}")
                    painter.drawText(x, y, text)
                    print("텍스트 그리기 완료")
                    
                finally:
                    painter.end()
                    print("프린트 작업 완료")
            else:
                print("painter.begin() 실패!")
                
        except Exception as e:
            print(f"프린트 중 오류 발생: {str(e)}")
            print("상세 오류:")
            print(traceback.format_exc())
                
    def direct_print(self, text, x, y):
        print(f"다이렉트 프린트 시작: text='{text}'")
        try:
            self.print_text(text, x, y)
        except Exception as e:
            print(f"다이렉트 프린트 중 오류: {str(e)}")
            print("상세 오류:")
            print(traceback.format_exc())
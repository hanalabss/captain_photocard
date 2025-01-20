from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout, QSizePolicy, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from .hangul_composer import HangulComposer


class VirtualKeyboard(QWidget):
    # 기본 한글 매핑
    hangul_map = {
        'Q': 'ㅂ', 'W': 'ㅈ', 'E': 'ㄷ', 'R': 'ㄱ', 'T': 'ㅅ', 
        'Y': 'ㅛ', 'U': 'ㅕ', 'I': 'ㅑ', 'O': 'ㅐ', 'P': 'ㅔ',
        'A': 'ㅁ', 'S': 'ㄴ', 'D': 'ㅇ', 'F': 'ㄹ', 'G': 'ㅎ', 
        'H': 'ㅗ', 'J': 'ㅓ', 'K': 'ㅏ', 'L': 'ㅣ',
        'Z': 'ㅋ', 'X': 'ㅌ', 'C': 'ㅊ', 'V': 'ㅍ', 'B': 'ㅠ', 
        'N': 'ㅜ', 'M': 'ㅡ'
    }

    # Shift 상태일 때의 한글 매핑
    shift_hangul_map = {
        'Q': 'ㅃ', 'W': 'ㅉ', 'E': 'ㄸ', 'R': 'ㄲ', 'T': 'ㅆ',
        'Y': 'ㅛ', 'U': 'ㅕ', 'I': 'ㅑ', 'O': 'ㅒ', 'P': 'ㅖ',
        'A': 'ㅁ', 'S': 'ㄴ', 'D': 'ㅇ', 'F': 'ㄹ', 'G': 'ㅎ',
        'H': 'ㅗ', 'J': 'ㅓ', 'K': 'ㅏ', 'L': 'ㅣ',
        'Z': 'ㅋ', 'X': 'ㅌ', 'C': 'ㅊ', 'V': 'ㅍ', 'B': 'ㅠ',
        'N': 'ㅜ', 'M': 'ㅡ'
    }

    def __init__(self, input_widget, second_screen=None):
        super().__init__()
        self.input_widget = input_widget
        self.second_screen = second_screen  # SecondScreen 인스턴스 저장

        self.is_hangul = False
        self.is_uppercase = False
        self.hangul_composer = HangulComposer()
        self.initUI()
        self.update_keyboard_labels()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(5)
        self.setStyleSheet("""
        VirtualKeyboard {
            background-color: #1B2838;
            border: 2px solid #00FFC2;
            border-radius: 15px;
            padding: 10px;
        }
        """)
            
        self.keys = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
        ]

        self.button_widgets = []
        for row in self.keys:
            row_layout = QGridLayout()
            row_layout.setSpacing(5)
            row_buttons = []
            for i, key in enumerate(row):
                button = QPushButton(self.get_display_key(key))
                button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                button.setFont(QFont('맑은 고딕', 20))
                button.clicked.connect(lambda checked, text=key: self.button_clicked(text))
                button.setStyleSheet(self.get_button_style())
                row_layout.addWidget(button, 0, i)
                row_buttons.append(button)
            self.layout.addLayout(row_layout)
            self.button_widgets.append(row_buttons)

        special_layout = QGridLayout()
        special_layout.setSpacing(5)

        # 각 버튼 설정
        hangul_btn = QPushButton('한/영')
        hangul_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        hangul_btn.setFont(QFont('맑은 고딕', 20))
        hangul_btn.clicked.connect(self.toggle_hangul)
        hangul_btn.setStyleSheet(self.get_special_button_style('#4299E1'))
        hangul_btn.setFixedWidth(80)  # 고정 너비 설정

        shift_btn = QPushButton('Shift')
        shift_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        shift_btn.setFont(QFont('맑은 고딕', 20))
        shift_btn.clicked.connect(self.toggle_shift)
        shift_btn.setStyleSheet(self.get_special_button_style('#3182CE'))
        shift_btn.setFixedWidth(80)  # 고정 너비 설정

        space_btn = QPushButton('Space')
        space_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        space_btn.setFont(QFont('맑은 고딕', 20))
        space_btn.clicked.connect(self.space_pressed)
        space_btn.setStyleSheet(self.get_button_style())

        backspace_btn = QPushButton('←')
        backspace_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        backspace_btn.setFont(QFont('맑은 고딕', 20))
        backspace_btn.clicked.connect(self.backspace)
        backspace_btn.setStyleSheet(self.get_special_button_style('#E53E3E'))

        print_btn = QPushButton('인쇄')
        print_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        print_btn.setFont(QFont('맑은 고딕', 20))
        print_btn.clicked.connect(self.print_text)
        print_btn.setStyleSheet(self.get_special_button_style('#48BB78'))
        print_btn.setFixedWidth(80)
        
        # 레이아웃에 버튼 추가
        special_layout.addWidget(hangul_btn, 0, 0)
        special_layout.addWidget(shift_btn, 0, 1)
        special_layout.addWidget(space_btn, 0, 2)
        special_layout.addWidget(backspace_btn, 0, 3)
        special_layout.addWidget(print_btn, 0, 4)
        
        # 열 비율 설정 (총 10을 기준으로)
        special_layout.setColumnStretch(0, 2)  # 한/영 버튼
        special_layout.setColumnStretch(1, 2)  # Shift 버튼
        special_layout.setColumnStretch(2, 4)  # Space 버튼
        special_layout.setColumnStretch(3, 2)  # Backspace 버튼
        special_layout.setColumnStretch(4, 2)  # 인쇄 버튼

        self.layout.addLayout(special_layout)
        self.setLayout(self.layout)

    def button_clicked(self, key):
        if self.is_hangul and key in self.hangul_map:
            # Shift 상태에 따라 적절한 자모 선택
            jamo = self.shift_hangul_map[key] if self.is_uppercase else self.hangul_map[key]
            committed, current = self.hangul_composer.add_jamo(jamo)
            
            text = self.input_widget.text()
            if text:
                text = text[:-1] if len(text) > 0 else ""
            
            if committed:
                text += committed
            
            if current:
                text += current
            
            self.input_widget.setText(text)
            self.input_widget.setCursorPosition(len(text))
        else:
            self.input_widget.setText(self.input_widget.text() + 
                        (key.upper() if self.is_uppercase else key.lower()))

    def insert_text(self, char):
        if char:
            self.input_widget.setText(self.input_widget.text() + char)
            self.input_widget.setCursorPosition(len(self.input_widget.text()))

    def toggle_hangul(self):
        self.is_hangul = not self.is_hangul
        self.hangul_composer.reset()
        self.update_keyboard_labels()

    def toggle_shift(self):
        self.is_uppercase = not self.is_uppercase
        self.update_keyboard_labels()

    def space_pressed(self):
        composed = self.hangul_composer.commit()
        if composed:
            self.insert_text(composed)
        self.insert_text(' ')

    def backspace(self):
        text = self.input_widget.text()
        if text:
            self.hangul_composer.reset()
            self.input_widget.setText(text[:-1])
            self.input_widget.setCursorPosition(len(text) - 1)
            
    def print_text(self):
        if hasattr(self, 'second_screen') and self.second_screen:
            self.second_screen.print_input()
            
            
    def update_keyboard_labels(self):
        for row_buttons, row_keys in zip(self.button_widgets, self.keys):
            for button, key in zip(row_buttons, row_keys):
                if self.is_hangul:
                    if self.is_uppercase and key in self.shift_hangul_map:
                        button.setText(self.shift_hangul_map[key])
                    else:
                        button.setText(self.hangul_map.get(key, key))
                else:
                    button.setText(key.upper() if self.is_uppercase else key.lower())

    def get_display_key(self, key):
        if self.is_uppercase:
            return key.upper()
        return key.lower()

    def get_button_style(self):
        return """
            QPushButton {
                background-color: #2D3748;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton:pressed {
                background-color: #4A5568;
            }
        """

    def get_special_button_style(self, color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 10px;
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color)};
            }}
        """

    def darken_color(self, color):
        r, g, b = [int(color[i:i+2], 16) for i in (1, 3, 5)]
        return f'#{max(0, r-30):02X}{max(0, g-30):02X}{max(0, b-30):02X}'
    


# Example usage:
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    input_widget = QLineEdit()
    keyboard = VirtualKeyboard(input_widget)
    
    # Create main widget and layout
    main_widget = QWidget()
    main_layout = QVBoxLayout()
    
    # Add input widget and keyboard to layout
    main_layout.addWidget(input_widget)
    main_layout.addWidget(keyboard)
    
    # Set layout to main widget
    main_widget.setLayout(main_layout)
    main_widget.show()
    
    sys.exit(app.exec())
class HangulComposer:
    CHOSUNG = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 
               'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    JUNGSUNG = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 
                'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
    JONGSUNG = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ',
                'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 
                'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    
    # 쌍자음 매핑
    DOUBLE_CONSONANT_MAP = {
        'ㄱ': 'ㄲ',
        'ㄷ': 'ㄸ',
        'ㅂ': 'ㅃ',
        'ㅅ': 'ㅆ',
        'ㅈ': 'ㅉ'
    }
    
    # 겹받침 매핑
    COMPLEX_JONGSUNG_MAP = {
        ('ㄱ', 'ㅅ'): 'ㄳ',
        ('ㄴ', 'ㅈ'): 'ㄵ',
        ('ㄴ', 'ㅎ'): 'ㄶ',
        ('ㄹ', 'ㄱ'): 'ㄺ',
        ('ㄹ', 'ㅁ'): 'ㄻ',
        ('ㄹ', 'ㅂ'): 'ㄼ',
        ('ㄹ', 'ㅅ'): 'ㄽ',
        ('ㄹ', 'ㅌ'): 'ㄾ',
        ('ㄹ', 'ㅍ'): 'ㄿ',
        ('ㄹ', 'ㅎ'): 'ㅀ',
        ('ㅂ', 'ㅅ'): 'ㅄ'
    }

    def __init__(self):
        self.reset()
        self.current_text = ""
        self.previous_state = None
        self.last_jamo = None
        self.temp_jong = None

    def reset(self):
        self.cho = None
        self.jung = None
        self.jong = None
        self.last_jamo = None
        self.temp_jong = None

    def try_double_consonant(self, jamo):
        if (self.last_jamo in self.DOUBLE_CONSONANT_MAP and 
            self.last_jamo == jamo):
            return self.DOUBLE_CONSONANT_MAP[jamo]
        return jamo

    def try_complex_jongsung(self, current_jong, new_jong):
        if (current_jong, new_jong) in self.COMPLEX_JONGSUNG_MAP:
            return self.COMPLEX_JONGSUNG_MAP[(current_jong, new_jong)]
        return new_jong

    def add_jamo(self, jamo):
        result = None
        
        # 쌍자음 처리
        if jamo in self.CHOSUNG:
            jamo = self.try_double_consonant(jamo)
        
        # 모음이 입력된 경우
        if jamo in self.JUNGSUNG:
            if self.jong is not None:
                if self.jong in [v for v in self.COMPLEX_JONGSUNG_MAP.values()]:
                    for (j1, j2), complex_jong in self.COMPLEX_JONGSUNG_MAP.items():
                        if complex_jong == self.jong:
                            new_cho = j2
                            self.jong = j1
                            break
                else:
                    new_cho = self.jong
                    self.jong = None
                
                result = self.combine()
                self.cho = new_cho
                self.jung = jamo
            elif self.cho is not None and self.jung is None:
                self.jung = jamo
            else:
                result = self.commit()
                self.jung = jamo
                
        # 자음이 입력된 경우
        elif jamo in self.CHOSUNG:
            if self.cho is None and self.jung is None:
                self.cho = jamo
            elif self.cho is not None and self.jung is not None:
                if self.jong is None:
                    self.jong = jamo
                else:
                    new_jong = self.try_complex_jongsung(self.jong, jamo)
                    if new_jong != jamo:
                        self.jong = new_jong
                    else:
                        result = self.commit()
                        self.cho = jamo
            else:
                result = self.commit()
                self.cho = jamo

        self.last_jamo = jamo
        
        current = self.combine()
        if current:
            self.current_text = current
            
        return result, self.current_text

    def combine(self):
        if self.cho is not None and self.jung is not None:
            cho_idx = self.CHOSUNG.index(self.cho)
            jung_idx = self.JUNGSUNG.index(self.jung)
            jong_idx = self.JONGSUNG.index(self.jong) if self.jong else 0
            char_code = 0xAC00 + cho_idx * 588 + jung_idx * 28 + jong_idx
            return chr(char_code)
        elif self.cho is not None:
            return self.cho
        elif self.jung is not None:
            return self.jung
        return None

    def commit(self):
        result = self.combine()
        self.reset()
        return result

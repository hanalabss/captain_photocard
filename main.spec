# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('screens', 'screens'),  # screens 폴더만 유지
        ('config.txt', '.'),  # config.txt를 루트 디렉토리에 추가

    ],
    hiddenimports=[
        'wcwidth',
        'screens.second_screen',
        'screens.virtual_keyboard',
        'screens.hangul_composer',
        'screens.complete',
        'screens.print_manager',
        'screens.process_screen',
        'PyQt6.QtPrintSupport',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.QtCore',
        'sys',
        'os',
        'traceback',
        'QImage',
        'QGuiApplication',
        'QPalette',
        'QBrush',
        'QPainter',
        'QFont',
        'QColor',
        'QPixmap',
        'QTimer',
        'QVBoxLayout',
        'QWidget',
        'QLabel',
        'QLineEdit',
        'QPushButton',
        'QSizePolicy',
        'QPropertyAnimation',
        'QFontDatabase',
        'QPrinter',
        'Qt.AspectRatioMode',
        'Qt.TransformationMode',
        'Qt.WidgetAttribute',
        'Qt.WindowType',
        'Qt.KeyboardModifier',
        'Qt.Event',
        'pygame',
        'pygame.mixer',
        'pygame.mixer_music',
        'PyQt6.QtCore.Qt.Orientation',
        'PyQt6.QtWidgets.QHBoxLayout',
        'PyQt6.QtWidgets.QSlider'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
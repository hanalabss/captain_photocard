# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),  # 전체 assets 폴더를 복사
        ('screens', 'screens')
    ],
    hiddenimports=[
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
        'Qt.Event'
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
    debug=True,  # debug를 True로 유지
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # console을 True로 유지해서 로그 확인
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

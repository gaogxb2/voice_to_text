# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 配置文件
用于自定义打包选项
"""

import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# 收集所有需要的数据文件
datas = [
    ('readme.md', '.'),
]

# 收集隐藏导入
hiddenimports = [
    'gradio',
    'funasr',
    'modelscope',
    'torch',
    'torchaudio',
    'librosa',
    'soundfile',
    'numpy',
    'scipy',
    'PIL',
    'PIL._tkinter_finder',
]

# 收集子模块
hiddenimports += collect_submodules('gradio')
hiddenimports += collect_submodules('funasr')
hiddenimports += collect_submodules('modelscope')

a = Analysis(
    ['webui.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='SenseVoice',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

app = BUNDLE(
    exe,
    name='SenseVoice',
    icon=None,
    bundle_identifier='com.sensevoice.app',
)


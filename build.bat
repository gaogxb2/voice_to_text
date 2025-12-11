@echo off
REM 快速打包脚本 (Windows)

echo ==========================================
echo SenseVoice 打包工具
echo ==========================================
echo.

REM 检查 PyInstaller
where pyinstaller >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo PyInstaller 未安装，正在安装...
    pip install pyinstaller
)

echo 开始打包...
echo.

REM 打包启动器（推荐，包含自动模型检查）
pyinstaller --name=SenseVoice ^
    --onefile ^
    --windowed ^
    --add-data="readme.md;." ^
    --hidden-import=gradio ^
    --hidden-import=funasr ^
    --hidden-import=modelscope ^
    --hidden-import=torch ^
    --hidden-import=torchaudio ^
    --collect-all=gradio ^
    --collect-all=funasr ^
    launcher.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ==========================================
    echo ✓ 打包成功！
    echo ==========================================
    echo.
    echo 可执行文件位置: dist\SenseVoice.exe
    echo.
    echo 分发说明:
    echo 1. 将 dist\SenseVoice.exe 分发给用户
    echo 2. 首次运行需要网络连接下载模型
    echo 3. 可以将 README_用户使用说明.txt 一起分发
) else (
    echo.
    echo ==========================================
    echo ✗ 打包失败
    echo ==========================================
)

pause


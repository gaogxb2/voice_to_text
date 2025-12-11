@echo off
REM 一键配置国内镜像源脚本 (Windows)

echo ==========================================
echo 配置国内镜像源
echo ==========================================
echo.

REM 配置 pip 镜像源
echo 1. 配置 pip 镜像源...
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

echo ✓ pip 镜像源已配置为: 清华大学镜像
echo.

REM 配置 ModelScope 镜像源
echo 2. 配置 ModelScope 镜像源...
setx MODELSCOPE_ENVIRONMENT "cn" >nul 2>&1

echo ✓ ModelScope 镜像源已配置
echo.
echo ==========================================
echo 配置完成！
echo ==========================================
echo.
echo 注意: ModelScope 环境变量需要重新打开终端才能生效
echo.
echo 现在可以使用以下命令下载模型:
echo   python download_model.py --model small --mirror
echo.
pause


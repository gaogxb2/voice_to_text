#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
打包脚本 - 将项目打包成可执行文件
支持 Windows (.exe) 和 macOS (.app)
"""

import os
import sys
import subprocess
import platform

def check_pyinstaller():
    """检查 PyInstaller 是否已安装"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """安装 PyInstaller"""
    print("正在安装 PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    print("✓ PyInstaller 安装完成")

def build_executable():
    """构建可执行文件"""
    system = platform.system()
    
    print(f"检测到系统: {system}")
    print("开始打包...")
    
    # PyInstaller 命令参数
    cmd = [
        "pyinstaller",
        "--name=SenseVoice",
        "--onefile",  # 打包成单个文件
        "--windowed",  # 无控制台窗口（GUI 模式）
        "--add-data=readme.md;." if system == "Windows" else "--add-data=readme.md:.",
        "--hidden-import=gradio",
        "--hidden-import=funasr",
        "--hidden-import=modelscope",
        "--hidden-import=torch",
        "--hidden-import=torchaudio",
        "--hidden-import=librosa",
        "--hidden-import=soundfile",
        "--hidden-import=numpy",
        "--hidden-import=scipy",
        "--collect-all=gradio",
        "--collect-all=funasr",
        "webui.py"
    ]
    
    # macOS 特定设置
    if system == "Darwin":
        cmd.extend([
            "--osx-bundle-identifier=com.sensevoice.app",
            "--icon=NONE"  # 可以添加 .icns 图标文件
        ])
    
    # Windows 特定设置
    if system == "Windows":
        cmd.extend([
            "--icon=NONE"  # 可以添加 .ico 图标文件
        ])
    
    try:
        subprocess.check_call(cmd)
        print("\n✓ 打包完成！")
        
        if system == "Darwin":
            print("可执行文件位置: dist/SenseVoice.app")
        elif system == "Windows":
            print("可执行文件位置: dist/SenseVoice.exe")
        else:
            print("可执行文件位置: dist/SenseVoice")
            
    except subprocess.CalledProcessError as e:
        print(f"\n✗ 打包失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("SenseVoice 打包工具")
    print("=" * 60)
    
    # 检查 PyInstaller
    if not check_pyinstaller():
        print("PyInstaller 未安装")
        response = input("是否安装 PyInstaller? (y/n): ")
        if response.lower() == 'y':
            install_pyinstaller()
        else:
            print("需要 PyInstaller 才能打包，退出")
            return
    
    # 构建可执行文件
    if build_executable():
        print("\n" + "=" * 60)
        print("打包成功！")
        print("=" * 60)
        print("\n使用说明:")
        print("1. 可执行文件在 dist/ 目录下")
        print("2. 首次运行需要下载模型（需要网络连接）")
        print("3. 可以将整个 dist/ 目录分发给用户")
    else:
        print("\n打包失败，请检查错误信息")

if __name__ == "__main__":
    main()


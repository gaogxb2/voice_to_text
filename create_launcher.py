#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
创建启动器脚本
用于在打包后的应用中自动下载模型和启动服务
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def get_resource_path(relative_path):
    """获取资源文件路径（支持打包后的应用）"""
    try:
        # PyInstaller 创建的临时文件夹路径
        base_path = sys._MEIPASS
    except Exception:
        # 开发环境
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def check_model():
    """检查模型是否存在"""
    model_path = "./models/iic/SenseVoiceSmall"
    if os.path.exists(model_path) and os.path.exists(os.path.join(model_path, "model.pt")):
        return True, model_path
    return False, None

def download_model():
    """下载模型"""
    print("正在下载模型，这可能需要几分钟...")
    try:
        from download_model import download_model as dl_model
        result = dl_model("small", "./models")
        if result:
            print("✓ 模型下载完成")
            return True
        else:
            print("✗ 模型下载失败")
            return False
    except Exception as e:
        print(f"下载模型时出错: {e}")
        return False

def start_webui():
    """启动 Web UI"""
    print("正在启动 SenseVoice...")
    try:
        # 导入并启动 webui
        from webui import main
        main()
    except KeyboardInterrupt:
        print("\n程序已停止")
    except Exception as e:
        print(f"启动失败: {e}")
        input("按 Enter 键退出...")

def main():
    """主函数"""
    print("=" * 60)
    print("SenseVoice 语音识别系统")
    print("=" * 60)
    print()
    
    # 检查模型
    model_exists, model_path = check_model()
    
    if not model_exists:
        print("检测到模型文件不存在")
        response = input("是否现在下载模型? (y/n): ")
        if response.lower() == 'y':
            if not download_model():
                print("模型下载失败，程序退出")
                input("按 Enter 键退出...")
                return
        else:
            print("需要模型文件才能运行，程序退出")
            input("按 Enter 键退出...")
            return
    
    print(f"✓ 模型已就绪: {model_path}")
    print()
    print("正在启动 Web 界面...")
    print("启动后会自动打开浏览器")
    print("如果没有自动打开，请访问: http://localhost:7860")
    print()
    
    # 延迟打开浏览器
    time.sleep(2)
    try:
        webbrowser.open('http://localhost:7860')
    except:
        pass
    
    # 启动 Web UI
    start_webui()

if __name__ == "__main__":
    main()


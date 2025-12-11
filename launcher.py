#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SenseVoice 启动器
用于打包后的可执行文件，自动检查模型并启动服务
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading
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
    print("\n" + "=" * 60)
    print("正在下载模型，这可能需要几分钟...")
    print("=" * 60)
    try:
        # 尝试导入下载函数
        try:
            from download_model import download_model as dl_model
        except ImportError:
            # 如果无法导入，使用 subprocess
            subprocess.run([sys.executable, "download_model.py", "--model", "small"])
            return check_model()[0]
        
        result = dl_model("small", "./models")
        if result:
            print("\n✓ 模型下载完成")
            return True
        else:
            print("\n✗ 模型下载失败")
            return False
    except Exception as e:
        print(f"\n下载模型时出错: {e}")
        print("请检查网络连接后重试")
        return False

def open_browser():
    """延迟打开浏览器"""
    time.sleep(3)  # 等待服务启动
    try:
        webbrowser.open('http://localhost:7860')
        print("\n✓ 浏览器已自动打开")
    except Exception as e:
        print(f"\n无法自动打开浏览器: {e}")
        print("请手动访问: http://localhost:7860")

def start_webui():
    """启动 Web UI"""
    print("\n" + "=" * 60)
    print("正在启动 SenseVoice Web 界面...")
    print("=" * 60)
    print("\n访问地址: http://localhost:7860")
    print("如果没有自动打开浏览器，请手动访问上述地址")
    print("\n按 Ctrl+C 停止服务\n")
    
    # 在后台线程中打开浏览器
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    try:
        # 导入并启动 webui
        from webui import main
        main()
    except KeyboardInterrupt:
        print("\n\n程序已停止")
    except Exception as e:
        print(f"\n启动失败: {e}")
        import traceback
        traceback.print_exc()
        input("\n按 Enter 键退出...")

def main():
    """主函数"""
    print("=" * 60)
    print("SenseVoice 语音识别系统")
    print("=" * 60)
    print()
    
    # 检查模型
    model_exists, model_path = check_model()
    
    if not model_exists:
        print("⚠️  检测到模型文件不存在")
        print()
        print("首次使用需要下载模型文件（约 900MB）")
        print("需要网络连接，下载时间取决于网速")
        print()
        
        # 在 GUI 环境下，可能需要不同的输入方式
        try:
            response = input("是否现在下载模型? (y/n): ").strip().lower()
        except:
            # 如果无法获取输入（如打包后的应用），直接尝试下载
            response = 'y'
            print("自动开始下载模型...")
        
        if response == 'y' or response == '':
            if not download_model():
                print("\n模型下载失败")
                print("请检查网络连接后重新运行程序")
                input("\n按 Enter 键退出...")
                return
        else:
            print("\n需要模型文件才能运行")
            print("请稍后重新运行程序并下载模型")
            input("\n按 Enter 键退出...")
            return
    
    print(f"✓ 模型已就绪: {model_path}")
    print()
    
    # 启动 Web UI
    start_webui()

if __name__ == "__main__":
    main()


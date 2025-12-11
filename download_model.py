#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SenseVoice 模型下载脚本
支持下载 SenseVoiceSmall 和 SenseVoiceMedium 模型
"""

import os
import argparse
from modelscope.hub.snapshot_download import snapshot_download


def download_model(model_name="small", cache_dir="./models"):
    """
    下载 SenseVoice 模型
    
    Args:
        model_name: 模型大小，可选 "small" 或 "medium"
        cache_dir: 模型缓存目录
    """
    # 模型映射
    model_map = {
        "small": "iic/SenseVoiceSmall",
        "medium": "iic/SenseVoiceMedium"
    }
    
    if model_name not in model_map:
        print(f"错误: 不支持的模型名称 '{model_name}'")
        print(f"支持的模型: {', '.join(model_map.keys())}")
        return None
    
    model_id = model_map[model_name]
    
    print(f"开始下载模型: {model_id}")
    print(f"保存目录: {os.path.abspath(cache_dir)}")
    print("这可能需要一些时间，请耐心等待...")
    
    try:
        model_dir = snapshot_download(
            model_id, 
            cache_dir=cache_dir,
            revision="master"
        )
        print(f"\n✓ 模型下载完成!")
        print(f"模型路径: {model_dir}")
        return model_dir
    except Exception as e:
        print(f"\n✗ 下载失败: {str(e)}")
        print("\n提示:")
        print("1. 检查网络连接")
        print("2. 如果在中国大陆，可能需要配置代理或使用镜像源")
        print("3. 确保有足够的磁盘空间")
        return None


def main():
    parser = argparse.ArgumentParser(description="下载 SenseVoice 模型")
    parser.add_argument(
        "--model", 
        type=str, 
        default="small",
        choices=["small", "medium"],
        help="要下载的模型大小 (默认: small)"
    )
    parser.add_argument(
        "--cache_dir",
        type=str,
        default="./models",
        help="模型缓存目录 (默认: ./models)"
    )
    
    args = parser.parse_args()
    
    download_model(args.model, args.cache_dir)


if __name__ == "__main__":
    main()


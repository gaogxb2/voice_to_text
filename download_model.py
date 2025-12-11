#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SenseVoice 模型下载脚本
支持下载 SenseVoiceSmall 和 SenseVoiceMedium 模型
支持配置镜像源以加速下载
"""

import os
import argparse
from modelscope.hub.snapshot_download import snapshot_download

# 配置 ModelScope 镜像源（如果需要）
def setup_mirror():
    """配置 ModelScope 镜像源"""
    # 检查环境变量
    mirror_url = os.environ.get('MODELSCOPE_MIRROR')
    
    if mirror_url:
        print(f"使用镜像源: {mirror_url}")
        # 设置 ModelScope 的镜像源
        os.environ['MODELSCOPE_ENVIRONMENT'] = 'cn'
        return mirror_url
    
    # 如果没有设置，尝试使用默认的国内镜像
    # ModelScope 会自动检测并使用国内镜像（如果可用）
    return None


def download_model(model_name="small", cache_dir="./models", use_mirror=False):
    """
    下载 SenseVoice 模型
    
    Args:
        model_name: 模型大小，可选 "small" 或 "medium"
        cache_dir: 模型缓存目录
        use_mirror: 是否使用镜像源
    """
    # 配置镜像源
    if use_mirror:
        setup_mirror()
    
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
    if use_mirror:
        print("使用镜像源加速下载...")
    print("这可能需要一些时间，请耐心等待...")
    
    try:
        # 如果使用镜像，设置环境变量
        if use_mirror:
            os.environ['MODELSCOPE_ENVIRONMENT'] = 'cn'
        
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
        print("2. 如果在中国大陆，尝试使用 --mirror 参数:")
        print("   python download_model.py --model small --mirror")
        print("3. 或设置环境变量:")
        print("   export MODELSCOPE_ENVIRONMENT=cn")
        print("   python download_model.py --model small")
        print("4. 确保有足够的磁盘空间")
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
    parser.add_argument(
        "--mirror",
        action="store_true",
        help="使用国内镜像源加速下载（推荐在中国大陆使用）"
    )
    
    args = parser.parse_args()
    
    download_model(args.model, args.cache_dir, args.mirror)


if __name__ == "__main__":
    main()


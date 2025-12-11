#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SenseVoice 使用示例
支持音频文件的语音识别
"""

import os
import argparse
from funasr import AutoModel


def transcribe_audio(audio_path, model_dir=None, model_name="small"):
    """
    转录音频文件
    
    Args:
        audio_path: 音频文件路径
        model_dir: 模型目录路径（如果为None，将自动下载）
        model_name: 模型名称，可选 "small" 或 "medium"
    
    Returns:
        识别结果文本
    """
    # 检查音频文件是否存在
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"音频文件不存在: {audio_path}")
    
    # 模型映射
    model_map = {
        "small": "iic/SenseVoiceSmall",
        "medium": "iic/SenseVoiceMedium"
    }
    
    if model_name not in model_map:
        raise ValueError(f"不支持的模型名称: {model_name}")
    
    model_id = model_map[model_name]
    
    print(f"加载模型: {model_id}")
    if model_dir:
        print(f"使用本地模型: {model_dir}")
    
    # 初始化模型
    # 如果提供了 model_dir，使用本地模型；否则自动下载
    if model_dir and os.path.exists(model_dir):
        model = AutoModel(
            model=model_dir,
            device="cpu",  # 使用 CPU，如果有 GPU 可改为 "cuda"
            vad_model="fsmn-vad",
            punc_model="ct-punc",
        )
    else:
        model = AutoModel(
            model=model_id,
            device="cpu",
            vad_model="fsmn-vad",
            punc_model="ct-punc",
        )
    
    print(f"正在识别音频: {audio_path}")
    
    # 执行识别
    result = model.generate(input=audio_path)
    
    # 提取文本结果
    if result and len(result) > 0:
        text = result[0].get("text", "")
        return text
    else:
        return "识别失败，未返回结果"


def main():
    parser = argparse.ArgumentParser(description="使用 SenseVoice 进行语音识别")
    parser.add_argument(
        "--audio_path",
        type=str,
        required=True,
        help="音频文件路径"
    )
    parser.add_argument(
        "--model_dir",
        type=str,
        default=None,
        help="本地模型目录路径（可选，如果不提供将自动下载）"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="small",
        choices=["small", "medium"],
        help="模型大小 (默认: small)"
    )
    
    args = parser.parse_args()
    
    try:
        result = transcribe_audio(
            args.audio_path,
            model_dir=args.model_dir,
            model_name=args.model
        )
        
        print("\n" + "="*50)
        print("识别结果:")
        print("="*50)
        print(result)
        print("="*50)
        
    except Exception as e:
        print(f"错误: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())


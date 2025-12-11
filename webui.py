#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SenseVoice Web UI
提供图形界面进行语音识别
"""

import os
import gradio as gr
from funasr import AutoModel


# 全局模型变量
model = None
model_name = "small"


def load_model(model_dir=None, selected_model="small"):
    """加载模型"""
    global model, model_name
    
    model_map = {
        "small": "iic/SenseVoiceSmall",
        "medium": "iic/SenseVoiceMedium"
    }
    
    model_name = selected_model
    model_id = model_map[selected_model]
    
    try:
        if model_dir and os.path.exists(model_dir):
            model = AutoModel(
                model=model_dir,
                device="cpu",
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
        return "✓ 模型加载成功"
    except Exception as e:
        return f"✗ 模型加载失败: {str(e)}"


def transcribe(audio_file, model_dir_input):
    """转录音频"""
    global model
    
    if model is None:
        return "错误: 请先加载模型"
    
    if audio_file is None:
        return "错误: 请上传音频文件或录制音频"
    
    try:
        result = model.generate(input=audio_file)
        
        if result and len(result) > 0:
            text = result[0].get("text", "")
            return text
        else:
            return "识别失败，未返回结果"
    except Exception as e:
        return f"识别错误: {str(e)}"


def transcribe_realtime(audio, auto_submit):
    """实时转录音频（录音后自动识别）"""
    global model
    
    if model is None:
        return "错误: 请先加载模型", None
    
    if audio is None:
        return "等待录音...", None
    
    try:
        import tempfile
        import numpy as np
        import soundfile as sf
        
        # 处理不同的音频输入格式
        if isinstance(audio, tuple):
            # Gradio Audio 返回格式: (sample_rate, audio_data)
            sample_rate, audio_data = audio
            # 转换为 numpy 数组
            if isinstance(audio_data, list):
                audio_data = np.array(audio_data, dtype=np.float32)
            elif not isinstance(audio_data, np.ndarray):
                audio_data = np.array(audio_data, dtype=np.float32)
            
            # 如果是单声道，确保是 1D 数组
            if len(audio_data.shape) > 1 and audio_data.shape[0] == 1:
                audio_data = audio_data[0]
            
            # 保存为临时文件
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            tmp_file.close()
            sf.write(tmp_file.name, audio_data, sample_rate)
            audio_path = tmp_file.name
        elif isinstance(audio, str):
            # 如果是文件路径
            audio_path = audio
        elif isinstance(audio, dict):
            # Gradio 可能返回字典格式
            audio_path = audio.get("name") or audio.get("path")
            if not audio_path:
                return "错误: 无法获取音频文件路径", None
        else:
            return f"错误: 不支持的音频格式: {type(audio)}", None
        
        # 执行识别
        result = model.generate(input=audio_path)
        
        if result and len(result) > 0:
            text = result[0].get("text", "")
            return text, audio_path
        else:
            return "识别失败，未返回结果", audio_path
    except Exception as e:
        import traceback
        error_msg = f"识别错误: {str(e)}\n{traceback.format_exc()}"
        return error_msg, None


def create_interface():
    """创建 Gradio 界面"""
    with gr.Blocks(title="SenseVoice 语音识别") as demo:
        gr.Markdown("# SenseVoice 语音识别系统")
        gr.Markdown("支持实时录音识别和音频文件上传识别")
        
        with gr.Row():
            with gr.Column():
                model_selector = gr.Radio(
                    choices=["small", "medium"],
                    value="small",
                    label="选择模型"
                )
                model_dir_input = gr.Textbox(
                    label="本地模型路径（可选）",
                    placeholder="例如: ./models/iic/SenseVoiceSmall",
                    value="./models/iic/SenseVoiceSmall"
                )
                load_btn = gr.Button("加载模型", variant="primary")
                model_status = gr.Textbox(label="模型状态", interactive=False)
        
        with gr.Tabs():
            with gr.TabItem("🎤 实时录音识别"):
                gr.Markdown("### 点击下方录音按钮，开始说话，录音结束后自动识别")
                with gr.Row():
                    with gr.Column():
                        realtime_audio = gr.Audio(
                            label="实时录音",
                            type="numpy",
                            sources=["microphone"],
                            format="wav"
                        )
                        auto_submit = gr.Checkbox(
                            label="录音后自动识别",
                            value=True
                        )
                        realtime_transcribe_btn = gr.Button("开始识别", variant="primary")
                    with gr.Column():
                        realtime_output = gr.Textbox(
                            label="识别结果",
                            lines=10,
                            interactive=False
                        )
                        realtime_audio_playback = gr.Audio(
                            label="录音回放",
                            type="filepath",
                            interactive=False
                        )
            
            with gr.TabItem("📁 上传音频文件"):
                gr.Markdown("### 上传音频文件进行识别")
                with gr.Row():
                    with gr.Column():
                        audio_input = gr.Audio(
                            label="上传音频文件",
                            type="filepath",
                            sources=["upload"]
                        )
                        transcribe_btn = gr.Button("开始识别", variant="primary")
                    with gr.Column():
                        output_text = gr.Textbox(
                            label="识别结果",
                            lines=10,
                            interactive=False
                        )
        
        # 绑定事件
        load_btn.click(
            fn=load_model,
            inputs=[model_dir_input, model_selector],
            outputs=model_status
        )
        
        transcribe_btn.click(
            fn=transcribe,
            inputs=[audio_input, model_dir_input],
            outputs=output_text
        )
        
        # 实时录音识别
        realtime_transcribe_btn.click(
            fn=transcribe_realtime,
            inputs=[realtime_audio, auto_submit],
            outputs=[realtime_output, realtime_audio_playback]
        )
        
        # 如果启用自动识别，录音结束后自动触发
        realtime_audio.change(
            fn=transcribe_realtime,
            inputs=[realtime_audio, auto_submit],
            outputs=[realtime_output, realtime_audio_playback]
        )
        
        # 自动加载默认模型
        demo.load(
            fn=load_model,
            inputs=[model_dir_input, model_selector],
            outputs=model_status
        )
    
    return demo


def main():
    """主函数"""
    print("启动 SenseVoice Web UI...")
    print("访问地址: http://localhost:7860")
    
    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )


if __name__ == "__main__":
    main()


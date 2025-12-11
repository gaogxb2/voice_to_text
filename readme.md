# SenseVoice 本地离线部署

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

一个完整的 SenseVoice 语音识别本地离线部署方案，支持实时录音识别和音频文件上传识别。

## ✨ 特性

- 🎤 **实时录音识别** - 支持麦克风实时录音和自动识别
- 📁 **文件上传识别** - 支持上传音频文件进行识别
- 🔒 **完全离线** - 模型下载后无需网络连接
- 🌐 **Web 界面** - 友好的 Gradio Web UI
- 💻 **命令行工具** - 支持命令行批量处理
- 🚀 **易于部署** - 一键安装脚本，开箱即用
- 📦 **可执行文件** - 支持打包成 .exe/.app，无需安装 Python

## 📋 简介

SenseVoice 是阿里达摩院开发的语音识别模型，支持：
- 自动语音识别（ASR）
- 语言识别（LID）
- 语音情感识别（SER）
- 音频事件检测（AED）

## 系统要求

- Python 3.8 或更高版本
- 至少 4GB 可用内存（推荐 8GB+）
- 足够的磁盘空间用于存储模型文件（约 2-5GB）

## 部署步骤

### 1. 创建虚拟环境

推荐使用 conda 或 venv 创建独立的 Python 环境：

```bash
# 使用 conda
conda create -n sensevoice python=3.8
conda activate sensevoice

# 或使用 venv
python -m venv sensevoice_env
source sensevoice_env/bin/activate  # Linux/Mac
# sensevoice_env\Scripts\activate  # Windows
```

### 2. 安装依赖

**稳定版配置（推荐）：**
```bash
pip install -r requirements.txt
```

**最新版配置（使用 PyTorch 2.3.0+ 和 NumPy 2.0+）：**
```bash
pip install -r requirements_latest.txt
```

> 💡 **选择建议**：
> - **生产环境/稳定性优先**：使用 `requirements.txt`（PyTorch 2.2.2 + NumPy 1.26.4）
> - **新项目/追求最新技术**：使用 `requirements_latest.txt`（PyTorch 2.3.0+ + NumPy 2.0+）

如果在中国大陆，建议使用国内镜像源：

```bash
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com
```

### 3. 下载模型

运行下载脚本：

```bash
# 基本用法
python download_model.py

# 如果在中国大陆，使用镜像源加速（推荐）
python download_model.py --mirror

# 或设置环境变量
export MODELSCOPE_ENVIRONMENT=cn  # Linux/macOS
# set MODELSCOPE_ENVIRONMENT=cn    # Windows CMD
python download_model.py
```

> 💡 **镜像源配置**: 如果下载失败，请查看 [配置镜像源.md](配置镜像源.md) 了解详细配置方法。

或者手动下载模型：

```python
from modelscope.hub.snapshot_download import snapshot_download

# 下载 SenseVoiceSmall 模型（较小，适合快速测试）
model_dir = snapshot_download("iic/SenseVoiceSmall", cache_dir='./models')

# 或下载 SenseVoiceMedium 模型（性能更好）
# model_dir = snapshot_download("iic/SenseVoiceMedium", cache_dir='./models')
```

### 4. 使用示例

#### 方式一：使用 Python API

```bash
python example_usage.py --audio_path your_audio.wav
```

#### 方式二：使用 Web UI

```bash
python webui.py
```

然后在浏览器中访问 `http://localhost:7860`

## 📦 打包成可执行文件

为了让非技术用户也能使用，可以将项目打包成可执行文件：

### 快速打包

**macOS/Linux:**
```bash
./build.sh
```

**Windows:**
```cmd
build.bat
```

### 详细说明

查看 [打包说明.md](打包说明.md) 了解详细的打包步骤和选项。

打包后的文件：
- **Windows**: `dist/SenseVoice.exe`
- **macOS**: `dist/SenseVoice.app`
- **Linux**: `dist/SenseVoice`

### 用户使用

打包后的可执行文件可以直接分发给用户：
1. 双击运行（首次需要网络下载模型）
2. 自动打开浏览器使用 Web 界面
3. 无需安装 Python 或任何依赖

详细用户说明请查看 [README_用户使用说明.txt](README_用户使用说明.txt)

## 项目结构

```
voice_to_text/
├── readme.md              # 本文件
├── requirements.txt       # Python 依赖
├── download_model.py      # 模型下载脚本
├── example_usage.py       # 使用示例
├── webui.py              # Web 界面
├── launcher.py           # 启动器（用于打包）
├── build.sh / build.bat   # 打包脚本
├── build.spec            # PyInstaller 配置
├── 打包说明.md            # 打包详细指南
├── README_用户使用说明.txt # 最终用户说明
└── models/               # 模型文件存储目录（自动创建）
```

## 常见问题

### Q: 模型下载失败怎么办？

A: 确保网络连接正常，或使用国内镜像源。也可以手动从 ModelScope 下载模型文件。

### Q: 内存不足怎么办？

A: 使用较小的模型（SenseVoiceSmall），或增加系统内存。

### Q: 如何离线使用？

A: 下载模型后，确保 `cache_dir` 指向本地模型目录，程序将自动使用本地模型，无需网络连接。

## 📚 参考资源

- [SenseVoice GitHub](https://github.com/FunAudioLLM/SenseVoice)
- [ModelScope 模型页面](https://www.modelscope.cn/models/iic/SenseVoiceSmall)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

请参考 SenseVoice 官方许可证。

## ⭐ Star History

如果这个项目对您有帮助，请给个 Star ⭐️


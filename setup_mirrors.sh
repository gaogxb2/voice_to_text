#!/bin/bash
# 一键配置国内镜像源脚本 (Linux/macOS)

echo "=========================================="
echo "配置国内镜像源"
echo "=========================================="
echo ""

# 配置 pip 镜像源
echo "1. 配置 pip 镜像源..."
mkdir -p ~/.pip

cat > ~/.pip/pip.conf << 'EOF'
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple/
[install]
trusted-host = pypi.tuna.tsinghua.edu.cn
EOF

echo "✓ pip 镜像源已配置为: 清华大学镜像"
echo ""

# 配置 ModelScope 镜像源
echo "2. 配置 ModelScope 镜像源..."
if [ -f ~/.bashrc ]; then
    if ! grep -q "MODELSCOPE_ENVIRONMENT" ~/.bashrc; then
        echo 'export MODELSCOPE_ENVIRONMENT=cn' >> ~/.bashrc
        echo "✓ 已添加到 ~/.bashrc"
    else
        echo "✓ ~/.bashrc 中已存在配置"
    fi
fi

if [ -f ~/.zshrc ]; then
    if ! grep -q "MODELSCOPE_ENVIRONMENT" ~/.zshrc; then
        echo 'export MODELSCOPE_ENVIRONMENT=cn' >> ~/.zshrc
        echo "✓ 已添加到 ~/.zshrc"
    else
        echo "✓ ~/.zshrc 中已存在配置"
    fi
fi

echo ""
echo "=========================================="
echo "配置完成！"
echo "=========================================="
echo ""
echo "请运行以下命令使配置生效:"
echo "  source ~/.bashrc  # 如果使用 bash"
echo "  source ~/.zshrc   # 如果使用 zsh"
echo ""
echo "或重新打开终端"
echo ""
echo "现在可以使用以下命令下载模型:"
echo "  python download_model.py --model small --mirror"
echo ""


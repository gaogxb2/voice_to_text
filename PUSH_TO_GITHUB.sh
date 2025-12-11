#!/bin/bash
# GitHub 推送脚本
# 使用方法: ./PUSH_TO_GITHUB.sh YOUR_USERNAME REPO_NAME

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "使用方法: ./PUSH_TO_GITHUB.sh YOUR_USERNAME REPO_NAME"
    echo "例如: ./PUSH_TO_GITHUB.sh xianbo voice_to_text"
    exit 1
fi

USERNAME=$1
REPO_NAME=$2

echo "正在设置 GitHub 远程仓库..."
echo "仓库地址: https://github.com/$USERNAME/$REPO_NAME"

# 添加远程仓库
git remote add origin https://github.com/$USERNAME/$REPO_NAME.git 2>/dev/null || \
git remote set-url origin https://github.com/$USERNAME/$REPO_NAME.git

# 设置分支为 main
git branch -M main

echo ""
echo "请先在 GitHub 上创建仓库: https://github.com/new"
echo "仓库名称: $REPO_NAME"
echo ""
read -p "仓库已创建？(y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "正在推送代码..."
    git push -u origin main
    echo ""
    echo "✓ 代码已成功推送到 GitHub!"
    echo "访问: https://github.com/$USERNAME/$REPO_NAME"
else
    echo "请先创建仓库，然后重新运行此脚本"
fi


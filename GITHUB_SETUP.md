# GitHub 仓库设置指南

## 步骤 1: 在 GitHub 上创建新仓库

1. 登录 GitHub
2. 点击右上角的 "+" 号，选择 "New repository"
3. 填写仓库信息：
   - Repository name: `voice_to_text` (或您喜欢的名称)
   - Description: `SenseVoice 本地离线部署 - 支持实时录音识别和文件上传识别`
   - 选择 Public 或 Private
   - **不要**勾选 "Initialize this repository with a README"（因为我们已经有了）
4. 点击 "Create repository"

## 步骤 2: 推送代码到 GitHub

在终端中执行以下命令（将 `YOUR_USERNAME` 替换为您的 GitHub 用户名）：

```bash
# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/voice_to_text.git

# 或者使用 SSH（如果您配置了 SSH key）
# git remote add origin git@github.com:YOUR_USERNAME/voice_to_text.git

# 推送代码
git branch -M main
git push -u origin main
```

## 步骤 3: 验证

访问您的 GitHub 仓库页面，确认所有文件都已成功上传。

## 后续更新

如果以后需要更新代码：

```bash
git add .
git commit -m "更新说明"
git push
```


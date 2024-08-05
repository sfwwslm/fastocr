#!/bin/bash
# 构建Docker镜像脚本

echo "从 pyproject.toml 读取版本号..."

VERSION=$(python3 scripts/get_version.py)

echo "Version: $VERSION"

echo "开始构建镜像..."
sudo docker build -t "fastocr:$VERSION" .

echo "查看镜像列表..."
sudo docker images

echo "构建完成!"
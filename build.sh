#!/bin/bash
# 构建Docker镜像脚本

echo "从 pyproject.toml 读取版本号..."

version=$(awk -F' *= *' '/^version *= */ {gsub(/"/, "", $2); print $2}' pyproject.toml)

echo "Version: $version"

echo "开始构建镜像..."
sudo docker build -t "fastocr:$version" .

echo "查看镜像列表..."
sudo docker images

echo "构建完成!"
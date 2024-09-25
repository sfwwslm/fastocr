#!/bin/bash

echo "从 pyproject.toml 读取版本号..."

version=$(awk -F' *= *' '/^version *= */ {gsub(/"/, "", $2); print $2}' pyproject.toml)
name=$(awk -F' *= *' '/^name *= */ {gsub(/"/, "", $2); print $2}' pyproject.toml)

# 检查版本号和项目名称是否成功读取
if [ -z "$version" ]; then
    echo "Error: 版本号未找到."
    exit 1
fi

if [ -z "$name" ]; then
    echo "Error: 项目名称未找到."
    exit 1
fi

echo "项目名称: $name"
echo "版本号: $version"

echo "开始构建镜像..."

if sudo docker build -t "$name:$version" .; then
    echo "镜像构建成功: $name:$version"
else
    echo "Error: 镜像构建失败."
    exit 1
fi

echo "查看镜像列表..."
sudo docker images | grep "$name"

echo "构建完成!"

if [ "$1" == "save" ]; then 
    echo "开始保存镜像..."

    # 保存并压缩镜像
    if sudo docker save "$name:$version" | gzip > "$name-$version.tar.gz"; then
        echo "镜像保存成功: $name-$version.tar.gz，可以使用 docker load -i $name-$version.tar.gz 命令加载镜像"
    else
        echo "Error: 镜像保存失败."
        exit 1
    fi
fi

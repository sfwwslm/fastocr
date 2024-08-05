### Docker
- 构建docker镜像
    ```shell
    sudo docker build -t fastocr:0.0.1 . && sudo docker images
    ```
- 启动容器
    ```
    sudo docker run -d --name fastocr -p 20000:20000 --restart always fastocr:0.0.1
    ```

- `sudo docker stop fastocr && sudo docker rm fastocr && sudo docker rmi fastocr`
- `sudo docker logs -f fastocr`
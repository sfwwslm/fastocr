### Docker
- 构建docker镜像
    ```shell
    sudo docker build -t fastocr .
    ```
- 启动容器
    ```
    docker run -d --name fastocr -p 20000:20000 --restart always fastocr
    ```

- `sudo docker stop fastocr && sudo docker rmi fastocr && sudo docker rm fastocr`
- `sudo docker logs -f fastocr`
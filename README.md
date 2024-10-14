# Docker

## 构建docker镜像

```shell
sudo docker build -t fastocr:0.0.1 . && sudo docker images
```

## 启动容器

```shell
sudo docker run -d --name fastocr -p 20000:20000 --restart always fastocr
```

## 调试

- `sudo docker stop fastocr && sudo docker rm fastocr && sudo docker rmi fastocr`
- `sudo docker logs -f fastocr`

## Nginx Proxy

```conf
# ssl证书地址
ssl_certificate     /etc/nginx/ssl/private.pem;
ssl_certificate_key  /etc/nginx/ssl/private.key;
    
# ssl验证相关配置
ssl_session_timeout  5m;
ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;

ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3; # Dropping SSLv3, ref: POODLE
ssl_prefer_server_ciphers on;

ssl_session_cache shared:SSL:10m;  # 10MB 共享缓存
ssl_session_tickets off;          # 如果不需要会话票据可以禁用，以提高安全性

server {
    listen       8020 ssl;
    server_name  10.121.111.125;

    location / {
        proxy_pass http://127.0.0.1:20000;
    }
}
```

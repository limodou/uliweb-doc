# Nginx配置例子

## 反代例子
```
server {
    listen 80;
    server_name xxx;
    location / {
        proxy_pass http://localhost:3000/;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Server $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    #static files
    location ~ ^/static/ {
        root /home/xxx/xxx/export/;
    }
    #favicon
    location = /favicon.ico {
        alias /home/xxx/xxx/favicon.ico;
    }
}
```
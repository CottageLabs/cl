# Serve the basics to initialise SSL from certbot
server {
    listen 80;

    server_name cottagelabs.com;
    root /home/cloo/cl/serve/;

    # Block .git and other hidden files (except .well-known for SSL)
    location ~ /\.(?!well-known).* {
        deny all;
        access_log off;
        log_not_found off;
    }

    location / {
        try_files /$uri /$uri.html /index.html /404 =404;
        add_header Access-Control-Allow-Origin *;
    }
}

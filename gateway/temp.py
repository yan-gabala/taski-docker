server {
  listen 80;

  # Запросы по адресам /api/... перенаправляй в контейнер backend
  location /api/ {
    # Это и есть нужная строка:
    # при перенаправлении запроса в контейнер backend
    # подменить адрес "backend" в заголовке запроса 
    # на тот адрес, который пользователь ввёл в браузере
    proxy_set_header Host $http_host;
    proxy_pass http://backend:8000/api/;
  }
  location /admin/ {
    # И в этом блоке то же самое:
    proxy_set_header Host $http_host;
    proxy_pass http://backend:8000/admin/;
  }

  location / {
    alias /staticfiles/;
    index index.html;
  }
}


# Файл docker-compose.yml
version: '3'

volumes:
  pg_data:
  # Новый volume — для статических файлов
  static:

services:
  db:
    image: postgres:13.10
    env_file: .env
    volumes:
      - pg_data:/var/lib/postgresql/data
  backend:
    build: ./backend/
    env_file: .env
    # Тут подключаем volume к backend
    volumes:
      - static:/backend_static
  frontend:
    env_file: .env
    build: ./frontend/
  gateway:
    build: ./gateway/
    # А тут подключаем volume со статикой к gateway
    volumes:
      - static:/staticfiles/
    ports:
      - 8000:80



# docker-compose.yml
version: '3'

volumes:
  pg_data:
  static:

services:
  db:
    image: postgres:13
    env_file: .env
    volumes:
      - pg_data:/var/lib/postgresql/data
  backend:
    build: ./backend/
    env_file: .env
    volumes:
      - static:/backend_static

  frontend:
    env_file: .env
    build: ./frontend/
    command: cp -r /app/build/. /frontend_static/
    volumes:
      - static:/frontend_static

  gateway:
    build: ./nginx/
    env_file: .env
    volumes:
      - static:/staticfiles
    ports:
      - 8000:80
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt && pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
COPY . .
EXPOSE 8000
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]


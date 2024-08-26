FROM python:3.12.4

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN ln -snf /usr/share/zoneinfo/Asia/Yekaterinburg /etc/localtime && echo "Asia/Yekaterinburg" > /etc/timezone

COPY . .

ENTRYPOINT ["python", "Telegramm.py"]


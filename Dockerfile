FROM python:3.9.5-buster
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
RUN touch out.txt
CMD ["python", "main.py", "listen"]

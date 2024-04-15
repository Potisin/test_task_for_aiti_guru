FROM python:3.11

RUN mkdir /test_task_for_aiti_guru

WORKDIR /test_task_for_aiti_guru

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD uvicorn main:app --host 0.0.0.0 --reload

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest", "tests/tests_ui/", "-n", "3", "--alluredir=allure-results", "-v"]
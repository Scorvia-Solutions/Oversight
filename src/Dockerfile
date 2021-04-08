FROM python:3
LABEL "repository"="https://github.com/Scorvia-Solutions/Oversight"
LABEL "maintainer"="Scorvia Solutions"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "./main.py" ]
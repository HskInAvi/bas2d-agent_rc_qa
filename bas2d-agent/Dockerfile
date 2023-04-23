FROM python:3.9

ADD . .

RUN python3 -m pip install -r test-requirements.txt --extra-index-url=https://avikus:avi1357\!\!@pypi.avikuslab.com

CMD ["python3", "/app/main.py"]
FROM snakepacker/python:all as builder

RUN python3.9 -m venv /usr/share/python3/app
RUN /usr/share/python3/app/bin/pip install -U pip

COPY requirements.txt /mnt/
RUN /usr/share/python3/app/bin/pip install -Ur /mnt/requirements.txt

COPY /dist/dia-0.0.1-py3-none-any.whl /usr/share/python3/app/bin
RUN /usr/share/python3/app/bin/pip install /usr/share/python3/app/bin/dia-0.0.1-py3-none-any.whl

RUN /usr/share/python3/app/bin/pip check

FROM snakepacker/python:3.9 as api

RUN mkdir /mnt/log
COPY --from=builder /usr/share/python3/app /usr/share/python3/app


RUN ln -snf /usr/share/python3/app/bin/dia /usr/local/bin/
CMD ["dia"]

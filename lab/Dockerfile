FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8 \
    LABEL=vbox-guestctrl-copyfrom-dotdot \
    WITNESS=VBOX-GUESTCTRL-COPYFROM-DOTDOT-WITNESS

WORKDIR /lab

RUN mkdir -p /work/vbox-copy /work/oracle /work/dst-root /lab

COPY poc.py /lab/poc.py

CMD ["python3", "-c", "import time; time.sleep(10**9)"]

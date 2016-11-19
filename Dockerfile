FROM python:2.7

MAINTAINER Martin Kuchynar <matokuchy@gmail.com>

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD entrypoint.sh /
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD [ "/bin/bash" ]

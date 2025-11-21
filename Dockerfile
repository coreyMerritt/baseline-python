FROM rockylinux:9.3

WORKDIR /app

COPY "." "/app/"

RUN dnf install -y \
  python3.11 \
  python3.11-pip \
  postgresql-devel \
  gcc \
  libpq-devel &&\
  dnf clean all

RUN ln -sf /usr/bin/python3.11 /usr/bin/python3 &&\
  ln -sf /usr/bin/pip3.11 /usr/bin/pip3

CMD ["bash", "./start-with-uvicorn.sh"]

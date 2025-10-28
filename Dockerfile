FROM rockylinux:9.3
WORKDIR /app
COPY "." "/app/"
RUN dnf install -y python3.11 python3.11-pip \
  postgresql-devel gcc libpq-devel && \
  ln -sf /usr/bin/python3.11 /usr/bin/python3 && \
  ln -sf /usr/bin/pip3.11 /usr/bin/pip3 && \
  dnf clean all
CMD ["bash", "./start-with-uvicorn.sh"]

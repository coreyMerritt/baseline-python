FROM rockylinux:9.3

WORKDIR /app

RUN mkdir -p "/etc/projectname/dev" &&\
  mkdir -p "/etc/projectname/model" &&\
  mkdir -p "/etc/projectname/prod" &&\
  mkdir -p "/etc/projectname/test"

COPY "." "/app/"

COPY "./config/model/*" "/etc/projectname/model/"

RUN dnf update -y

RUN dnf install -y \
  python3.11 \
  python3.11-pip \
  sudo

RUN dnf install -y \
  gcc \
  jq \
  libpq-devel \
  postgresql-devel

RUN dnf clean all

RUN ln -sf /usr/bin/python3.11 /usr/bin/python3 &&\
  ln -sf /usr/bin/pip3.11 /usr/bin/pip3 &&\
  ln -sf /usr/bin/python3.11 /usr/bin/python && \
  ln -sf /usr/bin/pip3.11 /usr/bin/pip

RUN ./install.sh "prod"

# Install script copies .env.model -> .env, but we don't want this messing with our docker env vars
RUN rm -rf ./.env

CMD ["./start.sh", "prod"]

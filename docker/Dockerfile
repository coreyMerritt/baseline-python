FROM rockylinux:9.3

SHELL ["/bin/bash", "-c"]
WORKDIR /app

# Build Args
ARG FOO_PROJECT_NAME_DEPLOYMENT_ENVIRONMENT
ARG FOO_PROJECT_NAME_GLOBAL_CONFIG_DIR
ARG FOO_PROJECT_NAME_MODEL_CONFIG_DIR

# Validate Build Args that don't have a default
RUN [[ -n "$FOO_PROJECT_NAME_DEPLOYMENT_ENVIRONMENT" ]] || { echo "ERROR: FOO_PROJECT_NAME_DEPLOYMENT_ENVIRONMENT build arg is required" && exit 1; }
RUN [[ -n "$FOO_PROJECT_NAME_GLOBAL_CONFIG_DIR" ]] || { echo "ERROR: FOO_PROJECT_NAME_GLOBAL_CONFIG_DIR build arg is required" && exit 1; }
RUN [[ -n "$FOO_PROJECT_NAME_MODEL_CONFIG_DIR" ]] || { echo "ERROR: FOO_PROJECT_NAME_MODEL_CONFIG_DIR build arg is required" && exit 1; }

# Export Build Args
ENV FOO_PROJECT_NAME_DEPLOYMENT_ENVIRONMENT="$FOO_PROJECT_NAME_DEPLOYMENT_ENVIRONMENT"
ENV FOO_PROJECT_NAME_GLOBAL_CONFIG_DIR="$FOO_PROJECT_NAME_GLOBAL_CONFIG_DIR"
ENV FOO_PROJECT_NAME_MODEL_CONFIG_DIR="$FOO_PROJECT_NAME_MODEL_CONFIG_DIR"

COPY "." "/app/"

RUN rm -rf "./.env"

RUN dnf update -y
RUN dnf install -y \
  python3.11 \
  python3.11-pip \
  sudo
RUN dnf install -y \
  gcc
RUN dnf install -y \
  jq \
  libpq-devel \
  postgresql-devel
RUN dnf clean all

RUN ln -sf /usr/bin/python3.11 /usr/bin/python3 &&\
  ln -sf /usr/bin/pip3.11 /usr/bin/pip3 &&\
  ln -sf /usr/bin/python3.11 /usr/bin/python && \
  ln -sf /usr/bin/pip3.11 /usr/bin/pip

RUN ./install.sh ${FOO_PROJECT_NAME_DEPLOYMENT_ENVIRONMENT}

ENTRYPOINT ["./run-server.sh"]

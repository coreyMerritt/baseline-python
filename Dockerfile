FROM rockylinux:9.3

SHELL ["/bin/bash", "-c"]
WORKDIR /app

# Build Args
ARG PROJECTNAME_DEPLOYMENT_ENVIRONMENT
ARG PROJECTNAME_GLOBAL_CONFIG_DIR
ARG PROJECTNAME_MODEL_CONFIG_DIR

# Validate Build Args that don't have a default
RUN [[ -n "$PROJECTNAME_DEPLOYMENT_ENVIRONMENT" ]] || { echo "ERROR: PROJECTNAME_DEPLOYMENT_ENVIRONMENT build arg is required" && exit 1; }
RUN [[ -n "$PROJECTNAME_GLOBAL_CONFIG_DIR" ]] || { echo "ERROR: PROJECTNAME_GLOBAL_CONFIG_DIR build arg is required" && exit 1; }
RUN [[ -n "$PROJECTNAME_MODEL_CONFIG_DIR" ]] || { echo "ERROR: PROJECTNAME_MODEL_CONFIG_DIR build arg is required" && exit 1; }

# Export Build Args
ENV PROJECTNAME_DEPLOYMENT_ENVIRONMENT="$PROJECTNAME_DEPLOYMENT_ENVIRONMENT"
ENV PROJECTNAME_GLOBAL_CONFIG_DIR="$PROJECTNAME_GLOBAL_CONFIG_DIR"
ENV PROJECTNAME_MODEL_CONFIG_DIR="$PROJECTNAME_MODEL_CONFIG_DIR"

COPY "." "/app/"

RUN mkdir "./.env.d" &&\
  echo "PROJECTNAME_DEPLOYMENT_ENVIRONMENT=test" > "./.env.d/.env.test" &&\
  echo "PROJECTNAME_DEPLOYMENT_ENVIRONMENT=dev" > "./.env.d/.env.dev" &&\
  echo "PROJECTNAME_DEPLOYMENT_ENVIRONMENT=prod" > "./.env.d/.env.prod" &&\
  echo "PROJECTNAME_GLOBAL_CONFIG_DIR=${PROJECTNAME_GLOBAL_CONFIG_DIR}" > "./.env.d/.env.${PROJECTNAME_DEPLOYMENT_ENVIRONMENT}" &&\
  echo "PROJECTNAME_MODEL_CONFIG_DIR=${PROJECTNAME_MODEL_CONFIG_DIR}" > "./.env.d/.env.${PROJECTNAME_DEPLOYMENT_ENVIRONMENT}"

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

RUN ./install.sh ${PROJECTNAME_DEPLOYMENT_ENVIRONMENT}

ENTRYPOINT ["./start-server.sh", "test"]

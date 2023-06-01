FROM python:3.11-alpine

# Essentials
RUN apk update && \
    apk --no-cache add \
        gcc musl-dev linux-headers python3-dev libffi-dev \
        postgresql-dev musl-dev \
        bash \
        bash-completion \
        coreutils \
        findutils \
        gawk \
        git \
        curl \
        zip \
        py3-pip \
        openssl \
        openssh \
        ca-certificates && \
        update-ca-certificates

# Install latest Azure CLI Tools
RUN pip install --upgrade pip && \
	pip install --no-cache-dir --prefer-binary azure-cli && \
	az config set auto-upgrade.enable=yes

# Install kubectl and kubelogin using Azure CLI
RUN az aks install-cli \
    && kubectl version --client \
    && kubelogin --version

# Install helm (v3)
#ENV DESIRED_VERSION=3.8.2
RUN curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 && \
    chmod 700 get_helm.sh && \
    ./get_helm.sh && \
    helm version && \
    rm -f get_helm.sh && \
    helm plugin install https://github.com/chartmuseum/helm-push

# Install jq/yq
ENV JQ_VERSION=1.6
ENV YQ_VERSION=3.3.0
RUN curl -sSL -o /usr/local/bin/jq "https://github.com/stedolan/jq/releases/download/jq-${JQ_VERSION}/jq-linux64" \
    && curl -sSL -o /usr/local/bin/yq "https://github.com/mikefarah/yq/releases/download/${YQ_VERSION}/yq_linux_amd64" \
    && chmod +x /usr/local/bin/jq /usr/local/bin/yq

# Install others tools
RUN pip install --no-cache-dir --prefer-binary \
   rich \
   flask \
   requests \
   redis \
   psycopg2 \
   SQLAlchemy \
   Flask-SQLAlchemy \
   sqlalchemy-utils

# Entrypoint
RUN mkdir /app
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod 755 /app/entrypoint.sh

ENTRYPOINT ["/bin/bash", "-c", "/app/entrypoint.sh"]

# Build Go programs (only corrupter at the moment)
FROM golang:1-trixie AS go-build
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
RUN go install github.com/r00tman/corrupter@latest


# Build Python package and dependencies
FROM python:3.14-trixie AS python-build
RUN apt-get update && apt-get install -y \
        git \
        libffi-dev \
        gcc \
        g++ \
        libleveldb-dev \
        libsnappy-dev \
        make \
        zlib1g-dev \
        libtiff-dev \
        libfreetype6-dev \
        libpng-dev \
        libjpeg-dev \
        liblcms2-dev \
        libwebp-dev \
        libssl-dev \
        cargo \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/venv
WORKDIR /opt/venv
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip to latest version
RUN pip install --no-cache-dir --upgrade pip==25.3

RUN mkdir -p /src
WORKDIR /src

# Install bot package and dependencies
COPY . .
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir .[fast]
RUN pip install --no-cache-dir uvloop


# Package everything
FROM python:3.14-slim-trixie AS final
# Install native dependencies
RUN apt-get update && apt-get install -y \
        libffi8 \
        libleveldb1d \
        libsnappy1v5 \
        zlib1g \
        libtiff6 \
        libfreetype6 \
        libpng16-16 \
        libjpeg62-turbo \
        liblcms2-2 \
        libwebp7 \
        libssl3 \
        git \
    && rm -rf /var/lib/apt/lists/*

# Create bot user
RUN useradd -m -u 1000 pyrobud

# Create data directory for the bot user
RUN mkdir -p /data
RUN chown pyrobud:pyrobud /data

# Ensure we a volume is mounted even if the user doesn't explicitly specify it,
# to prevent unintentional data loss
VOLUME [ "/data" ]

# Copy Go programs
COPY --from=go-build /go/bin/corrupter /usr/local/bin

# Copy Python venv
ENV PATH="/opt/venv/bin:$PATH"
COPY --from=python-build /opt/venv /opt/venv

# Set runtime settings
USER pyrobud
WORKDIR /data
CMD ["pyrobud"]

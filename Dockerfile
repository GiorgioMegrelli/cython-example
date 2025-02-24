FROM ubuntu:22.04

WORKDIR /app

# Update indeces
RUN apt update

# Install components
RUN apt install -y \
    bash \
    curl \
    build-essential

# Install python components
RUN apt install -y \
    python3 \
    python3-pip

# Install python-dev components
RUN python_version=$(python3 -V | grep -oE '[0-9]+\.[0-9]+') && apt install -y \
    "python${python_version}-dev" \
    "libpython${python_version}-dev"

# Minimize size of the image
RUN rm -rf /var/lib/apt/lists/*

# Install required packaage
RUN python3 -m pip install cython

CMD ["/bin/bash"]

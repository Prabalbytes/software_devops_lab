# 1. Base Jenkins image
FROM jenkins/jenkins:lts

# 2. Switch to root to install packages
USER root

# 3. Install Python, pip, Git and virtual environment support
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv git && \
    rm -rf /var/lib/apt/lists/*

# 4. Create Python virtual environment
RUN python3 -m venv /opt/venv

# 5. Add Python tools
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir flake8 pytest

# 6. Switch back to Jenkins user
USER jenkins
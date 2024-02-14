# Source:
#   https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
FROM python:3.11.0-bullseye

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application contents
RUN mkdir templates/
COPY index.html ./templates/

# TODO Move to a dedicated directory i.e.
# WORKDIR /python-docker
# COPY . .

COPY __init__.py .
COPY frontend.py .
COPY models.py .

# Run the application:
CMD ["python", "frontend.py"]

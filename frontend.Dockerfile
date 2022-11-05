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
COPY index.html .

# Run the application:
COPY frontend.py .
CMD ["python", "frontend.py"]


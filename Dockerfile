FROM python:3.10.13

SHELL ["/bin/bash", "-c"]

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN pip install --upgrade pip

#RUN apt update && apt -qy install libpq-dev


RUN useradd -rms /bin/bash app && chmod 777 /opt /run

# Set work directory
WORKDIR /code

RUN mkdir /code/static && mkdir /code/media && chown -R app:app /code && chmod 755 /code

COPY --chown=app:app . .

RUN pip install -r requirements.txt

USER app

FROM python:3.9-slim-buster as base
RUN apt-get update
RUN apt-get install -y curl
WORKDIR /app
RUN pip install poetry
COPY poetry.toml .
COPY poetry.lock .
COPY pyproject.toml .
ENV DB_NAME=card_board
EXPOSE 5000

FROM base as production
RUN poetry config virtualenvs.create false --local && poetry install --no-dev --no-root
COPY /todo_app ./todo_app
COPY /entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
#ENV PORT=8000
ENTRYPOINT /entrypoint.sh

FROM base as development
RUN poetry install
ENTRYPOINT poetry run flask run --host=0.0.0.0

FROM base as test
RUN poetry install
RUN apt-get update -qqy && apt-get install -qqy wget gnupg unzip
# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update -qqy \
  && apt-get -qqy install google-chrome-stable \
  && rm /etc/apt/sources.list.d/google-chrome.list \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*
RUN CHROME_MAJOR_VERSION=$(google-chrome --version | sed -E "s/.* ([0-9]+)(\.[0-9]+){3}.*/\1/") \
  && CHROME_DRIVER_VERSION=$(wget --no-verbose -O - "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_MAJOR_VERSION}") \
  && echo "Using chromedriver version: "$CHROME_DRIVER_VERSION \
  && wget --no-verbose -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
  && unzip /tmp/chromedriver_linux64.zip -d /usr/bin \
  && rm /tmp/chromedriver_linux64.zip \
  && chmod 755 /usr/bin/chromedriver
COPY .env.test .
COPY tests ./tests
COPY test_e2e ./test_e2e
COPY todo_app ./todo_app
ENTRYPOINT ["poetry", "run", "pytest"]
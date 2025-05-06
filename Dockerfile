FROM python:3.8.20-bookworm

WORKDIR /open-bst

RUN apt-get update && apt-get install -y libgl1 && rm -rf /var/lib/apt/lists/*

COPY ./open-bst/lanekeeping/requirements.txt /open-bst
RUN pip install --no-cache-dir -r /open-bst/requirements.txt

COPY ./open-bst/ /open-bst

CMD ["python", "-m", "lanekeeping.udacity.run_udacity_MINE"]
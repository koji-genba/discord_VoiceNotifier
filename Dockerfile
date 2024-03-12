FROM python:3.11-slim-bookworm as builder

WORKDIR /app
COPY ./VoiceNotifier.py .
RUN mkdir data && chmod 777 data

ENV PYTHONUSERBASE=/app/__pypackages__
RUN pip --no-cache-dir install --upgrade pip && pip install --no-cache-dir --user discord

FROM gcr.io/distroless/python3-debian12:nonroot

WORKDIR /app
COPY --from=builder /app .

ENV PYTHONUSERBASE=/app/__pypackages__
CMD ["VoiceNotifier.py"]

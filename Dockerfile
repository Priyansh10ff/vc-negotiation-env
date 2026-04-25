FROM python:3.11-slim

WORKDIR /app

COPY vc_negotiation_env/ /app/vc_negotiation_env/

RUN pip install fastapi uvicorn pydantic openenv-core requests

ENV PYTHONPATH=/app

EXPOSE 7860

CMD ["uvicorn", "vc_negotiation_env.server.app:app", "--host", "0.0.0.0", "--port", "7860"]
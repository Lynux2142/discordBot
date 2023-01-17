FROM python:3
WORKDIR /app
RUN apt-get update && python -m pip install -U discord.py
ADD LynuxBot.py .
ADD config.json .
CMD ["python", "LynuxBot.py"]

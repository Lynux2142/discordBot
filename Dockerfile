FROM python:3.9.2
WORKDIR /app
RUN apt-get update && python -m pip install -U discord.py
ADD LynuxBot.py .
CMD ["python", "LynuxBot.py"]

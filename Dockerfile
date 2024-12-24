FROM python:3.10.8-slim-buster

# Install system dependencies including ALSA
RUN apt-get update && apt-get install -y \
    python3-pygame \
    libsdl2-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-ttf-2.0-0 \
    x11-xserver-utils \
    libasound2 \
    libasound2-plugins \
    pulseaudio \
    tk \
    && rm -rf /var/lib/apt/lists/*

# Configure ALSA settings
RUN mkdir -p /etc/alsa && \
    echo "pcm.!default { type null }" > /etc/asound.conf

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Configure display and audio
ENV DISPLAY=host.docker.internal:0
ENV SDL_AUDIODRIVER=alsa
ENV PULSE_SERVER=host.docker.internal

CMD ["python", "main.py"]
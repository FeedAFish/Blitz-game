FROM mcr.microsoft.com/windows/servercore:ltsc2019

# Install Chocolatey
RUN powershell -Command \
    Set-ExecutionPolicy Bypass -Scope Process -Force; \
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; \
    iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# Install Python and dependencies
RUN choco install -y python3 --version=3.10.8 && \
    choco install -y vcredist140 && \
    refreshenv

# Add Python to PATH
RUN setx /M PATH "%PATH%;C:\Python310;C:\Python310\Scripts"

# Set working directory
WORKDIR C:/app

# Copy application files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Configure environment
ENV PYTHONUNBUFFERED=1
ENV SDL_VIDEODRIVER=dummy
ENV SDL_AUDIODRIVER=dummy

# Set the entry point
CMD ["python", "main.py"]
# NuclearShield Quick Start

NuclearShield is a defensive, read-only cybersecurity assurance workstation that runs locally using Docker.

## Requirements

### Windows and macOS
Install Docker Desktop and make sure Docker is running.

### Linux
Install Docker Engine with Docker Compose support and make sure the Docker service is running.

## Windows

1. Download and extract the NuclearShield Windows package.
2. Start Docker Desktop.
3. Wait until Docker Desktop reports that the engine is running.
4. Double-click `Start-NuclearShield.bat`.
5. Wait while the required containers are prepared.
6. NuclearShield will open in your browser automatically.

To stop NuclearShield, double-click `Stop-NuclearShield.bat`.

## macOS

Open Terminal in the extracted NuclearShield folder.

First time only:

```bash
chmod +x start-nuclearshield.sh stop-nuclearshield.sh
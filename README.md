# qBittorrent Cleanup Tool

## Overview
A Python-based tool to manage qBittorrent torrents, focusing on:
- Identifying torrents without hardlinks
- Setting minimum seed time by tracker
- Marking or deleting torrents based on configurable criteria

## Features
- Manual or automatic torrent deletion
- Tracker-specific seed time requirements
- Ignore list for protected torrents
- Push notifications
- Comprehensive logging

## Prerequisites
- Docker
- qBittorrent running and accessible
- Notifarr (optional, for notifications)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/qbittorrent-cleanup.git
cd qbittorrent-cleanup
```

2. Configure `config.yaml`:
- Update qBittorrent connection details
- Set seed time requirements
- Configure notification preferences

3. Build Docker container:
```bash
docker build -t qbittorrent-cleanup .
```

4. Run the container:
```bash
docker run -d \
  -v /path/to/config:/app/config.yaml \
  -v /path/to/logs:/logs \
  qbittorrent-cleanup
```

## Configuration

See `config.yaml` for detailed configuration options:
- Tracker seed times
- Deletion mode (manual/automatic)
- Notification settings

## Contributing
Contributions welcome! Please submit pull requests or open issues.

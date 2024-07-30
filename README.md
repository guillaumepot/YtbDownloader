# YtbDownloader

A video downloader and Audio converter for Youtube.

For tests on your own content only, not provided to download illegal content.


Two versions:
- Server-client (with docker)
- App GUI (tkinter python)


<img src="./media/ytb_downloader.jpeg" width="350" height="350">


---


## Project Information

- **Version**: 0.2.0
- **Development Stage**: Prod
- **Author**: Guillaume Pot
- **Contact Information**: guillaumepot.pro@outlook.com

---


## Table of Contents
- [Repository Architecture](#repository-architecture)
- [Requirements](#requirements)
- [Changelogs](#Changelogs)
- [Roadmap](#roadmap)

---


## Repository Architecture

```
├── .github
│   │
│   └── workflows
|           |
|           ├── .env
|           |
|           └── upload_docker_images.yaml
|   
├── architecture
│        │
|        |
|        ├── app
|        |    |
|        |    ├── app_functions.py
|        |    |
|        |    ├── app.py
|        |    |
|        |    └── ytb_downloader.jpeg
|        |
│        └── client-server
|                  |
|                  ├── logs
|                  |
|                  ├── src
|                  |    |
|                  |    ├── Dockerfile
|                  |    |
|                  |    ├── requirements.txt
|                  |    |
|                  |    ├── script.py
|                  |    |
|                  |    └── streamlit
|                  |
|                  ├── storage
|                  | 
|                  ├── audio
|                  |
|                  ├── video
|                  |
|                  └── docker-compose.yaml
|        
├── changelogs
|        
├── media
|     |
|     └── ytb_downloader.jpeg
|
├── .gitignore
|
├── LICENSE
│
├── README.md
|
└── requirements.txt


```

---

## Requirements

**Server app**
    - Docker
    - Docker Compose

---

## Changelogs

[v0.2.0](./changelogs/0.2.0.md)
[v0.1.0](./changelogs/0.1.0.md)


---

## Roadmap

-
-
# YtbDownloader
A video downloader and Audio converter for Youtube.

For tests on your own content only, not provided to download illegal content.


<img src="./media/ytb_downloader.jpeg" width="350" height="350">


---


## Project Information

- **Version**: 0.1.0
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
├── logs
|        
├── changelogs
|        
├── media
|       |
|       └── ytb_downloader.jpeg
|
|
├── src
|    |
|    ├── Dockerfile
|    |
|    ├── requirements.txt
|    |
|    ├── script.py
|    |
|    └── streamlit
|
├── storage
|     |
|     ├── audio
|     |
|     └── video
|
├── utils
|     |
|     └── script_standalone.py
|
├── docker-compose.yaml
|
├── LICENSE
│
└── README.md
```

---

## Requirements

**Server app**
    - Python
    - Docker
    - Docker Compose

**Standalone**
    - Python
    - [WIP]

---

## Changelogs

[WIP]
"[v0.1.0](./changelogs/0.1.0.md)"



---

## Roadmap

**[Done]**
```
0.1.0
- First version of the app containing a script & a Streamlit UI + Dockerfile & compose

```


**[Todo]**  
```
0.1.1
- Add standalone script
```

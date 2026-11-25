# news-image-20261125-ka

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/hiduplahzomb/news-image-20261125-ka/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/hiduplahzomb/news-image-20261125-ka/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A front-page image summing up the world's news of Wednesday 25 November 2026 in one 1024×1024 PNG: a masthead with the full date, a lead story on the three oil tankers hit by mines in the Strait of Hormuz, six pictogram news panels (Putin, Trump–Iran, Ukraine's strike in Libya, Norway's $7bn Ukraine pledge, Pakistan's first astronaut, the Sarkozy Libya trial), each with a single line of detail, and an "In Brief" band (trade, Senegal, Bangladesh, Gaza). The image is drawn fresh from scratch by `render.py` (Pillow, no network); `main.py` only copies the finished `entry.png` to the output directory and verifies the copy byte-for-byte.

## Run it

```sh
python3 render.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>

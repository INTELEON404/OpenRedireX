![OpenRedirex](https://github.com/INTELEON404/Template/blob/main/SVG/carbon.png?raw=true)


---

## 🧠 About OpenRedireX

**OpenRedireX** is a lightweight, high-performance fuzzer designed to identify **Open Redirect vulnerabilities** in modern web applications.

It focuses on **accuracy over noise** by using curated payloads, keyword-based fuzzing, and concurrent request handling to uncover exploitable redirect issues that are commonly missed during manual testing.

Ideal for **bug bounty hunters**, **penetration testers**, and **security researchers**.

---

## ✨ Features

- 🔍 Detects open redirects using smart payload injection
- ⚡ High-speed concurrent fuzzing
- 🎯 Keyword-based URL replacement (`FUZZ` by default)
- 🧩 Supports custom payload lists
- 📈 Progress tracking with real-time feedback
- 🧪 Designed to minimize false positives
- 🛠 Simple CLI interface

---

## 🏗 Installation

Clone the repository and run the setup script:

```sh
git clone https://github.com/INTELEON404/OpenRedireX.git
cd OpenRedireX
chmod +x setup.sh
./setup.sh
````

---

## ⛏ Usage

OpenRedireX reads URLs from **stdin** and replaces a keyword with redirect payloads.

### Command Syntax

```sh
openredirex [-p payloads] [-k keyword] [-c concurrency]
```

### Options

* `-p`, `--payloads`
  File containing redirect payloads
  *(default: built-in payload list)*

* `-k`, `--keyword`
  Keyword in URL to replace
  *(default: FUZZ)*

* `-c`, `--concurrency`
  Number of concurrent requests
  *(default: 100)*

---

## 📌 Example

### Input URLs

```txt
https://newsroom.example.com/logout?redirect=FUZZ
https://auth.example.com/logout?redirect_uri=FUZZ
https://example.com/page?next=FUZZ
```

### Run the fuzzer

```sh
cat urls.txt | openredirex -p payloads.txt -k FUZZ -c 50
```

The tool will replace `FUZZ` with each payload and test for unsafe redirects concurrently.

---

## 📦 Dependencies

OpenRedireX uses the following libraries:

* `argparse`
* `asyncio`
* `aiohttp`
* `concurrent.futures`
* `tqdm`

Install required external dependencies:

```sh
pip install aiohttp tqdm
```

---

## ⚠ Disclaimer

This tool is intended **for educational and authorized security testing only**.
Do **not** use OpenRedireX against systems without explicit permission.
The author is not responsible for misuse.

---

## 👤 Author

* GitHub: [https://github.com/INTELEON404](https://github.com/INTELEON404)
* Github: [https://github.com/devanshbatham](https://github.com/devanshbatham)


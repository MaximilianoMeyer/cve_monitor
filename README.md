# CVE Monitor

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Description

CVE Monitor is an automated vulnerability monitoring tool that tracks new Common Vulnerabilities and Exposures (CVEs) from the National Vulnerability Database (NVD) and sends real-time notifications via Telegram. It helps security teams and developers stay informed about newly published vulnerabilities with CVSS scores and detailed descriptions.

## Features

- 🔍 Automatic CVE monitoring from NVD
- 📱 Real-time Telegram notifications with formatted alerts
- ⏱️ Configurable check intervals for flexibility
- 🎯 Customizable daily CVE limits
- 📊 CVSS scores included in notifications
- 📝 Detailed logging of all operations
- 🎥 YouTube channel monitoring (bonus feature)
- 🧵 Support for Telegram topic threads

## Tech Stack

- **Language:** Python 3.7+
- **HTTP Client:** requests
- **Configuration:** python-dotenv
- **Notifications:** Telegram Bot API

## Prerequisites

- Python 3.7 or higher
- Telegram Bot Token (obtain from [@BotFather](https://t.me/botfather))
- Telegram Chat ID where notifications will be sent
- Internet connection to access NVD API

## Getting Started

### Installation

1. Clone the repository:
```bash
git clone https://github.com/MaximilianoMeyer/cve-monitor.git
cd cve-monitor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root directory:
```bash
cp .env.example .env  # if available, or create manually
```

4. Configure your environment variables (see [Environment Variables](#environment-variables) section below)

### Running the Application

```bash
python main.py
```

When prompted, enter the maximum number of CVEs you want to receive per day. The monitor will then begin checking for new vulnerabilities and send Telegram notifications.

## Usage

### Basic Usage

1. Start the monitor:
```bash
python main.py
```

2. Enter the desired number of CVEs to monitor per day when prompted

3. The application will:
   - Check the NVD API at configured intervals (default: every hour)
   - Send Telegram notifications for each new CVE found
   - Include CVSS scores and vulnerability descriptions
   - Provide direct links to NVD details

### Notification Example

```
🚨 Nova CVE Detectada 🚨

ID: CVE-2024-XXXX
CVSS Score: 7.5
Descrição: Descrição da vulnerabilidade...
Link: https://nvd.nist.gov/vuln/detail/CVE-2024-XXXX
```

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `TELEGRAM_TOKEN` | Your Telegram bot token | Yes | - |
| `TELEGRAM_CHAT_ID` | Chat ID for CVE notifications | Yes | - |
| `CHECK_INTERVAL` | Seconds between NVD API checks | No | 3600 |
| `MESSAGE_DELAY` | Seconds delay between Telegram messages | No | 2 |
| `GITHUB_TOKEN` | GitHub token for API requests (optional) | No | - |
| `TELEGRAM_YOUTUBE_THREAD_ID` | Topic thread ID for YouTube notifications | No | - |
| `YOUTUBE_API_KEY` | YouTube API key for channel monitoring | No | - |
| `YOUTUBE_CHANNEL_IDS` | Comma-separated YouTube channel IDs to monitor | No | - |

## Project Structure

```
cve-monitor/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── monitors/
│   ├── __init__.py
│   ├── cve_monitor.py     # CVE monitoring logic
│   └── youtube_monitor.py # YouTube channel monitoring
└── utils/
    ├── __init__.py
    ├── config.py          # Configuration management
    └── logger.py          # Logging setup
```

**Directory Descriptions:**

- **monitors/**: Contains monitor implementations for CVEs and YouTube channels
- **utils/**: Utility modules for configuration loading and logging

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to improve the project. When contributing:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<p align="center">
  </a>
</p>

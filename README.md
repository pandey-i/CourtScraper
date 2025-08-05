# 🏛️ Court Data Fetcher & Mini-Dashboard

A powerful web application for scraping and displaying court case information from the Delhi High Court website. Built with Python, Flask, Selenium, and modern web technologies.

![Court Data Fetcher](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0.1-green.svg)
![Selenium](https://img.shields.io/badge/Selenium-4.8.0-orange.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Features](#-features)
- [Live Demo](#-live-demo)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🔍 Core Functionality
- **Automated Case Search** - Search cases by type, number, and filing year
- **CAPTCHA Bypass** - Automatic CAPTCHA solving using multiple methods
- **Real-time Scraping** - Live data extraction from Delhi High Court website
- **PDF Generation** - Download case details as formatted PDF reports
- **Database Logging** - Track all queries and responses for analytics

### 🎨 User Interface
- **Modern Web UI** - Beautiful, responsive design with loading animations
- **Dynamic Dropdowns** - Pre-populated case type options from the court website
- **Results Pagination** - View multiple results with client-side pagination
- **Interactive Elements** - Clickable links to case details and orders
- **Loading Animations** - Professional feedback during search operations

### 📊 Analytics & History
- **Query History** - View all previous searches with timestamps
- **Success Statistics** - Track success rates and popular case types
- **Response Logging** - Store raw HTML responses for debugging
- **Performance Metrics** - Monitor scraping efficiency and errors

### 🛠️ Technical Features
- **Headless Browser** - Runs Chrome without GUI for server deployment
- **Anti-Detection** - Bypasses bot detection mechanisms
- **Error Handling** - Comprehensive error management and user feedback
- **Docker Support** - Containerized deployment for consistency
- **Unit Testing** - Automated testing for core functionality

## 🌐 Live Demo

**Deploy your own instance:**
- **Railway**: [railway.app](https://railway.app) - Free tier available
- **Render**: [render.com](https://render.com) - Free tier available
- **DigitalOcean**: [digitalocean.com](https://digitalocean.com) - Production ready

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/pandey-i/CourtScraper.git
cd CourtScraper

# Build and run with Docker
docker build -t court-scraper .
docker run -p 5000:5000 court-scraper

# Access at http://localhost:5000
```

### Option 2: Local Installation

```bash
# Clone the repository
git clone https://github.com/pandey-i/CourtScraper.git
cd CourtScraper

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Download ChromeDriver (matching your Chrome version)
# Download from: https://chromedriver.chromium.org/

# Run the application
python app.py
```

## 📖 Usage

### Basic Search

1. **Open the application** at `http://localhost:5000`
2. **Select Case Type** from the dropdown (e.g., "ARB.P.")
3. **Enter Case Number** (e.g., "101")
4. **Enter Filing Year** (e.g., "2020")
5. **Click "Search Case"** and wait for results

### Understanding Results

The application displays:
- **S.No.** - Serial number of the result
- **Case No.** - Case number with link to details
- **Date of Judgment/Order** - Date with link to order PDF
- **Party** - Names of parties involved
- **Corrigendum** - Any corrections or amendments

### Additional Features

- **Download PDF** - Click "Download PDF Report" for formatted case details
- **View History** - Click "Query History" to see previous searches
- **Check Statistics** - Click "Statistics" for success rates and analytics
- **Pagination** - Navigate through multiple results using page numbers

## 🔧 API Documentation

### Endpoints

#### `GET /`
- **Description**: Main search interface
- **Response**: HTML page with search form

#### `POST /fetch`
- **Description**: Submit case search
- **Parameters**:
  - `case_type` (string): Type of case
  - `case_number` (string): Case number
  - `filing_year` (string): Filing year
- **Response**: HTML page with search results

#### `GET /download/<filename>`
- **Description**: Download generated PDF
- **Parameters**:
  - `filename` (string): PDF filename
- **Response**: PDF file download

#### `GET /history`
- **Description**: View query history
- **Response**: HTML page with search history

#### `GET /stats`
- **Description**: View search statistics
- **Response**: HTML page with analytics

#### `GET /health`
- **Description**: Health check endpoint
- **Response**: JSON with service status

## 🚀 Deployment

### Railway (Recommended - Free)

1. **Sign up** at [railway.app](https://railway.app)
2. **Connect GitHub** repository
3. **Deploy automatically** - Railway detects Dockerfile
4. **Get live URL** instantly

### Render (Free Tier)

1. **Sign up** at [render.com](https://render.com)
2. **Connect GitHub** repository
3. **Create Web Service**
4. **Deploy with Docker**

### DigitalOcean App Platform

1. **Sign up** at [digitalocean.com](https://digitalocean.com)
2. **Create App** from GitHub
3. **Configure environment**
4. **Deploy with SSL**

### Local Production

```bash
# Set environment variables
export FLASK_ENV=production
export FLASK_APP=app.py

# Run with Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🏗️ Architecture

### Technology Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Backend Framework | Flask | 2.0.1 | Web application framework |
| Web Scraping | Selenium | 4.8.0 | Browser automation |
| Database | SQLite3 | Built-in | Data persistence |
| PDF Generation | FPDF2 | Latest | Document creation |
| CAPTCHA Solving | SpeechRecognition, pytesseract | Latest | Anti-bot bypass |
| Frontend | HTML5, CSS3, JavaScript | - | User interface |
| Template Engine | Jinja2 | Built-in | Dynamic HTML generation |
| Containerization | Docker | Latest | Deployment consistency |

### System Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │    │   Flask App     │    │   Selenium      │
│                 │◄──►│   (app.py)      │◄──►│   (scraper.py)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   SQLite DB     │
                       │  (database.py)  │
                       └─────────────────┘
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ -v --cov=scraper --cov=database --cov-report=xml

# Run specific test file
python -m pytest tests/test_scraper.py -v
```

### Test Coverage

- **CAPTCHA Solving**: Tests direct extraction, audio, and OCR methods
- **PDF Generation**: Tests file creation and cleanup
- **Database Operations**: Tests query logging and retrieval
- **Case Types**: Validates dropdown options from court website

## 📁 Project Structure

```
CourtScraper/
├── app.py                      # Flask application entry point
├── scraper.py                  # Core web scraping logic
├── database.py                 # Database operations
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker container definition
├── railway.json               # Railway deployment config
├── deploy.sh                  # Deployment script
├── .github/workflows/         # CI/CD pipeline
│   └── ci.yml
├── tests/                     # Unit tests
│   └── test_scraper.py
├── templates/                 # HTML templates
│   ├── index.html
│   ├── results.html
│   ├── history.html
│   └── stats.html
├── static/                    # Static assets
│   ├── css/
│   └── downloads/            # Generated PDFs
└── docs/                     # Documentation
    ├── TECHNICAL_DOCUMENTATION.md
    ├── QUICK_START.md
    ├── LIVE_DEPLOYMENT.md
    └── DEPLOYMENT.md
```

## 🔒 Security & Ethics

### CAPTCHA Solving Methods

1. **Direct Extraction** (Primary)
   - Extracts CAPTCHA from `<span id="captcha-code">`
   - Most reliable for Delhi High Court site

2. **Audio Recognition** (Fallback)
   - Uses SpeechRecognition library
   - Converts audio CAPTCHA to text

3. **OCR Processing** (Fallback)
   - Uses pytesseract for image CAPTCHA
   - Processes CAPTCHA images with OCR

4. **Manual Solving** (Last Resort)
   - Opens browser for manual CAPTCHA entry
   - Used when automatic methods fail

### Ethical Considerations

- **Respectful Scraping**: Reasonable request rates
- **Legal Compliance**: Follow website terms of service
- **Transparency**: Clear logging of automated actions
- **Educational Purpose**: For legal research and education

## 🤝 Contributing

### Development Setup

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Run tests**
   ```bash
   python -m pytest tests/ -v
   ```
5. **Submit a pull request**

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Include type hints where appropriate

### Testing Guidelines

- Write tests for new features
- Maintain test coverage above 80%
- Test both success and failure scenarios
- Mock external dependencies

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Delhi High Court for providing public case information
- Selenium team for web automation tools
- Flask community for the excellent web framework
- Open source contributors for various Python libraries

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section in documentation
- Review the technical documentation for implementation details

---

**Built with ❤️ for legal professionals and researchers**

**Happy Scraping! 🏛️**

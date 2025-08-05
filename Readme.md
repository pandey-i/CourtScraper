# 🏛️ Court Data Fetcher & Mini-Dashboard

A powerful web application for scraping and displaying court case information from the Delhi High Court website. Built with Python, Flask, Selenium, and modern web technologies.

## 📋 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Technical Architecture](#-technical-architecture)
- [Database Schema](#-database-schema)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

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

## 📸 Screenshots

### Main Search Interface
![Search Interface](docs/images/search-interface.png)

### Results Display
![Results Display](docs/images/results-display.png)

### Query History
![Query History](docs/images/query-history.png)

## 🚀 Installation

### Prerequisites
- Python 3.11+
- Chrome Browser
- ChromeDriver (version 138.0.7204.184)

### Option 1: Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/court-scraper.git
   cd court-scraper
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\Activate.ps1
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download ChromeDriver**
   - Download from: https://chromedriver.chromium.org/
   - Extract `chromedriver.exe` to project root
   - Ensure version matches your Chrome browser

5. **Run the application**
   ```bash
   python app.py
   ```

### Option 2: Docker Installation

1. **Build the Docker image**
   ```bash
   docker build -t court-scraper .
   ```

2. **Run the container**
   ```bash
   docker run -p 5000:5000 court-scraper
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

## 🏗️ Technical Architecture

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

### Key Technologies

- **Backend**: Python 3.11, Flask 2.0.1
- **Web Scraping**: Selenium 4.8.0, Chrome WebDriver
- **Database**: SQLite3 (built-in)
- **PDF Generation**: FPDF2
- **CAPTCHA Solving**: SpeechRecognition, pytesseract, PIL
- **Frontend**: HTML5, CSS3, JavaScript, Jinja2 templates

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

## 🗄️ Database Schema

### Tables

#### `queries` Table
```sql
CREATE TABLE queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_type TEXT NOT NULL,
    case_number TEXT NOT NULL,
    filing_year TEXT NOT NULL,
    query_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending',
    error_message TEXT
);
```

#### `responses` Table
```sql
CREATE TABLE responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query_id INTEGER,
    sno TEXT,
    case_no TEXT,
    case_no_link TEXT,
    date TEXT,
    date_link TEXT,
    party TEXT,
    corrigendum TEXT,
    pdf_filename TEXT,
    raw_response TEXT,
    response_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (query_id) REFERENCES queries (id)
);
```

### Database Operations

- **Query Logging**: `log_query(case_type, case_number, filing_year)`
- **Status Updates**: `update_query_status(query_id, status, error_message)`
- **Response Logging**: `log_response(query_id, result_data, raw_response)`
- **History Retrieval**: `get_query_history(limit=10)`
- **Statistics**: `get_query_stats()`

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

### Test Structure

```
tests/
├── test_scraper.py      # Core scraping functionality
├── test_database.py     # Database operations
└── test_integration.py  # End-to-end tests
```

## 🚀 Deployment

### Production Deployment

1. **Environment Setup**
   ```bash
   export FLASK_ENV=production
   export FLASK_APP=app.py
   ```

2. **Database Initialization**
   ```bash
   python -c "from database import init_database; init_database()"
   ```

3. **ChromeDriver Setup**
   ```bash
   # Ensure ChromeDriver is in PATH or project directory
   chmod +x chromedriver
   ```

4. **Run with Gunicorn**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

### Docker Deployment

```bash
# Build image
docker build -t court-scraper .

# Run container
docker run -d -p 5000:5000 --name court-scraper-app court-scraper

# View logs
docker logs court-scraper-app
```

### CI/CD Pipeline

The project includes GitHub Actions workflow (`.github/workflows/ci.yml`) that:
- Runs automated tests
- Performs code linting
- Conducts security checks
- Builds Docker images
- Uploads coverage reports

## 🔧 Troubleshooting

### Common Issues

#### ChromeDriver Issues
```bash
# Error: chromedriver executable needs to be in PATH
# Solution: Download correct version and place in project root
wget https://chromedriver.storage.googleapis.com/138.0.7204.184/chromedriver_win32.zip
```

#### CAPTCHA Solving Failures
```bash
# Error: CAPTCHA solving failed
# Solution: Check internet connection and try manual solving
```

#### Database Errors
```bash
# Error: database is locked
# Solution: Ensure no other processes are accessing the database
```

#### Flask Import Errors
```bash
# Error: cannot import name 'url_quote' from 'werkzeug.urls'
# Solution: Install compatible werkzeug version
pip install "werkzeug<2.1.0"
```

### Debug Mode

Enable debug mode for detailed error information:
```python
# In app.py
app.run(debug=True)
```

### Log Files

Check application logs for detailed error information:
```bash
# View Flask logs
tail -f flask.log

# View Selenium logs
tail -f selenium.log
```

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
- Check the troubleshooting section
- Review the documentation

---

**Built with ❤️ for legal professionals and researchers**
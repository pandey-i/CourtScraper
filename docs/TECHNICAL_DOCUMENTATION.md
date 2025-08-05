# Technical Documentation

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Code Structure](#code-structure)
3. [Core Components](#core-components)
4. [Database Design](#database-design)
5. [Web Scraping Implementation](#web-scraping-implementation)
6. [CAPTCHA Solving](#captcha-solving)
7. [Error Handling](#error-handling)
8. [Performance Optimization](#performance-optimization)
9. [Security Considerations](#security-considerations)
10. [Testing Strategy](#testing-strategy)

## Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                     │
├─────────────────────────────────────────────────────────────┤
│  HTML Templates (Jinja2)  │  CSS/JS  │  Loading Animations │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                       │
├─────────────────────────────────────────────────────────────┤
│  Flask Routes  │  Request Handling  │  Response Generation │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                    │
├─────────────────────────────────────────────────────────────┤
│  Scraper Module  │  Database Module  │  PDF Generator     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                              │
├─────────────────────────────────────────────────────────────┤
│  SQLite Database  │  File System  │  External APIs        │
└─────────────────────────────────────────────────────────────┘
```

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

## Code Structure

```
CourtScraper/
├── app.py                      # Flask application entry point
├── scraper.py                  # Core web scraping logic
├── database.py                 # Database operations
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker container definition
├── .github/workflows/          # CI/CD pipeline
│   └── ci.yml
├── tests/                      # Unit tests
│   └── test_scraper.py
├── templates/                  # HTML templates
│   ├── index.html
│   ├── results.html
│   ├── history.html
│   └── stats.html
├── static/                     # Static assets
│   ├── css/
│   └── downloads/             # Generated PDFs
└── docs/                      # Documentation
    └── TECHNICAL_DOCUMENTATION.md
```

## Core Components

### 1. Flask Application (`app.py`)

**Purpose**: Main application entry point and route handling

**Key Functions**:
- `index()`: Renders main search interface
- `fetch()`: Handles case search requests
- `download()`: Serves generated PDF files
- `history()`: Displays query history
- `stats()`: Shows analytics

**Route Structure**:
```python
@app.route('/')           # Main page
@app.route('/fetch')      # Search endpoint
@app.route('/download')   # PDF download
@app.route('/history')    # Query history
@app.route('/stats')      # Analytics
```

### 2. Web Scraper (`scraper.py`)

**Purpose**: Handles all web scraping operations

**Key Functions**:
- `scrape_case_data()`: Main scraping function
- `solve_captcha()`: CAPTCHA solving orchestration
- `solve_captcha_direct()`: Direct CAPTCHA extraction
- `save_result_as_pdf()`: PDF generation

**Scraping Flow**:
1. Initialize Chrome WebDriver
2. Navigate to court website
3. Fill search form
4. Solve CAPTCHA if present
5. Submit form and wait for results
6. Parse table data
7. Generate PDF report
8. Clean up resources

### 3. Database Module (`database.py`)

**Purpose**: Manages all database operations

**Key Functions**:
- `init_database()`: Creates tables
- `log_query()`: Records search queries
- `log_response()`: Stores scraped data
- `get_query_history()`: Retrieves search history
- `get_query_stats()`: Calculates analytics

## Database Design

### Schema Overview

```sql
-- Queries table: Stores all search attempts
CREATE TABLE queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_type TEXT NOT NULL,
    case_number TEXT NOT NULL,
    filing_year TEXT NOT NULL,
    query_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending',
    error_message TEXT
);

-- Responses table: Stores scraped results
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

### Data Flow

1. **Query Logging**: When user submits search
2. **Status Updates**: During scraping process
3. **Response Storage**: After successful scraping
4. **History Retrieval**: For analytics and debugging

## Web Scraping Implementation

### Selenium Configuration

```python
options = Options()
options.add_argument('--headless')  # Run without GUI
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
```

### Anti-Detection Techniques

1. **WebDriver Property Removal**:
   ```python
   driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
   ```

2. **User-Agent Spoofing**: Uses default Chrome user agent

3. **Session Management**: Maintains cookies and session state

4. **Random Delays**: Adds realistic timing between actions

### Element Location Strategy

**Fallback Approach**:
1. Try by ID first
2. Try by NAME second
3. Try by XPath last
4. Debug with element listing

```python
try:
    element = driver.find_element(By.ID, 'element_id')
except:
    try:
        element = driver.find_element(By.NAME, 'element_name')
    except:
        element = driver.find_element(By.XPATH, "//input[@type='text']")
```

## CAPTCHA Solving

### Multi-Method Approach

1. **Direct Extraction** (Primary Method)
   ```python
   def solve_captcha_direct(driver):
       captcha_span = driver.find_element(By.ID, "captcha-code")
       return captcha_span.text.strip()
   ```

2. **Audio Recognition** (Fallback)
   ```python
   def solve_captcha_audio(driver):
       # Download audio file
       # Use SpeechRecognition
       # Return transcribed text
   ```

3. **OCR Processing** (Fallback)
   ```python
   def solve_captcha_ocr(driver):
       # Extract CAPTCHA image
       # Use pytesseract for OCR
       # Return recognized text
   ```

4. **Manual Solving** (Last Resort)
   ```python
   def solve_captcha_manual(driver):
       # Open browser for manual entry
       # Wait for user input
   ```

### Success Rate Optimization

- **Method Priority**: Direct extraction → Audio → OCR → Manual
- **Error Handling**: Graceful fallback between methods
- **Timeout Management**: Prevents infinite waiting
- **Logging**: Tracks success/failure rates

## Error Handling

### Comprehensive Error Management

1. **Network Errors**:
   ```python
   try:
       driver.get(url)
   except WebDriverException as e:
       log_error(f"Network error: {e}")
       return None
   ```

2. **Element Not Found**:
   ```python
   try:
       element = driver.find_element(By.ID, 'element')
   except NoSuchElementException:
       # Try alternative selectors
       # Log for debugging
   ```

3. **CAPTCHA Failures**:
   ```python
   if not captcha_solved:
       update_query_status(query_id, "failed", "CAPTCHA solving failed")
       return None
   ```

4. **Database Errors**:
   ```python
   try:
       log_query(case_type, case_number, filing_year)
   except sqlite3.Error as e:
       print(f"Database error: {e}")
   ```

### User-Friendly Error Messages

- **Technical Errors**: Logged for debugging
- **User Errors**: Displayed in simple language
- **Recovery Suggestions**: Provided when possible

## Performance Optimization

### Scraping Optimization

1. **Headless Mode**: Reduces resource usage
2. **Connection Pooling**: Reuses WebDriver instances
3. **Caching**: Stores frequently accessed data
4. **Parallel Processing**: Future enhancement for multiple searches

### Database Optimization

1. **Indexed Queries**: Fast retrieval of historical data
2. **Batch Operations**: Efficient bulk inserts
3. **Connection Management**: Proper cleanup of database connections

### Memory Management

1. **Resource Cleanup**: Proper WebDriver disposal
2. **File Management**: Automatic PDF cleanup
3. **Session Management**: Efficient cookie handling

## Security Considerations

### Input Validation

```python
def validate_input(case_type, case_number, filing_year):
    if not case_type or not case_number or not filing_year:
        return False
    if not filing_year.isdigit() or len(filing_year) != 4:
        return False
    return True
```

### SQL Injection Prevention

- **Parameterized Queries**: All database operations use placeholders
- **Input Sanitization**: Clean user inputs before processing

### File Security

- **Path Validation**: Ensure downloads are in safe directory
- **File Type Checking**: Validate PDF files before serving
- **Access Control**: Restrict file access to authorized users

### CAPTCHA Ethics

- **Respectful Scraping**: Reasonable request rates
- **Legal Compliance**: Follow website terms of service
- **Transparency**: Clear logging of automated actions

## Testing Strategy

### Unit Testing

**Test Categories**:
1. **CAPTCHA Solving**: All methods tested independently
2. **PDF Generation**: File creation and cleanup
3. **Database Operations**: CRUD operations
4. **Input Validation**: Edge cases and error conditions

**Test Structure**:
```python
class TestScraper(unittest.TestCase):
    def setUp(self):
        # Mock WebDriver
        self.mock_driver = Mock()
    
    def test_captcha_solving(self):
        # Test CAPTCHA extraction
        pass
    
    def test_pdf_generation(self):
        # Test PDF creation
        pass
```

### Integration Testing

1. **End-to-End Scraping**: Full workflow testing
2. **Database Integration**: Real database operations
3. **Web Interface**: User interaction testing

### Performance Testing

1. **Response Time**: Measure scraping duration
2. **Success Rate**: Track CAPTCHA solving success
3. **Resource Usage**: Monitor memory and CPU usage

### Test Coverage Goals

- **Code Coverage**: >80% for core modules
- **Function Coverage**: All public functions tested
- **Error Coverage**: All error paths tested
- **Integration Coverage**: Key workflows tested

## Future Enhancements

### Planned Features

1. **Multi-Court Support**: Extend to other court websites
2. **Advanced Analytics**: Machine learning for pattern recognition
3. **API Endpoints**: RESTful API for external integrations
4. **Real-time Updates**: WebSocket for live notifications
5. **Mobile App**: Native mobile application

### Technical Improvements

1. **Async Processing**: Non-blocking scraping operations
2. **Distributed Scraping**: Multiple worker processes
3. **Advanced CAPTCHA**: AI-powered solving
4. **Caching Layer**: Redis for performance
5. **Monitoring**: Prometheus metrics and alerts

---

*This technical documentation provides a comprehensive overview of the Court Data Fetcher implementation. For specific implementation details, refer to the source code and inline comments.* 
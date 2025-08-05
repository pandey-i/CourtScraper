# 🚀 Quick Start Guide

Get your Court Data Fetcher up and running in 5 minutes!

## Prerequisites

- ✅ Python 3.11 or higher
- ✅ Chrome browser installed
- ✅ Internet connection

## Option 1: Docker (Recommended)

### 1. Install Docker
Download and install Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop/)

### 2. Clone and Run
```bash
# Clone the repository
git clone https://github.com/yourusername/court-scraper.git
cd court-scraper

# Build and run with Docker
docker build -t court-scraper .
docker run -p 5000:5000 court-scraper
```

### 3. Access the Application
Open your browser and go to: **http://localhost:5000**

## Option 2: Local Installation

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/court-scraper.git
cd court-scraper
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download ChromeDriver
- Go to [chromedriver.chromium.org](https://chromedriver.chromium.org/)
- Download version matching your Chrome browser
- Extract `chromedriver.exe` to project root

### 5. Run Application
```bash
python app.py
```

### 6. Access the Application
Open your browser and go to: **http://localhost:5000**

## 🎯 First Search

1. **Select Case Type**: Choose "ARB.P." from dropdown
2. **Enter Case Number**: Type "101"
3. **Enter Filing Year**: Type "2020"
4. **Click "Search Case"**: Watch the loading animation
5. **View Results**: See scraped case information

## 📊 Available Features

### Core Features
- ✅ **Case Search**: Search by type, number, and year
- ✅ **PDF Download**: Download case details as PDF
- ✅ **Loading Animation**: Professional user feedback
- ✅ **Error Handling**: User-friendly error messages

### Analytics Features
- 📊 **Query History**: View all previous searches
- 📈 **Statistics**: Success rates and popular case types
- 🔍 **Debug Info**: Detailed logging for troubleshooting

## 🛠️ Troubleshooting

### Common Issues

**Docker Issues**
```bash
# If Docker isn't running
Start-Process "Docker Desktop"

# If port is in use
docker run -p 5001:5000 court-scraper
```

**ChromeDriver Issues**
```bash
# Download correct version
wget https://chromedriver.storage.googleapis.com/138.0.7204.184/chromedriver_win32.zip
```

**Python Issues**
```bash
# Update pip
python -m pip install --upgrade pip

# Install werkzeug fix
pip install "werkzeug<2.1.0"
```

### Getting Help

1. **Check Logs**: Look for error messages in terminal
2. **Verify ChromeDriver**: Ensure version matches Chrome browser
3. **Test Internet**: Ensure connection to court website
4. **Check Dependencies**: Verify all packages installed correctly

## 🎉 Success!

Your Court Data Fetcher is now running! 

**Next Steps:**
- Try different case types and numbers
- Explore the history and statistics pages
- Download PDF reports
- Check the technical documentation for advanced features

**Need Help?**
- Check the full [README.md](README.md) for detailed documentation
- Review [Technical Documentation](docs/TECHNICAL_DOCUMENTATION.md) for implementation details
- Create an issue on GitHub for bugs or feature requests

---

**Happy Scraping! 🏛️** 
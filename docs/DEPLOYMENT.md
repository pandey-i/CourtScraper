# 🚀 Deployment Guide

Complete guide for deploying the Court Data Fetcher to various environments.

## Table of Contents

- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Production Setup](#production-setup)
- [Monitoring & Maintenance](#monitoring--maintenance)

## Local Development

### Prerequisites
```bash
# System requirements
- Python 3.11+
- Chrome browser
- ChromeDriver (matching Chrome version)
- Git
```

### Setup Steps
```bash
# 1. Clone repository
git clone https://github.com/yourusername/court-scraper.git
cd court-scraper

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows
.\venv\Scripts\Activate.ps1
# Linux/Mac
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Download ChromeDriver
# Download from: https://chromedriver.chromium.org/
# Extract to project root

# 6. Initialize database
python -c "from database import init_database; init_database()"

# 7. Run application
python app.py
```

### Development Configuration
```python
# app.py - Development settings
app.run(debug=True, host='0.0.0.0', port=5000)
```

## Docker Deployment

### Single Container Deployment

```bash
# 1. Build image
docker build -t court-scraper .

# 2. Run container
docker run -d \
  --name court-scraper \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  court-scraper

# 3. View logs
docker logs court-scraper

# 4. Stop container
docker stop court-scraper
```

### Docker Compose Deployment

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  court-scraper:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - FLASK_ENV=production
      - FLASK_APP=app.py
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Run with Docker Compose:
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Multi-Container Deployment

```yaml
version: '3.8'

services:
  court-scraper:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
    environment:
      - FLASK_ENV=production
    depends_on:
      - redis
    restart: unless-stopped

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - court-scraper

volumes:
  redis_data:
```

## Cloud Deployment

### AWS Deployment

#### EC2 Deployment
```bash
# 1. Launch EC2 instance (Ubuntu 20.04)
# 2. Install Docker
sudo apt update
sudo apt install docker.io docker-compose

# 3. Clone repository
git clone https://github.com/yourusername/court-scraper.git
cd court-scraper

# 4. Build and run
docker build -t court-scraper .
docker run -d -p 80:5000 court-scraper
```

#### ECS Deployment
```yaml
# task-definition.json
{
  "family": "court-scraper",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "court-scraper",
      "image": "court-scraper:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "FLASK_ENV",
          "value": "production"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/court-scraper",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Google Cloud Deployment

#### App Engine Deployment
```yaml
# app.yaml
runtime: python311
entrypoint: gunicorn -b :$PORT app:app

env_variables:
  FLASK_ENV: production

automatic_scaling:
  target_cpu_utilization: 0.6
  min_instances: 1
  max_instances: 10
```

#### Cloud Run Deployment
```bash
# 1. Build and push to Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/court-scraper

# 2. Deploy to Cloud Run
gcloud run deploy court-scraper \
  --image gcr.io/PROJECT_ID/court-scraper \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure Deployment

#### Container Instances
```bash
# Deploy to Azure Container Instances
az container create \
  --resource-group myResourceGroup \
  --name court-scraper \
  --image court-scraper:latest \
  --dns-name-label court-scraper \
  --ports 5000
```

#### App Service
```bash
# Deploy to Azure App Service
az webapp create \
  --resource-group myResourceGroup \
  --plan myAppServicePlan \
  --name court-scraper \
  --deployment-container-image-name court-scraper:latest
```

## Production Setup

### Environment Configuration

Create `.env` file:
```bash
# Production environment variables
FLASK_ENV=production
FLASK_APP=app.py
DATABASE_URL=sqlite:///court_scraper.db
LOG_LEVEL=INFO
CHROME_DRIVER_PATH=/usr/local/bin/chromedriver
```

### Security Configuration

#### Nginx Configuration
```nginx
# nginx.conf
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
}
```

#### SSL Configuration
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Database Setup

#### SQLite (Default)
```bash
# Initialize database
python -c "from database import init_database; init_database()"

# Backup database
cp court_scraper.db backup_$(date +%Y%m%d_%H%M%S).db
```

#### PostgreSQL (Optional)
```python
# database.py - PostgreSQL configuration
import psycopg2

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'court_scraper'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', '')
    )
```

### Logging Configuration

```python
# logging_config.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
        handlers=[
            RotatingFileHandler('logs/court_scraper.log', maxBytes=10000000, backupCount=5),
            logging.StreamHandler()
        ]
    )
```

## Monitoring & Maintenance

### Health Checks

```python
# health_check.py
@app.route('/health')
def health_check():
    try:
        # Check database connection
        from database import get_db_connection
        conn = get_db_connection()
        conn.close()
        
        # Check ChromeDriver
        from selenium import webdriver
        driver = webdriver.Chrome()
        driver.quit()
        
        return {'status': 'healthy'}, 200
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500
```

### Performance Monitoring

#### Application Metrics
```python
# metrics.py
from flask import request
import time

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def log_request(response):
    duration = time.time() - request.start_time
    print(f"{request.method} {request.path} {response.status_code} {duration:.2f}s")
    return response
```

#### System Monitoring
```bash
# Monitor resource usage
docker stats court-scraper

# Monitor logs
docker logs -f court-scraper

# Monitor disk usage
df -h

# Monitor memory usage
free -h
```

### Backup Strategy

#### Automated Backups
```bash
#!/bin/bash
# backup.sh

# Create backup directory
mkdir -p backups

# Backup database
cp court_scraper.db backups/court_scraper_$(date +%Y%m%d_%H%M%S).db

# Backup logs
tar -czf backups/logs_$(date +%Y%m%d_%H%M%S).tar.gz logs/

# Clean old backups (keep last 7 days)
find backups/ -name "*.db" -mtime +7 -delete
find backups/ -name "*.tar.gz" -mtime +7 -delete
```

#### Cron Job Setup
```bash
# Add to crontab
crontab -e

# Daily backup at 2 AM
0 2 * * * /path/to/backup.sh

# Weekly backup on Sunday at 3 AM
0 3 * * 0 /path/to/weekly_backup.sh
```

### Update Strategy

#### Docker Updates
```bash
# Pull latest changes
git pull origin main

# Rebuild image
docker build -t court-scraper .

# Stop old container
docker stop court-scraper

# Remove old container
docker rm court-scraper

# Start new container
docker run -d --name court-scraper -p 5000:5000 court-scraper
```

#### Zero-Downtime Deployment
```bash
# Blue-green deployment
docker run -d --name court-scraper-new -p 5001:5000 court-scraper

# Test new version
curl http://localhost:5001/health

# Switch traffic
docker stop court-scraper
docker run -d --name court-scraper -p 5000:5000 court-scraper

# Remove old container
docker rm court-scraper-old
```

## Troubleshooting

### Common Issues

#### Container Won't Start
```bash
# Check container logs
docker logs court-scraper

# Check resource usage
docker stats court-scraper

# Restart container
docker restart court-scraper
```

#### ChromeDriver Issues
```bash
# Check ChromeDriver version
chromedriver --version

# Update ChromeDriver
wget https://chromedriver.storage.googleapis.com/LATEST_VERSION/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
```

#### Database Issues
```bash
# Check database file
ls -la court_scraper.db

# Repair database
sqlite3 court_scraper.db "VACUUM;"

# Reset database
rm court_scraper.db
python -c "from database import init_database; init_database()"
```

### Performance Optimization

#### Resource Limits
```yaml
# docker-compose.yml
services:
  court-scraper:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

#### Caching Strategy
```python
# Add Redis caching
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_cached_result(case_type, case_number, filing_year):
    key = f"{case_type}_{case_number}_{filing_year}"
    return redis_client.get(key)
```

---

**For additional support, refer to the [Technical Documentation](TECHNICAL_DOCUMENTATION.md) or create an issue on GitHub.** 
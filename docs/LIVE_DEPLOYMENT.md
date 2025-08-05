# 🌐 Live Website Deployment Guide

Deploy your Court Data Fetcher to a live website accessible from anywhere!

## 🚀 Quick Deploy Options (Free)

### **Option 1: Railway (Recommended)**

**Steps:**
1. **Sign up** at [railway.app](https://railway.app)
2. **Connect GitHub** repository
3. **Deploy automatically** - Railway detects Dockerfile
4. **Get live URL** instantly

```bash
# Railway automatically:
# - Builds from Dockerfile
# - Deploys to live URL
# - Provides SSL certificate
# - Handles scaling
```

**Benefits:**
- ✅ **Free tier** available
- ✅ **Automatic SSL** certificate
- ✅ **Custom domain** support
- ✅ **GitHub integration**
- ✅ **Auto-deploy** on push

### **Option 2: Render**

**Steps:**
1. **Sign up** at [render.com](https://render.com)
2. **Connect GitHub** repository
3. **Create Web Service**
4. **Configure build settings**

```yaml
# render.yaml
services:
  - type: web
    name: court-scraper
    env: docker
    plan: free
    buildCommand: docker build -t court-scraper .
    startCommand: python app.py
    envVars:
      - key: FLASK_ENV
        value: production
```

### **Option 3: Heroku**

**Steps:**
1. **Install Heroku CLI**
2. **Login and create app**
3. **Deploy with Git**

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login and deploy
heroku login
heroku create court-scraper-app
git push heroku main

# Open live URL
heroku open
```

## 💰 Paid Hosting Options

### **Option 4: DigitalOcean App Platform**

**Steps:**
1. **Sign up** at [digitalocean.com](https://digitalocean.com)
2. **Create App** from GitHub
3. **Configure environment**
4. **Deploy with SSL**

**Benefits:**
- ✅ **Reliable infrastructure**
- ✅ **Global CDN**
- ✅ **Auto-scaling**
- ✅ **Custom domains**

### **Option 5: AWS Elastic Beanstalk**

**Steps:**
1. **AWS Console** → Elastic Beanstalk
2. **Upload Docker image**
3. **Configure environment**
4. **Deploy with load balancer**

```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-east-1.amazonaws.com
docker build -t court-scraper .
docker tag court-scraper:latest your-account.dkr.ecr.us-east-1.amazonaws.com/court-scraper:latest
docker push your-account.dkr.ecr.us-east-1.amazonaws.com/court-scraper:latest
```

## 🔧 Production Configuration

### **Environment Variables**

Create `.env` file for production:
```bash
# Production settings
FLASK_ENV=production
FLASK_APP=app.py
PORT=5000
HOST=0.0.0.0

# Database settings
DATABASE_URL=sqlite:///court_scraper.db

# Security settings
SECRET_KEY=your-secret-key-here
```

### **Update app.py for Production**

```python
# app.py - Production configuration
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    app.run(host=host, port=port, debug=False)
```

### **Dockerfile Optimization**

```dockerfile
# Optimized for production
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome and ChromeDriver
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Download ChromeDriver
RUN wget -q https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/138.0.7204.184/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip \
    && mv chromedriver-linux64/chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf chromedriver-linux64.zip chromedriver-linux64

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directories
RUN mkdir -p static/downloads

# Set environment
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Run application
CMD ["python", "app.py"]
```

## 🌍 Custom Domain Setup

### **Domain Configuration**

1. **Purchase domain** (Namecheap, GoDaddy, etc.)
2. **Configure DNS** to point to your hosting provider
3. **Add SSL certificate** (usually automatic)

### **DNS Settings**

```
# For Railway
Type: CNAME
Name: www
Value: your-app.railway.app

# For Render
Type: CNAME  
Name: www
Value: your-app.onrender.com
```

## 📊 Monitoring & Analytics

### **Add Google Analytics**

```html
<!-- Add to templates/base.html -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### **Add Uptime Monitoring**

```python
# health_check.py
@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }
```

## 🔒 Security Considerations

### **HTTPS Enforcement**

```python
# app.py - Force HTTPS in production
from flask import redirect, request

@app.before_request
def before_request():
    if request.headers.get('X-Forwarded-Proto') == 'http':
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)
```

### **Rate Limiting**

```python
# Add rate limiting
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/fetch', methods=['POST'])
@limiter.limit("10 per minute")
def fetch():
    # Your existing code
    pass
```

## 🚀 Deployment Checklist

### **Pre-Deployment**
- [ ] **Test locally** with production settings
- [ ] **Update requirements.txt** with all dependencies
- [ ] **Configure environment variables**
- [ ] **Add health check endpoint**
- [ ] **Test Docker build** locally

### **Deployment**
- [ ] **Choose hosting provider**
- [ ] **Connect GitHub repository**
- [ ] **Configure build settings**
- [ ] **Set environment variables**
- [ ] **Deploy and test**

### **Post-Deployment**
- [ ] **Test all features** on live site
- [ ] **Configure custom domain**
- [ ] **Set up monitoring**
- [ ] **Add analytics**
- [ ] **Document live URL**

## 🎯 Recommended Deployment Flow

### **For Quick Launch (Railway)**

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Railway**
   - Go to [railway.app](https://railway.app)
   - Connect GitHub repository
   - Deploy automatically

3. **Get Live URL**
   - Railway provides: `https://your-app.railway.app`
   - Add custom domain if needed

### **For Production (DigitalOcean)**

1. **Prepare for production**
   ```bash
   # Update app.py for production
   # Configure environment variables
   # Test Docker build
   ```

2. **Deploy to DigitalOcean**
   - Create App Platform
   - Connect GitHub repository
   - Configure environment

3. **Set up custom domain**
   - Configure DNS
   - Add SSL certificate
   - Test all features

## 📈 Performance Optimization

### **Caching Strategy**

```python
# Add Redis caching
import redis
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(expiry=3600):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = f"search_{hash(str(args) + str(kwargs))}"
            result = redis_client.get(cache_key)
            if result:
                return json.loads(result)
            result = f(*args, **kwargs)
            redis_client.setex(cache_key, expiry, json.dumps(result))
            return result
        return decorated_function
    return decorator
```

### **CDN Configuration**

```html
<!-- Add CDN for static assets -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
```

---

## 🎉 **Your Live Website is Ready!**

**Next Steps:**
1. **Choose a deployment option** (Railway recommended for quick start)
2. **Follow the deployment steps**
3. **Test your live website**
4. **Share your URL** with users

**Need Help?**
- Check hosting provider documentation
- Review error logs for debugging
- Test all features after deployment

**Happy Deploying! 🚀** 
#!/bin/bash

# Court Data Fetcher Deployment Script
# This script helps deploy to various platforms

echo "🏛️ Court Data Fetcher Deployment Script"
echo "========================================"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    exit 1
fi

# Check if remote is set
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ No remote repository found. Please add your GitHub repository:"
    echo "   git remote add origin https://github.com/yourusername/court-scraper.git"
    exit 1
fi

echo "✅ Git repository ready"

# Push to GitHub
echo "📤 Pushing to GitHub..."
git add .
git commit -m "Deploy to production $(date)"
git push origin main

echo ""
echo "🚀 Deployment Options:"
echo "======================"
echo ""
echo "1. Railway (Recommended - Free & Easy)"
echo "   - Go to https://railway.app"
echo "   - Sign up and connect GitHub"
echo "   - Deploy automatically"
echo "   - Get live URL instantly"
echo ""
echo "2. Render (Free Tier Available)"
echo "   - Go to https://render.com"
echo "   - Connect GitHub repository"
echo "   - Create Web Service"
echo "   - Deploy with Docker"
echo ""
echo "3. Heroku (Free Tier Discontinued)"
echo "   - Install Heroku CLI"
echo "   - Run: heroku create court-scraper-app"
echo "   - Run: git push heroku main"
echo ""
echo "4. DigitalOcean App Platform"
echo "   - Go to https://digitalocean.com"
echo "   - Create App from GitHub"
echo "   - Configure environment"
echo "   - Deploy with SSL"
echo ""
echo "📋 Pre-deployment Checklist:"
echo "============================"
echo "✅ Git repository initialized"
echo "✅ Code committed and pushed"
echo "✅ Dockerfile present"
echo "✅ Requirements.txt updated"
echo "✅ Environment variables configured"
echo ""
echo "🎯 Quick Start with Railway:"
echo "1. Visit https://railway.app"
echo "2. Sign up with GitHub"
echo "3. Click 'New Project'"
echo "4. Select 'Deploy from GitHub repo'"
echo "5. Choose your repository"
echo "6. Railway will automatically detect Dockerfile and deploy"
echo "7. Get your live URL in minutes!"
echo ""
echo "🌐 Your live website will be available at:"
echo "   https://your-app-name.railway.app"
echo ""
echo "📚 For detailed instructions, see:"
echo "   docs/LIVE_DEPLOYMENT.md"
echo ""
echo "Happy Deploying! 🚀" 
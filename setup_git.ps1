# Git Setup Script for CDR Analysis Project
# Run this in PowerShell from your project directory

Write-Host "🔧 Setting up Git configuration..." -ForegroundColor Green

# Configure Git identity
git config --global user.name "Varsha R"
git config --global user.email "varsha1530@gmail.com"

Write-Host "✅ Git identity configured" -ForegroundColor Green

# Check current status
Write-Host "📋 Current Git status:" -ForegroundColor Yellow
git status

# Add all files
Write-Host "📁 Adding all files..." -ForegroundColor Green
git add .

# Create commit
Write-Host "💾 Creating initial commit..." -ForegroundColor Green
git commit -m "Initial commit: CDR Intelligence Platform v2.0

Features:
- Advanced PDF parsing for call records
- Interactive cell tower geolocation
- Professional forensic analysis dashboard
- Responsive design with excellent contrast
- Demo mode for testing without API keys"

# Ensure we're on main branch
Write-Host "🌿 Setting main branch..." -ForegroundColor Green
git branch -M main

# Add remote origin (if not already added)
Write-Host "🔗 Adding remote origin..." -ForegroundColor Green
git remote add origin https://github.com/varsha1530/cdr-analysis.git 2>$null

# Push to GitHub
Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Green
git push -u origin main

Write-Host "✅ Setup complete! Your project is now on GitHub." -ForegroundColor Green
Write-Host "🌐 Visit: https://github.com/varsha1530/cdr-analysis" -ForegroundColor Cyan
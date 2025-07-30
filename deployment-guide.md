# NEXUS AI Deployment Guide

This guide will walk you through deploying NEXUS AI to both `nexus-agent.io` and `nexus-agent.org` using GitHub Pages.

## 🎯 Overview

- **nexus-agent.io**: Live NEXUS AI application interface
- **nexus-agent.org**: Project documentation and marketing site
- **Backend API**: Deployed separately (Railway, Heroku, Vercel, etc.)

## 📋 Prerequisites

1. **Domain Ownership**: You must own both domains
2. **GitHub Account**: For repository hosting and GitHub Pages
3. **Backend Hosting**: For the Flask API (Railway, Heroku, Vercel, etc.)

## 🚀 Step-by-Step Deployment

### Step 1: Repository Setup

1. **Create GitHub Repository**
   ```bash
   # Initialize git (if not already done)
   git init
   git add .
   git commit -m "Initial NEXUS AI setup"
   
   # Create GitHub repository and push
   # (Do this through GitHub web interface)
   git remote add origin https://github.com/yourusername/nexus-ai.git
   git push -u origin main
   ```

2. **Enable GitHub Pages**
   - Go to repository Settings → Pages
   - Source: Deploy from a branch
   - Branch: `gh-pages` (will be created by GitHub Actions)
   - Folder: `/ (root)`

### Step 2: Domain Configuration

1. **Configure DNS Records**
   
   For both domains, add these records:
   ```
   Type: CNAME
   Name: @
   Value: yourusername.github.io
   TTL: 3600
   ```

2. **Add Custom Domains in GitHub**
   - Go to repository Settings → Pages
   - Add custom domain: `nexus-agent.io`
   - Add custom domain: `nexus-agent.org`
   - Check "Enforce HTTPS"

### Step 3: Backend Deployment

Choose one of these options:

#### Option A: Railway (Recommended)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy backend
cd backend
railway login
railway init
railway up
```

#### Option B: Heroku
```bash
# Install Heroku CLI
# Deploy backend
cd backend
heroku create nexus-ai-api
git push heroku main
```

#### Option C: Vercel
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy backend
cd backend
vercel --prod
```

### Step 4: Environment Configuration

1. **Set Environment Variables**
   ```bash
   # For Railway/Heroku/Vercel
   FLASK_ENV=production
   PORT=8080
   ```

2. **Update API URL in Frontend**
   - The app automatically detects production vs development
   - For custom API domains, update `app/script.js`

### Step 5: Test Deployment

1. **Build Locally**
   ```bash
   ./scripts/deploy.sh both --serve
   ```

2. **Test Both Sites**
   - App: http://localhost:8000
   - Docs: http://localhost:8001

3. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy NEXUS AI to production"
   git push origin main
   ```

### Step 6: Verify Deployment

1. **Check GitHub Actions**
   - Go to repository Actions tab
   - Verify both workflows completed successfully

2. **Test Live Sites**
   - App: https://nexus-agent.io
   - Docs: https://nexus-agent.org

3. **Test API Integration**
   - Verify app can connect to backend API
   - Test query functionality

## 🔧 Configuration Details

### GitHub Actions Workflows

The project includes two workflows:

1. **deploy-app.yml**: Deploys app to `nexus-agent.io`
2. **deploy-docs.yml**: Deploys docs to `nexus-agent.org`

Both trigger on pushes to `main` branch and deploy to GitHub Pages.

### CORS Configuration

The backend API is configured to accept requests from:
- `https://nexus-agent.io`
- `https://www.nexus-agent.io`
- `https://nexus-agent.org`
- `https://www.nexus-agent.org`
- `http://localhost:3000` (development)
- `http://localhost:8000` (development)

### Build Process

The build scripts:
1. Copy files to `dist/` directory
2. Optimize images (if ImageMagick available)
3. Minify CSS/JS (if tools available)
4. Generate sitemap and robots.txt
5. Create deployment manifests

## 🐛 Troubleshooting

### Common Issues

1. **DNS Not Propagated**
   - Wait 24-48 hours for DNS propagation
   - Check with `dig nexus-agent.io` or `nslookup nexus-agent.io`

2. **GitHub Pages Not Working**
   - Verify custom domain is added in repository settings
   - Check for DNS verification errors
   - Ensure HTTPS is enforced

3. **API Connection Issues**
   - Verify backend is deployed and running
   - Check CORS configuration
   - Test API endpoints directly

4. **Build Failures**
   - Check GitHub Actions logs
   - Verify all required files exist
   - Test build locally first

### Debug Commands

```bash
# Test local build
./scripts/deploy.sh both

# Test individual components
./scripts/deploy.sh app --serve
./scripts/deploy.sh docs --serve

# Check backend
curl https://your-api-domain.com/health

# Check DNS
dig nexus-agent.io
dig nexus-agent.org
```

## 📊 Monitoring

### GitHub Actions
- Monitor deployment status in Actions tab
- Check for build failures or errors
- Review deployment logs

### Domain Health
- Use tools like UptimeRobot for monitoring
- Set up alerts for downtime
- Monitor SSL certificate status

### Performance
- Use Google PageSpeed Insights
- Monitor Core Web Vitals
- Track API response times

## 🔄 Updates and Maintenance

### Regular Updates
1. **Code Changes**: Push to `main` branch
2. **Automatic Deployment**: GitHub Actions handle deployment
3. **Verification**: Test both sites after deployment

### Backend Updates
1. **API Changes**: Deploy to your hosting service
2. **Environment Variables**: Update in hosting dashboard
3. **Database Changes**: Run migrations if needed

### Domain Renewal
- Set up auto-renewal for both domains
- Monitor expiration dates
- Keep DNS records updated

## 🎉 Success Checklist

- [ ] Both domains are live and accessible
- [ ] GitHub Actions workflows are working
- [ ] Backend API is deployed and responding
- [ ] App can connect to backend API
- [ ] Documentation site is complete
- [ ] SSL certificates are active
- [ ] DNS propagation is complete
- [ ] Performance is acceptable
- [ ] Monitoring is set up

## 📞 Support

If you encounter issues:

1. **Check the logs**: GitHub Actions, hosting service logs
2. **Test locally**: Use `./scripts/deploy.sh both --serve`
3. **Verify configuration**: DNS, CORS, environment variables
4. **Contact support**: Your hosting service's support team

---

**Congratulations!** Your NEXUS AI deployment is now live at:
- 🌐 App: https://nexus-agent.io
- 📚 Docs: https://nexus-agent.org 
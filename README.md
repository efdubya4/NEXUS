# NEXUS AI - Neural Expert eXchange & Unified Specialization System

An advanced AI system that combines multiple specialized agents to provide comprehensive assistance across various domains.

## 🌐 Domains

- **Application**: [nexus-agent.io](https://nexus-agent.io) - Live NEXUS AI application interface
- **Documentation**: [nexus-agent.org](https://nexus-agent.org) - Project documentation and marketing

## 🏗️ Project Structure

```
NEXUS/
├── app/                    # Application for nexus-agent.io
│   ├── index.html         # Main app interface
│   ├── script.js          # App JavaScript
│   ├── styles.css         # App styles
│   └── assets/            # App-specific assets
├── docs/                   # Documentation for nexus-agent.org
│   ├── index.html         # Documentation homepage
│   ├── pages/             # Documentation pages
│   ├── assets/            # Documentation assets
│   └── _config.yml        # Site configuration
├── shared/                 # Common assets and components
│   ├── components/         # Shared UI components
│   ├── styles/            # Shared styles
│   └── assets/            # Shared assets
├── backend/                # Backend API (for app domain)
│   ├── nexus_api.py       # Flask API server
│   ├── nexus_guardian.py  # NEXUS Guardian core
│   └── requirements.txt   # Python dependencies
├── .github/workflows/      # GitHub Actions deployment
│   ├── deploy-app.yml     # App deployment workflow
│   └── deploy-docs.yml    # Docs deployment workflow
├── scripts/                # Build and deployment scripts
│   ├── build-app.sh       # App build script
│   ├── build-docs.sh      # Docs build script
│   └── deploy.sh          # Main deployment script
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd NEXUS
   ```

2. **Set up the backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   python nexus_api.py
   ```

3. **Build and serve the app locally**
   ```bash
   ./scripts/deploy.sh app --serve
   ```

4. **Build and serve the docs locally**
   ```bash
   ./scripts/deploy.sh docs --serve
   ```

## 🛠️ Development

### Building the Application

```bash
# Build app only
./scripts/deploy.sh app

# Build docs only
./scripts/deploy.sh docs

# Build both
./scripts/deploy.sh both

# Build and serve locally
./scripts/deploy.sh app --serve
```

### Backend Development

The backend API is built with Flask and provides the following endpoints:

- `POST /api/nexus/query` - Process user queries
- `GET /api/nexus/status` - Get system status
- `GET /api/nexus/metrics` - Get performance metrics
- `GET /api/nexus/agents` - Get available agents
- `POST /api/nexus/test` - Test endpoint
- `GET /health` - Health check

### Frontend Development

The frontend consists of two main parts:

1. **App** (`app/`) - The main NEXUS AI application interface
2. **Docs** (`docs/`) - Documentation and marketing site

Both use vanilla HTML, CSS, and JavaScript for simplicity and fast loading.

## 🌍 Deployment

### Automatic Deployment (GitHub Actions)

The project uses GitHub Actions for automatic deployment:

- **App**: Deploys to `nexus-agent.io` when changes are pushed to `main` branch
- **Docs**: Deploys to `nexus-agent.org` when changes are pushed to `main` branch

### Manual Deployment

1. **Build the project**
   ```bash
   ./scripts/deploy.sh both
   ```

2. **Deploy to your hosting service**
   - App files: `dist/app/`
   - Docs files: `dist/docs/`

### Backend Deployment

The backend can be deployed to various services:

- **Railway**: `railway up`
- **Heroku**: `heroku create && git push heroku main`
- **Vercel**: `vercel --prod`
- **DigitalOcean App Platform**: Upload the backend directory

## 🔧 Configuration

### Environment Variables

For the backend API:

```bash
# Development
FLASK_ENV=development
PORT=5001

# Production
FLASK_ENV=production
PORT=8080
```

### Domain Configuration

1. **DNS Setup**
   - Point `nexus-agent.io` to GitHub Pages
   - Point `nexus-agent.org` to GitHub Pages
   - Point `api.nexus-agent.io` to your backend hosting

2. **GitHub Pages**
   - Enable GitHub Pages in repository settings
   - Configure custom domains for both sites
   - Set up SSL certificates (automatic with GitHub Pages)

## 📚 Documentation

- [Getting Started](https://nexus-agent.org/pages/getting-started.html)
- [API Reference](https://nexus-agent.org/pages/api-reference.html)
- [Agent Guide](https://nexus-agent.org/pages/agent-guide.html)
- [Examples](https://nexus-agent.org/pages/examples.html)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with `./scripts/deploy.sh both --serve`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [nexus-agent.org](https://nexus-agent.org)
- **Application**: [nexus-agent.io](https://nexus-agent.io)
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Contact**: contact@nexus-agent.org

## 🎯 Roadmap

- [ ] Add more specialized agents
- [ ] Implement user authentication
- [ ] Add conversation history
- [ ] Create mobile app
- [ ] Add API rate limiting
- [ ] Implement advanced analytics

---

Built with ❤️ by the NEXUS AI team
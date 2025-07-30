#!/bin/bash

# NEXUS AI Deployment Script
# This script deploys both the app and documentation sites

set -e

echo "🚀 NEXUS AI Deployment Script"
echo "=============================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[HEADER]${NC} $1"
}

# Check arguments
if [ $# -eq 0 ]; then
    echo "Usage: $0 [app|docs|both] [--serve]"
    echo ""
    echo "Options:"
    echo "  app     - Deploy only the application (nexus-agent.io)"
    echo "  docs    - Deploy only the documentation (nexus-agent.org)"
    echo "  both    - Deploy both app and docs"
    echo "  --serve - Start local server after build for testing"
    echo ""
    echo "Examples:"
    echo "  $0 app --serve    # Build and serve app locally"
    echo "  $0 docs           # Build docs only"
    echo "  $0 both           # Build both app and docs"
    exit 1
fi

DEPLOY_TYPE=$1
SERVE_FLAG=""

if [ "$2" = "--serve" ]; then
    SERVE_FLAG="--serve"
fi

# Check if we're in the right directory
if [ ! -f "app/index.html" ] || [ ! -f "docs/index.html" ]; then
    print_error "Required directories not found. Please run this script from the project root."
    exit 1
fi

print_header "Starting NEXUS AI deployment..."

# Create dist directory
mkdir -p dist

# Deploy based on type
case $DEPLOY_TYPE in
    "app")
        print_status "Deploying NEXUS AI App (nexus-agent.io)..."
        ./scripts/build-app.sh $SERVE_FLAG
        print_status "✅ App deployment completed!"
        ;;
    "docs")
        print_status "Deploying NEXUS AI Documentation (nexus-agent.org)..."
        ./scripts/build-docs.sh $SERVE_FLAG
        print_status "✅ Documentation deployment completed!"
        ;;
    "both")
        print_status "Deploying both NEXUS AI App and Documentation..."
        
        print_status "Building app..."
        ./scripts/build-app.sh
        
        print_status "Building docs..."
        ./scripts/build-docs.sh
        
        print_status "✅ Both deployments completed!"
        
        if [ "$SERVE_FLAG" = "--serve" ]; then
            print_warning "Cannot serve both simultaneously. Use individual commands:"
            echo "  $0 app --serve    # For app"
            echo "  $0 docs --serve   # For docs"
        fi
        ;;
    *)
        print_error "Invalid deployment type: $DEPLOY_TYPE"
        echo "Valid options: app, docs, both"
        exit 1
        ;;
esac

# Summary
print_header "Deployment Summary"
echo "======================"

if [ "$DEPLOY_TYPE" = "app" ] || [ "$DEPLOY_TYPE" = "both" ]; then
    echo "🌐 App: https://nexus-agent.io"
    echo "📁 App build: dist/app/"
fi

if [ "$DEPLOY_TYPE" = "docs" ] || [ "$DEPLOY_TYPE" = "both" ]; then
    echo "📚 Docs: https://nexus-agent.org"
    echo "📁 Docs build: dist/docs/"
fi

echo ""
print_status "Next steps:"
echo "1. Push to GitHub to trigger automatic deployment"
echo "2. Configure DNS records for your domains"
echo "3. Set up GitHub Pages with custom domains"
echo "4. Deploy backend API to your preferred hosting service"

echo ""
print_status "Deployment completed successfully! 🎉" 
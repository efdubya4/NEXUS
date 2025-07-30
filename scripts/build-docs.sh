#!/bin/bash

# NEXUS AI Documentation Build Script
# This script builds the NEXUS AI documentation site for deployment

set -e

echo "📚 Building NEXUS AI Documentation..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# Check if we're in the right directory
if [ ! -f "docs/index.html" ]; then
    print_error "Docs directory not found. Please run this script from the project root."
    exit 1
fi

print_status "Starting documentation build process..."

# Create build directory
BUILD_DIR="dist/docs"
mkdir -p $BUILD_DIR

print_status "Copying documentation files..."

# Copy docs files
cp -r docs/* $BUILD_DIR/

# Copy shared assets if they exist
if [ -d "shared" ]; then
    print_status "Copying shared assets..."
    cp -r shared/* $BUILD_DIR/ 2>/dev/null || true
fi

# Create CNAME file for custom domain
echo "nexus-agent.org" > $BUILD_DIR/CNAME

# Generate sitemap
print_status "Generating sitemap..."
cat > $BUILD_DIR/sitemap.xml << EOF
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://nexus-agent.org/</loc>
    <lastmod>$(date -u +%Y-%m-%d)</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://nexus-agent.org/pages/getting-started.html</loc>
    <lastmod>$(date -u +%Y-%m-%d)</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://nexus-agent.org/pages/api-reference.html</loc>
    <lastmod>$(date -u +%Y-%m-%d)</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://nexus-agent.org/pages/agent-guide.html</loc>
    <lastmod>$(date -u +%Y-%m-%d)</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://nexus-agent.org/pages/examples.html</loc>
    <lastmod>$(date -u +%Y-%m-%d)</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
</urlset>
EOF

# Create robots.txt
cat > $BUILD_DIR/robots.txt << EOF
User-agent: *
Allow: /

Sitemap: https://nexus-agent.org/sitemap.xml
EOF

# Optimize images (if ImageMagick is available)
if command -v convert &> /dev/null; then
    print_status "Optimizing images..."
    find $BUILD_DIR -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" | while read file; do
        convert "$file" -strip -quality 85 "$file"
    done
else
    print_warning "ImageMagick not found. Skipping image optimization."
fi

# Minify CSS and JS (if tools are available)
if command -v uglifyjs &> /dev/null; then
    print_status "Minifying JavaScript..."
    find $BUILD_DIR -name "*.js" | while read file; do
        uglifyjs "$file" -o "$file" --compress --mangle
    done
else
    print_warning "UglifyJS not found. Skipping JavaScript minification."
fi

if command -v cleancss &> /dev/null; then
    print_status "Minifying CSS..."
    find $BUILD_DIR -name "*.css" | while read file; do
        cleancss "$file" -o "$file"
    done
else
    print_warning "CleanCSS not found. Skipping CSS minification."
fi

# Create deployment manifest
cat > $BUILD_DIR/deployment.json << EOF
{
  "version": "$(date +%Y%m%d-%H%M%S)",
  "build_time": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "domain": "nexus-agent.org",
  "type": "documentation"
}
EOF

# Set proper permissions
chmod -R 755 $BUILD_DIR

print_status "Documentation build completed successfully!"
print_status "Build directory: $BUILD_DIR"
print_status "Files built: $(find $BUILD_DIR -type f | wc -l)"

# Optional: Start local server for testing
if [ "$1" = "--serve" ]; then
    print_status "Starting local server for testing..."
    cd $BUILD_DIR
    python3 -m http.server 8001 &
    SERVER_PID=$!
    echo "Server running at http://localhost:8001"
    echo "Press Ctrl+C to stop the server"
    trap "kill $SERVER_PID" INT
    wait $SERVER_PID
fi

echo "✅ NEXUS AI documentation build completed!" 
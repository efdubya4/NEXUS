#!/bin/bash

# NEXUS AI App Build Script
# This script builds the NEXUS AI application for deployment

set -e

echo "🚀 Building NEXUS AI App..."

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
if [ ! -f "app/index.html" ]; then
    print_error "App directory not found. Please run this script from the project root."
    exit 1
fi

print_status "Starting build process..."

# Create build directory
BUILD_DIR="dist/app"
mkdir -p $BUILD_DIR

print_status "Copying app files..."

# Copy app files
cp -r app/* $BUILD_DIR/

# Copy shared assets if they exist
if [ -d "shared" ]; then
    print_status "Copying shared assets..."
    cp -r shared/* $BUILD_DIR/ 2>/dev/null || true
fi

# Create CNAME file for custom domain
echo "nexus-agent.io" > $BUILD_DIR/CNAME

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
  "domain": "nexus-agent.io",
  "type": "app"
}
EOF

# Set proper permissions
chmod -R 755 $BUILD_DIR

print_status "Build completed successfully!"
print_status "Build directory: $BUILD_DIR"
print_status "Files built: $(find $BUILD_DIR -type f | wc -l)"

# Optional: Start local server for testing
if [ "$1" = "--serve" ]; then
    print_status "Starting local server for testing..."
    cd $BUILD_DIR
    python3 -m http.server 8000 &
    SERVER_PID=$!
    echo "Server running at http://localhost:8000"
    echo "Press Ctrl+C to stop the server"
    trap "kill $SERVER_PID" INT
    wait $SERVER_PID
fi

echo "✅ NEXUS AI app build completed!" 
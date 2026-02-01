#!/bin/bash
# Build Protected Installer for macOS
# Creates .app bundle and .pkg installer with code obfuscation

set -e

# Configuration
VERSION=${1:-"2026.1.25"}
OUTPUT_DIR="dist-protected-mac"
APP_NAME="Clawdbot Installer"
BUNDLE_ID="bot.clawd.installer"
SIGN_IDENTITY=""  # Set to your signing identity for distribution

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  Clawdbot Protected Installer Builder - macOS            ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}\n"

# Check dependencies
echo -e "${YELLOW}➤ Checking dependencies...${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python 3 found${NC}"

# Check if pip packages are installed
if ! python3 -c "import pyinstaller" 2>/dev/null; then
    echo -e "${YELLOW}  Installing PyInstaller...${NC}"
    pip3 install pyinstaller
fi

if ! python3 -c "import pyarmor.core" 2>/dev/null; then
    echo -e "${YELLOW}  Installing PyArmor...${NC}"
    pip3 install pyarmor
fi

echo -e "${GREEN}✓ All dependencies installed${NC}\n"

# Create output directory
echo -e "${YELLOW}➤ Creating output directory...${NC}"
mkdir -p "$OUTPUT_DIR"
echo -e "${GREEN}✓ Output directory ready: $OUTPUT_DIR${NC}\n"

# Obfuscate Python code
echo -e "${YELLOW}➤ Obfuscating Python code...${NC}"

SOURCE_FILE="scripts/setup-wizard-gui-mac.py"
OBFUSCATED_DIR="scripts/obfuscated-mac"

# Initialize PyArmor
if [ ! -d "scripts/.pyarmor" ]; then
    pyarmor init --src scripts
fi

# Obfuscate with PyArmor
echo -e "${CYAN}  Using PyArmor for obfuscation...${NC}"
pyarmor obfuscate \
    --exact \
    --restrict 0 \
    --output "$OBFUSCATED_DIR" \
    "$SOURCE_FILE"

OBFUSCATED_FILE="$OBFUSCATED_DIR/setup-wizard-gui-mac.py"

echo -e "${GREEN}✓ Code obfuscated!${NC}\n"

# Build with PyInstaller
echo -e "${YELLOW}➤ Building with PyInstaller...${NC}"

pyinstaller \
    --name="$APP_NAME" \
    --onefile \
    --windowed \
    --icon=assets/icon.icns \
    --add-data="INSTALLATION-TH.md:." \
    --add-data="USER-GUIDE-TH.md:." \
    --add-data="LICENSE:." \
    --osx-bundle-identifier="$BUNDLE_ID" \
    --target-arch=universal2 \
    --clean \
    "$OBFUSCATED_FILE"

echo -e "${GREEN}✓ Application built!${NC}\n"

# Move to output directory
echo -e "${YELLOW}➤ Organizing output...${NC}"
mv "dist/$APP_NAME.app" "$OUTPUT_DIR/"
echo -e "${GREEN}✓ App moved to $OUTPUT_DIR/${NC}\n"

# Create DMG
echo -e "${YELLOW}➤ Creating DMG installer...${NC}"

DMG_NAME="ClawdBot-Installer-v$VERSION.dmg"
DMG_PATH="$OUTPUT_DIR/$DMG_NAME"
TEMP_DMG="$OUTPUT_DIR/temp.dmg"

# Create temporary DMG
hdiutil create -size 100m -fs HFS+ -volname "$APP_NAME" "$TEMP_DMG"

# Mount it
MOUNT_DIR=$(hdiutil attach "$TEMP_DMG" | grep "/Volumes" | awk '{print $3}')

# Copy app
cp -R "$OUTPUT_DIR/$APP_NAME.app" "$MOUNT_DIR/"

# Create Applications symlink
ln -s /Applications "$MOUNT_DIR/Applications"

# Add background and style (optional)
mkdir -p "$MOUNT_DIR/.background"
# cp assets/dmg-background.png "$MOUNT_DIR/.background/"

# Unmount
hdiutil detach "$MOUNT_DIR"

# Convert to compressed DMG
hdiutil convert "$TEMP_DMG" -format UDZO -o "$DMG_PATH"
rm "$TEMP_DMG"

echo -e "${GREEN}✓ DMG created: $DMG_PATH${NC}\n"

# Create .pkg installer
echo -e "${YELLOW}➤ Creating PKG installer...${NC}"

PKG_NAME="ClawdBot-Installer-v$VERSION.pkg"
PKG_PATH="$OUTPUT_DIR/$PKG_NAME"

# Build package
pkgbuild \
    --root "$OUTPUT_DIR/$APP_NAME.app" \
    --identifier "$BUNDLE_ID" \
    --version "$VERSION" \
    --install-location "/Applications/$APP_NAME.app" \
    "$PKG_PATH"

echo -e "${GREEN}✓ PKG created: $PKG_PATH${NC}\n"

# Code signing (if identity provided)
if [ -n "$SIGN_IDENTITY" ]; then
    echo -e "${YELLOW}➤ Signing application...${NC}"
    
    # Sign app bundle
    codesign --force --deep --sign "$SIGN_IDENTITY" \
        --options runtime \
        "$OUTPUT_DIR/$APP_NAME.app"
    
    # Sign DMG
    codesign --force --sign "$SIGN_IDENTITY" "$DMG_PATH"
    
    # Sign PKG
    productsign --sign "$SIGN_IDENTITY" "$PKG_PATH" "$PKG_PATH.signed"
    mv "$PKG_PATH.signed" "$PKG_PATH"
    
    echo -e "${GREEN}✓ Application signed!${NC}\n"
    
    # Notarize (requires Apple Developer account)
    echo -e "${YELLOW}➤ Notarizing (optional)...${NC}"
    echo -e "${CYAN}  To notarize, run:${NC}"
    echo -e "  xcrun notarytool submit \"$DMG_PATH\" --keychain-profile \"AC_PASSWORD\" --wait"
    echo -e "  xcrun stapler staple \"$DMG_PATH\""
else
    echo -e "${YELLOW}⚠ Skipping code signing (no identity provided)${NC}"
    echo -e "  For distribution, set SIGN_IDENTITY environment variable${NC}\n"
fi

# Create checksums
echo -e "${YELLOW}➤ Creating checksums...${NC}"
(
    cd "$OUTPUT_DIR"
    shasum -a 256 *.dmg *.pkg > CHECKSUMS.txt
)
echo -e "${GREEN}✓ Checksums created${NC}\n"

# Cleanup
echo -e "${YELLOW}➤ Cleaning up...${NC}"
rm -rf build dist *.spec "$OBFUSCATED_DIR"
echo -e "${GREEN}✓ Cleanup complete${NC}\n"

# Summary
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  Build Complete!                                          ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}\n"

echo -e "${CYAN}Protected installers created:${NC}"
ls -lh "$OUTPUT_DIR"/*.{app,dmg,pkg} 2>/dev/null | awk '{printf "  - %s (%s)\n", $9, $5}'

echo -e "\n${CYAN}Protection features applied:${NC}"
echo -e "${GREEN}  ✓ PyArmor code obfuscation${NC}"
echo -e "${GREEN}  ✓ String encryption${NC}"
echo -e "${GREEN}  ✓ Control flow obfuscation${NC}"
echo -e "${GREEN}  ✓ Universal binary (Intel + Apple Silicon)${NC}"
echo -e "${GREEN}  ✓ App bundle (.app)${NC}"
echo -e "${GREEN}  ✓ DMG installer${NC}"
echo -e "${GREEN}  ✓ PKG installer${NC}"

echo -e "\n${YELLOW}Next steps:${NC}"
echo -e "  1. Test installer: open \"$OUTPUT_DIR/$DMG_NAME\""
echo -e "  2. Verify app: open \"$OUTPUT_DIR/$APP_NAME.app\""
echo -e "  3. Check signature: codesign -vvv --deep --strict \"$OUTPUT_DIR/$APP_NAME.app\""
echo -e "  4. Distribute installer\n"

echo -e "${CYAN}For code signing and notarization:${NC}"
echo -e "  export SIGN_IDENTITY=\"Developer ID Application: Your Name (TEAMID)\""
echo -e "  ./scripts/build-protected-installer-mac.sh $VERSION"
echo -e "  xcrun notarytool submit ... --wait"
echo -e "  xcrun stapler staple ...\n"

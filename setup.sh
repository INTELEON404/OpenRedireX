#!/bin/bash

# Define constants for neatness
TOOL_NAME="openredirex"
SOURCE_FILE="openredirex"
INSTALL_PATH="/usr/local/bin/$TOOL_NAME"

echo "[*] STARTING INSTALLATION OF $TOOL_NAME..."

# 1. Check if the source file exists before moving
if [ ! -f "$SOURCE_FILE" ]; then
    echo "[-] Error: $SOURCE_FILE NOT FOUND IN THE CURRENT DIRECTORY."
    exit 1
fi

# 2. Rename and Move 
echo "[+] Moving $TOOL_NAME to $INSTALL_PATH..."
sudo mv "$SOURCE_FILE" "$INSTALL_PATH"

# 3. Set permissions
echo "[+] SETTING EXECUTABLE PERMISSIONS..."
sudo chmod +x "$INSTALL_PATH"

# 4. Clean up junk files
echo "[+] CLEANING UP TEMPORARY FILES..."
rm -f openredirex.pyc 2>/dev/null
rm -rf __pycache__ 2>/dev/null

# 5. Verify installation
if command -v $TOOL_NAME >/dev/null 2>&1; then
    echo "[!] $TOOL_NAME HAS BEEN INSTALLED SUCCESSFULLY!"
    echo "[*] YOU CAN NOW RUN IT FROM ANYWHERE BY TYPING: $TOOL_NAME"
else
    echo "[-] INSTALLATION FAILED. PLEASE CHECK YOUR /usr/local/bin permissions."
fi

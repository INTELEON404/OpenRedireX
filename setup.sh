#!/bin/bash

TOOL_NAME="openredirex"
SOURCE_FILE="openredirex.py"
INSTALL_PATH="/usr/local/bin/$TOOL_NAME"

echo "[*] Starting installation of $TOOL_NAME..."

if [ ! -f "$SOURCE_FILE" ]; then
    echo "[-] Error: $SOURCE_FILE not found in the current directory."
    exit 1
fi


echo "[+] Moving $TOOL_NAME to $INSTALL_PATH..."
sudo mv "$SOURCE_FILE" "$INSTALL_PATH"

echo "[+] Setting executable permissions..."
sudo chmod +x "$INSTALL_PATH"


echo "[+] Cleaning up temporary files..."
rm -f openredirex.pyc 2>/dev/null
rm -rf __pycache__ 2>/dev/null


if command -v $TOOL_NAME >/dev/null 2>&1; then
    echo "[!] $TOOL_NAME has been installed successfully!"
    echo "[*] You can now run it from anywhere by typing: $TOOL_NAME"
else
    echo "[-] Installation failed. Please check your /usr/local/bin permissions."
fi

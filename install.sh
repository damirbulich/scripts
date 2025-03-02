#!/bin/bash

# install_aliases.sh

# Function to find Python 3 binary
find_python3() {
    for py in python3 python python3.11 python3.10 python3.9; do
        if command -v "$py" >/dev/null 2>&1; then
            if "$py" --version 2>/dev/null | grep -q "Python 3"; then
                echo "$py"
                return 0
            fi
        fi
    done
    echo "python3"
    return 1
}

# Get the directory where this script is located (repo root)
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Determine which shell config file to use
CONFIG_FILE=""
if [ -f "$HOME/.zshrc" ] && [ "$SHELL" = "/bin/zsh" ] || [ "$SHELL" = "/usr/bin/zsh" ]; then
    CONFIG_FILE="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    CONFIG_FILE="$HOME/.bashrc"
else
    echo "Neither .bashrc nor .zshrc found. Creating .bashrc"
    CONFIG_FILE="$HOME/.bashrc"
    touch "$CONFIG_FILE"
fi

# Find Python 3 binary
PYTHON3_BIN=$(find_python3)
if [ $? -ne 0 ]; then
    echo "Warning: Could not verify Python 3 installation. Using 'python3' as default"
fi

# Define the aliases
ALIASES="# Aliases from repo at $REPO_DIR
alias ctx='$REPO_DIR/contextify.sh'
alias modgen='$PYTHON3_BIN $REPO_DIR/nestjs-modgen.py'
alias work='$REPO_DIR/tmux-work.sh'"

# Escape special characters in REPO_DIR for sed
ESCAPED_REPO_DIR=$(printf '%s\n' "$REPO_DIR" | sed 's/[[\.*^$/]/\\&/g')

# Check if aliases already exist and update the file
if grep -q "# Aliases from repo at $REPO_DIR" "$CONFIG_FILE"; then
    echo "Aliases already exist in $CONFIG_FILE. Updating them..."
    # Create a temporary file
    TEMP_FILE=$(mktemp)
    # Remove existing aliases block and write to temp file
    sed "/# Aliases from repo at $ESCAPED_REPO_DIR/,/alias work/d" "$CONFIG_FILE" > "$TEMP_FILE"
    # Move temp file to original location
    mv "$TEMP_FILE" "$CONFIG_FILE"
fi

# Append aliases to config file
echo -e "\n$ALIASES" >> "$CONFIG_FILE"

echo "Aliases installed to $CONFIG_FILE!"
echo "Please run 'source $CONFIG_FILE' or restart your terminal to use them."
echo "Installed aliases:"
echo "  ctx    -> $REPO_DIR/contextify.sh"
echo "  modgen -> $PYTHON3_BIN $REPO_DIR/nestjs-modgen.py"
echo "  work   -> $REPO_DIR/tmux-work.sh"

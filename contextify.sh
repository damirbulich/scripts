#!/bin/bash

# Temporary file to store the output before copying to clipboard
temp_file=$(mktemp)

# Function to process files
process_files() {
    local dir="$1"
    # Find all files and process them (relative to current dir)
    find "$dir" -type f | while read -r file; do
        # Skip binary files and common non-text extensions
        case "$file" in
            *.png|*.jpg|*.jpeg|*.gif|*.bmp|*.pdf|*.zip|*.tar|*.gz|*.bin|*.exe|*.o)
                continue;;
        esac
        
        # Add file path as header (relative to current dir)
        relative_path="${file#./}"
        echo "=== Content from: $relative_path ===" >> "$temp_file"
        
        # Try to extract text content
        if file "$file" | grep -q "text"; then
            cat "$file" >> "$temp_file" 2>/dev/null
            echo -e "\n" >> "$temp_file"
        fi
    done
}

# Check if fzf is installed
if ! command -v fzf >/dev/null 2>&1; then
    echo "Error: fzf is not installed. Please install it first."
    rm -f "$temp_file"
    exit 1
fi

echo "Select subfolders to process (TAB to toggle selection, Enter to confirm):"
# Use find to list directories in CWD, pipe to fzf with multi-select and preview
selected_dirs=$(find . -type d | fzf -m --preview 'tree -C {} | head -n 20' --preview-window=up:40%)

if [ -z "$selected_dirs" ]; then
    echo "No folders selected. Exiting."
    rm -f "$temp_file"
    exit 0
fi

# Process each selected directory, handling multi-line input correctly
echo "Selected folders:"
echo "$selected_dirs" | while IFS= read -r dir; do
    echo "  - $dir"
    process_files "$dir"
done

# Function to copy to clipboard
copy_to_clipboard() {
    if command -v xclip >/dev/null 2>&1; then
        xclip -selection clipboard < "$temp_file"
    elif command -v wl-copy >/dev/null 2>&1; then
        wl-copy < "$temp_file"
    elif command -v pbcopy >/dev/null 2>&1; then
        pbcopy < "$temp_file"
    else
        echo "Error: No clipboard tool found (install xclip, wl-copy, or pbcopy)"
        cat "$temp_file"  # Output to terminal as fallback
        rm -f "$temp_file"
        exit 1
    fi
}

# Copy to clipboard and clean up
if [ -s "$temp_file" ]; then
    copy_to_clipboard
    echo "Done! Text has been copied to clipboard."
    echo "Total lines: $(wc -l < "$temp_file")"
else
    echo "No text content found to copy."
fi

# Clean up temporary file
rm -f "$temp_file"

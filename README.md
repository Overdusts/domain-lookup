# DOMAIN LOOKUP TOOL

A simple Python GUI application that searches for specific domains in all `.txt` files within a selected folder.

## Features

- 🔍 **Easy Folder Selection**: Browse and select any folder on your system
- 📝 **Domain Search**: Search for any domain name in all text files
- 🔄 **Recursive Search**: Searches through all subdirectories automatically
- 📊 **Detailed Results**: Shows file names, line numbers, and matching content
- 💾 **Export Results**: Save search results to a text file
- ⚡ **Fast & Efficient**: Uses regex for quick pattern matching
- 🎨 **User-Friendly GUI**: Clean interface with progress indicator

## Requirements

- Python 3.6 or higher
- tkinter (usually comes pre-installed with Python)

## Installation

1. Clone this repository or download the `domain_finder.py` file
2. Make sure you have Python installed:
   ```bash
   python3 --version
   ```

No additional packages needed! tkinter comes with Python by default.

## Usage

### Running the Tool

**Linux/Mac:**
```bash
python3 domain_finder.py
```

**Windows:**
```bash
python domain_finder.py
```

Or simply double-click the `domain_finder.py` file.

### How to Use

1. **Select Folder**: Click the "Browse" button next to "Select Folder" and choose the folder containing your .txt files
2. **Enter Domain**: Type the domain you want to search for (e.g., `example.com`, `google.com`)
3. **Search**: Click the "Search" button or press Enter
4. **View Results**: Results will appear in the text area showing:
   - Total number of matches
   - File names where matches were found
   - Line numbers and content
5. **Export** (Optional): Click "Export Results" to save the results to a file

### Example

If you search for `github.com` in a folder containing text files, the tool will:
- Find all occurrences of "github.com" (case-insensitive)
- Show you which files contain the domain
- Display the exact line numbers and content
- Allow you to export the results for later reference

## Features Explained

### Case-Insensitive Search
The search is case-insensitive, so searching for `Example.COM` will match `example.com`, `EXAMPLE.COM`, `Example.com`, etc.

### Recursive Search
The tool automatically searches through all subdirectories within the selected folder.

### File Encoding
The tool handles various text encodings and will skip over any characters it can't read, ensuring it doesn't crash on unusual files.

## Use Cases

- Find all references to a specific domain in log files
- Search for URLs in documentation
- Locate email addresses from a particular domain
- Audit files for specific website mentions
- Compliance and security audits

## Contributing

Feel free to fork this project and submit pull requests for any improvements!

## License

MIT License - feel free to use this tool however you like!

## Troubleshooting

### "Module not found: tkinter"
**Linux users**: Install tkinter with:
```bash
sudo apt-get install python3-tk  # Debian/Ubuntu
sudo yum install python3-tkinter  # Fedora/RHEL
```

**Mac users**: tkinter should come with Python. If not, reinstall Python from python.org

**Windows users**: Reinstall Python and make sure to check "tcl/tk and IDLE" during installation

### "Permission Denied"
Make the script executable:
```bash
chmod +x domain_finder.py
```

### Large Folders Are Slow
The tool searches through all .txt files recursively. For folders with thousands of files, it may take a few seconds. The progress bar will show activity during the search.

## Author

Created for easy domain searching in text files!

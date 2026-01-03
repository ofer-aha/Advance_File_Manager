# Advanced File Manager

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

A powerful desktop application for managing file operations with hash verification, duplicate detection, and intelligent move/copy capabilities.

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Configuration](#configuration) • [Contributing](#contributing)

</div>

---

## 🌟 Features

### File Operations
- **Smart Move/Copy**: Intelligently moves or copies files based on configurable size thresholds
- **Hash Verification**: Ensures file integrity during move/copy operations using SHA-256
- **Batch Processing**: Handle multiple files efficiently with progress tracking
- **Undo Support**: Full undo capability for move and copy operations
- **Dry Run Mode**: Preview operations before execution
- **Extension Grouping**: Automatically organize files by extension

### Hash & Integrity Tools
- **Multiple Hash Algorithms**: Support for MD5, SHA-1, SHA-256, and SHA-512
- **File Hash Calculator**: Calculate and compare file hashes
- **Folder Hash Scanner**: Batch hash calculation for entire directories
- **Hash Tree Builder**: Create hierarchical hash trees with export capability
- **Folder Comparison**: Compare source and destination folders by hash

### Duplicate Detection
- **Smart Duplicate Finder**: Detect duplicate files using configurable hash algorithms
- **Group Selection**: Select all duplicates except one per group
- **Bulk Operations**: Delete or move duplicate files in bulk
- **Progress Tracking**: Real-time progress display with current file indicator

### User Interface
- **Modern GUI**: Built with CustomTkinter for a sleek, modern appearance
- **Multi-language Support**: Hebrew and English interface languages
- **Dark/Light Themes**: Auto, dark, and light theme options
- **Tabbed Interface**: Organized workflow with dedicated tabs for each function

### Logging & Monitoring
- **Comprehensive Logging**: All operations logged with timestamps
- **Log Viewer**: Built-in log file viewer and manager
- **Automatic Cleanup**: Configurable log retention period

---

## 📋 Requirements

- Python 3.9 or higher
- Operating System: Windows, Linux, or macOS

### Dependencies
```
customtkinter>=5.0.0
```

---

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/ofer-aha/Advance_File_Manager.git
cd Advance_File_Manager
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install customtkinter
```

### 3. Run the Application
```bash
python file_org/file_org.py
```

---

## 📖 Usage

### Move/Copy Files

1. **Select Source and Destination Folders**
   - Click "Browse" to choose folders
   
2. **Choose Operation Mode**
   - Select "Move Files" or "Copy Files"
   
3. **Configure Settings**
   - Set Smart Move threshold (MB)
   - Enable/disable options:
     - Multithreading
     - Dry Run
     - Clean Empty Folders
     - Group by Extension

4. **Start Operation**
   - Click "Start Move" or "Start Copy"
   - Monitor progress in real-time

### Hash Verification

#### Single File Hash
1. Navigate to **Hash Check → File Hash** tab
2. Select a file
3. Choose hash algorithm (MD5, SHA-1, SHA-256, SHA-512)
4. Click "Calculate Hash"
5. Compare with expected hash if needed

#### Folder Hash Scan
1. Navigate to **Hash Check → Folder Hash** tab
2. Select folder to scan
3. Choose hash algorithms (can select multiple)
4. Click "Start Folder Hash"
5. Export results as TXT or JSON

#### Hash Tree
1. Navigate to **Hash Check → Hash Tree** tab
2. Select root folder
3. Choose algorithms
4. Click "Build Hash Tree"
5. View hierarchical structure
6. Export as JSON

### Duplicate Detection

1. Navigate to **Hash Check → Duplicates** tab
2. Select folder to scan
3. Choose hash algorithm
4. Click "Find Duplicates"
5. Review duplicate groups
6. Use actions:
   - **Select All But 1 per Group**: Keeps one copy of each duplicate
   - **Delete Selected Files**: Permanently delete selected duplicates
   - **Move Selected Files**: Move duplicates to another location

### Folder Comparison

1. Navigate to **Hash Check → Compare** tab
2. Select source and destination folders
3. Choose hash algorithm
4. Click "Start Compare"
5. Review results:
   - **MATCH**: Files are identical
   - **MISMATCH**: Files differ
   - **MISSING**: File not found in destination
6. Export results if needed

### Undo Operations

1. Navigate to **Undo** tab
2. View operation history
3. Select operations to undo:
   - **Undo Selected**: Undo specific operations
   - **Undo Last**: Undo most recent operation
   - **Undo All**: Undo all pending operations

### Settings

1. Navigate to **Settings** tab
2. Configure:
   - Language (Hebrew/English)
   - Theme Mode (Light/Dark/Auto)
   - Smart Move Threshold (MB)
   - Log Retention (days)
3. Click "Save Settings"

---

## 🛠️ Configuration

The application stores configuration in `config.json`:

```json
{
    "language": "en",
    "theme_mode": "auto",
    "smart_move_threshold": 50,
    "log_retention_days": 7
}
```

### Configuration Options

| Option | Values | Description |
|--------|--------|-------------|
| `language` | `"en"`, `"he"` | Interface language |
| `theme_mode` | `"light"`, `"dark"`, `"auto"` | UI theme |
| `smart_move_threshold` | Integer (MB) | Size threshold for smart move operations |
| `log_retention_days` | Integer (days) | Number of days to keep log files |

---

## 📝 Logging

Logs are stored in the `logs/` directory with the format `YYYY-MM-DD.log`.

### Log Levels
- **INFO**: Normal operations
- **WARN**: Warnings (e.g., hash mismatches)
- **ERROR**: Errors during operations
- **DETAIL**: Detailed operation information

---

## 🔒 Smart Move Logic

The application uses intelligent file moving strategies:

### Large Files (≥ Threshold)
- Direct move operation (faster)
- No hash verification needed
- Original file removed after move

### Small Files (< Threshold)
1. Copy file to destination
2. Calculate SHA-256 hash of both files
3. If hashes match: delete source file
4. If hashes mismatch: keep both files and log warning

### Copy Mode
- Always performs hash verification
- Keeps source file intact
- Removes destination copy if hash mismatch occurs

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add comments for complex logic
- Update documentation for new features
- Test thoroughly before submitting

---

## 🐛 Known Issues

- Large folder operations may take time (use multithreading option for better performance)
- Theme changes require application restart for full effect

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**Ofer Aha**

- GitHub: [@ofer-aha](https://github.com/ofer-aha)
- Project Link: [https://github.com/ofer-aha/Advance_File_Manager](https://github.com/ofer-aha/Advance_File_Manager)

---

## 🙏 Acknowledgments

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Inspired by advanced file management needs
- Thanks to all contributors and users

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/ofer-aha/Advance_File_Manager/issues) page
2. Create a new issue with detailed information
3. Include log files if applicable

---

## 🗺️ Roadmap

- [ ] Multi-threaded hash calculation
- [ ] Cloud storage integration
- [ ] File synchronization features
- [ ] Advanced filtering options
- [ ] Portable executable builds
- [ ] Plugin system
- [ ] Command-line interface

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ by Ofer Aha

</div>
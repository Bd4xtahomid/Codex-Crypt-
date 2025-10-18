# 🔐 Quantum Codex Crypt - Complete User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [How It Works](#how-it-works)
3. [Security Layers Explained](#security-layers-explained)
4. [Installation & Setup](#installation--setup)
5. [Configuration](#configuration)
6. [Usage Guide](#usage-guide)
7. [Features](#features)
8. [FAQ](#faq)
9. [Security Best Practices](#security-best-practices)

---

## Introduction

**Quantum Codex Crypt** is an advanced multi-layer encryption system that combines classical and quantum-resistant cryptography with steganography to provide ultimate message security. The system hides encrypted messages inside images, making them invisible to unauthorized viewers.

### Key Features
- ✅ **Quantum-Resistant Encryption** using Kyber ML-KEM-512
- ✅ **7-Layer Security Architecture** for maximum protection
- ✅ **Steganography** to hide encrypted data in images
- ✅ **Modern GUI & Terminal Interfaces**
- ✅ **Phrase Management** for quick message access
- ✅ **Copy-to-Clipboard** functionality
- ✅ **Progress Indicators** for encryption/decryption
- ✅ **Comprehensive Error Handling**

---

## How It Works

### Encryption Process
```
Original Message
    ↓
[1] Vigenère Cipher
    ↓
[2] Kyber ML-KEM-512 Encryption (Quantum-Resistant)
    ↓
[3] AES-256-GCM Encryption
    ↓
[4] HMAC-SHA256 Integrity Tag
    ↓
[5] Numeric Encoding (Obfuscation)
    ↓
[6] Data Scrambling
    ↓
[7] Base64 Encoding
    ↓
[8] LSB Steganography (Hide in Image)
    ↓
Secret Image (Looks Normal)
```

### Decryption Process
The decryption process reverses all the layers in the exact opposite order, requiring all three encryption keys:
1. **Vigenère Key** - For the classical cipher layer
2. **Kyber Decryption Key (DK)** - For quantum-resistant decryption
3. **Scramble Key** - For unscrambling the data

---

## Security Layers Explained

### Layer 1: Vigenère Cipher
- **What it does**: Classical polyalphabetic substitution cipher
- **Purpose**: Initial text obfuscation using a 37-character random key
- **Security**: Resistant to frequency analysis

### Layer 2: Kyber ML-KEM-512 (Quantum-Resistant)
- **What it does**: Post-quantum key encapsulation mechanism
- **Purpose**: Protection against future quantum computer attacks
- **Standard**: NIST FIPS 203 compliant
- **Security Level**: ~128-bit quantum security

### Layer 3: AES-256-GCM
- **What it does**: Advanced Encryption Standard with Galois/Counter Mode
- **Purpose**: Strong symmetric encryption of data
- **Key Size**: 256-bit (derived from Kyber shared secret)
- **Features**: Built-in authentication

### Layer 4: HMAC-SHA256
- **What it does**: Hash-based Message Authentication Code
- **Purpose**: Data integrity verification
- **Protection**: Detects tampering or corruption

### Layer 5: Numeric Encoding
- **What it does**: Converts bytes to numbers using mathematical transformation
- **Formula**: `(byte * multiplier + adder) % modulus`
- **Purpose**: Additional obfuscation layer

### Layer 6: Data Scrambling
- **What it does**: Randomly shuffles data positions using seed-based algorithm
- **Key**: 32-character scramble key
- **Purpose**: Makes pattern analysis impossible

### Layer 7: LSB Steganography
- **What it does**: Hides data in image's Least Significant Bits
- **Method**: Modifies the last bit of RGB pixel values
- **Result**: Visually identical image with hidden encrypted data

---

## Installation & Setup

### Requirements
- Python 3.11 or higher
- PNG image for cover (512x512 or larger recommended)

### Installation Steps

1. **Install Dependencies** (Auto-handled in Replit)
```bash
pip install kyber-py cryptography pillow rich pyperclip
```

2. **Setup Directories** (Auto-created on first run)
```
Secret/
├── images/      # Cover images
├── keys/        # Encryption keys
├── phrases/     # Saved messages
└── logs/        # Application logs

Decrypt/        # For no-input decryption
```

3. **Add Cover Image**
Place a PNG image in `Secret/images/cover.png` for encryption.

---

## Configuration

Edit `config.py` to customize the application:

### Operation Modes
```python
MODE = "gui"  # Options: "gui", "terminal_with_input", "terminal_no_input"
```

### Security Settings
```python
VIGENERE_KEY_LENGTH = 37      # Classical cipher key length
SCRAMBLE_KEY_LENGTH = 32      # Scramble key length
KYBER_SECURITY_LEVEL = 512    # Quantum security level
```

### Application Behavior
```python
AUTO_SAVE_PHRASES = False     # Auto-save messages as phrases
AUTO_COPY_KEYS = True         # Copy keys to clipboard
SHOW_PROGRESS = True          # Show progress indicators
```

### Logging
```python
ENABLE_LOGGING = True
LOG_LEVEL = "INFO"            # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

---

## Usage Guide

### GUI Mode

#### Starting the Application
```bash
python main.py
```

#### Encrypting a Message
1. **Enter Message**: Type directly or click "📝 Load Saved Phrase"
2. **Select Cover Image**: Click "📁 Browse" and choose a PNG image
3. **Encrypt**: Click "🔒 Encrypt & Hide in Image"
4. **Save Keys**: Keys are automatically saved and can be copied to clipboard
5. **Result**: Encrypted image saved in `Secret/YYYYMMDD_HHMMSS/images/secret.png`

#### Decrypting a Message
1. **Select Secret Image**: Browse to the encrypted PNG file
2. **Click Decrypt**: Click "🔓 Decrypt from Image"
3. **Enter Keys**: Provide all three keys when prompted
   - Vigenère Key
   - Kyber DK (hexadecimal)
   - Scramble Key
4. **View Result**: Decrypted message appears in output area

#### Phrase Management
- **Save Phrase**: Click "💾 Save Current Phrase" to store current message
- **Load Phrase**: Click "📝 Load Saved Phrase" to browse and select saved messages
- **Storage**: Phrases saved in `Secret/phrases/` with timestamps

#### Additional Features
- **Copy Output**: Click "📋 Copy to Clipboard" to copy results
- **Clear Fields**: Clear message or output areas with "🗑️ Clear" buttons
- **Status Bar**: Shows current operation status at bottom

---

### Terminal Mode (With Input)

#### Starting Interactive Terminal
```python
# In config.py
MODE = "terminal_with_input"
```

```bash
python main.py
```

#### Main Menu Options
```
1. Encrypt Message   🔒
2. Decrypt Message   🔓
3. View Saved Phrases 📝
4. Exit              🚪
```

#### Encrypting in Terminal
1. Select option **1** (Encrypt)
2. Choose message input:
   - Type new message
   - Load saved phrase
3. Enter cover image path (or use default)
4. Watch progress indicators
5. Keys displayed and optionally copied to clipboard

#### Decrypting in Terminal
1. Select option **2** (Decrypt)
2. Enter secret image path
3. Choose key input method:
   - Enter manually
   - Load from keys.txt file
4. View decrypted message
5. Optionally copy to clipboard

#### Viewing Saved Phrases
1. Select option **3** (View Phrases)
2. Browse table of saved phrases with timestamps
3. Select by number to view or use

---

### Terminal Mode (No Input)

Perfect for automation and scripting.

#### Configuration
```python
# In config.py
MODE = "terminal_no_input"
DEFAULT_ACTION = "encrypt"  # or "decrypt"
MESSAGE = "Your message here"
```

#### Auto-Encryption
```bash
python main.py
```
- Uses `MESSAGE` from config
- Uses `Secret/images/cover.png` as cover image
- Saves to timestamped folder automatically

#### Auto-Decryption
```python
# In config.py
DEFAULT_ACTION = "decrypt"
```

Required files in `Decrypt/` folder:
- `secret.png` - The encrypted image
- `keys.txt` - File containing all three keys

Format of `keys.txt`:
```
Vigenère Key: YOUR_KEY_HERE
Kyber DK: YOUR_HEX_KEY_HERE
Scramble Key: YOUR_SCRAMBLE_KEY_HERE
```

---

## Features

### 1. Phrase Management System
- **Save Messages**: Store frequently used messages
- **Quick Access**: Browse and load saved phrases
- **Timestamped**: Each phrase has unique timestamp
- **Searchable**: Easy to find specific phrases

### 2. Copy to Clipboard
- **Encryption Keys**: One-click copy of all keys
- **Decrypted Messages**: Copy results instantly
- **Cross-Platform**: Works on Windows, Mac, Linux

### 3. Progress Indicators
- **Visual Feedback**: See encryption/decryption progress
- **Layer Tracking**: Know which security layer is processing
- **Terminal & GUI**: Available in both interfaces

### 4. Error Handling
- **User-Friendly Messages**: Clear error explanations
- **Troubleshooting Hints**: Suggestions for common issues
- **Logging**: Detailed logs for debugging

### 5. Modern UI
- **Dark Theme**: Easy on the eyes
- **Rich Terminal**: Colored output, tables, panels
- **Intuitive Layout**: Logical flow and clear buttons

---

## FAQ

### Q: What image formats are supported?
**A:** Currently, only PNG format is supported for maximum steganography quality. JPEG compression can destroy hidden data.

### Q: Can I use the same cover image multiple times?
**A:** Yes, but each encryption creates a unique output image with different hidden data.

### Q: How secure is this really?
**A:** Extremely secure. The 7-layer approach with quantum-resistant Kyber makes it highly resistant to both classical and quantum attacks. The steganography layer adds invisibility.

### Q: What happens if I lose the keys?
**A:** The message is **permanently unrecoverable**. Always backup your keys securely. Consider:
- Encrypted password manager
- Physical backup in secure location
- Split keys across multiple secure channels

### Q: Can I encrypt files or only text?
**A:** Currently text only. File encryption may be added in future versions.

### Q: How large can my message be?
**A:** Limited by image size. A 512x512 PNG can hold ~50KB of encrypted data. Larger images = more capacity.

### Q: Does the secret image look different?
**A:** No! LSB steganography makes changes invisible to human eyes. The image looks identical to the original.

### Q: What's the Kyber DK hex format?
**A:** It's the decryption key in hexadecimal format (0-9, a-f). It's quite long (~1568 characters for ML-KEM-512).

---

## Security Best Practices

### Key Management
✅ **DO:**
- Store keys in encrypted password manager
- Use separate secure channels for sharing keys
- Backup keys in multiple secure locations
- Delete keys from clipboard after use
- Use unique keys for each message

❌ **DON'T:**
- Store keys in plain text files
- Send keys via same channel as encrypted image
- Reuse keys across multiple messages
- Leave keys in clipboard
- Share keys over unsecured channels

### Message Security
✅ **DO:**
- Use large, high-quality cover images (1024x1024 or larger)
- Verify message integrity after decryption
- Delete session folders after extracting data
- Use strong, random keys (auto-generated is best)

❌ **DON'T:**
- Use small or low-quality images
- Compress encrypted images (destroys hidden data)
- Modify secret images in any way
- Share cover image patterns publicly

### Operational Security
✅ **DO:**
- Run on trusted, secure systems
- Verify source of encrypted images
- Keep software updated
- Enable logging for audit trails
- Test decryption before deleting originals

❌ **DON'T:**
- Use on compromised systems
- Trust images from unknown sources
- Disable security features
- Delete originals before verification

---

## Troubleshooting

### "Image not found" Error
- **Cause**: Invalid file path
- **Solution**: Check path, ensure PNG format

### "Decryption Failed" Error
- **Possible Causes**:
  1. Incorrect keys (most common)
  2. Corrupted image file
  3. Wrong image selected
  4. Image was compressed/modified
- **Solution**: Verify keys, check image integrity

### "Data too large for image" Error
- **Cause**: Message + encryption overhead exceeds image capacity
- **Solution**: Use larger cover image or shorter message

### Keys Not Copying to Clipboard
- **Cause**: Clipboard access restricted
- **Solution**: Manually copy from keys.txt file

---

## Support & Contributing

### Getting Help
- Check logs in `Secret/logs/app.log`
- Review error messages carefully
- Consult this guide's FAQ section

### Reporting Issues
When reporting issues, include:
- Error message (if any)
- Steps to reproduce
- Config.py settings (sanitize sensitive data)
- Log excerpt (last 20 lines)

### Contributing
This is an open-source project. Contributions welcome:
- Bug fixes
- Feature enhancements
- Documentation improvements
- Security audits

---

## Technical Reference

### File Structure
```
.
├── main.py                 # Entry point
├── config.py              # Configuration
├── USER_GUIDE.md         # This guide
├── Secret/               # Data storage
│   ├── images/          # Cover images
│   ├── keys/            # Encryption keys
│   ├── phrases/         # Saved messages
│   ├── logs/            # Application logs
│   └── YYYYMMDD_HHMMSS/ # Session folders
├── Decrypt/             # Decryption staging
└── src/                 # Source code
    ├── gui_mode.py      # GUI implementation
    ├── terminal_mode.py # Terminal UI
    ├── encrypt_utils.py # Encryption functions
    ├── decrypt_utils.py # Decryption functions
    └── stego_utils.py   # Steganography functions
```

### Key File Format
```
Vigenère Key: <37-character alphanumeric>
Kyber DK: <1568-character hexadecimal>
Scramble Key: <32-character alphanumeric>
```

### Session Folder Structure
```
Secret/YYYYMMDD_HHMMSS/
├── images/
│   └── secret.png       # Encrypted image
└── keys/
    └── keys.txt         # Encryption keys
```

---

## License & Credits

**License**: MIT License - Free to use, modify, and distribute

**Credits**:
- Developed by Rex and the Codex Team
- Built with Python, Tkinter, Rich
- Uses Kyber ML-KEM (NIST FIPS 203)
- Cryptography by Python Cryptography library

**Visit**: [Rex's Bio](https://slat.cc/toha)

---

## Version History

**Current Version**: 2.0
- ✨ Enhanced GUI with modern dark theme
- ✨ Beautiful terminal UI with Rich library
- ✨ Phrase management system
- ✨ Copy-to-clipboard functionality
- ✨ Comprehensive configuration options
- ✨ Progress indicators
- ✨ Improved error handling
- ✨ Complete documentation

---

**Stay Secure! 🔐**

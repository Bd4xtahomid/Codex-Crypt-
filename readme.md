# Quantum Codex Crypt

## Description
This is a quantum-resistant encryption tool that uses multi-layer encryption (Vigenère, Kyber, AES-256-GCM, HMAC, numeric encoding, scrambling, and LSB steganography) to secure messages and hide them in images. Designed for non-coders with a simple GUI or terminal interface.

Made by Rex and the Codex Team. This is a non-profit project, open for anyone to edit, improve, and contribute. Visit Rex's bio: [https://slat.cc/toha](https://slat.cc/toha).

## Features
- **GUI Mode**: User-friendly interface for encryption/decryption.
- **Terminal Modes**: No-input (uses config message) or with-input.
- **Phrase Storage**: Save phrases in 'Secret/phrases'.
- **Organized Storage**: Outputs in timestamped folders under 'Secret'.
- **Dedicated Decryption Folder**: Place secret.png and keys.txt in 'Decrypt' for no-input decryption.
- **Delete to Remove**: Simply delete the subfolder to erase data.
- **Advanced Security**: Quantum-resistant (Kyber), integrity (HMAC), obfuscation (scrambling/numeric).
- **Logging**: Tracks operations in 'Secret/logs/app.log' for debugging.

## Requirements
- Python 3.10+
- Libraries: `pip install kyber-py cryptography pillow`

## Setup
1. Clone the repo: `git clone https://github.com/iamrexeditd/codex-Crypt-.git`
3. Navigate to the folder: `cd Codex-Crypt`
4. Install dependencies: `pip install -r requirements.txt`
5. Place a cover image (e.g., cover.png) in `Secret/images` for encryption.
6. Run: `python main.py`

## Configuration
Edit `config.py`:
- `MESSAGE`: Default message for no-input encryption.
- `MODE`: "gui", "terminal_no_input", or "terminal_with_input".
- `DEFAULT_ACTION`: "encrypt" or "decrypt" for terminal_no_input mode.

## Usage
### GUI Mode
- Launch: `python main.py` (with `MODE = "gui"`).
- Enter message or use default.
- Browse for cover image.
- Click "Encrypt & Hide" to generate secret.png and keys.txt in `Secret/<timestamp>`.
- For decryption, browse secret.png, enter keys, and click "Decrypt from Image".
- Save phrases to `Secret/phrases` with "Add Phrase".

### Terminal Mode
- **With Input** (`MODE = "terminal_with_input"`):
  - Run: `python main.py`.
  - Choose encrypt/decrypt.
  - For encrypt: Enter message and cover image path.
  - For decrypt: Enter secret.png path and keys.
- **No Input** (`MODE = "terminal_no_input"`):
  - For encrypt: Uses `MESSAGE` from config.py and `cover.png` in `Secret/images`.
  - For decrypt: Uses `Decrypt/secret.png` and `Decrypt/keys.txt`.
  - Set `DEFAULT_ACTION` in config.py to choose encrypt or decrypt.

**No-Input Decryption**:
- Set `DEFAULT_ACTION = "decrypt"` in config.py.
- Place `secret.png` in `Decrypt/`.
- Place `keys.txt` in `Decrypt/` with format: Vigenère Key:  Kyber SK:  Scramble Key:
- Run: `python main.py`.

## Security Notes
- Keys are saved in plain text—store securely or memorize.
- Use large images (e.g., 512x512 or larger) for steganography.
- Quantum-resistant with Kyber for future-proofing.
- Follow best practices: No hard-coded secrets, PoLP, protected branches on GitHub.

## Contributing
See CONTRIBUTING.md for guidelines on contributions, security reporting, and improving the project.

## License
MIT License. Feel free to fork and improve!

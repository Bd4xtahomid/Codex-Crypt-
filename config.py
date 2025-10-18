
# ═══════════════════════════════════════════════════════════
#  QUANTUM CODEX CRYPT - CONFIGURATION FILE
# ═══════════════════════════════════════════════════════════

# ───────────────────────────────────────────────────────────
# OPERATION MODE
# ───────────────────────────────────────────────────────────
# Options: "gui", "terminal_no_input", "terminal_with_input"
# - gui: Launch graphical interface
# - terminal_no_input: Auto mode using settings below
# - terminal_with_input: Interactive command-line interface
MODE = "gui"

# ───────────────────────────────────────────────────────────
# DEFAULT SETTINGS (for no-input modes)
# ───────────────────────────────────────────────────────────
# Default message to encrypt in no-input mode
MESSAGE = "This is a secure encrypted message."

# Default action for terminal_no_input mode
# Options: "encrypt" or "decrypt"
DEFAULT_ACTION = "encrypt"

# ───────────────────────────────────────────────────────────
# SECURITY SETTINGS
# ───────────────────────────────────────────────────────────
# Vigenère key length (default: 37 characters)
# Longer keys provide better security
VIGENERE_KEY_LENGTH = 37

# Scramble key length (default: 32 characters)
# Used for data scrambling layer
SCRAMBLE_KEY_LENGTH = 32

# Kyber security level
# Options: 512, 768, 1024 (higher = more secure but slower)
# Note: Currently only 512 is implemented
KYBER_SECURITY_LEVEL = 512

# ───────────────────────────────────────────────────────────
# FILE PATHS & DIRECTORIES
# ───────────────────────────────────────────────────────────
# Default cover image for no-input encryption
DEFAULT_COVER_IMAGE = "Secret/images/cover.png"

# Output directory for encrypted files
OUTPUT_DIR = "Secret"

# Directory for decryption in no-input mode
DECRYPT_DIR = "Decrypt"

# Phrases storage directory
PHRASES_DIR = "Secret/phrases"

# ───────────────────────────────────────────────────────────
# APPLICATION SETTINGS
# ───────────────────────────────────────────────────────────
# Enable logging
ENABLE_LOGGING = True

# Log file path
LOG_FILE = "Secret/logs/app.log"

# Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = "INFO"

# Auto-save phrases after encryption (GUI mode)
AUTO_SAVE_PHRASES = False

# Show encryption progress indicators
SHOW_PROGRESS = True

# ───────────────────────────────────────────────────────────
# STEGANOGRAPHY SETTINGS
# ───────────────────────────────────────────────────────────
# Output image format
OUTPUT_IMAGE_FORMAT = "PNG"

# Image quality (1-100, only for JPEG)
IMAGE_QUALITY = 95

# ───────────────────────────────────────────────────────────
# TERMINAL UI SETTINGS
# ───────────────────────────────────────────────────────────
# Enable colored output in terminal
TERMINAL_COLORS = True

# Auto-copy keys to clipboard after encryption
AUTO_COPY_KEYS = True

# Auto-copy decrypted message to clipboard
AUTO_COPY_DECRYPTED = True

# ───────────────────────────────────────────────────────────
# GUI SETTINGS
# ───────────────────────────────────────────────────────────
# Window size (width x height)
GUI_WINDOW_SIZE = "800x700"

# Theme: "dark" or "light"
GUI_THEME = "dark"

# Font size
GUI_FONT_SIZE = 10

# Show welcome message on startup
SHOW_WELCOME = True

# ───────────────────────────────────────────────────────────
# ADVANCED SETTINGS
# ───────────────────────────────────────────────────────────
# Numeric encoding parameters (for obfuscation layer)
NUMERIC_MULTIPLIER = 23
NUMERIC_ADDER = 57
NUMERIC_MODULUS = 100003

# Timestamp format for folders/files
TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"

# ═══════════════════════════════════════════════════════════
#  DO NOT MODIFY BELOW THIS LINE
# ═══════════════════════════════════════════════════════════

# Validate configuration
if MODE not in ["gui", "terminal_no_input", "terminal_with_input"]:
    raise ValueError(f"Invalid MODE: {MODE}")

if DEFAULT_ACTION not in ["encrypt", "decrypt"]:
    raise ValueError(f"Invalid DEFAULT_ACTION: {DEFAULT_ACTION}")

if LOG_LEVEL not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
    raise ValueError(f"Invalid LOG_LEVEL: {LOG_LEVEL}")

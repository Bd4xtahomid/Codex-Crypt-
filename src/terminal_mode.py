import os
import base64
import time
import config
from src.encrypt_utils import *
from src.decrypt_utils import *
from src.stego_utils import *
import logging
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint
from rich.markdown import Markdown
import pyperclip

console = Console()

def show_banner():
    """Display application banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║      🔐 QUANTUM CODEX CRYPT 🔐                       ║
    ║                                                       ║
    ║   Multi-Layer Quantum-Resistant Encryption System    ║
    ║   with Steganography & Advanced Security             ║
    ╚═══════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")
    console.print("Security Layers: Vigenère • Kyber ML-KEM-512 • AES-256-GCM • HMAC • LSB Stego\n", style="dim")

def list_saved_phrases():
    """Display list of saved phrases and allow selection"""
    phrases_dir = os.path.join('Secret', 'phrases')
    
    if not os.path.exists(phrases_dir) or not os.listdir(phrases_dir):
        console.print("❌ No saved phrases found.", style="bold red")
        return None
    
    phrase_files = sorted(os.listdir(phrases_dir), reverse=True)
    
    # Create table
    table = Table(title="📝 Saved Phrases", show_header=True, header_style="bold magenta")
    table.add_column("#", style="cyan", width=6)
    table.add_column("Timestamp", style="green", width=20)
    table.add_column("Preview", style="white")
    
    phrase_data = {}
    for i, filename in enumerate(phrase_files, 1):
        filepath = os.path.join(phrases_dir, filename)
        with open(filepath, 'r') as f:
            content = f.read().strip()
            preview = content[:60] + "..." if len(content) > 60 else content
            timestamp = filename.replace('phrase_', '').replace('.txt', '')
            table.add_row(str(i), timestamp, preview)
            phrase_data[i] = content
    
    console.print(table)
    
    choice = Prompt.ask("\n[bold cyan]Select phrase number (or 0 to cancel)[/bold cyan]", default="0")
    
    try:
        choice_num = int(choice)
        if choice_num == 0:
            return None
        if choice_num in phrase_data:
            console.print(f"✅ Loaded phrase #{choice_num}", style="bold green")
            return phrase_data[choice_num]
        else:
            console.print("❌ Invalid selection", style="bold red")
            return None
    except ValueError:
        console.print("❌ Invalid input", style="bold red")
        return None

def save_phrase(message):
    """Save message as a phrase"""
    if message:
        phrase_path = os.path.join('Secret', 'phrases', f"phrase_{time.strftime('%Y%m%d_%H%M%S')}.txt")
        with open(phrase_path, 'w') as f:
            f.write(message)
        console.print(f"✅ Phrase saved to: [cyan]{phrase_path}[/cyan]", style="bold green")
        logging.info(f"Phrase added: {phrase_path}")
        return True
    return False

def encrypt_mode(mode, sub_path):
    """Handle encryption operations"""
    console.print("\n[bold green]🔒 ENCRYPTION MODE[/bold green]")
    console.print("─" * 60 + "\n")
    
    # Get message
    if mode == "terminal_no_input":
        message = config.MESSAGE
        console.print(f"Using default message from config", style="dim")
    else:
        console.print("[bold]Choose message input method:[/bold]")
        console.print("  1. Type new message")
        console.print("  2. Load saved phrase")
        
        choice = Prompt.ask("[bold cyan]Select option[/bold cyan]", choices=["1", "2"], default="1")
        
        if choice == "2":
            message = list_saved_phrases()
            if not message:
                message = Prompt.ask("[bold yellow]Enter message manually[/bold yellow]")
        else:
            message = Prompt.ask("[bold yellow]Enter message to encrypt[/bold yellow]")
        
        # Ask if user wants to save this phrase
        if Confirm.ask("💾 Save this message as a phrase for later?", default=False):
            save_phrase(message)
    
    # Get image path
    if mode == "terminal_no_input":
        image_path = 'Secret/images/cover.png'
    else:
        image_path = Prompt.ask("[bold yellow]Enter cover image path[/bold yellow]", default="Secret/images/cover.png")
    
    if not os.path.exists(image_path):
        console.print(f"❌ Image not found: {image_path}", style="bold red")
        return
    
    # Encryption process with progress
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        task = progress.add_task("[cyan]Encrypting...", total=7)
        
        progress.update(task, description="[cyan]1/7 Applying Vigenère cipher...")
        vig_key = generate_long_key()
        scramble_key = generate_long_key(32)
        vig_ct = vigenere_encrypt(message, vig_key)
        progress.advance(task)
        
        progress.update(task, description="[cyan]2/7 Kyber quantum-resistant encryption...")
        encrypted_bundle, dk, hmac_tag = kyber_hybrid_encrypt(vig_ct.encode())
        encrypted_bundle_with_tag = encrypted_bundle + hmac_tag
        progress.advance(task)
        
        progress.update(task, description="[cyan]3/7 Applying numeric encoding...")
        nums = numeric_encode(encrypted_bundle_with_tag)
        progress.advance(task)
        
        progress.update(task, description="[cyan]4/7 Scrambling data...")
        scrambled_nums = scramble_nums(nums, scramble_key)
        progress.advance(task)
        
        progress.update(task, description="[cyan]5/7 Base64 encoding...")
        concat = '-'.join(scrambled_nums)
        b64 = base64.b64encode(concat.encode()).decode()
        progress.advance(task)
        
        progress.update(task, description="[cyan]6/7 Hiding in image (LSB steganography)...")
        output_path = os.path.join(sub_path, 'images', "secret.png")
        lsb_steganography_hide(image_path, b64.encode(), output_path)
        progress.advance(task)
        
        progress.update(task, description="[cyan]7/7 Saving encryption keys...")
        keys_path = os.path.join(sub_path, 'keys', "keys.txt")
        with open(keys_path, 'w') as f:
            f.write(f"Vigenère Key: {vig_key}\n")
            f.write(f"Kyber DK: {dk.hex()}\n")
            f.write(f"Scramble Key: {scramble_key}\n")
        progress.advance(task)
    
    # Success panel
    success_panel = Panel(
        f"[bold green]✅ ENCRYPTION SUCCESSFUL![/bold green]\n\n"
        f"[cyan]📁 Encrypted Image:[/cyan] {output_path}\n"
        f"[cyan]🔑 Keys Saved To:[/cyan] {keys_path}\n\n"
        f"[yellow]Security Layers Applied:[/yellow]\n"
        f"  • Vigenère Cipher\n"
        f"  • Kyber ML-KEM-512 (Quantum-resistant)\n"
        f"  • AES-256-GCM Encryption\n"
        f"  • HMAC-SHA256 Integrity\n"
        f"  • Numeric Encoding\n"
        f"  • Data Scrambling\n"
        f"  • LSB Steganography\n\n"
        f"[dim]💡 Tip: Delete folder '{os.path.basename(sub_path)}' to remove all traces[/dim]",
        border_style="green",
        title="Encryption Complete"
    )
    console.print(success_panel)
    
    # Copy keys option
    if mode != "terminal_no_input":
        if Confirm.ask("\n📋 Copy keys to clipboard?", default=True):
            with open(keys_path, 'r') as f:
                keys_content = f.read()
            try:
                pyperclip.copy(keys_content)
                console.print("✅ Keys copied to clipboard!", style="bold green")
            except:
                console.print("⚠️  Clipboard not available", style="yellow")
    
    logging.info("Terminal encryption completed")

def decrypt_mode(mode):
    """Handle decryption operations"""
    console.print("\n[bold blue]🔓 DECRYPTION MODE[/bold blue]")
    console.print("─" * 60 + "\n")
    
    try:
        if mode == "terminal_no_input":
            image_path = 'Decrypt/secret.png'
            keys_path = 'Decrypt/keys.txt'
            
            if not os.path.exists(image_path) or not os.path.exists(keys_path):
                raise ValueError("Decrypt folder must contain secret.png and keys.txt for no-input mode")
            
            console.print(f"[dim]Using files from Decrypt folder...[/dim]")
            
            with open(keys_path, 'r') as f:
                lines = f.readlines()
                vig_key = lines[0].split(': ')[1].strip()
                dk_hex = lines[1].split(': ')[1].strip()
                scramble_key = lines[2].split(': ')[1].strip()
        else:
            image_path = Prompt.ask("[bold yellow]Enter secret image path[/bold yellow]")
            
            if not os.path.exists(image_path):
                raise ValueError(f"Image not found: {image_path}")
            
            console.print("\n[bold]Key Input Options:[/bold]")
            console.print("  1. Enter keys manually")
            console.print("  2. Load from keys.txt file")
            
            key_choice = Prompt.ask("[bold cyan]Select option[/bold cyan]", choices=["1", "2"], default="2")
            
            if key_choice == "2":
                keys_file = Prompt.ask("[bold yellow]Enter path to keys.txt[/bold yellow]", default="Decrypt/keys.txt")
                if os.path.exists(keys_file):
                    with open(keys_file, 'r') as f:
                        lines = f.readlines()
                        vig_key = lines[0].split(': ')[1].strip()
                        dk_hex = lines[1].split(': ')[1].strip()
                        scramble_key = lines[2].split(': ')[1].strip()
                    console.print("✅ Keys loaded from file", style="green")
                else:
                    console.print("❌ Keys file not found, enter manually", style="red")
                    key_choice = "1"
            
            if key_choice == "1":
                vig_key = Prompt.ask("[bold yellow]Enter Vigenère Key[/bold yellow]")
                dk_hex = Prompt.ask("[bold yellow]Enter Kyber DK (hex)[/bold yellow]")
                scramble_key = Prompt.ask("[bold yellow]Enter Scramble Key[/bold yellow]")
        
        dk = bytes.fromhex(dk_hex)
        
        # Decryption process with progress
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            task = progress.add_task("[cyan]Decrypting...", total=7)
            
            progress.update(task, description="[cyan]1/7 Extracting hidden data...")
            b64_data = lsb_steganography_retrieve(image_path)
            progress.advance(task)
            
            progress.update(task, description="[cyan]2/7 Decoding base64...")
            b64_str = b64_data.decode(errors='ignore').rstrip('\x00')
            concat = base64.b64decode(b64_str).decode()
            nums = concat.split('-')
            progress.advance(task)
            
            progress.update(task, description="[cyan]3/7 Unscrambling data...")
            unscrambled_nums = unscramble_nums(nums, scramble_key)
            progress.advance(task)
            
            progress.update(task, description="[cyan]4/7 Reversing numeric encoding...")
            bundle_with_tag = reverse_numeric(unscrambled_nums)
            progress.advance(task)
            
            progress.update(task, description="[cyan]5/7 Kyber decryption...")
            vig_recovered = kyber_hybrid_decrypt(bundle_with_tag, dk).decode()
            progress.advance(task)
            
            progress.update(task, description="[cyan]6/7 Vigenère decryption...")
            plaintext = vigenere_decrypt(vig_recovered, vig_key)
            progress.advance(task)
            
            progress.update(task, description="[cyan]7/7 Complete!")
            progress.advance(task)
        
        # Success panel with decrypted message
        success_panel = Panel(
            f"[bold green]✅ DECRYPTION SUCCESSFUL![/bold green]\n\n"
            f"[bold yellow]📄 Decrypted Message:[/bold yellow]\n\n"
            f"[bold white]{plaintext}[/bold white]",
            border_style="green",
            title="Decryption Complete"
        )
        console.print(success_panel)
        
        # Copy message option
        if mode != "terminal_no_input":
            if Confirm.ask("\n📋 Copy decrypted message to clipboard?", default=True):
                try:
                    pyperclip.copy(plaintext)
                    console.print("✅ Message copied to clipboard!", style="bold green")
                except:
                    console.print("⚠️  Clipboard not available", style="yellow")
        
        logging.info("Terminal decryption completed")
        
    except Exception as e:
        error_panel = Panel(
            f"[bold red]❌ DECRYPTION FAILED[/bold red]\n\n"
            f"[yellow]Error:[/yellow] {str(e)}\n\n"
            f"[dim]Possible causes:[/dim]\n"
            f"  • Incorrect encryption keys\n"
            f"  • Corrupted image file\n"
            f"  • Wrong image selected",
            border_style="red",
            title="Error"
        )
        console.print(error_panel)
        logging.error(f"Terminal decryption failed: {str(e)}")

def run_terminal_mode(mode):
    """Main terminal mode entry point"""
    try:
        show_banner()
        
        # Create subfolder for encryption
        subfolder = time.strftime("%Y%m%d_%H%M%S")
        sub_path = os.path.join('Secret', subfolder)
        
        if mode == "terminal_no_input":
            choice = config.DEFAULT_ACTION
            console.print(f"[dim]Running in no-input mode: {choice}[/dim]\n")
        else:
            # Main menu
            menu_table = Table(show_header=False, box=None)
            menu_table.add_row("[bold cyan]1[/bold cyan]", "[bold]Encrypt Message[/bold]", "🔒")
            menu_table.add_row("[bold cyan]2[/bold cyan]", "[bold]Decrypt Message[/bold]", "🔓")
            menu_table.add_row("[bold cyan]3[/bold cyan]", "[bold]View Saved Phrases[/bold]", "📝")
            menu_table.add_row("[bold cyan]4[/bold cyan]", "[bold]Exit[/bold]", "🚪")
            
            console.print(menu_table)
            console.print()
            
            choice_map = {"1": "encrypt", "2": "decrypt", "3": "phrases", "4": "exit"}
            user_choice = Prompt.ask("[bold cyan]Select option[/bold cyan]", choices=["1", "2", "3", "4"], default="1")
            choice = choice_map[user_choice]
        
        if choice == "encrypt":
            if not os.path.exists(sub_path):
                os.makedirs(sub_path)
                os.makedirs(os.path.join(sub_path, 'images'))
                os.makedirs(os.path.join(sub_path, 'keys'))
            encrypt_mode(mode, sub_path)
        
        elif choice == "decrypt":
            decrypt_mode(mode)
        
        elif choice == "phrases":
            list_saved_phrases()
        
        elif choice == "exit":
            console.print("\n[bold cyan]👋 Goodbye! Stay secure![/bold cyan]\n")
        
    except KeyboardInterrupt:
        console.print("\n\n[bold yellow]⚠️  Operation cancelled by user[/bold yellow]\n")
    except Exception as e:
        console.print(f"\n[bold red]❌ Error: {str(e)}[/bold red]\n", style="bold red")
        logging.error(f"Terminal mode failed: {str(e)}")
        

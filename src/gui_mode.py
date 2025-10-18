
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import os
import base64
import time
from src.encrypt_utils import *
from src.decrypt_utils import *
from src.stego_utils import *
import config
import logging

class EncryptApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Quantum Codex Crypt - Ultra-Secure Encryption")
        self.root.geometry("800x700")
        self.root.configure(bg='#1e1e1e')
        
        # Generate encryption keys
        self.vig_key = generate_long_key()
        self.scramble_key = generate_long_key(32)
        
        # Create timestamped subfolder for this session
        self.subfolder = time.strftime("%Y%m%d_%H%M%S")
        self.sub_path = os.path.join('Secret', self.subfolder)
        if not os.path.exists(self.sub_path):
            os.makedirs(self.sub_path)
            os.makedirs(os.path.join(self.sub_path, 'images'))
            os.makedirs(os.path.join(self.sub_path, 'keys'))
        
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', padding=10, font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='white', background='#1e1e1e')
        style.configure('Section.TLabel', font=('Arial', 12, 'bold'), foreground='#4CAF50', background='#1e1e1e')
        style.configure('Info.TLabel', font=('Arial', 10), foreground='#b0b0b0', background='#1e1e1e')
        
        # Title
        title_frame = tk.Frame(root, bg='#1e1e1e')
        title_frame.pack(fill=tk.X, padx=20, pady=15)
        ttk.Label(title_frame, text="🔐 Quantum Codex Crypt", style='Title.TLabel').pack()
        ttk.Label(title_frame, text="Multi-layer quantum-resistant encryption with steganography", style='Info.TLabel').pack()
        
        # Main container
        main_frame = tk.Frame(root, bg='#1e1e1e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Message section
        message_frame = tk.LabelFrame(main_frame, text=" Message ", bg='#2d2d2d', fg='#4CAF50', font=('Arial', 11, 'bold'), padx=10, pady=10)
        message_frame.pack(fill=tk.X, pady=10)
        
        # Message input with scrollbar
        msg_input_frame = tk.Frame(message_frame, bg='#2d2d2d')
        msg_input_frame.pack(fill=tk.X, pady=5)
        
        self.message_entry = tk.Text(msg_input_frame, height=4, width=70, font=('Courier', 10), bg='#3d3d3d', fg='white', insertbackground='white')
        self.message_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.message_entry.insert(tk.END, config.MESSAGE)
        
        scrollbar = tk.Scrollbar(msg_input_frame, command=self.message_entry.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.message_entry.config(yscrollcommand=scrollbar.set)
        
        # Message buttons
        btn_frame = tk.Frame(message_frame, bg='#2d2d2d')
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="📝 Load Saved Phrase", command=self.load_phrase).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="💾 Save Current Phrase", command=self.add_phrase).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑️ Clear", command=lambda: self.message_entry.delete('1.0', tk.END)).pack(side=tk.LEFT, padx=5)
        
        # Cover Image section
        image_frame = tk.LabelFrame(main_frame, text=" Cover Image ", bg='#2d2d2d', fg='#4CAF50', font=('Arial', 11, 'bold'), padx=10, pady=10)
        image_frame.pack(fill=tk.X, pady=10)
        
        img_input_frame = tk.Frame(image_frame, bg='#2d2d2d')
        img_input_frame.pack(fill=tk.X, pady=5)
        
        self.image_path_var = tk.StringVar()
        tk.Entry(img_input_frame, textvariable=self.image_path_var, width=60, font=('Arial', 10), bg='#3d3d3d', fg='white', insertbackground='white').pack(side=tk.LEFT, padx=5)
        ttk.Button(img_input_frame, text="📁 Browse", command=self.browse_image).pack(side=tk.LEFT, padx=5)
        
        # Action buttons
        action_frame = tk.Frame(main_frame, bg='#1e1e1e')
        action_frame.pack(fill=tk.X, pady=15)
        
        encrypt_btn = tk.Button(action_frame, text="🔒 Encrypt & Hide in Image", command=self.encrypt, 
                               bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'), padx=20, pady=10, cursor='hand2')
        encrypt_btn.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)
        
        decrypt_btn = tk.Button(action_frame, text="🔓 Decrypt from Image", command=self.decrypt, 
                               bg='#2196F3', fg='white', font=('Arial', 12, 'bold'), padx=20, pady=10, cursor='hand2')
        decrypt_btn.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)
        
        # Output section
        output_frame = tk.LabelFrame(main_frame, text=" Output ", bg='#2d2d2d', fg='#4CAF50', font=('Arial', 11, 'bold'), padx=10, pady=10)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.output_text = tk.Text(output_frame, height=8, font=('Courier', 9), bg='#3d3d3d', fg='#00ff00', insertbackground='white', wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        output_scrollbar = tk.Scrollbar(output_frame, command=self.output_text.yview)
        output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=output_scrollbar.set)
        
        # Output buttons
        output_btn_frame = tk.Frame(output_frame, bg='#2d2d2d')
        output_btn_frame.pack(fill=tk.X)
        
        ttk.Button(output_btn_frame, text="📋 Copy to Clipboard", command=self.copy_output).pack(side=tk.LEFT, padx=5)
        ttk.Button(output_btn_frame, text="🗑️ Clear Output", command=lambda: self.output_text.delete('1.0', tk.END)).pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(root, textvariable=self.status_var, bg='#0d0d0d', fg='#4CAF50', font=('Arial', 9), anchor=tk.W, padx=10, pady=5)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def load_phrase(self):
        """Load a saved phrase from Secret/phrases"""
        try:
            phrases_dir = os.path.join('Secret', 'phrases')
            if not os.path.exists(phrases_dir) or not os.listdir(phrases_dir):
                messagebox.showinfo("No Phrases", "No saved phrases found. Save a phrase first!")
                return
            
            # Create phrase selection dialog
            phrase_window = tk.Toplevel(self.root)
            phrase_window.title("Select Phrase")
            phrase_window.geometry("600x400")
            phrase_window.configure(bg='#2d2d2d')
            
            tk.Label(phrase_window, text="📝 Saved Phrases", font=('Arial', 14, 'bold'), 
                    bg='#2d2d2d', fg='#4CAF50').pack(pady=10)
            
            # Listbox with scrollbar
            list_frame = tk.Frame(phrase_window, bg='#2d2d2d')
            list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            scrollbar = tk.Scrollbar(list_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            phrase_list = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, 
                                    font=('Courier', 10), bg='#3d3d3d', fg='white', selectmode=tk.SINGLE)
            phrase_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=phrase_list.yview)
            
            # Load phrases
            phrase_files = sorted(os.listdir(phrases_dir), reverse=True)
            phrase_data = {}
            
            for i, filename in enumerate(phrase_files):
                filepath = os.path.join(phrases_dir, filename)
                with open(filepath, 'r') as f:
                    content = f.read().strip()
                    preview = content[:50] + "..." if len(content) > 50 else content
                    display = f"{filename.replace('phrase_', '').replace('.txt', '')} - {preview}"
                    phrase_list.insert(tk.END, display)
                    phrase_data[i] = content
            
            def select_phrase():
                selection = phrase_list.curselection()
                if selection:
                    self.message_entry.delete('1.0', tk.END)
                    self.message_entry.insert(tk.END, phrase_data[selection[0]])
                    phrase_window.destroy()
                    self.status_var.set("Phrase loaded successfully")
            
            btn_frame = tk.Frame(phrase_window, bg='#2d2d2d')
            btn_frame.pack(pady=10)
            
            tk.Button(btn_frame, text="Load Selected", command=select_phrase, 
                     bg='#4CAF50', fg='white', font=('Arial', 11, 'bold'), padx=20, pady=5).pack(side=tk.LEFT, padx=5)
            tk.Button(btn_frame, text="Cancel", command=phrase_window.destroy, 
                     bg='#757575', fg='white', font=('Arial', 11, 'bold'), padx=20, pady=5).pack(side=tk.LEFT, padx=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load phrases: {str(e)}")
            logging.error(f"Load phrase failed: {str(e)}")

    def add_phrase(self):
        """Save current message as a phrase"""
        message = self.message_entry.get("1.0", tk.END).strip()
        if message:
            phrase_path = os.path.join('Secret', 'phrases', f"phrase_{time.strftime('%Y%m%d_%H%M%S')}.txt")
            with open(phrase_path, 'w') as f:
                f.write(message)
            messagebox.showinfo("Success", f"✅ Phrase saved successfully!\n\nLocation: {phrase_path}")
            self.status_var.set(f"Phrase saved: {phrase_path}")
            logging.info(f"Phrase added: {phrase_path}")
        else:
            messagebox.showerror("Error", "No message to save!")

    def browse_image(self):
        """Browse for cover image"""
        path = filedialog.askopenfilename(
            title="Select Cover Image",
            filetypes=[("PNG Images", "*.png"), ("All Images", "*.png *.jpg *.jpeg")]
        )
        if path:
            self.image_path_var.set(path)
            self.status_var.set(f"Image selected: {os.path.basename(path)}")

    def copy_output(self):
        """Copy output text to clipboard"""
        output = self.output_text.get("1.0", tk.END).strip()
        if output:
            self.root.clipboard_clear()
            self.root.clipboard_append(output)
            self.status_var.set("Copied to clipboard!")
            messagebox.showinfo("Success", "Output copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No output to copy")

    def encrypt(self):
        """Encrypt message and hide in image"""
        try:
            self.status_var.set("Encrypting...")
            self.root.update()
            
            message = self.message_entry.get("1.0", tk.END).strip()
            image_path = self.image_path_var.get()
            
            if not image_path or not message:
                raise ValueError("Both message and cover image are required!")
            
            if not os.path.exists(image_path):
                raise ValueError(f"Image file not found: {image_path}")
            
            # Multi-layer encryption
            vig_ct = vigenere_encrypt(message, self.vig_key)
            encrypted_bundle, dk, hmac_tag = kyber_hybrid_encrypt(vig_ct.encode())
            encrypted_bundle_with_tag = encrypted_bundle + hmac_tag
            nums = numeric_encode(encrypted_bundle_with_tag)
            scrambled_nums = scramble_nums(nums, self.scramble_key)
            concat = '-'.join(scrambled_nums)
            b64 = base64.b64encode(concat.encode()).decode()
            
            # Hide in image
            output_path = os.path.join(self.sub_path, 'images', "secret.png")
            lsb_steganography_hide(image_path, b64.encode(), output_path)
            
            # Save keys
            keys_path = os.path.join(self.sub_path, 'keys', "keys.txt")
            with open(keys_path, 'w') as f:
                f.write(f"Vigenère Key: {self.vig_key}\n")
                f.write(f"Kyber DK: {dk.hex()}\n")
                f.write(f"Scramble Key: {self.scramble_key}\n")
            
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"✅ ENCRYPTION SUCCESSFUL!\n\n")
            self.output_text.insert(tk.END, f"📁 Encrypted image: {output_path}\n")
            self.output_text.insert(tk.END, f"🔑 Keys saved to: {keys_path}\n\n")
            self.output_text.insert(tk.END, f"Security Layers Applied:\n")
            self.output_text.insert(tk.END, f"  1. Vigenère Cipher\n")
            self.output_text.insert(tk.END, f"  2. Kyber ML-KEM-512 (Quantum-resistant)\n")
            self.output_text.insert(tk.END, f"  3. AES-256-GCM Encryption\n")
            self.output_text.insert(tk.END, f"  4. HMAC-SHA256 Integrity Check\n")
            self.output_text.insert(tk.END, f"  5. Numeric Encoding\n")
            self.output_text.insert(tk.END, f"  6. Data Scrambling\n")
            self.output_text.insert(tk.END, f"  7. LSB Steganography\n\n")
            self.output_text.insert(tk.END, f"💡 Tip: Delete the folder '{self.subfolder}' to remove all traces.")
            
            self.status_var.set("✅ Encryption completed successfully")
            messagebox.showinfo("Success", "Message encrypted and hidden successfully!")
            
        except Exception as e:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"❌ ENCRYPTION FAILED\n\n{str(e)}")
            self.status_var.set("❌ Encryption failed")
            messagebox.showerror("Encryption Error", str(e))
            logging.error(f"Encryption failed: {str(e)}")

    def decrypt(self):
        """Decrypt message from image"""
        try:
            self.status_var.set("Decrypting...")
            self.root.update()
            
            image_path = self.image_path_var.get()
            if not image_path:
                raise ValueError("Please select an image to decrypt")
            
            if not os.path.exists(image_path):
                raise ValueError(f"Image file not found: {image_path}")
            
            # Get keys from user
            vig_key = simpledialog.askstring("Vigenère Key", "Enter Vigenère Key:")
            dk_hex = simpledialog.askstring("Kyber Key", "Enter Kyber DK (hex):")
            scramble_key = simpledialog.askstring("Scramble Key", "Enter Scramble Key:")
            
            if not vig_key or not dk_hex or not scramble_key:
                raise ValueError("All keys are required for decryption!")
            
            dk = bytes.fromhex(dk_hex)
            
            # Decrypt layers
            b64_data = lsb_steganography_retrieve(image_path)
            b64_str = b64_data.decode(errors='ignore').rstrip('\x00')
            concat = base64.b64decode(b64_str).decode()
            nums = concat.split('-')
            unscrambled_nums = unscramble_nums(nums, scramble_key)
            bundle_with_tag = reverse_numeric(unscrambled_nums)
            vig_recovered = kyber_hybrid_decrypt(bundle_with_tag, dk).decode()
            plaintext = vigenere_decrypt(vig_recovered, vig_key)
            
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"✅ DECRYPTION SUCCESSFUL!\n\n")
            self.output_text.insert(tk.END, f"📄 Decrypted Message:\n")
            self.output_text.insert(tk.END, f"{'-'*60}\n")
            self.output_text.insert(tk.END, f"{plaintext}\n")
            self.output_text.insert(tk.END, f"{'-'*60}\n")
            
            self.status_var.set("✅ Decryption completed successfully")
            messagebox.showinfo("Success", "Message decrypted successfully!")
            
        except ValueError as e:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"❌ DECRYPTION FAILED\n\n{str(e)}")
            self.status_var.set("❌ Decryption failed")
            messagebox.showerror("Decryption Error", str(e))
            logging.error(f"Decryption failed: {str(e)}")
        except Exception as e:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"❌ DECRYPTION FAILED\n\nInvalid keys or corrupted data.\nError: {str(e)}")
            self.status_var.set("❌ Decryption failed")
            messagebox.showerror("Decryption Error", "Invalid keys or corrupted data")
            logging.error(f"Decryption failed: {str(e)}")

def run_gui():
    root = tk.Tk()
    app = EncryptApp(root)
    root.mainloop()
        

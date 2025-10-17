
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
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
        self.root.title("Ultra-Secure Encryption 🔐")
        self.vig_key = generate_long_key()
        self.scramble_key = generate_long_key(32)
        
        tk.Label(root, text="Message:").pack()
        self.message_entry = tk.Text(root, height=2, width=50)
        self.message_entry.pack()
        self.message_entry.insert(tk.END, config.MESSAGE)
        
        tk.Button(root, text="Add Phrase", command=self.add_phrase).pack()
        
        tk.Label(root, text="Cover Image:").pack()
        self.image_path_var = tk.StringVar()
        tk.Entry(root, textvariable=self.image_path_var, width=50).pack()
        tk.Button(root, text="Browse Image", command=self.browse_image).pack()
        
        tk.Button(root, text="Encrypt & Hide", command=self.encrypt).pack()
        tk.Button(root, text="Decrypt from Image", command=self.decrypt).pack()
        
        tk.Label(root, text="Output:").pack()
        self.output_text = tk.Text(root, height=5, width=50)
        self.output_text.pack()

    def add_phrase(self):
        message = self.message_entry.get("1.0", tk.END).strip()
        if message:
            phrase_path = os.path.join('Secret', 'phrases', f"phrase_{time.strftime('%Y%m%d_%H%M%S')}.txt")
            with open(phrase_path, 'w') as f:
                f.write(message)
            messagebox.showinfo("Success", f"Phrase added to {phrase_path}")
            logging.info(f"Phrase added: {phrase_path}")
        else:
            messagebox.showerror("Error", "No message to add!")

    def browse_image(self):
        path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
        self.image_path_var.set(path)

    def encrypt(self):
        try:
            message = self.message_entry.get("1.0", tk.END).strip()
            image_path = self.image_path_var.get()
            if not image_path or not message:
                raise ValueError("Message and image required")
            
            vig_ct = vigenere_encrypt(message, self.vig_key)
            
            encrypted_bundle, sk, hmac_tag = kyber_hybrid_encrypt(vig_ct.encode())
            encrypted_bundle_with_tag = encrypted_bundle + hmac_tag
            
            nums = numeric_encode(encrypted_bundle_with_tag)
            
            scrambled_nums = scramble_nums(nums, self.scramble_key)
            
            concat = '-'.join(scrambled_nums)
            b64 = base64.b64encode(concat.encode()).decode()
            
            output_path = os.path.join(sub_path, 'images', "secret.png")
            lsb_steganography_hide(image_path, b64.encode(), output_path)
            
            keys_path = os.path.join(sub_path, 'keys', "keys.txt")
            with open(keys_path, 'w') as f:
                f.write(f"Vigenère Key: {self.vig_key}\n")
                f.write(f"Kyber SK: {sk.hex()}\n")
                f.write(f"Scramble Key: {self.scramble_key}\n")
            
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"Encrypted and hidden in {output_path}\nKeys saved to {keys_path}\nDelete folder to remove.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            logging.error(f"Encryption failed: {str(e)}")

    def decrypt(self):
        try:
            image_path = self.image_path_var.get()
            if not image_path:
                raise ValueError("Select an image")
            
            vig_key = simpledialog.askstring("Input", "Enter Vigenère Key:")
            sk_hex = simpledialog.askstring("Input", "Enter Kyber SK (hex):")
            scramble_key = simpledialog.askstring("Input", "Enter Scramble Key:")
            if not vig_key or not sk_hex or not scramble_key:
                raise ValueError("Keys required")
            sk = bytes.fromhex(sk_hex)
            
            b64_data = lsb_steganography_retrieve(image_path)
            
            concat = b64_data.decode(errors='ignore').rstrip('\x00')
            nums = concat.split('-')
            
            unscrambled_nums = unscramble_nums(nums, scramble_key)
            
            bundle_with_tag = reverse_numeric(unscrambled_nums)
            
            vig_recovered = kyber_hybrid_decrypt(bundle_with_tag, sk).decode()
            
            plaintext = vigenere_decrypt(vig_recovered, vig_key)
            
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"Decrypted: {plaintext}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            logging.error(f"Decryption failed: {str(e)}")

def run_gui():
    root = tk.Tk()
    app = EncryptApp(root)
    root.mainloop()
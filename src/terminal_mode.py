
import os
import base64
import time
import config
from src.encrypt_utils import *
from src.decrypt_utils import *
from src.stego_utils import *
import logging

def run_terminal_mode(mode):
    try:
        if mode == "terminal_no_input":
            choice = config.DEFAULT_ACTION
        else:
            choice = input("Enter 'encrypt' or 'decrypt': ").lower()
        if choice == "encrypt":
            if mode == "terminal_no_input":
                message = config.MESSAGE
                image_path = 'cover.png'
            else:
                message = input("Enter message: ")
                image_path = input("Enter cover image path: ")
            vig_key = generate_long_key()
            scramble_key = generate_long_key(32)
            vig_ct = vigenere_encrypt(message, vig_key)
            encrypted_bundle, sk, hmac_tag = kyber_hybrid_encrypt(vig_ct.encode())
            encrypted_bundle_with_tag = encrypted_bundle + hmac_tag
            nums = numeric_encode(encrypted_bundle_with_tag)
            scrambled_nums = scramble_nums(nums, scramble_key)
            concat = '-'.join(scrambled_nums)
            b64 = base64.b64encode(concat.encode()).decode()
            output_path = os.path.join(sub_path, 'images', "secret.png")
            lsb_steganography_hide(image_path, b64.encode(), output_path)
            keys_path = os.path.join(sub_path, 'keys', "keys.txt")
            with open(keys_path, 'w') as f:
                f.write(f"Vigenère Key: {vig_key}\n")
                f.write(f"Kyber SK: {sk.hex()}\n")
                f.write(f"Scramble Key: {scramble_key}\n")
            print(f"Encrypted and hidden in {output_path}")
            print(f"Keys saved to {keys_path}")
            logging.info("Terminal encryption completed")
        elif choice == "decrypt":
            if mode == "terminal_no_input":
                image_path = 'Decrypt/secret.png'
                keys_path = 'Decrypt/keys.txt'
                if not os.path.exists(image_path) or not os.path.exists(keys_path):
                    raise ValueError("Decrypt folder must contain secret.png and keys.txt for no_input mode")
                with open(keys_path, 'r') as f:
                    lines = f.readlines()
                    vig_key = lines[0].split(': ')[1].strip()
                    sk_hex = lines[1].split(': ')[1].strip()
                    scramble_key = lines[2].split(': ')[1].strip()
            else:
                image_path = input("Enter secret image path: ")
                vig_key = input("Enter Vigenère Key: ")
                sk_hex = input("Enter Kyber SK (hex): ")
                scramble_key = input("Enter Scramble Key: ")
            sk = bytes.fromhex(sk_hex)
            b64_data = lsb_steganography_retrieve(image_path)
            concat = b64_data.decode(errors='ignore').rstrip('\x00')
            nums = concat.split('-')
            unscrambled_nums = unscramble_nums(nums, scramble_key)
            bundle_with_tag = reverse_numeric(unscrambled_nums)
            vig_recovered = kyber_hybrid_decrypt(bundle_with_tag, sk).decode()
            plaintext = vigenere_decrypt(vig_recovered, vig_key)
            print(f"Decrypted: {plaintext}")
            logging.info("Terminal decryption completed")
    except Exception as e:
        print(f"Error: {str(e)}")
        logging.error(f"Terminal mode failed: {str(e)}")

import os
import base64
import random
import string
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hmac, hashes
from kyber_py import Kyber
import logging

logging.basicConfig(filename='Secret/logs/app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_long_key(length=37):
    key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    logging.info(f"Generated key of length {length}")
    return key

def vigenere_encrypt(plaintext, key):
    plaintext = plaintext.upper().replace(' ', '')
    key = key.upper()
    ciphertext = ''
    key_repeated = (key * (len(plaintext) // len(key) + 1))[:len(plaintext)]
    for p, k in zip(plaintext, key_repeated):
        if p.isalpha():
            shift = ord(k) - ord('A')
            ciphertext += chr((ord(p) - ord('A') + shift) % 26 + ord('A'))
        else:
            ciphertext += p
    logging.info("Vigenère encryption completed")
    return ciphertext

def kyber_hybrid_encrypt(data):
    kyber = Kyber()
    pk, sk = kyber.keygen()
    ct, shared_secret = kyber.encap(pk)
    aesgcm = AESGCM(shared_secret)
    nonce = os.urandom(12)
    encrypted_data = aesgcm.encrypt(nonce, data, None)
    encrypted_bundle = b''.join([ct, nonce, encrypted_data])
    h = hmac.HMAC(shared_secret, hashes.SHA256())
    h.update(encrypted_bundle)
    hmac_tag = h.finalize()
    logging.info("Kyber hybrid encryption completed")
    return encrypted_bundle, sk, hmac_tag

def numeric_encode(data, multiplier=23, add=57, mod=100003):
    return [str((byte * multiplier + add) % mod) for byte in data]

def scramble_nums(nums, seed_key):
    random.seed(seed_key)
    indices = list(range(len(nums)))
    random.shuffle(indices)
    scrambled = [None] * len(nums)
    for i, idx in enumerate(indices):
        scrambled[idx] = nums[i]
    logging.info("Scrambling completed")
    return scrambled
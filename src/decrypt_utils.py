
import random
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hmac, hashes
from kyber_py import Kyber
import logging

logging.basicConfig(filename='Secret/logs/app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def vigenere_decrypt(ciphertext, key):
    key = key.upper()
    plaintext = ''
    key_repeated = (key * (len(ciphertext) // len(key) + 1))[:len(ciphertext)]
    for c, k in zip(ciphertext, key_repeated):
        if c.isalpha():
            shift = ord(k) - ord('A')
            plaintext += chr((ord(c) - ord('A') - shift) % 26 + ord('A'))
        else:
            plaintext += c
    logging.info("Vigenère decryption completed")
    return plaintext

def kyber_hybrid_decrypt(encrypted_bundle_with_tag, sk):
    hmac_tag = encrypted_bundle_with_tag[-32:]
    encrypted_bundle = encrypted_bundle_with_tag[:-32]
    kyber = Kyber()
    ct, nonce, encrypted_data = encrypted_bundle[:kyber.ciphertext_bytes], encrypted_bundle[kyber.ciphertext_bytes:kyber.ciphertext_bytes+12], encrypted_bundle[kyber.ciphertext_bytes+12:]
    shared_secret = kyber.decap(ct, sk)
    h = hmac.HMAC(shared_secret, hashes.SHA256())
    h.update(encrypted_bundle)
    try:
        h.verify(hmac_tag)
        logging.info("HMAC verification successful")
    except:
        logging.error("HMAC verification failed")
        raise ValueError("HMAC verification failed")
    aesgcm = AESGCM(shared_secret)
    return aesgcm.decrypt(nonce, encrypted_data, None)

def reverse_numeric(nums, multiplier=23, add=57, mod=100003):
    inv_mult = pow(multiplier, -1, mod)
    data = bytearray()
    for num_str in nums:
        if num_str:
            num = int(num_str)
            byte_val = ((num - add) * inv_mult) % mod
            data.append(byte_val % 256)
    return bytes(data)

def unscramble_nums(scrambled, seed_key):
    random.seed(seed_key)
    indices = list(range(len(scrambled)))
    random.shuffle(indices)
    unscrambled = [None] * len(scrambled)
    for i, idx in enumerate(indices):
        unscrambled[i] = scrambled[idx]
    logging.info("Unscrambling completed")
    return unscrambled
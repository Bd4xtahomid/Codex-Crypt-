
from PIL import Image
import logging

def lsb_steganography_hide(image_path, data, output_path):
    try:
        img = Image.open(image_path).convert('RGB')
        pixels = list(img.getdata())
        data_with_len = len(data).to_bytes(4, 'big') + data
        bin_data = ''.join(format(byte, '08b') for byte in data_with_len)
        if len(bin_data) > len(pixels) * 3:
            raise ValueError("Data too large for image")
        bin_pixels = []
        data_idx = 0
        for pixel in pixels:
            r, g, b = pixel
            if data_idx < len(bin_data):
                r = (r & 0xFE) | int(bin_data[data_idx])
                data_idx += 1
            if data_idx < len(bin_data):
                g = (g & 0xFE) | int(bin_data[data_idx])
                data_idx += 1
            if data_idx < len(bin_data):
                b = (b & 0xFE) | int(bin_data[data_idx])
                data_idx += 1
            bin_pixels.append((r, g, b))
        img.putdata(bin_pixels)
        img.save(output_path)
        logging.info(f"Data hidden in {output_path}")
    except Exception as e:
        logging.error(f"Steganography hide failed: {str(e)}")
        raise

def lsb_steganography_retrieve(image_path):
    try:
        img = Image.open(image_path).convert('RGB')
        pixels = list(img.getdata())
        bin_data = ''
        for pixel in pixels:
            r, g, b = pixel
            bin_data += str(r & 1)
            bin_data += str(g & 1)
            bin_data += str(b & 1)
        byte_data = bytes(int(bin_data[i:i+8], 2) for i in range(0, len(bin_data), 8))
        data_len = int.from_bytes(byte_data[:4], 'big')
        logging.info("Data retrieved from image")
        return byte_data[4:4+data_len]
    except Exception as e:
        logging.error(f"Steganography retrieve failed: {str(e)}")
        raise
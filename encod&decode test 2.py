import random
import string

def generate_passkey():
    symbols = ['+', '-', '*', '/']
    key = random.choice(symbols) + ''.join(random.choices(string.ascii_uppercase, k=4))
    return key

def calculate_shift(passkey):
    symbol, letters = passkey[0], passkey[1:]
    shift_value = sum(ord(char) - 64 for char in letters)  # Convert A=1, B=2, etc.
    if symbol == '-':
        shift_value *= -1
    elif symbol == '*':
        shift_value *= 2
    elif symbol == '/':
        shift_value = max(1, shift_value // 2)
    return shift_value

def shift_text(text, shift):
    shifted = ''.join(chr((ord(char) + shift) % 256) for char in text)
    return shifted

def text_to_binary(text):
    return ' '.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary):
    return ''.join(chr(int(b, 2)) for b in binary.split())

MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----', ' ': '/'  # Space = '/'
}
REVERSE_MORSE_CODE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}

def text_to_morse(text):
    return ' '.join(MORSE_CODE_DICT.get(char.upper(), '') for char in text)

def morse_to_text(morse):
    return ''.join(REVERSE_MORSE_CODE_DICT.get(code, '') for code in morse.split())

def encode_message(text):
    passkey = generate_passkey()
    shift_value = calculate_shift(passkey)
    shifted_text = shift_text(text, shift_value)
    binary_text = text_to_binary(shifted_text)
    morse_code = text_to_morse(binary_text)
    return passkey, morse_code

def decode_message(morse, passkey):
    shift_value = calculate_shift(passkey) * -1
    binary_text = morse_to_text(morse)
    shifted_text = binary_to_text(binary_text)
    original_text = shift_text(shifted_text, shift_value)
    return original_text

def main():
    choice = input("Do you want to Encode or Decode? (E/D): ").strip().upper()
    if choice == 'E':
        text = input("Enter the text to encode: ")
        passkey, encoded_message = encode_message(text)
        print(f"Passkey: {passkey}")
        print(f"Encoded Message: {encoded_message}")
    elif choice == 'D':
        encoded_text = input("Enter the encoded Morse code: ")
        passkey = input("Enter the passkey: ")
        try:
            decoded_message = decode_message(encoded_text, passkey)
            print(f"Decoded Message: {decoded_message}")
        except Exception as e:
            print("Error in decoding: Invalid passkey or encoded text!")
    else:
        print("Invalid choice! Please enter 'E' to Encode or 'D' to Decode.")

if __name__ == "__main__":
    main()

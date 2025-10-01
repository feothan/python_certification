import random

def encrypt_caesar(message, shift_right):
    letter_index = list("abcdefghijklmnopqrstuvwxyz")

    simple_message = ''.join(char for char in message if char.isalpha())
    simpler_message = simple_message.lower()

    encrypted_message = ''
    for letter in simpler_message:
        new_index = letter_index.index(letter) + shift_right
        if new_index > 25:
            new_index -= 26
        encrypted_message += letter_index[new_index]
    return encrypted_message

def decrypt_caesar(encrypted_message, shift_right):
    letter_index = list("abcdefghijklmnopqrstuvwxyz")

    decrypted_message = ''
    for letter in encrypted_message:
        new_index = letter_index.index(letter) - shift_right
        if new_index < 0:
            new_index += 26
        decrypted_message += letter_index[new_index]
    return decrypted_message

def generate_random_code_key():
    letters1 = letters2 = "abcdefghijklmnopqrstuvwxyz"
    code_key = []
    for letter in letters1:
        random_letter = random.choice(letters2)
        code_key.append((letter, random_letter))
        letters2 = letters2.replace(random_letter, "")
    return code_key

def encrypt_dict(message, code_key):
    simple_message = ''.join(char for char in message if char.isalpha())
    simpler_message = simple_message.lower()

    encrypted_message = ''
    for letter in simpler_message:
        for left_side, right_side in code_key:
            if left_side == letter:
                new_letter = right_side
                break
        encrypted_message += new_letter
    return encrypted_message

def decrypt_dict(encrypted_message, code_key):

    decrypted_message = ''
    for letter in encrypted_message:
        for left_side, right_side in code_key:
            if right_side == letter:
                new_letter = left_side
                break
        decrypted_message += new_letter
    return decrypted_message

message = "This is all I have to say today!"
shift_right = 7
print("The message =", message)
secret = encrypt_caesar(message, shift_right)
print("The message (Caesar) encrypted by", shift_right, "=", secret)
secret_revealed = decrypt_caesar(secret, 7)
print ("The message decrypted =", secret_revealed)

message = "This is all I have to say today!"
code_key = generate_random_code_key()
print("The message =", message)
secret = encrypt_dict(message, code_key)
print("The message (dictionary) encrypted =", secret)
secret_revealed = decrypt_dict(secret, code_key)
print("The message decrypted =", secret_revealed)
print("The cipher used was", code_key)
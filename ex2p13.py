from cryptek import *
import codecs

def key_value_parser(string):
    key_val_list = string.split('&')
    JSON_str = "{"
    for pair in key_val_list:
        key, val = pair.split('=')
        JSON_str += '\n\t' + key + ": '" + val + "',"
    JSON_str = JSON_str[:-1]
    JSON_str += "\n}"
    return JSON_str

def profile_for(email_str):
    if email_str.__contains__("&") or email_str.__contains__("="):
        print("Contains illegal characters.")
        return ''
    profile_str = f"email={email_str}&uid=10&role=user"
    return profile_str

def encrypted_profile_for(email_str):
    profile_str = profile_for(email_str)
    profile_str = PKCSpad(profile_str.encode(), blocksize) 
    return AES_encrypt(key_b, profile_str)

def decrypt_profile(encrypted_profile):
    user_profile = AES_decrypt(key_b, encrypted_profile)
    user_profile = PKCSstrip(user_profile)
    JSON = key_value_parser(user_profile.decode())
    return JSON

if __name__ == "__main__":
    blocksize=16
    ## Generate fixed random key
    key_b = rand_bytes(blocksize)

    ## Encrypt the profile string (test)
    cipher_profile = encrypted_profile_for("foo@bar.com")

    ## Figure out how 'admin' encrypts when at the start of a block
    pad = blocksize - len("admin")
    pad_char = bytes([pad]).decode()
    email_pad = "fo@bar.comadmin" + pad_char * pad

    cipher_0 = encrypted_profile_for(email_pad)
    admin_priv_block = cipher_0[blocksize:2*blocksize]

    ## Create a profile where role = aligns with end of block
    email_prefix = "foooo@bar.com"
    cipher_1 = encrypted_profile_for(email_prefix)
    
    ## append "admin" (with pad) ciper
    crafted_prof = cipher_1[:2*blocksize] + admin_priv_block
    priv_esc = decrypt_profile(crafted_prof)

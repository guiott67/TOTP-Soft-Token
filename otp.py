# This file contains all functions required to cmpute TOTP according to RFC-6238 (using SHA-1 Hash function) 
# Learn more at https://www.rfc-editor.org/rfc/rfc6238

import base64, struct, hashlib, time

# compute XOR of two bytes strings, using the Python XOR operator.
def xor(x, y):
    result = b''
    for i in range(min(len(x), len(y))):
        result += bytes([x[i] ^ y[i]])
    return result

# Compute HMAC value given message, key and Hash function.
# For more information, see RFC-2104 on rfc-editor.org
def hmac (message, key, hashFn):
    # Define ipad and opad values
    ipad = b'\x36' * 64
    opad = b'\x5c' * 64

    # add padding to the key
    paddedKey = key + b'\x00' * (64 - len(key))

    # Compute hash of iKeypad and message using sha1 function
    hash1 = hashFn(xor(paddedKey, ipad))
    hash1.update(message)

    # Same operation with oKeypad and first hash
    hash2 = hashFn(xor(paddedKey, opad))
    hash2.update(hash1.digest())

    return hash2.digest()


# Call hmac function to compute TOTP token, given a secret.
def totpToken(secret):
    # Decode base32 encoded secret
    key = base64.b32decode(secret, True)

    # Encode current time divided by 30 in binary string (64-bit integer, big-endian)
    message = struct.pack(">Q", int(time.time())//30)
    # Call hmac function to get hmac-sha1 value from message and key
    hash = hmac(message, key, hashlib.sha1)

    # Compute offset
    offset = hash[19]
    offset = offset & 15

    # Use offset to find TOTP
    code = struct.unpack(">I", hash[offset:offset+4])[0] & 0x7fffffff
    result = str(code % 1000000)

    # Add zeros if TOTP length smaller than 6
    while len(result) < 6:
        result = "0" + result

    return result
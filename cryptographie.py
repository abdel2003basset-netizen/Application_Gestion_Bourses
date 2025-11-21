import random


def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False
    return True

def find_primitive_root(p):
    phi = p - 1
    factors = set()
    n = phi
    i = 2
    while i * i <= n:
        if n % i == 0:
            factors.add(i)
            while n % i == 0:
                n //= i
        i += 1
    if n > 1:
        factors.add(n)
    for g in range(2, p):
        if all(pow(g, phi // f, p) != 1 for f in factors):
            return g
    return -1

def modinv(a, m):
    # Inverse modulaire (algorithme d'Euclide étendu)
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise Exception("Pas d'inverse modulaire")
    return x % m

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

# --- 1. Génération des clés  test cmd git---

def generate_keys():
    print("🔑 Génération des clés...")
    while True:
        p = random.randint(1000, 5000)
        if is_prime(p):
            break
    g = find_primitive_root(p)
    x = random.randint(1, p-2)  # clé privée
    y = pow(g, x, p)            # clé publique
    public_key = (p, g, y)
    private_key = x
    return public_key, private_key

# --- 2. Chiffrement ---

def encrypt(public_key, plaintext):
    p, g, y = public_key
    k = random.randint(1, p-2)         # aléatoire
    a = pow(g, k, p)
    cipher = []
    for char in plaintext:
        m = ord(char)
        b = (pow(y, k, p) * m) % p
        cipher.append((a, b))
    return cipher

# --- 3. Déchiffrement ---

def decrypt(private_key, public_key, ciphertext):
    p, g, y = public_key
    x = private_key
    decrypted = ''
    for a, b in ciphertext:
        s = pow(a, x, p)
        s_inv = modinv(s, p)
        m = (b * s_inv) % p
        decrypted += chr(m)
    return decrypted

# --- Utilisation ---

# Utilisateur A
public_key, private_key = generate_keys()
print("Clé publique :", public_key)
print("Clé privée :", private_key)

# Utilisateur B chiffre un message
message = "Hello ElGamal"
ciphered = encrypt(public_key, message)
print("\n Message chiffré :", ciphered)

# Utilisateur A déchiffre le message suivant
decrypted = decrypt(private_key, public_key, ciphered)
print(" Message déchiffré :", decrypted)

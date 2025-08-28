from gmssl.sm2 import CryptSM2

PRIVATE_KEY = "48af83d84b153c64d412708cc02119716dfaedbfcf8f87aca01d54f33888986e"
PUBLIC_KEY = "04ed4fa5e0586a0093725c584663db82a6c66cbf69fe7e0ca3cdca49cc2001f18992b7603ef0b3689b7919a022762d1b888085edd8861cbc1ea93de4e3ff7980fd"

sm2_crypt = CryptSM2(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY, mode=1)


# Python → Java (自动加 "04")
def encrypt_for_java(plaintext: str) -> str:
    cipher = sm2_crypt.encrypt(plaintext.encode("utf-8")).hex()
    return "04" + cipher


# Java → Python (自动去掉 "04")
def decrypt_from_java(cipher_hex: str) -> str:
    if cipher_hex.startswith("04"):
        cipher_hex = cipher_hex[2:]
    return sm2_crypt.decrypt(bytes.fromhex(cipher_hex)).decode("utf-8")


# ---------------- 测试 ----------------
# Python 加密，供 Java 解密
py2java_cipher = encrypt_for_java("123")
print("Python → Java:", py2java_cipher)

# Java 密文解密（你提供的）
java_cipher = "04c6c9ed6ec9323c8647949a743c8fc2fbe02f10a5fe0ce6b0bf48ade4374f78f2410d4b486fa6cb02b2abce4baf56dd5b609c2f2286963f4887182748210dcd525505c8de3ff21a8abcfd621ae7763b4b5b8b09d510486c9b3ce91463a4667053a17505"
print("Java → Python:", decrypt_from_java(java_cipher))

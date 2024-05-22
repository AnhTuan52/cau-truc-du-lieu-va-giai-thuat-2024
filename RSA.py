from math import sqrt
#required for the sqrt() function, if you want to avoid doing **0.5
import random
#required for randrange
from random import randint as rand

#just to use the well known keyword rand() from C++


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return -1


def isprime(n):
    if n < 2:
        return False
    elif n == 2:
        return True
    else:
        for i in range(2, int(sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
    return True


#initial two random numbers p,q
p = rand(1, 1000)
q = rand(1, 1000)


def generate_keypair(p, q, keysize):
    # Kích thước khóa là độ dài bit của \( n \), vì vậy nó phải nằm trong khoảng từ \( n_{\text{Min}} \) đến \( n_{\text{Max}} + 1 \).
    # << là toán tử bitwise
    # x << y giống như nhân x với 2**y
    #  điều này để giá trị p và q có độ dài bit tương tự nhau
    # điều này sẽ tạo ra một giá trị n khó phân tích thành p và q.

    nMin = 1 << (keysize - 1)
    nMax = (1 << keysize) - 1
    primes = [2]
    # chúng tôi chọn hai số nguyên tố trong phạm vi (bắt đầu, dừng) sao cho chênh lệch độ dài bit tối đa là 2.
    start = 1 << (keysize // 2 - 1)
    stop = 1 << (keysize // 2 + 1)

    if start >= stop:
        return []

    for i in range(3, stop + 1, 2):
        for p in primes:
            if i % p == 0:
                break
        else:
            primes.append(i)

    while (primes and primes[0] < start):
        del primes[0]

    #chọn p và q từ các số nguyên tố được tạo.
    while primes:
        p = random.choice(primes)
        primes.remove(p)
        q_values = [q for q in primes if nMin <= p * q <= nMax]
        if q_values:
            q = random.choice(q_values)
            break
    print(p, q)
    n = p * q
    phi = (p - 1) * (q - 1)

    #Tạo khóa công khai với điều kiện 1<e<φ(n)
    e = random.randrange(1, phi)
    g = gcd(e, phi)

    while True:
        #miễn là gcd(1,phi(n)) không bằng 1, hãy tiếp tục tạo e
        e = random.randrange(1, phi)
        g = gcd(e, phi)
        #Tạo khóa bí mật
        d = mod_inverse(e, phi)
        if g == 1 and e != d:
            break

    #khóa công khai (e,n)
    #pkhóa riêng (d,n)

    return ((e, n), (d, n))


def encrypt(msg_plaintext, package):
    #giải nén cặp mã hóa
    e, n = package
    msg_ciphertext = [pow(ord(c), e, n) for c in msg_plaintext]
    return msg_ciphertext


def decrypt(msg_ciphertext, package):
    d, n = package
    msg_plaintext = [chr(pow(c, d, n)) for c in msg_ciphertext]
    # Không cần sử dụng ord() vì c bây giờ là một số
    # Sau khi giải mã, chúng tôi chuyển nó trở lại ký tự
    # được nối thành một chuỗi để có kết quả cuối cùng
    return (''.join(msg_plaintext))


#-------------------------------------------------------------
#driver program
if __name__ == "__main__":
    bit_length = int(input("Enter bit_length: "))
    print("Running RSA...")
    print("Generating public/private keypair...")
    public, private = generate_keypair(
        p, q, 2**bit_length)  # 8 là giá trị kích thước khóa (độ dài bit)
    print("Public Key: ", public)
    print("Private Key: ", private)
    msg = input("Write msg: ")
    print([ord(c) for c in msg])
    encrypted_msg = encrypt(msg, public)
    print("Encrypted msg: ")
    print(''.join(map(lambda x: str(x), encrypted_msg)))
    print("Decrypted msg: ")
    print(decrypt(encrypted_msg, private))

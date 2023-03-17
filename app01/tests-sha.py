from hashlib import sha256
pow2, sum1 = 1, 0
for pow1 in range(1, 1000001):
    while True:
        sha = sha256(f'{pow1 * pow2}'.encode()).hexdigest()
        if sha[:1] == "0":
            sum1 += pow2;
            print(pow1, pow2)
            pow2 = 1
            break
        pow2 += 1
print(sum1 // 1000000)
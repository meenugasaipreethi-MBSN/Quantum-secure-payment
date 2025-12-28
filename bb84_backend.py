import random

def generate_quantum_key():
    key = ''.join(str(random.randint(0,1)) for _ in range(16))
    return key
def calculate_qber():
    # Simulated QBER (real BB84 concept)
    return random.uniform(0.01, 0.15)
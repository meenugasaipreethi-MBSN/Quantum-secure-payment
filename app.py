import streamlit as st
import random

st.set_page_config(page_title="Quantum Secure Payment", layout="centered")

st.title("🔐 Quantum Secure Online Payment (BB84)")

KEY_LENGTH = 16

# ---------- BB84 FUNCTIONS ----------
def generate_bits(n):
    return [random.randint(0, 1) for _ in range(n)]

def generate_bases(n):
    return [random.choice(['+', 'x']) for _ in range(n)]

def bob_measure(alice_bits, alice_bases, bob_bases):
    results = []
    for i in range(len(alice_bits)):
        if alice_bases[i] == bob_bases[i]:
            results.append(alice_bits[i])
        else:
            results.append(random.randint(0, 1))
    return results

def sift_key(alice_bits, bob_bits, alice_bases, bob_bases):
    final_key = []
    for i in range(len(alice_bits)):
        if alice_bases[i] == bob_bases[i]:
            final_key.append(alice_bits[i])
    return final_key

def calculate_qber(alice_key, bob_key):
    errors = sum(1 for a, b in zip(alice_key, bob_key) if a != b)
    if len(alice_key) == 0:
        return 0
    return errors / len(alice_key)

# ---------- UI ----------
if st.button("🔑 Generate Quantum Key"):

    alice_bits = generate_bits(KEY_LENGTH)
    alice_bases = generate_bases(KEY_LENGTH)
    bob_bases = generate_bases(KEY_LENGTH)

    bob_results = bob_measure(alice_bits, alice_bases, bob_bases)

    alice_key = sift_key(alice_bits, bob_results, alice_bases, bob_bases)
    bob_key = sift_key(bob_results, bob_results, alice_bases, bob_bases)

    qber = calculate_qber(alice_key, bob_key)

    st.subheader("BB84 Simulation Results")
    st.write("Alice Bits:", alice_bits)
    st.write("Alice Bases:", alice_bases)
    st.write("Bob Bases:", bob_bases)
    st.write("Alice Final Key:", alice_key)
    st.write("Bob Final Key:", bob_key)

    st.subheader("📊 QBER Analysis")
    st.write(f"QBER = {qber:.2%}")

    if qber <= 0.11:
        st.success("✅ Channel Secure – No Eavesdropping Detected")

        st.subheader("💳 Secure Payment")
        amount = st.number_input("Enter Payment Amount", min_value=1)

        if st.button("Pay Securely"):
            st.success(f"Payment of ₹{amount} completed using Quantum Key 🔐")

    else:
        st.error("🚨 Attack Detected! Payment Blocked")

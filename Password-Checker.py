import string
import getpass
import hashlib
import requests

# ---------------- CONFIG ----------------
USE_API_FALLBACK = False  # only used if no wordlists are found

COMMON_PASSWORDS = {
    "password", "123456", "123456789", "qwerty",
    "abc123", "password1", "111111", "123123"
}

COMMON_PATTERNS = ["12345", "qwerty", "asdf", "zxcv"]


# ---------------- WORDLIST CHECK (MULTI-FILE, STREAM SAFE) ----------------
def check_in_wordlists(password, files=("hello.txt", )):
    for filename in files:
        try:
            with open(filename, "r", encoding="latin-1") as f:
                for line in f:
                    if line.strip() == password:
                        return f"Found in {filename}"
        except FileNotFoundError:
            continue
    return None


# ---------------- OPTIONAL HAVE I BEEN PWNED API ----------------
def check_pwned_api(password):
    sha1_pwd = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1_pwd[:5]
    suffix = sha1_pwd[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    try:
        res = requests.get(url, timeout=5)
        if res.status_code != 200:
            return None

        for line in res.text.splitlines():
            h, count = line.split(":")
            if h == suffix:
                return int(count)
        return 0
    except:
        return None


# ---------------- MAIN PASSWORD CHECK ----------------
def check_pwd():
    password = getpass.getpass("Enter Password: ")
    strength = 0
    remarks = ""

    lower = upper = num = space = special = 0

    for c in password:
        if c in string.ascii_lowercase:
            lower += 1
        elif c in string.ascii_uppercase:
            upper += 1
        elif c in string.digits:
            num += 1
        elif c.isspace():
            space += 1
        else:
            special += 1

    # base strength scoring
    if lower: strength += 1
    if upper: strength += 1
    if num: strength += 1
    if space: strength += 1
    if special: strength += 1

    weaknesses = []

    # ---------------- PATTERN CHECKS ----------------
    if password.lower() in COMMON_PASSWORDS:
        weaknesses.append("Common password")

    for p in COMMON_PATTERNS:
        if p in password.lower():
            weaknesses.append(f"Contains pattern: {p}")
            break

    if len(set(password)) <= 2:
        weaknesses.append("Too many repeated characters")

    if len(password) < 8:
        weaknesses.append("Too short (min 8 characters)")

    # ---------------- WORDLIST CHECKS ----------------
    wordlist_result = check_in_wordlists(password)

    if wordlist_result:
        weaknesses.append(f"Found in wordlist ({wordlist_result})")
        strength -= 2

    # fallback to API if no wordlists exist
    elif USE_API_FALLBACK:
        breach_count = check_pwned_api(password)
        if breach_count:
            weaknesses.append(f"Found in breaches {breach_count:,} times")
            strength -= 2

    # penalty for weaknesses
    strength -= len(weaknesses)
    if strength < 1:
        strength = 1

    # ---------------- RATING ----------------
    if strength == 1:
        remarks = "Very Weak Password"
    elif strength == 2:
        remarks = "Weak Password"
    elif strength == 3:
        remarks = "Moderate Password"
    elif strength == 4:
        remarks = "Strong Password"
    else:
        remarks = "Very Strong Password"

    # ---------------- OUTPUT ----------------
    print("\n--- Password Analysis ---")
    print(f"Lowercase: {lower}")
    print(f"Uppercase: {upper}")
    print(f"Numbers: {num}")
    print(f"Spaces: {space}")
    print(f"Special: {special}")

    print(f"\nStrength: {strength}/5")
    print(f"Result: {remarks}")

    if weaknesses:
        print("\n⚠️ Weaknesses detected:")
        for w in weaknesses:
            print("-", w)
    else:
        print("\n✅ No obvious weaknesses detected")

    # ---------------- CRACK TIME ----------------
    charset = 0
    if lower: charset += 26
    if upper: charset += 26
    if num: charset += 10
    if special: charset += 32

    if charset > 0:
        combos = charset ** len(password)
        seconds = combos / 1_000_000_000
        years = seconds / (60 * 60 * 24 * 365)

        print("\n--- Crack Time Estimate ---")
        print(f"{seconds:.2e} seconds")

        if years > 1e9:
            print(f"≈ {years/1e9:.2f} billion years")
        elif years > 1e6:
            print(f"≈ {years/1e6:.2f} million years")
        else:
            print(f"≈ {years:.2f} years")


# ---------------- LOOP ----------------
def ask():
    return input("Check password? (y/n): ").lower() == "y"


if __name__ == "__main__":

    print("Welcome to a Real-World Password Checker")
    print("This Password Checker helps check the weakness of your password strenght")
    print("using real-world set of wordlists")
    print("Author: Felix Godspower")
    print("Date Created: 1 May 2026")
    print("X handle: @boiGeepee")
    print("Whatsapp: 09052131903")
    print("Email: geehvck@gmail.com")
    while ask():
        check_pwd()

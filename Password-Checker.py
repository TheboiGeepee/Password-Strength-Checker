import string
import getpass
import hashlib
import requests
import sys
import time
from datetime import datetime

# ================= CONFIG =================
USE_API_FALLBACK = False  # Set True to enable HaveIBeenPwned API fallback

COMMON_PASSWORDS = {
    "password",
    "123456",
    "123456789",
    "qwerty",
    "abc123",
    "password1",
    "111111",
    "123123"
}

COMMON_PATTERNS = [
    "12345",
    "qwerty",
    "asdf",
    "zxcv"
]

# ================= ANIMATED TEXT =================
def animated_text(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# ================= CURRENT DATE & TIME =================
def show_datetime():
    now = datetime.now().astimezone()

    current_date = now.strftime("%A, %d %B %Y")
    current_time = now.strftime("%I:%M:%S %p")
    timezone = now.tzname()

    gmt_offset = now.strftime("%z")
    gmt_offset = f"GMT{gmt_offset[:3]}:{gmt_offset[3:]}"

    info = f"""
\033[95m═══════════════════════════════════════════════════════\033[0m
\033[96mCurrent Date :\033[0m {current_date}
\033[96mCurrent Time :\033[0m {current_time}
\033[96mTimezone     :\033[0m {timezone}
\033[96mGMT Offset   :\033[0m {gmt_offset}
\033[95m═══════════════════════════════════════════════════════\033[0m
"""

    animated_text(info, delay=0.005)

# ================= WORDLIST CHECK =================
def check_in_wordlists(password, files=("hello.txt",)):
    for filename in files:
        try:
            with open(filename, "r", encoding="latin-1") as f:
                for line in f:
                    if line.strip() == password:
                        return f"Found in {filename}"

        except FileNotFoundError:
            continue

    return None

# ================= HAVE I BEEN PWNED API =================
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

# ================= EXIT ANIMATION =================
def fancy_exit_with_dots(
    message="Program exited successfully. Goodbye!",
    delay=0.05,
    dots=5,
    dot_delay=0.3
):

    for _ in range(dots):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(dot_delay)

    print()

    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)

    print()

# ================= HUMAN READABLE TIME =================
def format_time(seconds):

    if seconds < 1:
        return "<1 second"

    intervals = (
        ('days', 60 * 60 * 24),
        ('hours', 60 * 60),
        ('minutes', 60),
        ('seconds', 1),
    )

    parts = []

    for name, count in intervals:

        value = int(seconds // count)

        if value:
            parts.append(f"{value} {name}")
            seconds %= count

    return ', '.join(parts)

# ================= PASSWORD STRENGTH BAR =================
def strength_bar(strength, max_strength=5, length=10):

    filled = int((strength / max_strength) * length)
    empty = length - filled

    return "[" + "█" * filled + "░" * empty + f"] {strength}/{max_strength}"

# ================= PASSWORD CHECKER =================
def check_pwd():

    password = getpass.getpass(
        "\n\033[93mEnter Password (or type exit): \033[0m"
    )

    # Exit option
    if password.lower() == "exit":

        fancy_exit_with_dots(
            "\033[91m❌ Program exited successfully. Goodbye!\033[0m"
        )

        sys.exit()

    strength = 0

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

    # ================= BASE STRENGTH =================
    if lower:
        strength += 1

    if upper:
        strength += 1

    if num:
        strength += 1

    if space:
        strength += 1

    if special:
        strength += 1

    weaknesses = []

    # ================= PATTERN CHECKS =================
    if password.lower() in COMMON_PASSWORDS:
        weaknesses.append("Common password")

    for p in COMMON_PATTERNS:

        if p in password.lower():
            weaknesses.append(f"Contains pattern: {p}")
            break

    if len(set(password)) <= 2:
        weaknesses.append("Too many repeated characters")

    if len(password) < 8:
        weaknesses.append("Too short (minimum 8 characters)")

    # ================= WORDLIST CHECK =================
    wordlist_result = check_in_wordlists(password)

    if wordlist_result:

        weaknesses.append(
            f"Found in wordlist ({wordlist_result})"
        )

        strength -= 2

    elif USE_API_FALLBACK:

        breach_count = check_pwned_api(password)

        if breach_count:

            weaknesses.append(
                f"Found in breaches {breach_count:,} times"
            )

            strength -= 2

    # ================= CRITICAL WEAKNESS =================
    critical_weaknesses = [
        "Common password",
        "Found in wordlist",
        "Found in breaches"
    ]

    if any(
        cw in w
        for w in weaknesses
        for cw in critical_weaknesses
    ):
        strength = 1

    else:

        strength -= len(weaknesses)

        if strength < 1:
            strength = 1

    # ================= PASSWORD RATING =================
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

    # ================= OUTPUT =================
    print("\n\033[95m--- Password Analysis ---\033[0m")

    print(
        f"\033[96mLowercase:\033[0m {lower}, "
        f"\033[96mUppercase:\033[0m {upper}, "
        f"\033[96mNumbers:\033[0m {num}, "
        f"\033[96mSpaces:\033[0m {space}, "
        f"\033[96mSpecial:\033[0m {special}"
    )

    print(
        f"\n\033[92mStrength:\033[0m "
        f"{strength_bar(strength)} | {remarks}"
    )

    # ================= WEAKNESSES =================
    if weaknesses:

        print("\n\033[91m⚠️ Weaknesses detected:\033[0m")

        for w in weaknesses:
            print(f"\033[91m-\033[0m {w}")

    else:
        print("\n\033[92m✅ No obvious weaknesses detected\033[0m")

    # ================= CRACK TIME =================
    charset = 0

    if lower:
        charset += 26

    if upper:
        charset += 26

    if num:
        charset += 10

    if special:
        charset += 32

    print("\n\033[95m--- Crack Time Estimate ---\033[0m")

    if any(
        cw in w
        for w in weaknesses
        for cw in critical_weaknesses
    ):
        print("\033[91m<1 second (already breached)\033[0m")

    elif charset > 0:

        combos = charset ** len(password)

        guesses_per_sec = 1_000_000_000

        seconds = combos / guesses_per_sec

        print(f"\033[93m{format_time(seconds)}\033[0m")

# ================= LOOP =================
def ask():

    choice = input(
        "\n\033[94mCheck password? (y/n or exit): \033[0m"
    ).lower().strip()

    if choice == "exit":

        fancy_exit_with_dots(
            "\033[91m❌ Program exited successfully. Goodbye!\033[0m"
        )

        sys.exit()

    return choice == "y"

# ================= MAIN =================
if __name__ == "__main__":

    intro = f"""
\033[96m╔════════════════════════════════════════════════════╗
║        Welcome to a Real-World Password Checker   ║
╠════════════════════════════════════════════════════╣
║  Author   : Felix Godspower                       ║
║  X        : @boiGeepee                            ║
║  Linkedin : Felix Godspower                           ║
║  Email    : geehvck@gmail.com                     ║
╚════════════════════════════════════════════════════╝\033[0m

\033[93m[ HOW TO USE ]\033[0m

\033[92m✔ This tool helps you:\033[0m
  • Check password strength
  • Detect weak/common passwords
  • Compare passwords against wordlists
  • Estimate crack time
  • Detect repeated patterns
  • Identify breached passwords (optional API mode)

\033[91m[ INSTRUCTIONS ]\033[0m
  • Type 'y' to check a password
  • Type 'n' to stop checking
  • Type 'exit' anytime to quit the program

\033[94mStay safe and use strong passwords.\033[0m
"""

    # Animated intro
    animated_text(intro, delay=0.003)

    # Show date & time
    show_datetime()

    # Program loop
    while True:

        if ask():
            check_pwd()

        else:

            fancy_exit_with_dots(
                "\033[91m❌ Goodbye!\033[0m"
            )

            break

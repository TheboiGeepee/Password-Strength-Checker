# 🔐 Real-World Password Checker & Generator

An advanced interactive Python-based password security toolkit designed for real-world password analysis and secure password generation.

This tool analyzes password strength using entropy calculations, pattern detection, breach detection, and realistic crack-time estimation while also providing cryptographically secure password generation for individuals and companies.

Built with a hacker-style terminal interface.

---

# 📸 Features

✅ Password strength analysis  
✅ Entropy calculation  
✅ Realistic crack-time estimation  
✅ Common password detection  
✅ Pattern detection  
✅ Wordlist comparison support  
✅ Optional HaveIBeenPwned API integration  
✅ Cryptographically secure password generator  
✅ Individual password generation mode  
✅ Company bulk password generation mode  
✅ Configurable password lengths  
✅ Hacker-style animated terminal UI  
✅ GMT date & time display  
✅ Secure local password generation  
✅ Secure HTTPS breach checking  
✅ Exit anytime using `exit`

---

# 🛡 Security Features

This project was designed with privacy and security in mind.

### ✔ Local Password Generation
Passwords are generated locally using Python's `secrets` module.

No passwords are sent to external servers.

---

### ✔ Secure Breach Checking
Optional breach detection uses the HaveIBeenPwned k-Anonymity API model.

Only the first 5 characters of the SHA1 hash are sent securely over HTTPS.

---

### ✔ No Password Storage
The application:
- Does NOT store passwords
- Does NOT log passwords
- Does NOT save user input
- Does NOT send passwords online

---

# ⚡ Password Analysis Includes

The checker analyzes:

- Lowercase letters
- Uppercase letters
- Numbers
- Special characters
- Common password usage
- Common attack patterns
- Repeated characters
- Password entropy
- Wordlist matches
- Known breach exposure

---

# 🔥 Realistic Crack-Time Estimates

Instead of fake mathematical simulations, this tool provides realistic estimates based on:

- Entropy
- Real-world password attack methods
- Known password exposure risks
- Modern brute-force capabilities

Example outputs:

```text
3 days
8 months
15 years
247 years
Millions of years
```

---

# 🔑 Password Generator Modes

## 👤 Individual Mode
Generate one extremely strong password securely.

Example:

```text
Generate for Individual or Company? (i/c): i
```

---

## 🏢 Company Mode
Generate multiple secure passwords at once for:

- Employees
- Servers
- Systems
- Databases
- Infrastructure

Example:

```text
Generate for Individual or Company? (i/c): c
How many passwords to generate?: 50
```

---

# 🧠 Password Strength Ratings

| Score | Rating |
|------|------|
| 1/5 | Very Weak |
| 2/5 | Weak |
| 3/5 | Moderate |
| 4/5 | Strong |
| 5/5 | Very Strong |

---

# 👨‍💻 Author

**Felix Godspower**

- X (Twitter): @boiGeepee
- LinkedIn: Felix Godspower

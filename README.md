# 🔐 Real-World Password Checker & Generator

An advanced interactive Python-based password security toolkit designed for real-world password analysis, authentication, and secure password generation.

This tool analyzes password strength using entropy calculations, pattern detection, breach detection, and realistic crack-time estimation while also providing cryptographically secure password generation for individuals and companies.

It also includes a built-in authentication system with permanent login support, password recovery, and security questions.

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
✅ Permanent login system  
✅ Security question recovery system  
✅ Password reset support  
✅ SHA-256 password hashing  
✅ Persistent authentication storage  
✅ Exit anytime using `exit`

---

# 🛡 Security Features

This project was designed with privacy and security in mind.

### ✔ Local Password Generation

Passwords are generated locally using Python's `secrets` module.

No generated passwords are sent to external servers.

---

### ✔ Secure Breach Checking

Optional breach detection uses the HaveIBeenPwned k-Anonymity API model.

Only the first 5 characters of the SHA1 hash are sent securely over HTTPS.

---

### ✔ Secure Authentication System

The authentication system uses SHA-256 hashing for:

- Master passwords
- Security question answers

No plaintext passwords are stored.

Authentication data is securely stored locally in:

```text
auth_data.json

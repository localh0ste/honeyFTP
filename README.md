# FTP Honeypot README

This project provides a simple Python-based FTP Honeypot designed to capture unauthorized login attempts and generate logs for Threat Intel analysis.

---

##  Features

* Simulates a real FTP service
* Supports **anonymous** and **admin** login attempts
* Logs all activity for threat analysis
* Lightweight and easy to run with Python 3
* Useful for SOC teams and research setups

---

## 📦 Requirements

* Python 3.x
* Standard Python libraries (no external dependencies)

---

## ▶️ How to Run

1. Clone or download the project folder to your system.
2. Ensure Python 3 is installed.
3. Open your terminal and navigate to the project directory.
4. Start the honeypot using:

```bash
python3 honey.py
```

5. Once started, the honeypot will:

   * Activate FTP-like listener on your system
   * Accept **anonymous** and **admin** login attempts
   * Record all interactions in the **logs folder** or as configured

---

## 📁 Log Collection

All activity captured by the honeypot—such as:

* Login attempts
* IP addresses
* Commands issued
* Timestamp of actions

---

## ⚠️ Disclaimer

This Honeypot is for **educational and research purposes only**. Do not deploy it on a production system or without proper authorization.

---

## 👨‍💻 Author

localh0ste

---

If you need a more detailed guide, diagrams, or enhancements for this README, feel free to ask!

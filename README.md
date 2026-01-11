# ECC Singularity Validator & KeyGen Simulator

![Project Status](https://img.shields.io/badge/Status-Complete-green)
![Language](https://img.shields.io/badge/Language-Python-blue)
![Topic](https://img.shields.io/badge/Cryptography-Elliptic_Curves-orange)

---

## 📋 Project Overview

This project demonstrates a **critical security weakness in Elliptic Curve Cryptography (ECC)**: the use of **singular elliptic curves**.

In ECC, if the curve parameters \( a \) and \( b \) produce a **zero discriminant**, the elliptic curve becomes **singular**. Singular curves **do not form a valid group**, which completely breaks ECC security and makes the **Discrete Logarithm Problem (DLP) trivial** to solve.

This tool acts as an **engineering-grade validator and simulator**, providing:

- Real-time **visualization** of elliptic curves
- Automatic **discriminant calculation**
- **Detection of singularities** (cusps and nodes)
- **Fail-safe blocking of key generation** on insecure curves

---

## 🛠 Prerequisites

You need **Python 3.x** and the following libraries:

- **NumPy** – numerical computation
- **Matplotlib** – interactive visualization & GUI

### Installation

```bash
pip install numpy matplotlib
```

python ecc_validator.py

## 🚀 How to Run

1.  Make sure Python 3.x is installed
2.  Install dependencies:
    ```bash
    pip install numpy matplotlib
    ```
3.  Run the application:
    ```bash
    python ecc_validator.py
    ```
    A graphical window will open showing the elliptic curve validator dashboard.

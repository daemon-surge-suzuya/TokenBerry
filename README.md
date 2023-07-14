# BerryTokenManager

This code provides a simple command-line interface for managing GitHub Personal
Access Tokens (PATs). It allows you to securely store and retrieve your PATs
using a password-based encryption scheme.

# Features

- Create new PAT: You can create and store new PATs along with their
  corresponding names.
- Display PATs: View the list of stored PATs.
- Copy token to clipboard: Copy a specific PAT to the clipboard for easy usage.
- Delete PAT: Remove a PAT from the stored list.
- Password protection: All PATs are encrypted using a password provided by the
  user.

# Prerequisites

Before using this code, make sure you have the following:

- Python 3 installed on your system.
- pyperclip

# Security Considerations

- The password you set is crucial for securing your PATs. Make sure to choose a
  strong and unique password.
- The PATs are encrypted using a password-based encryption scheme. However,
  please note that this code is for educational purposes and may not provide the
  same level of security as industry-standard encryption algorithms or dedicated
  key management systems.

# Disclaimer

This code is provided as-is and serves as a basic demonstration of token
management. It is recommended to use industry-standard solutions for managing
access tokens in production environments.

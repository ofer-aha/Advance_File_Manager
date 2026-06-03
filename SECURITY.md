# Security Policy

## ⚠️ Disclaimer & Liability

> **USE WITH CAUTION**
>
> This software is provided **"as is"**, without warranty of any kind, express or implied. The author(s) and contributors shall **not be held liable** for any damage, data loss, corruption, or unintended consequences resulting from the use or misuse of this application.
>
> File management operations such as **move, copy, delete, and duplicate removal are potentially destructive and irreversible**. Always ensure you have up-to-date backups of your data before using this tool. You use this software **entirely at your own risk**.

---

## 🔒 Supported Versions

| Version | Supported |
|---------|-----------|
| Latest (`main`) | ✅ Yes |
| Older releases | ❌ No |

---

## 🐛 Reporting a Vulnerability

If you discover a security vulnerability in this project, please follow responsible disclosure practices:

1. **Do NOT open a public GitHub issue** for security vulnerabilities.
2. **Contact the author directly** via GitHub: [@ofer-aha](https://github.com/ofer-aha)
3. Provide a clear description of the vulnerability, including:
   - Steps to reproduce the issue
   - Potential impact and severity
   - Any suggested mitigations or fixes

You can expect an initial response within **7 days**. Once confirmed, a fix will be prioritized and released as soon as possible.

---

## 🛡️ Security Considerations

When using Advanced File Manager, please be aware of the following:

- **Destructive Operations**: Delete and bulk-move operations are **permanent**. Use the **Dry Run** mode to preview operations before executing them.
- **Hash Verification**: Always enable hash verification when moving or copying critical data to ensure file integrity.
- **Untrusted Input**: Do not run this tool on directories containing untrusted or unknown files without reviewing them first.
- **Permissions**: Run the application with the **minimum required permissions**. Avoid running as root/administrator unless absolutely necessary.
- **Log Files**: Log files stored in the `logs/` directory may contain file paths and metadata. Ensure this directory is not exposed publicly.

---

## 📋 Safe Usage Checklist

- [ ] Back up important data before performing bulk operations
- [ ] Use **Dry Run** mode to preview changes before applying them
- [ ] Verify the source and destination paths carefully before starting operations
- [ ] Review duplicate groups manually before bulk deletion
- [ ] Keep log retention configured to avoid accumulation of sensitive path data

---

*For general support or questions, please visit the [Issues](https://github.com/ofer-aha/Advance_File_Manager/issues) page.*

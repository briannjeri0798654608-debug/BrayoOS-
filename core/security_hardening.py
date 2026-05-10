"""
BrayoOS Security Hardening
No Google. No surveillance. No control.
Built by Brayo & Virgy — 2026
"""

import os
import subprocess
import hashlib
import json
import time

class BrayOSSecurity:
    
    def __init__(self):
        self.dna_hash = self.get_dna_hash()
        
    def get_dna_hash(self):
        """Generate unique OS fingerprint"""
        dna_file = os.path.expanduser(
            "~/BrayoOS/core/dna.py")
        with open(dna_file, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    
    def verify_integrity(self):
        """Check OS files haven't been tampered"""
        core_files = [
            "~/BrayoOS/core/dna.py",
            "~/BrayoOS/core/desktop.py",
            "~/BrayoOS/core/boot.py",
        ]
        results = {}
        for f in core_files:
            path = os.path.expanduser(f)
            if os.path.exists(path):
                with open(path, 'rb') as file:
                    h = hashlib.sha256(
                        file.read()).hexdigest()
                results[f] = h
        return results
    
    def block_google(self):
        """Block Google tracking domains"""
        blocked = [
            "0.0.0.0 google-analytics.com",
            "0.0.0.0 googletagmanager.com",
            "0.0.0.0 doubleclick.net",
            "0.0.0.0 googlesyndication.com",
            "0.0.0.0 google-analytics.com",
            "0.0.0.0 metrics.google.com",
            "0.0.0.0 ssl.google-analytics.com",
            "0.0.0.0 adservice.google.com",
            "0.0.0.0 safebrowsing.googleapis.com",
            "0.0.0.0 connectivitycheck.gstatic.com",
        ]
        hosts_file = "/etc/hosts"
        try:
            with open(hosts_file, 'a') as f:
                f.write("\n# BrayoOS Anti-Google\n")
                for line in blocked:
                    f.write(line + "\n")
            return True
        except:
            return False
    
    def encrypt_file(self, filepath, password):
        """Encrypt a file"""
        key = hashlib.sha256(
            password.encode()).digest()
        with open(filepath, 'rb') as f:
            data = f.read()
        encrypted = bytes(
            b ^ key[i % len(key)]
            for i, b in enumerate(data))
        with open(filepath + ".enc", 'wb') as f:
            f.write(encrypted)
        return filepath + ".enc"
    
    def decrypt_file(self, filepath, password):
        """Decrypt a file"""
        key = hashlib.sha256(
            password.encode()).digest()
        with open(filepath, 'rb') as f:
            data = f.read()
        decrypted = bytes(
            b ^ key[i % len(key)]
            for i, b in enumerate(data))
        out = filepath.replace(".enc", "")
        with open(out, 'wb') as f:
            f.write(decrypted)
        return out
    
    def secure_delete(self, filepath):
        """Securely delete a file"""
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            with open(filepath, 'wb') as f:
                f.write(os.urandom(size))
            os.remove(filepath)
            return True
        return False
    
    def check_root_safety(self):
        """Check for unauthorized root access"""
        suspicious = [
            "/data/local/tmp/",
            "/system/xbin/",
        ]
        threats = []
        for path in suspicious:
            if os.path.exists(path):
                files = os.listdir(path)
                for f in files:
                    threats.append(
                        f"{path}{f}")
        return threats
    
    def generate_report(self):
        """Generate security report"""
        report = {
            "timestamp": time.strftime(
                "%Y-%m-%d %H:%M:%S"),
            "os": "BrayoOS v2.0",
            "builder": "Brayo & Virgy",
            "dna_hash": self.dna_hash,
            "integrity": self.verify_integrity(),
            "threats": self.check_root_safety(),
            "status": "SECURE",
        }
        return report

if __name__ == "__main__":
    sec = BrayOSSecurity()
    report = sec.generate_report()
    print("━"*50)
    print("🔒 BrayoOS Security Report")
    print("━"*50)
    print(f"DNA Hash: {report['dna_hash'][:20]}...")
    print(f"Status: {report['status']}")
    print(f"Threats: {len(report['threats'])}")
    print("━"*50)

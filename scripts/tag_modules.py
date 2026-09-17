#!/usr/bin/env python3
"""Heuristically tag each quiz question with its most likely CEH module, based on keyword matching."""
import json
import re
from pathlib import Path

DATA = Path("/Users/amayafontagne/ceh13-training/data")

# Ordered lists of (keyword, weight) per module. Longer/more specific phrases get higher weight.
MODULE_KEYWORDS = {
    "mod01": [
        ("information security", 3), ("hacker class", 3), ("white hat", 3), ("black hat", 3),
        ("gray hat", 3), ("hacktivist", 3), ("cyber kill chain", 4), ("mitre att&ck", 4),
        ("diamond model", 4), ("script kiddie", 3), ("defense-in-depth", 3), ("defense in depth", 3),
        ("risk management", 3), ("threat intelligence", 3), ("ethical hack", 2), ("suicide hacker", 3),
        ("cyberterrorist", 3), ("state-sponsored", 3),
    ],
    "mod02": [
        ("footprint", 3), ("reconnaissance", 3), ("whois", 3), ("google dork", 4), ("google hack", 3),
        ("shodan", 3), ("theharvester", 4), ("sublist3r", 4), ("netcraft", 3), ("dns record", 2),
        ("zone transfer", 3), ("social media footprint", 4),
    ],
    "mod03": [
        ("scanning network", 3), ("port scan", 3), ("nmap", 3), ("hping", 3), ("syn scan", 4),
        ("xmas scan", 4), ("null scan", 4), ("fin scan", 4), ("idle scan", 4), ("zombie scan", 4),
        ("banner grabbing", 3), ("war driving", 2), ("three-way handshake", 3), ("ack scan", 4),
    ],
    "mod04": [
        ("enumeration", 4), ("netbios", 3), ("snmp enum", 3), ("ldap enum", 3), ("nfs enum", 3),
        ("smtp enum", 3), ("smb enum", 3), ("null session", 4), ("enum4linux", 4), ("rpcclient", 4),
        ("community string", 3),
    ],
    "mod05": [
        ("vulnerability assessment", 4), ("vulnerability scann", 4), ("cvss", 4), ("nessus", 3),
        ("nikto", 3), ("openvas", 3), ("qualys", 3), ("vulnerability analysis", 4), ("common vulnerabilities", 3),
    ],
    "mod06": [
        ("password crack", 3), ("privilege escalation", 4), ("keylogger", 3), ("rootkit", 3),
        ("steganography", 3), ("meterpreter", 3), ("mimikatz", 4), ("pass the hash", 4), ("pass-the-hash", 4),
        ("buffer overflow", 3), ("hashcat", 3), ("john the ripper", 4), ("rainbow table", 3),
        ("system hacking", 3), ("clear track", 2), ("covering track", 2),
    ],
    "mod07": [
        ("malware", 3), ("\\bvirus\\b", 2), ("\\bworm\\b", 2), ("trojan", 3), ("ransomware", 3),
        ("botnet", 2), ("adware", 3), ("spyware", 3), ("fileless malware", 4), ("malware analysis", 4),
        ("crypter", 3), ("packer", 2),
    ],
    "mod08": [
        ("sniffing", 3), ("arp poison", 4), ("arp spoof", 3), ("mac flooding", 4), ("dhcp starvation", 4),
        ("wireshark", 2), ("promiscuous mode", 3), ("macof", 4), ("switch port stealing", 3),
    ],
    "mod09": [
        ("social engineering", 4), ("phishing", 3), ("spear phishing", 4), ("vishing", 4), ("smishing", 4),
        ("pretexting", 4), ("tailgating", 4), ("dumpster diving", 4), ("whaling", 4), ("piggybacking", 3),
        ("shoulder surfing", 3),
    ],
    "mod10": [
        ("denial-of-service", 4), ("denial of service", 4), ("\\bdos attack\\b", 3), ("ddos", 3),
        ("syn flood", 4), ("ping of death", 4), ("smurf attack", 4), ("botnet.*flood", 2),
        ("teardrop", 3), ("amplification attack", 3),
    ],
    "mod11": [
        ("session hijack", 4), ("session id", 3), ("session fixation", 4), ("csrf", 2),
        ("cookie theft", 3), ("firesheep", 3), ("session sidejacking", 4),
    ],
    "mod12": [
        ("firewall", 3), ("intrusion detection", 3), ("intrusion prevention", 3), ("\\bids\\b", 2),
        ("\\bips\\b", 2), ("honeypot", 3), ("honeynet", 3), ("packet filtering", 3), ("snort", 3),
        ("evading ids", 4), ("firewalking", 4),
    ],
    "mod13": [
        ("web server", 3), ("apache", 2), ("iis\\b", 2), ("nginx", 2), ("directory traversal", 3),
        ("web server misconfiguration", 4), ("http response splitting", 3), ("web defacement", 3),
    ],
    "mod14": [
        ("web application", 3), ("owasp", 3), ("cross-site scripting", 4), ("\\bxss\\b", 3),
        ("parameter tampering", 4), ("cookie poisoning", 3), ("broken authentication", 3),
        ("ssrf", 3), ("command injection", 3), ("directory listing", 2), ("buffer overflow.*web", 2),
    ],
    "mod15": [
        ("sql injection", 4), ("union select", 4), ("blind sql", 4), ("sqlmap", 4), ("havij", 4),
        ("error-based sql", 4), ("in-band sql", 3), ("out-of-band sql", 3),
    ],
    "mod16": [
        ("wireless network", 3), ("\\bwep\\b", 3), ("\\bwpa", 3), ("wi-fi", 2), ("wifi", 2),
        ("bluetooth", 3), ("\\bssid\\b", 3), ("access point", 2), ("wardriving", 4), ("evil twin", 4),
        ("aircrack", 4), ("rogue ap", 4), ("bluejacking", 4), ("bluesnarfing", 4),
    ],
    "mod17": [
        ("mobile device", 3), ("\\bandroid\\b", 3), ("\\bios\\b", 2), ("\\bapk\\b", 3), ("jailbreak", 4),
        ("mobile device management", 4), ("\\bmdm\\b", 3), ("rooting", 3), ("mobile platform", 3),
    ],
    "mod18": [
        ("\\biot\\b", 4), ("iot device", 5), ("iot network", 5), ("internet of things", 4),
        ("\\bscada\\b", 4), ("\\bplc\\b", 3), ("modbus", 4), ("connected device", 3),
        ("firmware", 2), ("rfid", 3), ("zigbee", 3), ("operational technology", 3),
    ],
    "mod19": [
        ("cloud comput", 4), ("\\baws\\b", 2), ("azure", 2), ("\\bgcp\\b", 2), ("\\bsaas\\b", 3),
        ("\\bpaas\\b", 3), ("\\biaas\\b", 3), ("docker", 2), ("kubernetes", 3), ("s3 bucket", 4),
        ("cloud security", 3), ("multi-tenan", 3),
    ],
    "mod20": [
        ("cryptograph", 4), ("encryption", 2), ("\\baes\\b", 2), ("\\brsa\\b", 2), ("hashing", 2),
        ("\\bpki\\b", 3), ("digital signature", 3), ("public key", 2), ("private key", 2),
        ("\\bssl\\b", 2), ("\\btls\\b", 2), ("certificate authority", 3),
    ],
}

COMPILED = {
    mod: [(re.compile(kw, re.IGNORECASE), w) for kw, w in kws]
    for mod, kws in MODULE_KEYWORDS.items()
}


def classify(text):
    scores = {}
    for mod, patterns in COMPILED.items():
        score = sum(w for pat, w in patterns if pat.search(text))
        if score:
            scores[mod] = score
    if not scores:
        return None
    return max(scores, key=scores.get)


def main():
    questions = json.loads((DATA / "questions.json").read_text(encoding="utf-8"))
    counts = {}
    for q in questions:
        blob = q["question"] + " " + " ".join(q["options"]) + " " + q.get("explanation", "")
        mod = classify(blob)
        q["module"] = mod
        counts[mod] = counts.get(mod, 0) + 1

    (DATA / "questions.json").write_text(json.dumps(questions, indent=2, ensure_ascii=False), encoding="utf-8")

    for mod in sorted(counts, key=lambda m: (m is None, m)):
        label = mod or "(non classé)"
        print(f"{label}: {counts[mod]}")
    print(f"Total: {len(questions)}")


if __name__ == "__main__":
    main()

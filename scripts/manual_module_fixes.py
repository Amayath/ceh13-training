#!/usr/bin/env python3
"""Manual overrides for questions the heuristic classifier left unclassified (or got wrong).
Applied on top of the automatic tag_modules.py pass.
"""
import json
from pathlib import Path

DATA = Path("/Users/amayafontagne/ceh13-training/data")

OVERRIDES = {
    "Exam Set 2-3": "mod14",     # three-tier app architecture
    "Exam Set 2-19": "mod08",    # SMB creds in plaintext -> sniffing
    "Exam Set 2-31": "mod03",    # Unicornscan OS identification
    "Exam Set 2-41": "mod03",    # DHCP subnet / IP range calc
    "Exam Set 2-63": "mod05",    # vulnerability report to colleagues
    "Exam Set 2-74": "mod19",    # five-tier container architecture -> cloud
    "Exam Set 2-80": "mod06",    # Metasploit AV bypass
    "Exam Set 2-95": "mod04",    # SNMP remote device management
    "Exam Set 2-100": "mod14",   # API reduce complexity -> web app
    "Exam Set 2-105": "mod03",   # log analysis, port 22 SSH
    "Exam Set 3-4": "mod03",     # TCP segment fundamentals
    "Exam Set 3-17": "mod01",    # rules of engagement document
    "Exam Set 3-29": "mod02",    # Linux DNS resolve command
    "Exam Set 3-39": "mod06",    # counter-based authentication (OTP)
    "Exam Set 3-57": "mod01",    # backup / long-term storage policy
    "Exam Set 3-58": "mod02",    # Google search operators
    "Exam Set 3-60": "mod01",    # biometric system selection
    "Exam Set 3-65": "mod08",    # monitor employee internet traffic
    "Exam Set 3-66": "mod01",    # risk assessment method
    "Exam Set 3-70": "mod20",    # IPSec modes
    "Exam Set 3-77": "mod09",    # smishing text message
    "Exam Set 3-78": "mod01",    # bollards / physical security
    "Exam Set 3-79": "mod01",    # VPN security policy
    "Exam Set 3-90": "mod20",    # IPsec component (ESP)
    "Exam Set 3-100": "mod08",   # ARP operation
    "Exam Set 3-102": "mod01",   # biometric control on company territory
    "Exam Set 3-121": "mod06",   # CAS / single sign-on
    "Exam Set 4-1": "mod06",     # USB silent file copy tool
    "Exam Set 4-10": "mod06",    # hide file in Linux (dot prefix)
    "Exam Set 4-34": "mod07",    # multiple domains -> fast flux / malware infra
    "Exam Set 4-41": "mod16",    # 802.11 range table
    "Exam Set 4-59": "mod15",    # SQLi prevention via whitelist
    "Exam Set 4-76": "mod06",    # insider logging in irregular hours
    "Exam Set 4-96": "mod16",    # antenna frequency band
    "Practice Questions-42": "mod01",   # residual risk
    "Practice Questions-43": "mod01",   # incident handling preparation phase
    "Practice Questions-45": "mod01",   # black-box pentest
    "Practice Questions-73": "mod02",   # DNS port 53 blocked
    "Practice Questions-79": "mod05",   # fuzzing
    "Practice Questions-80": "mod02",   # Google site: operator
    "Practice Questions-81": "mod01",   # ALE cost of recovery
    "Practice Questions-95": "mod14",   # SOAP protocol
    "Practice Questions-98": "mod06",   # Computer Management Console Windows
    "Practice Questions-112": "mod01",  # ethics / human trafficking
    "Practice Questions-120": "mod04",  # NTP UDP port enumeration
    "CEH v13 Dump-2": "mod09",    # spoofed email / phishing
    "CEH v13 Dump-10": "mod04",   # SNMP remote management
    "CEH v13 Dump-17": "mod14",   # web services routing info (SOAP/WSDL)
    "CEH v13 Dump-26": "mod19",   # container technology deployment
    "CEH v13 Dump-31": "mod04",   # LDAP automated tool
    "CEH v13 Dump-34": "mod08",   # SPAN port unencrypted traffic
    "CEH v13 Dump-37": "mod03",   # OS discovery
    "CEH v13 Dump-44": "mod06",   # username found, password attempt
    "CEH v13 Dump-46": "mod14",   # web API user-defined
    "CEH v13 Dump-47": "mod02",   # Google related: operator
    "CEH v13 Dump-55": "mod06",   # pivoting to own machine
    "CEH v13 Dump-56": "mod06",   # Metasploit privilege escalation
    "CEH v13 Dump-74": "mod06",   # insider irregular login hours
    "CEH v13 Dump-79": "mod01",   # Sarbanes-Oxley Act
    "CEH v13 Dump-80": "mod19",   # cloud deployment / shared tenancy
    "CEH v13 Dump-86": "mod08",   # SPAN port unencrypted traffic (dup)
    "CEH v13 Dump-90": "mod04",   # LDAP port 389
    "CEH v13 Dump-95": "mod02",   # website traffic/geolocation analysis tool
    "CEH v13 Dump-97": "mod05",   # vulnerability management program
    "CEH v13 Dump-100": "mod07",  # multiple domains -> fast flux
    "CEH v13 Dump-103": "mod14",  # centralized web API
    "CEH v13 Dump-117": "mod04",  # SMTP valid user enumeration (VRFY)
    "CEH v13 Dump-119": "mod01",  # medical breach / HIPAA-style law
}


def main():
    path = DATA / "questions.json"
    questions = json.loads(path.read_text(encoding="utf-8"))
    applied = 0
    for q in questions:
        if q["id"] in OVERRIDES:
            q["module"] = OVERRIDES[q["id"]]
            applied += 1
    path.write_text(json.dumps(questions, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Applied {applied}/{len(OVERRIDES)} overrides")

    still_unclassified = [q["id"] for q in questions if not q["module"]]
    print(f"Still unclassified: {len(still_unclassified)}")
    if still_unclassified:
        print(still_unclassified)


if __name__ == "__main__":
    main()

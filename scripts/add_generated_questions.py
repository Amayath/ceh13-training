#!/usr/bin/env python3
"""Add supplementary quiz questions (grounded in the course notes, not from a real exam bank)
for the thinnest modules, clearly tagged with a distinct source so they're never confused
with the verified exam-dump questions.
"""
import json
from pathlib import Path

DATA = Path("/Users/amayafontagne/ceh13-training/data")
SOURCE = "Fiches CEHv13 (généré)"

NEW_QUESTIONS = [
    # ---- Module 17: Hacking Mobile Platforms ----
    {"module": "mod17", "question": "Sur quel port TCP l'ADB (Android Debug Bridge) écoute-t-il par défaut, exploité lors d'une 'Wireless ADB Exploitation' ?",
     "options": ["4444", "5555", "8080", "443"], "correctIndex": 1,
     "explanation": "Le port 5555 est le port ADB par défaut. Lorsqu'il est exposé sur le réseau, un attaquant peut s'y connecter à distance et prendre le contrôle du device."},
    {"module": "mod17", "question": "Quel vecteur d'attaque ADB-Toolkit consiste à connecter physiquement le device cible via USB pour en prendre le contrôle total ?",
     "options": ["Physical Access Attack", "Wireless ADB Exploitation", "APK Payload Injection", "Real-Time Log Hijacking"], "correctIndex": 0,
     "explanation": "La Physical Access Attack nécessite une connexion USB directe entre l'attaquant et le device, contrairement à l'exploitation Wi-Fi qui se fait à distance."},
    {"module": "mod17", "question": "Quelle commande Android permet de capturer les logs système en temps réel, exploitée pour voler des identifiants ou tokens de session (Real-Time Log Hijacking) ?",
     "options": ["logcat", "dumpsys", "adb shell top", "pm list packages"], "correctIndex": 0,
     "explanation": "logcat affiche les logs système Android en direct ; un attaquant peut l'utiliser pour intercepter des informations sensibles affichées dans les logs d'une application."},
    {"module": "mod17", "question": "Qu'est-ce que l'App Tampering dans le contexte de l'exploitation Android via ADB ?",
     "options": [
        "Désinstaller une application légitime et installer une version backdoorée à sa place",
        "Modifier la configuration réseau du device",
        "Changer le mot de passe de l'utilisateur",
        "Désactiver le pare-feu du device"],
     "correctIndex": 0,
     "explanation": "L'App Tampering consiste à retirer une app légitime pour la remplacer par une version modifiée contenant un backdoor, via l'accès ADB."},
    {"module": "mod17", "question": "CypherRAT et CraxsRAT sont des exemples de quel type d'outil malveillant Android ?",
     "options": ["Antivirus mobile", "RAT (Remote Access Trojan) distribué via APK piégé", "VPN gratuit", "Gestionnaire de mots de passe"], "correctIndex": 1,
     "explanation": "Ce sont des RAT Android : une fois l'APK piégé installé par la victime, l'attaquant obtient un accès distant complet au device (fichiers, applications, contrôle)."},
    {"module": "mod17", "question": "Quel outil en ligne permet d'analyser un fichier APK suspect via un scan multi-moteurs antivirus ?",
     "options": ["VirusTotal", "Shodan", "Aircrack-ng", "Metasploit"], "correctIndex": 0,
     "explanation": "VirusTotal permet de soumettre un APK et de le faire analyser par de nombreux moteurs antivirus simultanément (analyse statique)."},
    {"module": "mod17", "question": "Quelle plateforme collaborative est spécialisée dans l'analyse et la détection de malware Android ?",
     "options": ["Koodous", "Netcraft", "Shodan", "Censys"], "correctIndex": 0,
     "explanation": "Koodous est une plateforme communautaire dédiée à l'analyse de fichiers APK et à la détection de malware Android."},
    {"module": "mod17", "question": "Qu'est-ce que l'APK Payload Injection via ADB-Toolkit ?",
     "options": [
        "L'installation de fichiers APK malveillants sur le device cible",
        "Le vol du numéro IMEI du device",
        "La modification du GPS du device",
        "L'interception des appels téléphoniques"],
     "correctIndex": 0,
     "explanation": "L'APK Payload Injection consiste à installer, via ADB, un APK malveillant directement sur le device de la cible."},
    {"module": "mod17", "question": "À quoi sert un décompilateur d'APK (Android APK Decompiler) dans une analyse de sécurité mobile ?",
     "options": [
        "À examiner le code source d'une application pour une analyse statique",
        "À accélérer le chargement de l'application",
        "À chiffrer l'APK avant sa distribution",
        "À signer numériquement l'APK"],
     "correctIndex": 0,
     "explanation": "Décompiler un APK permet d'inspecter son code (permissions, logique, chaînes suspectes) sans l'exécuter — une analyse statique classique."},
    {"module": "mod17", "question": "Qu'est-ce que le Shell-Based Exploitation dans le contexte d'une attaque ADB sur Android ?",
     "options": [
        "Exécuter des commandes directement via le shell ADB sur le système Android",
        "Créer un nouveau compte utilisateur sur le device",
        "Installer une mise à jour système officielle",
        "Réinitialiser le device aux paramètres d'usine"],
     "correctIndex": 0,
     "explanation": "Le shell ADB (adb shell) donne un accès en ligne de commande au système Android, permettant d'exécuter des commandes arbitraires."},
    {"module": "mod17", "question": "Quel est l'objectif principal du 'Data Extraction' comme vecteur d'attaque ADB ?",
     "options": [
        "Extraire des fichiers, médias et données d'application sensibles du device cible",
        "Augmenter la vitesse de traitement du device",
        "Installer un nouvel OS sur le device",
        "Synchroniser le device avec un cloud légitime"],
     "correctIndex": 0,
     "explanation": "La Data Extraction vise à récupérer, via ADB, des données sensibles stockées sur le device (fichiers, données d'app, médias)."},

    # ---- Module 19: Cloud Computing ----
    {"module": "mod19", "question": "Quel modèle de service cloud fournit une infrastructure brute (machines virtuelles, stockage, réseau) sans plus ?",
     "options": ["SaaS", "PaaS", "IaaS", "FaaS"], "correctIndex": 2,
     "explanation": "IaaS (Infrastructure as a Service, ex : AWS EC2, Azure VMs) fournit les briques d'infrastructure de base, à charge du client de gérer l'OS et les applications."},
    {"module": "mod19", "question": "Quel modèle de service cloud correspond à un logiciel prêt à l'emploi comme Gmail ou Zoom ?",
     "options": ["IaaS", "PaaS", "SaaS", "FaaS"], "correctIndex": 2,
     "explanation": "SaaS (Software as a Service) désigne un logiciel complet fourni et géré par le prestataire, accessible directement via Internet."},
    {"module": "mod19", "question": "Qu'est-ce que le FaaS (Function as a Service) ?",
     "options": [
        "L'exécution serverless de fonctions à la demande, sans gestion de serveur par le développeur",
        "Un service de sauvegarde automatique de fichiers",
        "Un antivirus cloud pour terminaux",
        "Un service de nom de domaine"],
     "correctIndex": 0,
     "explanation": "Le FaaS (ex : AWS Lambda) exécute du code à la demande en réponse à des événements, sans que le développeur ait à gérer l'infrastructure serveur."},
    {"module": "mod19", "question": "Selon la classification OWASP Cloud-Native Application Security (CNAS-2023), quel est le risque cloud classé n°1 ?",
     "options": ["Denial of Service", "Cloud Provider Misconfiguration", "Poor Secret Management", "Supply Chain Vulnerabilities"], "correctIndex": 1,
     "explanation": "La mauvaise configuration du fournisseur cloud (stockage, IAM, réseau) est le risque n°1 : elle mène directement à des fuites ou compromissions de données."},
    {"module": "mod19", "question": "Qu'est-ce qu'un 'Misconfigured Cloud Storage' comme menace cloud courante ?",
     "options": [
        "Des buckets S3 publics ou des bases de données ouvertes exposant des données",
        "Un ralentissement du réseau cloud",
        "Une panne du fournisseur cloud",
        "Un dépassement de quota de stockage"],
     "correctIndex": 0,
     "explanation": "Des buckets de stockage (comme Amazon S3) mal configurés en accès public sont l'une des causes les plus fréquentes de fuites de données dans le cloud."},
    {"module": "mod19", "question": "À quoi sert principalement Kubernetes ?",
     "options": [
        "Orchestrer, déployer et faire évoluer (scaler) des conteneurs à grande échelle",
        "Chiffrer le trafic réseau entre serveurs",
        "Scanner les vulnérabilités d'un réseau",
        "Gérer les certificats SSL/TLS"],
     "correctIndex": 0,
     "explanation": "Kubernetes est un orchestrateur de conteneurs qui automatise le déploiement, la mise à l'échelle et la gestion d'applications conteneurisées (souvent Docker)."},
    {"module": "mod19", "question": "Quel outil sert spécifiquement à énumérer des buckets Amazon S3 mal configurés ou publiquement accessibles ?",
     "options": ["LazyS3", "Trivy", "Nikto", "Aircrack-ng"], "correctIndex": 0,
     "explanation": "LazyS3 est un outil de reconnaissance dédié à la découverte de buckets S3 exposés publiquement."},
    {"module": "mod19", "question": "Qu'est-ce qu'un Community Cloud ?",
     "options": [
        "Un cloud partagé entre plusieurs organisations ayant des objectifs communs",
        "Un cloud réservé à une seule organisation",
        "Un cloud gratuit accessible à tous sans restriction",
        "Un cloud utilisé uniquement pour l'archivage"],
     "correctIndex": 0,
     "explanation": "Le Community Cloud est partagé entre plusieurs organisations qui ont des besoins communs (ex : plusieurs hôpitaux partageant une infrastructure de santé sécurisée)."},
    {"module": "mod19", "question": "Quel outil est utilisé pour scanner les vulnérabilités des images de conteneurs ?",
     "options": ["Trivy", "LazyS3", "S3Scanner", "CyberChef"], "correctIndex": 0,
     "explanation": "Trivy scanne les images de conteneurs (et environnements cloud) à la recherche de vulnérabilités connues dans leurs dépendances et couches."},
    {"module": "mod19", "question": "Dans quel modèle de déploiement cloud l'infrastructure est-elle dédiée exclusivement à une seule organisation ?",
     "options": ["Public Cloud", "Private Cloud", "Community Cloud", "Hybrid Cloud"], "correctIndex": 1,
     "explanation": "Le Private Cloud est réservé à une seule organisation, sur site ou hébergé par un tiers, contrairement au Public Cloud partagé entre plusieurs clients."},

    # ---- Module 11: Session Hijacking ----
    {"module": "mod11", "question": "Comment définit-on le Session Hijacking ?",
     "options": [
        "Prendre le contrôle de la session active d'un utilisateur en volant ou prédisant son Session ID",
        "Installer un keylogger sur la machine de la victime",
        "Envoyer des emails de phishing en masse",
        "Saturer un serveur de requêtes pour le rendre indisponible"],
     "correctIndex": 0,
     "explanation": "Le session hijacking consiste à s'approprier une session déjà authentifiée d'un utilisateur légitime, généralement via le vol de son Session ID/token."},
    {"module": "mod11", "question": "Quelles sont, dans l'ordre, les 4 étapes du cycle de vie d'une attaque de session hijacking ?",
     "options": [
        "Target Identification → Session ID Acquisition → Session Takeover → Exploitation",
        "Reconnaissance → Weaponization → Delivery → Installation",
        "Scanning → Enumeration → Gaining Access → Clearing Tracks",
        "Discovery → Analysis → Cracking → Compromising"],
     "correctIndex": 0,
     "explanation": "Le cycle propre au session hijacking commence par identifier une session vulnérable, puis acquérir le Session ID, en prendre le contrôle, et enfin l'exploiter."},
    {"module": "mod11", "question": "Quel outil/incident de 2010 a popularisé le sidejacking de sessions sur des réseaux Wi-Fi non sécurisés ?",
     "options": ["Firesheep", "Metasploit", "Aircrack-ng", "BeEF"], "correctIndex": 0,
     "explanation": "Firesheep était une extension de navigateur qui permettait de détourner facilement des sessions HTTP non chiffrées sur un Wi-Fi public."},
    {"module": "mod11", "question": "Qu'est-ce que la Session Fixation ?",
     "options": [
        "Forcer la victime à utiliser un Session ID connu à l'avance par l'attaquant",
        "Chiffrer la session avec une clé fixe",
        "Bloquer toutes les nouvelles sessions sur un serveur",
        "Générer un Session ID totalement aléatoire à chaque requête"],
     "correctIndex": 0,
     "explanation": "Dans une session fixation, l'attaquant impose à la victime un Session ID qu'il connaît déjà, puis l'utilise une fois que la victime s'est authentifiée avec."},
    {"module": "mod11", "question": "Comment un attaquant peut-il extraire un Session ID (ex : JSESSIONID) capturé avec Wireshark sur du trafic HTTP non chiffré ?",
     "options": [
        "En faisant un « Follow TCP Stream » sur la requête POST de connexion",
        "En redémarrant le serveur cible",
        "En modifiant le fichier hosts de la victime",
        "En utilisant une attaque par force brute sur le mot de passe"],
     "correctIndex": 0,
     "explanation": "Le « Follow TCP Stream » de Wireshark permet de reconstituer l'échange complet et d'y repérer le cookie de session transmis en clair."},
    {"module": "mod11", "question": "À quoi sert le Burp Suite Sequencer dans le cadre d'une analyse de session hijacking ?",
     "options": [
        "À tester la prévisibilité (l'entropie) des Session IDs générés par une application",
        "À intercepter le trafic Wi-Fi",
        "À cracker des mots de passe hors ligne",
        "À scanner les ports ouverts d'un serveur"],
     "correctIndex": 0,
     "explanation": "Sequencer analyse un échantillon de tokens/Session IDs pour évaluer s'ils sont suffisamment aléatoires ou s'ils peuvent être prédits."},
    {"module": "mod11", "question": "Quelles mesures permettent le mieux de se protéger contre le session hijacking ?",
     "options": [
        "HTTPS partout, HSTS, régénération du Session ID après authentification, cookies Secure/HttpOnly",
        "Utiliser des mots de passe plus longs uniquement",
        "Désactiver le JavaScript côté client",
        "Changer le port du serveur web"],
     "correctIndex": 0,
     "explanation": "Le chiffrement du trafic (HTTPS/HSTS) empêche l'interception du cookie, et régénérer le Session ID + le protéger (Secure/HttpOnly) limite le risque de vol/réutilisation."},
    {"module": "mod11", "question": "Citez un outil couramment utilisé pour réaliser une attaque MITM en vue d'un session hijacking.",
     "options": ["Ettercap", "Nikto", "Havij", "John the Ripper"], "correctIndex": 0,
     "explanation": "Ettercap (comme Bettercap) permet de se positionner en Man-in-the-Middle sur un réseau local pour intercepter le trafic, dont les cookies de session."},
    {"module": "mod11", "question": "Pourquoi transmettre un cookie de session en HTTP (non chiffré) est-il particulièrement dangereux ?",
     "options": [
        "Le cookie peut être intercepté en clair par sniffing puis réutilisé par un attaquant",
        "Le cookie expire immédiatement",
        "Le serveur refuse automatiquement la connexion",
        "Cela ralentit uniquement la connexion"],
     "correctIndex": 0,
     "explanation": "Sans chiffrement, un cookie de session circule en clair sur le réseau et peut être capturé par n'importe quel outil de sniffing, puis réutilisé pour usurper la session."},
    {"module": "mod11", "question": "Quel outil de type Browser Exploitation Framework peut être utilisé pour détourner une session via le navigateur d'une victime ?",
     "options": ["BeEF", "Hydra", "SQLMap", "Nessus"], "correctIndex": 0,
     "explanation": "BeEF (Browser Exploitation Framework) permet de « hooker » le navigateur d'une victime et d'exécuter des actions, y compris liées à sa session active."},

    # ---- Module 13: Hacking Web Servers ----
    {"module": "mod13", "question": "Quel est le serveur web open-source le plus utilisé au monde ?",
     "options": ["Nginx", "Apache HTTP Server", "LiteSpeed", "Tomcat"], "correctIndex": 1,
     "explanation": "Apache HTTP Server reste, historiquement et en volume, le serveur web open-source le plus déployé."},
    {"module": "mod13", "question": "Quel serveur web est particulièrement réputé pour son usage en reverse proxy et load balancer léger ?",
     "options": ["Nginx", "IIS", "Apache", "Node.js"], "correctIndex": 0,
     "explanation": "Nginx est très utilisé comme reverse proxy et load balancer grâce à sa légèreté et ses performances élevées sous forte charge."},
    {"module": "mod13", "question": "Qu'est-ce que le Directory Traversal sur un serveur web ?",
     "options": [
        "Une mauvaise validation des entrées permettant d'accéder à des fichiers hors de la racine web",
        "Une attaque qui sature la bande passante du serveur",
        "Une technique de chiffrement des répertoires",
        "Un mécanisme d'authentification par répertoire"],
     "correctIndex": 0,
     "explanation": "Le directory traversal (ex : ../../../etc/passwd) exploite une mauvaise validation des chemins de fichiers pour sortir de la racine web autorisée."},
    {"module": "mod13", "question": "Que permet de découvrir le 'banner grabbing' sur un serveur web ?",
     "options": [
        "Le type et la version du serveur exposés dans les en-têtes HTTP",
        "Le mot de passe administrateur du serveur",
        "La liste des utilisateurs connectés",
        "Le contenu chiffré de la base de données"],
     "correctIndex": 0,
     "explanation": "Le banner grabbing récupère les informations de version affichées dans les réponses du serveur (ex : Apache/2.4.6), utiles pour cibler des exploits connus."},
    {"module": "mod13", "question": "Pourquoi laisser les méthodes HTTP PUT, DELETE ou TRACE activées sur un serveur web est-il risqué ?",
     "options": [
        "Elles peuvent permettre l'upload de fichiers malveillants ou faciliter le cross-site tracing",
        "Elles ralentissent uniquement les performances du serveur",
        "Elles sont incompatibles avec HTTPS",
        "Elles désactivent automatiquement le cache"],
     "correctIndex": 0,
     "explanation": "Des méthodes HTTP non nécessaires activées élargissent la surface d'attaque : PUT peut permettre l'upload de fichiers, TRACE peut faciliter certaines attaques XST."},
    {"module": "mod13", "question": "Quelle directive de configuration Apache permet de masquer la version du serveur exposée dans les en-têtes HTTP ?",
     "options": ["ServerTokens Prod", "DisableBanner On", "HideVersion True", "SecureHeader Off"], "correctIndex": 0,
     "explanation": "ServerTokens Prod réduit les informations de version renvoyées par Apache dans ses en-têtes de réponse HTTP."},
    {"module": "mod13", "question": "Quel outil de footprinting identifie les technologies (CMS, frameworks, serveur) utilisées par un site web cible ?",
     "options": ["WhatWeb", "Hydra", "John the Ripper", "Responder"], "correctIndex": 0,
     "explanation": "WhatWeb analyse un site web et identifie les technologies sous-jacentes (serveur, CMS, frameworks, bibliothèques JS, etc.)."},
    {"module": "mod13", "question": "Quel outil permet d'obtenir un shell distant sur un serveur Windows en exploitant le protocole WinRM ?",
     "options": ["Evil-WinRM", "Aircrack-ng", "Wireshark", "Nikto"], "correctIndex": 0,
     "explanation": "Evil-WinRM est un outil dédié à l'exploitation de Windows Remote Management pour obtenir un shell interactif distant."},
    {"module": "mod13", "question": "À quoi sert principalement l'outil CrackMapExec dans un test d'intrusion sur un serveur Windows/Active Directory ?",
     "options": [
        "Post-exploitation et attaques de type pass-the-hash sur des environnements Windows/AD",
        "Scanner uniquement les ports ouverts d'un serveur",
        "Générer des rapports PDF automatiques",
        "Chiffrer le trafic réseau"],
     "correctIndex": 0,
     "explanation": "CrackMapExec est utilisé pour tester des identifiants, se déplacer latéralement et effectuer du pass-the-hash dans des environnements Windows/Active Directory."},
    {"module": "mod13", "question": "Quel scanner open-source est spécifiquement dédié à la détection de vulnérabilités et de mauvaises configurations sur un serveur web ?",
     "options": ["Nikto", "Hashcat", "CeWL", "Responder"], "correctIndex": 0,
     "explanation": "Nikto est un scanner de vulnérabilités open-source axé serveur web, qui teste des milliers de fichiers/configurations potentiellement dangereux."},

    # ---- Module 18: IoT and OT Hacking (already 19, small top-up) ----
    {"module": "mod18", "question": "Quelles sont, dans l'ordre, les 4 couches de l'architecture IoT ?",
     "options": [
        "Perception → Network → Processing → Application",
        "Access → Core → Edge → Cloud",
        "Physical → Data Link → Network → Transport",
        "Sensor → Gateway → Firewall → Application"],
     "correctIndex": 0,
     "explanation": "L'architecture IoT classique s'articule en 4 couches : Perception (capteurs), Network (transmission), Processing (traitement cloud/edge), Application (services utilisateur)."},
    {"module": "mod18", "question": "Quel protocole de messagerie léger est le plus utilisé pour la communication entre objets connectés en IoT ?",
     "options": ["MQTT", "SMTP", "FTP", "SNMP"], "correctIndex": 0,
     "explanation": "MQTT (Message Queuing Telemetry Transport) est un protocole publish/subscribe très léger, largement adopté en IoT pour sa faible consommation de bande passante."},
    {"module": "mod18", "question": "Quelle est la vulnérabilité IoT classée n°1 dans l'OWASP IoT Top 10 ?",
     "options": [
        "Weak, Guessable, or Hardcoded Passwords",
        "Lack of Physical Hardening",
        "Insecure Default Settings",
        "Insufficient Privacy Protection"],
     "correctIndex": 0,
     "explanation": "Les identifiants faibles, devinables ou codés en dur dans le firmware restent la vulnérabilité IoT la plus critique et la plus exploitée."},
    {"module": "mod18", "question": "Qu'est-ce qu'un PLC (Programmable Logic Controller) dans un environnement OT ?",
     "options": [
        "Le « cerveau » du système industriel qui exécute la logique de contrôle en temps réel",
        "Un pare-feu dédié aux réseaux industriels",
        "Un capteur de température basique",
        "Un protocole de chiffrement pour SCADA"],
     "correctIndex": 0,
     "explanation": "Le PLC exécute la logique de contrôle des processus industriels en temps réel — c'est l'élément central des automatismes industriels."},
    {"module": "mod18", "question": "Quelle est la priorité principale en environnement OT, à la différence de l'IT où la confidentialité prime souvent ?",
     "options": ["La haute disponibilité (continuité du processus physique)", "Le chiffrement de bout en bout", "La rapidité des mises à jour logicielles", "L'anonymisation des données"], "correctIndex": 0,
     "explanation": "En OT, l'arrêt d'un processus physique (usine, réseau électrique...) peut avoir des conséquences graves : la disponibilité prime généralement sur la confidentialité."},
    {"module": "mod18", "question": "Citez deux protocoles couramment utilisés dans les environnements industriels/OT.",
     "options": ["MODBUS et DNP3", "HTTP et FTP", "SMTP et POP3", "RDP et VNC"], "correctIndex": 0,
     "explanation": "MODBUS (communication entre PLC) et DNP3 (automatisation de sous-stations) sont deux protocoles OT très répandus, souvent peu ou pas sécurisés par défaut."},
    {"module": "mod18", "question": "Quel moteur de recherche est spécialisé dans la découverte de devices connectés exposés sur Internet (webcams, panneaux SCADA, routeurs) ?",
     "options": ["Shodan", "Google", "Bing", "DuckDuckGo"], "correctIndex": 0,
     "explanation": "Shodan indexe les bannières et services de devices connectés directement accessibles depuis Internet, ce qui en fait un outil de choix pour la reconnaissance IoT/OT."},
    {"module": "mod18", "question": "À quoi sert un Industrial Gateway dans une architecture OT ?",
     "options": [
        "À convertir des protocoles OT en protocoles compatibles IT (ex : MODBUS vers MQTT)",
        "À remplacer physiquement un PLC défaillant",
        "À chiffrer automatiquement tout le trafic OT",
        "À alimenter électriquement les capteurs"],
     "correctIndex": 0,
     "explanation": "Les industrial gateways font le pont entre les protocoles industriels historiques (MODBUS, DNP3...) et les protocoles IT modernes, facilitant l'intégration cloud/IT."},

    # ---- Module 15: SQL Injection (top-up) ----
    {"module": "mod15", "question": "Que provoque le payload ' OR 1=1 -- inséré dans un champ vulnérable ?",
     "options": [
        "La condition WHERE de la requête devient toujours vraie",
        "La base de données est immédiatement supprimée",
        "Le serveur web redémarre",
        "Le mot de passe de l'admin est automatiquement affiché"],
     "correctIndex": 0,
     "explanation": "Ce classique payload transforme la condition en tautologie (toujours vraie), ce qui peut contourner une authentification ou faire retourner toutes les lignes d'une requête."},
    {"module": "mod15", "question": "Qu'est-ce qu'une injection SQL de type Union-Based ?",
     "options": [
        "Elle utilise UNION SELECT pour combiner le résultat original avec des données d'une autre table",
        "Elle chiffre la réponse de la base de données",
        "Elle nécessite un accès physique au serveur",
        "Elle fonctionne uniquement sur MongoDB"],
     "correctIndex": 0,
     "explanation": "L'injection Union-Based ajoute une clause UNION SELECT pour extraire des données d'autres tables (ex : identifiants) via les résultats affichés par l'application."},
    {"module": "mod15", "question": "Quelle est la différence principale entre une injection SQL Boolean-Based Blind et Time-Based Blind ?",
     "options": [
        "La première observe un changement de comportement de la page, la seconde mesure un délai de réponse provoqué",
        "La première nécessite un accès admin, pas la seconde",
        "La première ne fonctionne que sur Oracle, la seconde sur MySQL",
        "Il n'y a aucune différence, ce sont des synonymes"],
     "correctIndex": 0,
     "explanation": "Boolean-Based Blind déduit des informations via une réponse vraie/fausse observable. Time-Based Blind déduit des informations en mesurant un délai (ex : SLEEP(5))."},
    {"module": "mod15", "question": "À quoi sert le test ' ORDER BY N -- lors d'une exploitation SQL Injection ?",
     "options": [
        "À déterminer le nombre de colonnes d'une table avant une injection UNION",
        "À supprimer une colonne de la table",
        "À chiffrer les données de la colonne",
        "À créer un nouvel utilisateur administrateur"],
     "correctIndex": 0,
     "explanation": "En augmentant N jusqu'à obtenir une erreur, un attaquant détermine le nombre exact de colonnes, une étape préalable classique à une injection UNION SELECT."},
    {"module": "mod15", "question": "Quel outil GUI automatisé permet de détecter et exploiter une injection SQL avec bypass automatique de login admin ?",
     "options": ["Havij", "Wireshark", "Nikto", "Responder"], "correctIndex": 0,
     "explanation": "Havij est un outil graphique qui automatise la détection de SQLi, le dump de données, et propose un bypass de login basé sur des payloads connus."},
    {"module": "mod15", "question": "Que fait la commande sqlmap -u <url> --dbs --random-agent ?",
     "options": [
        "Teste l'URL pour une injection SQL, liste les bases de données, et utilise un user-agent aléatoire",
        "Chiffre automatiquement la base de données cible",
        "Crée un compte administrateur sur le serveur",
        "Scanne uniquement les ports ouverts du serveur"],
     "correctIndex": 0,
     "explanation": "--dbs demande l'énumération des bases de données, --random-agent tente d'éviter la détection en changeant le User-Agent à chaque requête."},
    {"module": "mod15", "question": "Quelle est la meilleure défense technique contre les injections SQL ?",
     "options": [
        "Les requêtes préparées/paramétrées, combinées à une validation stricte des entrées",
        "Changer régulièrement le mot de passe de la base de données",
        "Désactiver JavaScript côté client",
        "Utiliser uniquement des cookies HttpOnly"],
     "correctIndex": 0,
     "explanation": "Les requêtes préparées séparent le code SQL des données utilisateur, empêchant structurellement l'injection, contrairement à la simple validation côté client."},
]


def main():
    path = DATA / "questions.json"
    questions = json.loads(path.read_text(encoding="utf-8"))
    existing_ids = {q["id"] for q in questions}

    counters = {}
    added = 0
    for item in NEW_QUESTIONS:
        mod = item["module"]
        counters[mod] = counters.get(mod, 0) + 1
        qid = f"Generated-{mod}-{counters[mod]}"
        while qid in existing_ids:
            counters[mod] += 1
            qid = f"Generated-{mod}-{counters[mod]}"
        questions.append({
            "id": qid,
            "question": item["question"],
            "options": item["options"],
            "correctIndex": item["correctIndex"],
            "explanation": item["explanation"],
            "source": SOURCE,
            "module": mod,
        })
        existing_ids.add(qid)
        added += 1

    path.write_text(json.dumps(questions, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Added {added} questions. Total now: {len(questions)}")

    from collections import Counter
    c = Counter(q["module"] for q in questions)
    for k in sorted(c):
        print(k, c[k])


if __name__ == "__main__":
    main()

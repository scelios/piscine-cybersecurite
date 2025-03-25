# OTP Generator

Ce projet est un générateur de mots de passe à usage unique (OTP) basé sur l'algorithme TOTP (Time-Based One-Time Password). Il permet de générer des clés secrètes, de les chiffrer, et de produire des tokens OTP valides. Il inclut également la génération de QR codes pour faciliter l'intégration avec des applications OTP.

---

## Utilisation

### Afficher l'aide

Pour afficher l'aide et les options disponibles, exécutez :

```bash
python ft_otp.py -h
```

---

### Générer une clé secrète OTP

Pour générer une clé secrète OTP et la chiffrer, utilisez l'option `-g` ou `--generate` suivie du chemin d'un fichier texte contenant la clé secrète brute :

```bash
python ft_otp.py -g key.txt
```

**Exemple :**  
Si le fichier `key.txt` contient la clé brute `mysecretkey1234567890`, le programme chiffrera cette clé et la sauvegardera dans un fichier `key.hex`.

---

### Générer des tokens OTP

Pour générer des tokens OTP à partir d'une clé secrète chiffrée, utilisez l'option `-k` ou `--key` suivie du chemin du fichier `.hex` contenant la clé chiffrée :

```bash
python ft_otp.py -k key.hex
```

**Exemple :**  
Si le fichier `key.hex` contient une clé valide, le programme générera une liste de tokens OTP valides pour la période actuelle et affichera un QR code pour l'un des tokens.

---

### Interruption du programme

Vous pouvez interrompre le programme à tout moment en appuyant sur `Ctrl+C`.

---

## Exemple de sortie

### Génération de clé secrète

```bash
$ python ft_otp.py -g secret.txt
Encrypting the secret key
Secret key saved to key.hex
```

### Génération de tokens OTP

```bash
$ python ft_otp.py -k key.hex
Generating the OTP tokens
Valid tokens: ['123456', '654321', '789012', '345678', '901234']
QR code generated for token: 789012
```

Un QR code sera affiché dans une fenêtre graphique.

---

## Avertissements

- Assurez-vous que les fichiers d'entrée respectent les formats attendus :
  - `.txt` pour les clés brutes.
  - `.hex` pour les clés chiffrées.
- Les clés secrètes doivent avoir une **longueur minimale de 64 caractères** et être un **multiple de 4**.

---

## Comparaison avec `oathtool`

Vous pouvez comparer les tokens générés avec l'outil `oathtool` :

```bash
oathtool --base32 --totp $(cat key.hex)
```

---

## Lancement du Docker
```bash
docker compose up --build
docker exec -it otp bash
```

## Licence

Ce projet est sous licence MIT. Vous êtes libre de l'utiliser, de le modifier et de le distribuer.
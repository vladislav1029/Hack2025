# Key generation


Generating a private key.
```sh
openssl genrsa -out src\key\private_key.pem 2048
```
Generating a public key from a private one.
```sh
openssl rsa -in src\key\private_key.pem -pubout -out src\key\public_key.pem
```

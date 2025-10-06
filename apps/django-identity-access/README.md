
## Cryptography setup
```shell

# crytography
pip install -r requirements.txt
python -m pip show cryptography
python -c "import cryptography; print('cryptography ok')"

mkdir -p keys
cd keys
openssl genrsa -out local_private.pem 2048\nopenssl rsa -in local_private.pem -pubout -out local_public.pem
# Mention above .pem files in .env.local and .env.production files and also in .env.qa file
```
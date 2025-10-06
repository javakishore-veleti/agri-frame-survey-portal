
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

# Object Authorization_token from this - use access key's value as Authorization_token
 curl -X POST http://localhost:6080/api/admin/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'
  
curl -X GET http://localhost:6080/api/admin/v1/whoami/ \
  -H "Authorization: Bearer <Authorization_token>"

```
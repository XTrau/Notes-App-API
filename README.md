# Run

```
docker-compose up -d --build
```

postgres port: 5432  
backend port: 8000

# Stop

```
docker-compose down
```

## Create ssl keys for auth working**

```
mkdir certs 
cd certs
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -pubout -in private_key.pem -out public_key.pem
cd ..
```
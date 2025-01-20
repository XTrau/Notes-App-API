This is an API for a Notes App that allows users to create, manage, and organize their personal notes.
The API supports essential CRUD (Create, Read, Update, Delete) operations, enabling users to create new notes,
view existing ones, update their content, and delete them when no longer needed. It also includes features
like authentication, allowing users to securely access their notes with JWT-based authorization.
JWT (JSON Web Token) authorization is implemented with the token being stored in a cookie.

Technology stack:
**Python, FastAPI, Pydantic, SQLAlchemy, PyJWT**

## Create ssl keys for auth working

```
mkdir certs 
cd certs
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -pubout -in private_key.pem -out public_key.pem
cd ..
```

## Run Project

### Python

#### Windows

```
python -m venv venv
./venv/Scripts/activate
pip install -r ./requirements.txt
python ./src/main.py
```

#### Linux

```
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
python ./src/main.py
```

### Docker

```
docker-compose up -d --build
```

postgres port: 5432  
backend port: 8000

To stop Docker project:

```
docker-compose down
```

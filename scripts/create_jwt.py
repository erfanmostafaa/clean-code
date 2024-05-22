import jwt
import os
from dotenv import load_dotenv

load_dotenv()


encoded_jwt = jwt.encode({"sub": "erfan@gmail.com"}, os.environ.get("JWT_SECRET"), algorithm=os.environ.get("JWT_ALGORITHM"))
print(encoded_jwt)

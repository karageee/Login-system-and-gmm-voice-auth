from datetime import datetime, timedelta
import jwt
api_key = "144cc764-0878-4484-9a36-ada1128fb3ae"
secret_key = 'e91e518a-4400-4a33-8f36-eb9e5ccdb096'

def jwt_encode():
    token = jwt.encode({'app_id': secret_key, 'exp':datetime.utcnow() + timedelta(minutes=60)}, api_key)
    print(str(token.decode('UTF-8')))

jwt_encode()
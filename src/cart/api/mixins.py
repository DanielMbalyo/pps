import pickle

class TokenMixin(object):
    token = None
    def create_token(self, data_dict):
        if type(data_dict) == type(dict()):
            # token = str(data_dict).encode('base64', 'strict')
            token = pickle.dumps(data_dict).hex()
            self.token = token
            return token
        else:
            raise ValueError("Creating a token must be a Python dictionary.")

    def parse_token(self, token=None):
        if token is None:
            return {}
        try:
            token_dict = pickle.loads(bytes.fromhex(token))
            return token_dict
        except:
            raise ValueError("Creating a token must be a Python dictionary.")

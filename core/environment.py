
class Environment:
    SANDBOX = "https://api.sandbox.paypal.com"
    PRODUCTION = "https://api.paypal.com"

    def __init__(self, client_id, client_secret, base_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url


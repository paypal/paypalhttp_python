from core import *

env = Environment(client_id="AYSq3RDGsmBLJE-otTkBtM-jBRd1TCQwFf9RGfwddNXWz0uFU9ztymylOhRS",
            client_secret="EGnHDxD_qRPdaLdZz8iCr8N7_MzF-YHPTkjs6NKYQvQSBngp4PTTVWkPZRbL",
            base_url=Environment.SANDBOX)

client = PayPalHttpClient(environment=env)

invoice = {
    "merchant_info": {
        "email": "jaypatel512-facilitator@hotmail.com"
    }
}

invoice_request = InvoiceRequestBuilder.create(invoice)

try:
    response = client.execute(invoice_request)
    print response.status_code
    print response.headers
    print response.result
except IOError as e:
    print e


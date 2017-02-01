# PayPal SDK 2.0.0-alpha

This is a preview of how PayPal SDKs will look in the next major version. We've simplified the interface to only provide
simple model objects and blueprints for HTTP calls. This repo currently only contains functionality for working with invoices
and invoice templates to serve as an example of the API going forward.

### Creating an Invoice

```python
from core import *
from sdk import *

env = Environment(client_id="AYSq3RDGsmBLJE-otTkBtM-jBRd1TCQwFf9RGfwddNXWz0uFU9ztymylOhRS",
            client_secret="EGnHDxD_qRPdaLdZz8iCr8N7_MzF-YHPTkjs6NKYQvQSBngp4PTTVWkPZRbL",
            base_url=Environment.SANDBOX)

client = PayPalHttpClient(environment=env)

invoice = {
    "merchant_info": {
        "email": "jaypatel512-facilitator@hotmail.com"
    }
}

invoice_request = InvoicesRequestBuilder.create(invoice)

try:
    response = client.execute(invoice_request)
    print response.status_code
    print response.headers
    print response.result
except IOError as e:
    print e

```

To try this out, clone this repo and either create your own samples directly in the `sample` module, or copy the code into your
project, to see how it might affect your existing integration.

Please feel free to create an issue in this repo with any feedback, questions, or concerns you have.

*NOTE*: This API is still in alpha, is subject to change, and should not be used in production.

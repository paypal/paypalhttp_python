import requests


class InvoiceRequestBuilder:

    @staticmethod
    def create(invoice):
        return requests.Request(method='POST', url="/v1/invoicing/invoices", json=invoice)

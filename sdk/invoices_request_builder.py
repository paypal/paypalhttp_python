# This class was generated on Wed, 01 Feb 2017 15:39:21 PST by version 0.01 of Braintree SDK Generator
# invoices_request_builder.py
# DO NOT EDIT
# @service invoices
# @body {"Name":"cancel","ReturnType":{"Name":"void","IsArray":false},"Parameters":[{"Name":"invoice_id","ArgumentType":{"Name":"string","IsArray":false},"Location":"path"}],"RequestType":{"Name":"Cancel Notification","ArgumentType":{"Name":"cancel_notification","IsArray":false},"Location":""},"Visibility":"EXTERNAL","HttpMethod":"POST","Path":"v1/invoicing/invoices/{invoice_id}/cancel","OauthScope":"https://uri.paypal.com/services/invoicing"}
# @body {"Name":"create","ReturnType":{"Name":"invoice","IsArray":false},"Parameters":[],"RequestType":{"Name":"Invoice","ArgumentType":{"Name":"invoice","IsArray":false},"Location":""},"Visibility":"EXTERNAL","HttpMethod":"POST","Path":"v1/invoicing/invoices","OauthScope":"https://uri.paypal.com/services/invoicing"}
# @body {"Name":"delete","ReturnType":{"Name":"void","IsArray":false},"Parameters":[{"Name":"invoice_id","ArgumentType":{"Name":"string","IsArray":false},"Location":"path"}],"RequestType":null,"Visibility":"EXTERNAL","HttpMethod":"DELETE","Path":"v1/invoicing/invoices/{invoice_id}","OauthScope":"https://uri.paypal.com/services/invoicing"}
# @body {"Name":"delete_external_payment","ReturnType":{"Name":"void","IsArray":false},"Parameters":[{"Name":"invoice_id","ArgumentType":{"Name":"string","IsArray":false},"Location":"path"},{"Name":"transaction_id","ArgumentType":{"Name":"string","IsArray":false},"Location":"path"}],"RequestType":null,"Visibility":"EXTERNAL","HttpMethod":"DELETE","Path":"v1/invoicing/invoices/{invoice_id}/payment-records/{transaction_id}","OauthScope":"https://uri.paypal.com/services/invoicing"}
# @body {"Name":"delete_external_refund","ReturnType":{"Name":"void","IsArray":false},"Parameters":[{"Name":"invoice_id","ArgumentType":{"Name":"string","IsArray":false},"Location":"path"},{"Name":"transaction_id","ArgumentType":{"Name":"string","IsArray":false},"Location":"path"}],"RequestType":null,"Visibility":"EXTERNAL","HttpMethod":"DELETE","Path":"v1/invoicing/invoices/{invoice_id}/refund-records/{transaction_id}","OauthScope":"https://uri.paypal.com/services/invoicing"}
# @body {"Name":"generate_number","ReturnType":{"Name":"void","IsArray":false},"Parameters":[],"RequestType":null,"Visibility":"EXTERNAL","HttpMethod":"POST","Path":"v1/invoicing/invoices/next-invoice-number","OauthScope":"https://uri.paypal.com/services/invoicing"}
# @body {"Name":"get","ReturnType":{"Name":"invoice","IsArray":false},"Parameters":[{"Name":"invoice_id","ArgumentType":{"Name":"string","IsArray":false},"Location":"path"}],"RequestType":null,"Visibility":"EXTERNAL","HttpMethod":"GET","Path":"v1/invoicing/invoices/{invoice_id}","OauthScope":"https://uri.paypal.com/services/invoicing"}
# @body {"Name":"get_all","ReturnType":{"Name":"invoices","IsArray":false},"Parameters":[{"Name":"page","ArgumentType":{"Name":"integer","IsArray":false},"Location":"query"},{"Name":"page_size","ArgumentType":{"Name":"integer","IsArray":false},"Location":"query"},{"Name":"total_count_required","ArgumentType":{"Name":"boolean","IsArray":false},"Location":"query"}],"RequestType":null,"Visibility":"EXTERNAL","HttpMethod":"GET","Path":"v1/invoicing/invoices/","OauthScope":"https://uri.paypal.com/services/invoicing"}
# @body {"Name":"qr_code","ReturnType":{"Name":"void","IsArray":false},"Parameters":[{"Name":"action","ArgumentType":{"Name":"string","IsArray":false},"Location":"query"},{"Name":"height","ArgumentType":{"Name":"integer","IsArray":false},"Location":"query"},{"Name":"invoice_id","ArgumentType":{"Name":"string","IsArray":false},"Location":"path"},{"Name":"width","ArgumentType":{"Name":"integer","IsArray":false},"Location":"query"}],"RequestType":null,"Visibility":"EXTERNAL","HttpMethod":"GET","Path":"v1/invoicing/invoices/{invoice_id}/qr-code","OauthScope":"https://uri.paypal.com/services/invoicing"}
# @body {"Name":"record_payment","ReturnType":{"Name":"void","IsArray":false},"Parameters":[{"Name":"invoice_id","ArgumentType":{"Name":"string","IsArray":false},"Location":"path"}],"RequestType":{"Name":"Payment Detail","ArgumentType":{"Name":"payment-detail","IsArray":false},"Location":""},"Visibility":"EXTERNAL","HttpMethod":"POST","Path":"v1/invoicing/invoices/{invoice_id}/record-payment","OauthScope":"https://uri.paypal.com/services/invoicing"}
# @body {"Name":"record_refund","ReturnType":{"Name":"void","IsArray":false},"Parameters":[{"Name":"invoice_id","ArgumentType":{"Name":"string","IsArray":false},"Location":"path"}],"RequestType":{"Name":"Refund Detail","ArgumentType":{"Name":"refund-detail","IsArray":false},"Location":""},"Visibility":"EXTERNAL","HttpMethod":"POST","Path":"v1/invoicing/invoices/{invoice_id}/record-refund","OauthScope":"https://uri.paypal.com/services/invoicing"}
# @body {"Name":"remind","ReturnType":{"Name":"void","IsArray":false},"Parameters":[{"Name":"invoice_id","ArgumentType":{"Name":"string","IsArray":false},"Location":"path"}],"RequestType":{"Name":"Notification","ArgumentType":{"Name":"notification","IsArray":false},"Location":""},"Visibility":"EXTERNAL","HttpMethod":"POST","Path":"v1/invoicing/invoices/{invoice_id}/remind","OauthScope":"https://uri.paypal.com/services/invoicing"}
# @body {"Name":"search","ReturnType":{"Name":"invoices","IsArray":false},"Parameters":[],"RequestType":{"Name":"Search","ArgumentType":{"Name":"search","IsArray":false},"Location":""},"Visibility":"EXTERNAL","HttpMethod":"POST","Path":"v1/invoicing/search","OauthScope":"https://uri.paypal.com/services/invoicing"}
# @body {"Name":"send","ReturnType":{"Name":"void","IsArray":false},"Parameters":[{"Name":"invoice_id","ArgumentType":{"Name":"string","IsArray":false},"Location":"path"},{"Name":"notify_merchant","ArgumentType":{"Name":"boolean","IsArray":false},"Location":"query"}],"RequestType":null,"Visibility":"EXTERNAL","HttpMethod":"POST","Path":"v1/invoicing/invoices/{invoice_id}/send","OauthScope":"https://uri.paypal.com/services/invoicing"}
# @body {"Name":"update","ReturnType":{"Name":"invoice","IsArray":false},"Parameters":[{"Name":"invoice_id","ArgumentType":{"Name":"string","IsArray":false},"Location":"path"},{"Name":"notify_merchant","ArgumentType":{"Name":"boolean","IsArray":false},"Location":"query"}],"RequestType":{"Name":"Invoice","ArgumentType":{"Name":"invoice","IsArray":false},"Location":""},"Visibility":"EXTERNAL","HttpMethod":"PUT","Path":"v1/invoicing/invoices/{invoice_id}","OauthScope":"https://uri.paypal.com/services/invoicing"}

import requests

class InvoicesRequestBuilder:

    @staticmethod
    def cancel(cancel_notification, invoice_id):
        """
        Cancels a sent invoice, by ID, and, optionally, sends a notification about the cancellation to the payer, merchant, and Cc: emails.
        """
        url = "/v1/invoicing/invoices/{invoice_id}/cancel?"
        url = url.replace("{invoice_id}", str(invoice_id))
        request = requests.Request(method="POST", url=url)
        request.json = cancel_notification
        return request

    @staticmethod
    def create(invoice):
        """
        Creates a draft invoice. You can optionally create an invoice [template](/docs/api/invoicing/#templates). Then, when you create an invoice from a template, the invoice is populated with the predefined data that the source template contains. To move the invoice from a draft to payable state, you must [send the invoice](/docs/api/invoicing/#invoices_send). In the JSON request body, include invoice details including merchant information. The `invoice` object must include an `items` array.<blockquote><strong>Note:</strong> The merchant specified in an invoice must have a PayPal account in good standing.</blockquote>
        """
        url = "/v1/invoicing/invoices?"
        request = requests.Request(method="POST", url=url)
        request.json = invoice
        return request

    @staticmethod
    def delete(invoice_id):
        """
        Deletes a draft invoice, by ID. Note that this call works for invoices in the draft state only. For invoices that have already been sent, you can [cancel the invoice](/docs/api/invoicing/#invoices_cancel). After you delete a draft invoice, you can no longer use it or show its details. However, you can reuse its invoice number.
        """
        url = "/v1/invoicing/invoices/{invoice_id}?"
        url = url.replace("{invoice_id}", str(invoice_id))
        request = requests.Request(method="DELETE", url=url)
        return request

    @staticmethod
    def delete_external_payment(invoice_id, transaction_id):
        """
        Deletes an external payment, by invoice ID and transaction ID.
        """
        url = "/v1/invoicing/invoices/{invoice_id}/payment-records/{transaction_id}?"
        url = url.replace("{invoice_id}", str(invoice_id))
        url = url.replace("{transaction_id}", str(transaction_id))
        request = requests.Request(method="DELETE", url=url)
        return request

    @staticmethod
    def delete_external_refund(invoice_id, transaction_id):
        """
        Deletes an external refund, by invoice ID and transaction ID.
        """
        url = "/v1/invoicing/invoices/{invoice_id}/refund-records/{transaction_id}?"
        url = url.replace("{invoice_id}", str(invoice_id))
        url = url.replace("{transaction_id}", str(transaction_id))
        request = requests.Request(method="DELETE", url=url)
        return request

    @staticmethod
    def generate_number():
        """
        Generates the next invoice number that is available to the user.
        """
        url = "/v1/invoicing/invoices/next-invoice-number?"
        request = requests.Request(method="POST", url=url)
        return request

    @staticmethod
    def get(invoice_id):
        """
        Shows details for a specified invoice, by ID.
        """
        url = "/v1/invoicing/invoices/{invoice_id}?"
        url = url.replace("{invoice_id}", str(invoice_id))
        request = requests.Request(method="GET", url=url)
        return request

    @staticmethod
    def get_all(page, page_size, total_count_required):
        """
        Lists merchant invoices. Optionally, you can specify one or more query parameters to filter the response.
        """
        url = "/v1/invoicing/invoices/?"
        url += "page=" + str(page) + "&"
        url += "page_size=" + str(page_size) + "&"
        url += "total_count_required=" + str(total_count_required) + "&"
        request = requests.Request(method="GET", url=url)
        return request

    @staticmethod
    def qr_code(action, height, invoice_id, width):
        """
        Generates a QR code for an invoice, by ID.<br/><br/>The QR code is a PNG image in [Base64-encoded](https://www.base64encode.org/) format that corresponds to the invoice ID. You can generate a QR code for an invoice and add it to a paper or PDF invoice. When a customer uses their mobile device to scan the QR code, he or she is redirected to the PayPal mobile payment flow where he or she can pay online with PayPal or a credit card.<br/><br/>Before you get a QR code, you must:<ol><li><p>[Create an invoice](#invoices_create). Specify `qrinvoice@paypal.com` as the recipient email address in the `billing_info` object. Use a customer email address only if you want to email the invoice.</p></li><li><p>[Send an invoice](#invoices_send) to move the invoice from a draft to payable state. If you specify `qrinvoice@paypal.com` as the recipient email address, the invoice is not emailed.</p></li></ol>
        """
        url = "/v1/invoicing/invoices/{invoice_id}/qr-code?"
        url = url.replace("{invoice_id}", str(invoice_id))
        url += "action=" + str(action) + "&"
        url += "height=" + str(height) + "&"
        url += "width=" + str(width) + "&"
        request = requests.Request(method="GET", url=url)
        return request

    @staticmethod
    def record_payment(payment_detail, invoice_id):
        """
        Marks the status of a specified invoice, by ID, as paid. Include a payment detail object that defines the payment method and other details in the JSON request body.
        """
        url = "/v1/invoicing/invoices/{invoice_id}/record-payment?"
        url = url.replace("{invoice_id}", str(invoice_id))
        request = requests.Request(method="POST", url=url)
        request.json = payment_detail
        return request

    @staticmethod
    def record_refund(refund_detail, invoice_id):
        """
        Marks the status of an invoice, by ID, as refunded. In the JSON request body, include a payment detail object that defines the payment method and other details.
        """
        url = "/v1/invoicing/invoices/{invoice_id}/record-refund?"
        url = url.replace("{invoice_id}", str(invoice_id))
        request = requests.Request(method="POST", url=url)
        request.json = refund_detail
        return request

    @staticmethod
    def remind(notification, invoice_id):
        """
        Sends a reminder about an invoice, by ID, to a customer. In the JSON request body, include a `notification` object that defines the subject of the reminder and other details.
        """
        url = "/v1/invoicing/invoices/{invoice_id}/remind?"
        url = url.replace("{invoice_id}", str(invoice_id))
        request = requests.Request(method="POST", url=url)
        request.json = notification
        return request

    @staticmethod
    def search(search):
        """
        Lists invoices that match search criteria. In the JSON request body, include a `search` object that specifies the search criteria.
        """
        url = "/v1/invoicing/search?"
        request = requests.Request(method="POST", url=url)
        request.json = search
        return request

    @staticmethod
    def send(invoice_id, notify_merchant):
        """
        Sends an invoice, by ID, to a customer.<blockquote><strong>Note:</strong> After you send an invoice, you cannot resend it.</blockquote><br/>Optionally, set the `notify_merchant` query parameter to also send the merchant an invoice update notification. Default is `true`.
        """
        url = "/v1/invoicing/invoices/{invoice_id}/send?"
        url = url.replace("{invoice_id}", str(invoice_id))
        url += "notify_merchant=" + str(notify_merchant) + "&"
        request = requests.Request(method="POST", url=url)
        return request

    @staticmethod
    def update(invoice, invoice_id, notify_merchant):
        """
        Fully updates an invoice, by ID. In the JSON request body, include a complete `invoice` object. This call does not support partial updates.
        """
        url = "/v1/invoicing/invoices/{invoice_id}?"
        url = url.replace("{invoice_id}", str(invoice_id))
        url += "notify_merchant=" + str(notify_merchant) + "&"
        request = requests.Request(method="PUT", url=url)
        request.json = invoice
        return request


# DO NOT EDIT

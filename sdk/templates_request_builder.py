# This class was generated on Wed, 01 Feb 2017 15:39:21 PST by version 0.01 of Braintree SDK Generator
# templates_request_builder.py
# DO NOT EDIT
# @service templates
# @body {"Name":"create","ReturnType":{"Name":"template","IsArray":false},"Parameters":[],"RequestType":{"Name":"Template","ArgumentType":{"Name":"template","IsArray":false},"Location":""},"Visibility":"EXTERNAL","HttpMethod":"POST","Path":"v1/invoicing/templates","OauthScope":"https://uri.paypal.com/services/invoicing"}
# @body {"Name":"delete","ReturnType":{"Name":"void","IsArray":false},"Parameters":[{"Name":"template_id","ArgumentType":{"Name":"string","IsArray":false},"Location":"path"}],"RequestType":null,"Visibility":"EXTERNAL","HttpMethod":"DELETE","Path":"v1/invoicing/templates/{template_id}","OauthScope":"https://uri.paypal.com/services/invoicing"}
# @body {"Name":"get","ReturnType":{"Name":"template","IsArray":false},"Parameters":[{"Name":"template_id","ArgumentType":{"Name":"string","IsArray":false},"Location":"path"}],"RequestType":null,"Visibility":"EXTERNAL","HttpMethod":"GET","Path":"v1/invoicing/templates/{template_id}","OauthScope":"https://uri.paypal.com/services/invoicing"}
# @body {"Name":"get_all","ReturnType":{"Name":"templates","IsArray":false},"Parameters":[{"Name":"fields","ArgumentType":{"Name":"string","IsArray":false},"Location":"query"}],"RequestType":null,"Visibility":"EXTERNAL","HttpMethod":"GET","Path":"v1/invoicing/templates/","OauthScope":"https://uri.paypal.com/services/invoicing"}
# @body {"Name":"update","ReturnType":{"Name":"template","IsArray":false},"Parameters":[{"Name":"template_id","ArgumentType":{"Name":"string","IsArray":false},"Location":"path"}],"RequestType":{"Name":"Template","ArgumentType":{"Name":"template","IsArray":false},"Location":""},"Visibility":"EXTERNAL","HttpMethod":"PUT","Path":"v1/invoicing/templates/{template_id}","OauthScope":"https://uri.paypal.com/services/invoicing"}

import requests

class TemplatesRequestBuilder:

    @staticmethod
    def create(template):
        """
        Creates a template.
        """
        url = "/v1/invoicing/templates?"
        request = requests.Request(method="POST", url=url)
        request.json = template
        return request

    @staticmethod
    def delete(template_id):
        """
        Deletes a template, by ID.
        """
        url = "/v1/invoicing/templates/{template_id}?"
        url = url.replace("{template_id}", str(template_id))
        request = requests.Request(method="DELETE", url=url)
        return request

    @staticmethod
    def get(template_id):
        """
        Shows details for a template, by ID.
        """
        url = "/v1/invoicing/templates/{template_id}?"
        url = url.replace("{template_id}", str(template_id))
        request = requests.Request(method="GET", url=url)
        return request

    @staticmethod
    def get_all(fields):
        """
        Lists all merchant-created templates. The list shows the emails, addresses, and phone numbers from the merchant profile.
        """
        url = "/v1/invoicing/templates/?"
        url += "fields=" + str(fields) + "&"
        request = requests.Request(method="GET", url=url)
        return request

    @staticmethod
    def update(template, template_id):
        """
        Updates a template, by ID. In the JSON request body, pass a complete `template` object. The update method does not support partial updates.
        """
        url = "/v1/invoicing/templates/{template_id}?"
        url = url.replace("{template_id}", str(template_id))
        request = requests.Request(method="PUT", url=url)
        request.json = template
        return request


# DO NOT EDIT

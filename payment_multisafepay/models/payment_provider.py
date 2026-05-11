from odoo import api, fields, models


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    code = fields.Selection(
        selection_add=[('multisafepay', "MultiSafepay")], ondelete={'multisafepay': 'set default'}
    )
    multisafepay_api_key = fields.Char(
        string="MultiSafepay API Key",
        required_if_provider='mutisafepay',
        copy=False,
    )


    def _build_request_url(self, endpoint, **kwargs):
        """Override of `payment` to build the request URL."""
        if self.code != 'multisafepay':
            return super()._build_request_url(endpoint, **kwargs)
        url = 'https://testapi.multisafepay.com/v1'
        clean_endpoint = endpoint.strip('/')
        return f'{url}/{clean_endpoint}?api_key={self.multisafepay_api_key}'

    def _build_request_headers(self, *args, **kwargs):
        """Override of `payment` to build the request headers."""
        if self.code != 'multisafepay':
            return super()._build_request_headers(*args, **kwargs)
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

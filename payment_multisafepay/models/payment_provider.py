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
    multisafepay_security_code = fields.Char(
        string="MultiSafepay Secret Code",
        required_if_provider='mutisafepay',
        copy=False,
    )
    multisafepay_website_id = fields.Char(
        string="Website ID",
        required_if_provider='mutisafepay',
        copy=False,
    )
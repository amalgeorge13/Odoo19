from odoo import models,api,fields
from odoo.addons.payment import utils as payment_utils
from odoo.tools import mute_logger, urls
from odoo.exceptions import ValidationError




class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):

        """ Override of payment to return MultisafePay-specific rendering values.

                Note: self.ensure_one() from `_get_processing_values`

                :param dict processing_values: The generic and specific processing values of the transaction
                :return: The dict of provider-specific rendering values
                :rtype: dict
                """
        if self.provider_code != 'multisafepay':
            return super()._get_specific_rendering_values(processing_values)
        payload = self._multisafepay_prepare_payment_request_payload()
        try:
            payment_data = self._send_api_request('POST', '/json/orders', json=payload)
        except ValidationError as error:
            self._set_error(str(error))
            return {}
        order_data= payment_data.get('data',payment_data)
        self.provider_reference = payment_data.get('order_id',self.reference)
        payment_url=order_data.get('payment_url')
        return {'api_url': payment_url, 'url_params': {}}


    def _multisafepay_prepare_payment_request_payload(self):
        """ Create the payload for the payment request based on the transaction values.

        :return: The request payload
        :rtype: dict
        """

        base_url = self.provider_id.get_base_url()
        _return_url = '/payment/multisafepay/return'
        _webhook_url = '/payment/multisafepay/webhook'
        redirect_url = urls.urljoin(base_url, _return_url)
        webhook_url = urls.urljoin(base_url, _webhook_url)


        payload = {
            'type': 'redirect',
            'order_id': self.reference,
            'amount': int(self.amount * 100),
            'currency': self.currency_id.name,
            "payment_options": {
                "notification_method": "POST",
                "close_window": False,
                'redirect_url':redirect_url,
                'notification_url': webhook_url
            },
            "customer": {
                "locale": "en_US",
                "disable_send_email": False
            },
            "checkout_options": {"validate_cart": False},
            "days_active": 30,
            "seconds_active": 2592000,
            'description': self.reference,
        }

        return payload
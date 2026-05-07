from odoo import models,api,fields
from odoo.addons.payment import utils as payment_utils
# from odoo.custom_addons.payment_multisafepay import utils as multisafepay_utils
#
from odoo.exceptions import ValidationError


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'


    def _get_specific_processing_values(self, processing_values):
        """ Override of `payment` to return the Paypal-specific processing values.

        Note: self.ensure_one() from `_get_processing_values`

        :param dict processing_values: The generic and specific processing values of the
                                       transaction.
        :return: The dict of provider-specific processing values
        :rtype: dict
        """
        if self.provider_code != 'multisafepay':
            return super()._get_specific_processing_values(processing_values)
        print("MultiSafePay Payment Transaction")
        payload = self._multisafepay_prepare_order_payload()
        print(payload)

        idempotency_key = payment_utils.generate_idempotency_key(
            self, scope='payment_request_order'
        )

        try:
            order_data = self._send_api_request(
                'POST', '/shop/payment', json=payload, idempotency_key=idempotency_key
            )
        except ValidationError as e:
            self._set_error(str(e))
            return {}

        return {'order_id': order_data['id']}
    #
    def _multisafepay_prepare_order_payload(self):
        """ Prepare the payload for the Paypal create order request.

        :return: The requested payload to create a Paypal order.
        :rtype: dict
        """
        partner_first_name, partner_last_name = payment_utils.split_partner_name(self.partner_name)


        # See https://developer.paypal.com/docs/api/orders/v2/#orders_create!ct=application/json
        print(self.amount)
        payload = {
            'type': 'redirect',
            'order_id': self.reference,
            'amount': self.amount,
            'currency': self.currency_id,
            "payment_options": {
                "notification_method": "POST",
                "close_window":False,
                # 'redirect_url': '',
                # 'notification_url': ''
            },
            'customer': {
                "locale": "en_US",
                "disable_send_email":False,
            },
            "checkout_options": {
            "days_active":30 ,
            "seconds_active": 2592000 ,
            'description': 'Order Description',
            }
        }
        # payload = {
        #     'intent': 'CAPTURE',
        #     'purchase_units': [
        #         {
        #             'reference_id': self.reference,
        #             'description': f'{self.company_id.name}: {self.reference}',
        #             'amount': {
        #                 'currency_code': self.currency_id.name,
        #                 'value': self.amount,
        #             },
        #             'payee':  {
        #                 'display_data': {
        #                     'brand_name': self.provider_id.company_id.name,
        #                 }
        #             },
        #         },
        #     ],
        #     'payment_source': {
        #         'multisafepay': {
        #             'name': {
        #                 'given_name': partner_first_name,
        #                 'surname': partner_last_name,
        #             },
        #         },
        #     },
        # }

    #     # PayPal does not accept None set to fields and to avoid users getting errors when email
    #     # is not set on company we will add it conditionally since its not a required field.
    #     if company_email := self.provider_id.company_id.email:
    #         payload['purchase_units'][0]['payee']['display_data']['business_email'] = company_email
    #
        return payload


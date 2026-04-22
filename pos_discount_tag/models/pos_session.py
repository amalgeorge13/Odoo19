from odoo import api, fields, models
class PosSession(models.Model):
    """Extend POS session to load custom models."""
    _inherit = 'pos.session'

    @api.model
    def _load_pos_data_models(self, config_id):
        """Return models to be loaded into the POS session."""
        data = super()._load_pos_data_models(config_id)
        data += ['product.discount.tag']
        print(data)
        return data

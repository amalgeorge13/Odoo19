/** @odoo-module */
import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { _t } from "@web/core/l10n/translation";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useRef, onMounted } from "@odoo/owl";
/**
* This class represents a custom popup in the Point of Sale.
* It extends the AbstractAwaitablePopup class.
*/
export class ProductButtonPopup extends AbstractAwaitablePopup {
   static template = "custom_popup.ProductButtonPopup";
   static defaultProps = {
       closePopup: _t("Cancel"),
       confirmText: _t("Save"),
       title: _t("Product List"),
   };
}

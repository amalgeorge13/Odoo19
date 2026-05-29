/** @odoo-module */
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { ProductsPopup } from "./products_popup";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";


/*
patching control button create new button action to list products in a popup screen
 */
patch(ControlButtons.prototype, {
    async onClickPopup() {
        await makeAwaitable(this.dialog, ProductsPopup, {
            title: _t("Products Popup!"),
        });
    }
});

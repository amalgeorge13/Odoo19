/** @odoo-module */
import {Dialog} from "@web/core/dialog/dialog";
import {usePos} from "@point_of_sale/app/hooks/pos_hook";
import {Component, useState} from "@odoo/owl";
import { CreateProduct } from "./create_product";
import { EditProduct } from "./edit_product";

import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";

/*
creating new component that listing products
*/

export class ProductsPopup extends Component {
    static template = "pos_product_creation.ProductsPopup";
    static components = {Dialog};

    setup() {
        this.pos = usePos();
        this.dialog= useService('dialog')
        this.state = useState({
            products: []
        });
        this.state.products = Array.from(this.pos.models["product.product"].records.values()).
        filter(product => product.type !== "service")
    }
    /*
    product creation popup
     */
    async createProduct() {
        this.props.close();
        await makeAwaitable(this.dialog, CreateProduct, {
            title: _t("Create Product!"),
        });
    }
    /*
    product edit popup
     */
    async editProduct(product) {
        this.props.close();
        await makeAwaitable(this.dialog, EditProduct, {
            title: _t("Edit Product!"),
            product: product,
        });
    }

    /*
    close popup screen
     */
    closePopupScreen() {
        this.props.close();
    }

}

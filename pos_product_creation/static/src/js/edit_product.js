import {Dialog} from "@web/core/dialog/dialog";
import {usePos} from "@point_of_sale/app/hooks/pos_hook";
import {Component, useState} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

/*
creating new component to edit existing product record
*/
export class EditProduct extends Component {
    static template = "pos_product_creation.EditProduct";
    static components = {Dialog};

    setup() {
        this.pos = usePos();
        this.orm = useService('orm');
        const product_name = this.props.product.name
        const product_price =this.props.product.lst_price
        this.state = useState({
            product : product_name ?? "",
            price : product_price || "",
            id : this.props.product.id
        });
    }
    /*
    when saving product orm call will work and edit the product record
    */
    async saveProduct(id) {
        const form = document.getElementById('productEditForm');
        const data = new FormData(form);

        const allValues = Object.fromEntries(data.entries());
        let result = await this.orm.call("product.product", "edit_product", [allValues,id], {});
        this.props.close();


    }

    /*
    close popup screen
    */
    closeEditProduct(){
        this.props.close();
    }


}
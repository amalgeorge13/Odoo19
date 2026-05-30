import {Dialog} from "@web/core/dialog/dialog";
import {Component, useState} from "@odoo/owl";

/*
creating new component to edit existing product record
*/
export class QrPopup extends Component {
    static template = "qr_generator.QrPopup";
    static components = {Dialog};

    setup() {
        super.setup();
    }
    async generateQR(ev) {
        const form = document.getElementById('QrGenerateForm');
        const data = new FormData(form);


        // Or view all values at once
        const allValues = Object.fromEntries(data.entries());
        console.log(allValues)

    }
    resetQR(){
        console.log(1111)
    }

    /*
    close popup screen
    */

    closeQrPopup(){
        this.props.close();
    }


}


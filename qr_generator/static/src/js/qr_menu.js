/** @odoo-module **/
import {Component, onWillStart, useState} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {QrPopup} from "./qr_popup";
// import {Dialog} from "@web/core/dialog/dialog";
import {ConfirmationDialog} from "@web/core/confirmation_dialog/confirmation_dialog";
import {useService} from "@web/core/utils/hooks";
import {_t} from "@web/core/l10n/translation";


export class QrMenu extends Component {
    static template = "qr_generator.QrMenu";

    setup() {
        super.setup();
        this.notification = useService("notification");
        this.dialogService = useService("dialog");
    }

    async onClickQrMenu() {
        this.dialogService.add(QrPopup, {
            title: _t("QR Generate!"),
        });
        // await makeAwaitable(this.dialog, QrPopup, {
        //     title: _t("GR Generate!"),
        // });
    }
}

registry
    .category("systray")
    .add("qr_generator.QrMenu", {Component: QrMenu}, {sequence: 20});

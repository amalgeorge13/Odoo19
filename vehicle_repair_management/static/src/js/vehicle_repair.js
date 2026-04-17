/** @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
import { renderToFragment } from "@web/core/utils/render";

export function _chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}
publicWidget.registry.get_repair_tab = publicWidget.Widget.extend({
   selector : '.repairs_section',
   async willStart() {
       var self = this;
            await rpc('/get_repair_records',).then((data) => {this.data = data;});
   },
    start: function () {
            var chunks = _chunk(this.data.repairs, 4)
            chunks[0].is_active = true
            var uniq = Date.now();
            this.$el.find('#carousel').html(
                renderToFragment('vehicle_repair_management.repair_template_highlight_carousel', {chunks,uniq})
            )
        },
});


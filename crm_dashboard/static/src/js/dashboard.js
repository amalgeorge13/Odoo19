/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component } from  "@odoo/owl";
const actionRegistry = registry.category("actions");
class CrmDashboard extends Component {
  setup() {
        super.setup();
        this.orm = useService('orm');
        this._fetch_data();
  }
  async _fetch_data(){
     let result = await this.orm.call("crm.lead", "get_tiles_data", [], {});

     document.getElementById('my_lead').innerHTML = `<span>${(result.total_leads.length)}</span>`;
     document.getElementById('my_opportunity').innerHTML = `<span>${result.total_opportunity.length}</span>`;
     document.getElementById('expected_revenue').innerHTML = `<span>${result.currency}${result.expected_revenue}</span>`;
     document.getElementById('revenue').innerHTML = `<span>${result.currency}${result.revenue}</span>`;
     document.getElementById('ratio').innerHTML = `<span>${(result.ratio)}%</span>`;
     document.getElementById('win_leads').innerHTML = `<span>Won - ${result.win_leads}</span>`;
     document.getElementById('lost_leads').innerHTML = `<span>Lost - ${result.lost_leads}</span>`;
  }
}

CrmDashboard.template = "crm_dashboard.CrmDashboard";
actionRegistry.add("crm_dashboard_tag", CrmDashboard);

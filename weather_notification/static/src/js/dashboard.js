/** @odoo-module **/
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {Component, onWillStart} from "@odoo/owl";

const actionRegistry = registry.category("actions");
let Chart1 =null
let Chart2 =null
let Chart3 =null
let Chart4 =null

class CrmDashboard extends Component {

    setup() {
        super.setup();
        this.orm = useService('orm');
        // this._fetch_data();


        onWillStart(async () => {
            this._fetch_data();
        });
    }
    onFilterChange(ev) {
        let newValue = ev.target.value;
        console.log("Filter changed to:", newValue);
        Chart1.destroy()
        Chart2.destroy()
        Chart3.destroy()
        Chart4.destroy()
        this._fetch_data(newValue);
    }
    /*
    * get whole data from python using orm call
    */
    async _fetch_data(newValue) {

        // if (newValue==true){
        //     var newValue=newValue
        // }

        let result = await this.orm.call("crm.lead", "get_tiles_data", [newValue], {});

        document.getElementById('my_lead').innerHTML = `<span>${(result.total_leads.length)}</span>`;
        document.getElementById('my_opportunity').innerHTML = `<span>${result.total_opportunity.length}</span>`;
        document.getElementById('expected_revenue').innerHTML = `<span>${result.currency}${result.expected_revenue}</span>`;
        document.getElementById('revenue').innerHTML = `<span>${result.currency}${result.revenue}</span>`;
        document.getElementById('ratio').innerHTML = `<span>${(result.ratio)}%</span>`;
        document.getElementById('win_leads').innerHTML = `<span>Won - ${result.win_leads}</span>`;
        document.getElementById('lost_leads').innerHTML = `<span>Lost - ${result.lost_leads}</span>`;
        document.getElementById('jan').innerHTML = `<span>${result.table_data[0]}</span>`;
        document.getElementById('feb').innerHTML = `<span>${result.table_data[1]}</span>`;
        document.getElementById('mar').innerHTML = `<span>${result.table_data[2]}</span>`;
        document.getElementById('apr').innerHTML = `<span>${result.table_data[3]}</span>`;
        document.getElementById('may').innerHTML = `<span>${result.table_data[4]}</span>`;
        document.getElementById('june').innerHTML = `<span>${result.table_data[5]}</span>`;
        document.getElementById('july').innerHTML = `<span>${result.table_data[6]}</span>`;
        document.getElementById('aug').innerHTML = `<span>${result.table_data[7]}</span>`;
        document.getElementById('sep').innerHTML = `<span>${result.table_data[8]}</span>`;
        document.getElementById('oct').innerHTML = `<span>${result.table_data[9]}</span>`;
        document.getElementById('nov').innerHTML = `<span>${result.table_data[10]}</span>`;
        document.getElementById('dec').innerHTML = `<span>${result.table_data[11]}</span>`;
        console.log(result.campaign)

        Chart1 = new Chart("chart_activity_pie", {
            type: "pie",
            data: {
                labels: ['Call', 'Email', 'Meeting', 'To-Do', 'Document'], // X-axis labels
                datasets: [{
                    label: 'Pie chart of Activities',
                    data: result.activities,
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(235, 206, 86, 0.2)',
                        'rgba(10, 112, 112, 0.2)',
                        'rgba(155, 35, 16, 0.2)'
                    ],
                    borderColor: [
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(235, 206, 86, 1)',
                        'rgba(10, 112, 112, 1)',
                        'rgba(155, 35, 16, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {}
        });
        Chart2 = new Chart(chart_activity_graph, {
            type: 'bar', // Choose the chart type (bar, line, pie, etc.)
            data: {
                labels: ['Lead', 'Opportunity',], // X-axis labels
                datasets: [{
                    label: 'Lead and Opportunity',
                    data: [result.total_leads.length, result.total_opportunity.length], // Y-axis data
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
        Chart3 = new Chart(chart_leads_medium_doughnut, {
            type: "doughnut",
            data: {
                labels: ['Email', 'Google Adwords', 'Banner', 'Website', 'LinkedIn'], // X-axis labels
                datasets: [{
                    label: 'Doughnut chart of Leads by Medium',
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(235, 206, 86, 0.2)',
                        'rgba(10, 112, 112, 0.2)',
                        'rgba(155, 35, 16, 0.2)'
                    ],
                    borderColor: [
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(235, 206, 86, 1)',
                        'rgba(10, 112, 112, 1)',
                        'rgba(155, 35, 16, 1)'
                    ],
                    data: result.medium
                }]
            },
            options: {}
        });
        Chart4 = new Chart("chart_leads_campaign_line", {
            type: "line",
            data: {
                labels: ['Campaign - Services', 'Campaign - Products', 'Sale', 'Christmas Special'],
                datasets: [{
                    label: 'line chart of Leads by Campaign',
                    data: result.campaign,
                    pointBackgroundColor: [
                                'rgba(54, 162, 235, 0.2)',
                                'rgba(255, 99, 132, 0.2)',
                                'rgba(235, 206, 86, 0.2)',
                                'rgba(10, 112, 112, 0.2)',
                            ],
                }]
            },
            option: {}
        });
    }
}
CrmDashboard.template = "crm_dashboard.CrmDashboard";
actionRegistry.add("crm_dashboard_tag", CrmDashboard);
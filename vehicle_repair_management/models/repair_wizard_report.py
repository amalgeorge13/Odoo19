import json
import io
from odoo import api, fields, models
from odoo.tools import date_utils, json_default
import xlsxwriter


class WizardReport(models.TransientModel):
    _name = 'wizard.report'
    _description = 'Wizard Report'

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    customer_ids = fields.Many2many('res.partner', string="Customer")
    advisor_ids = fields.Many2many('res.users', string="Advisor")

    def get_repair_data(self):
        query = """SELECT vehicle_repair.repair_reference,cp.name AS customer,
                        sp.name AS advisor,vehicle_repair.start_date,vehicle_repair.delivery_date
                        FROM vehicle_repair JOIN res_partner cp ON vehicle_repair.customer_name = cp.id 
                        JOIN res_partner sp ON vehicle_repair.service_advisor = sp.user_id
                        WHERE vehicle_repair.active = true"""
        query_params = []

        customer = []
        advisor = []
        if self.start_date:
            query = query + " AND start_date >= %s"
            query_params.append(self.start_date)
        if self.end_date:
            query = query + " AND delivery_date <= %s"
            query_params.append(self.end_date)
        if self.customer_ids:
            query = query + " AND customer_name IN %s"
            query_params.append(tuple(self.customer_ids.ids))
            if len(self.customer_ids) == 1:
                customer.append(self.customer_ids.name)
        if self.advisor_ids:
            query = query + " AND service_advisor IN %s"
            query_params.append(tuple(self.advisor_ids.ids))
            if len(self.advisor_ids) == 1:
                advisor.append(self.advisor_ids.name)

        query = query + " ORDER BY repair_reference ASC "

        self.env.cr.execute(query, query_params)
        repairs = self.env.cr.fetchall()
        return repairs,customer,advisor


    def action_print_pdf_report(self):

        repairs, customer, advisor = self.get_repair_data()

        datas = {
            'ids': [],
            'model': 'vehicle.repair',
            'form': repairs,
            'customer': customer,
            'advisor': advisor,
        }
        return self.env.ref(
            'vehicle_repair_management.action_vehicle_repair_report'
        ).report_action(self, data=datas)

    def action_print_excel_report(self):

        repairs,customer,advisor= self.get_repair_data()

        data = {
            'model_id': self.id,
            'customer': customer,
            'advisor': advisor,
            'repairs': repairs
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'wizard.report',
                     'options': json.dumps(data,default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Repair Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        title = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        sub = workbook.add_format(
            {'bold': True,'font_size':'12px','align': 'center'})
        head = workbook.add_format(
            {'bold': True,'font_size': '10px', 'align': 'center'})
        cell = workbook.add_format(
            {'font_size': '8px', 'align': 'center'})

        if data['customer'] or data['advisor']:
            if data['customer']:
                customer = data['customer'][0]
                sheet.merge_range('A5:B5', customer, sub)
                sheet.write(3,0, 'Customer:', head)
            if data['advisor']:
                advisor = data['advisor'][0]
                sheet.merge_range('C5:D5', advisor, sub)
                sheet.write(3, 2, 'Advisor:', head)

            sheet.merge_range('A2:E3', 'Vehicle Repair Report', title)
        else:
            sheet.merge_range('A3:E4', 'Vehicle Repair Report', title)

        col=0

        sheet.write(6, col, 'Reference', head)
        col+=1
        if not data['customer']:
            sheet.write(6, col, 'Customer', head)
            col += 1
        if not data['advisor']:
            sheet.write(6, col, 'Advisor', head)
            col += 1
        sheet.write(6, col, 'Start Date', head)
        col += 1
        sheet.write(6, col, 'Delivery Date', head)

        row = 7
        for rec in data['repairs']:
            col = 0
            sheet.write(row, col, rec[0], cell)
            col += 1
            if not data['customer']:
                sheet.write(row, col, rec[1], cell)
                col += 1
            if not data['advisor']:
                sheet.write(row, col, rec[2], cell)
                col += 1
            sheet.write(row, col, rec[3], cell)
            col += 1
            sheet.write(row, col, rec[4], cell)
            row += 1

        workbook.close()
        output.seek(0)

        response.stream.write(output.read())
        output.close()
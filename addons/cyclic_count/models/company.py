from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = 'res.company'
    warehouse_id = fields.One2many('cyclic.warehouse', 'company_id')




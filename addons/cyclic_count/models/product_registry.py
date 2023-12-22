
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class ProductRegistry(models.Model):
    _name= "cyclic.product.registry"
    _description="Registro Producto"
    system_units = fields.Integer(default=0, string="Unidades Sistema")
    real_units = fields.Integer(default=0, string="Unidades Reales")
    
    #Computed fields
    difference = fields.Integer(default=0, string="Diferencia", compute="_compute_difference")
    status = fields.Selection([('even','Cuadrado'),('difference','Diferencia'),('corrected','Conciliado')], compute="_compute_status")
    
    #Related fields
    product_id = fields.Many2one('cyclic.product', string="Producto")
    
    @api.depends('system_units', 'real_units')
    def _compute_difference(self):
        for record in self:
            record.difference = record.system_units - record.real_units
            
    @api.depends('difference')
    def _compute_status(self):
        for record in self:
            match record.difference:
                case 0:
                    record.status = 'even'
                case _:
                    record.status = 'difference'

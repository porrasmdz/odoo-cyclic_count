
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class ProductRegistry(models.Model):
    _name= "cyclic.product.registry"
    _description="Registro Producto"
    system_units = fields.Integer(default=0, string="Unidades Sistema")
    real_units = fields.Integer(default=0, string="Unidades Reales")
    
    #Computed fields
    difference = fields.Integer(default=0, string="Diferencia")
    status = fields.Selection([('even','Cuadrado'),('difference','Diferencia'),('corrected','Conciliado')])
    
    #Related fields
    product_id = fields.Many2one('cyclic.product', string="Producto")
    
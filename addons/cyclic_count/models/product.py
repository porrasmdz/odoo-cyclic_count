
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class Product(models.Model):
    _name= "cyclic.product"
    _description="Producto"

    _inherit= 'mail.thread'

    product_code = fields.Char(string="Codigo de Producto" ,tracking=True)
    sku = fields.Char(string="Sku" ,tracking=True) 
    name= fields.Char(string="Nombre" ,tracking=True)
    unit_cost = fields.Float(string="Costo Unitario" ,tracking=True)

    #Computed fields
    location_code = fields.Char(string="Codigo Ubicacion")
    #Related fields
    
    warehouse_id= fields.Many2one("cyclic.warehouse",string="Bodega")
    whlocation_id = fields.Many2one("cyclic.warehouse.subdivision",string="Subdivision de Bodega")
    mu_id = fields.Many2one("cyclic.measure.unit", string="Unidades de Medida")
    category_id = fields.Many2one("cyclic.product.category", string="Categoría")


    system_units = fields.Integer(default=0, string="Unidades Sistema")
    real_units = fields.Integer(default=0, string="Unidades Reales")
    
    #Computed fields
    difference = fields.Integer(default=0, string="Diferencia", compute="_compute_difference")
    status = fields.Selection([('even','Cuadrado'),('difference','Diferencia'),('corrected','Conciliado')], compute="_compute_status")
    
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

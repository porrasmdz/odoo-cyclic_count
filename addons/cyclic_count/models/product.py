
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class Product(models.Model):
    _name= "cyclic.product"
    _description="Producto"
    product_code = fields.Char(string="Codigo de Producto")
    sku = fields.Char(string="Sku") 
    name= fields.Char(string="Nombre")
    unit_cost = fields.Float(string="Costo Unitario")

    #Computed fields
    location_code = fields.Char(string="Codigo Ubicacion")
    #Related fields
    
    warehouse_id= fields.Many2one("cyclic.warehouse",string="Bodega")
    whlocation_id = fields.Many2one("cyclic.warehouse.subdivision",string="Subdivision de Bodega")
    mu_id = fields.Many2one("cyclic.measure.unit", string="Unidades de Medida")
    category_id = fields.Many2one("cyclic.product.category", string="Categoría")


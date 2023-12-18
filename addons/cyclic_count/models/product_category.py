
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class ProductCategory(models.Model):
    _name= "cyclic.product.category"
    _description="Categoría Producto"

    name = fields.Char(default="Categoria Test", string="Nombre")
    #Computed fields
    #Related fields
    prodcategory_id= fields.Many2one('cyclic.product.category', string="Categoría Padre")
    
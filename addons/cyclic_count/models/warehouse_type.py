
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class WarehouseType(models.Model):
    _name= "cyclic.warehouse.type"
    _description="Tipo Bodega"

    name = fields.Char(default="Stock", string="Nombre")
    #Computed fields
    #Related fields
    
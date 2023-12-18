
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class SubdivisionType(models.Model):
    _name= "cyclic.subdivision.type"
    _description="Tipo Subdivision Bodega"

    name = fields.Char(default="Percha", string="Nombre")
    #Computed fields
    #Related fields
    
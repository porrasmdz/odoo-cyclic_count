from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class MeasureUnit(models.Model):
    _name= "cyclic.measure.unit"
    _description="Unidad de Medida"

    name=fields.Char(string="Unidad de Medida")

    
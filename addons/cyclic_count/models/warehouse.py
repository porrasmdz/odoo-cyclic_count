from odoo import models, fields, api

class Warehouse(models.Model):
    _name= "cyclic.warehouse"
    _description="Bodega"

    name = fields.Char(default="Bodega Test", string="Nombre")
    province = fields.Char(string="Provincia")
    city = fields.Char(string="Ciudad")
    address = fields.Char(string="Dirección")

    #Computed Fields
    
    #Related Fields
    whtype_id = fields.Many2one("cyclic.warehouse.type",string="Tipo de Bodega") #Materia Primo, Transito, etc...
    company_id = fields.Many2one("res.company",string="Compañía")
    # city_id = fields.Many2one("res.city",string="Ciudad")
    partner_ids = fields.Many2many('res.partner', string="Encargados") #Modificar a One2Many, extendiendo res.partner en otro modelo

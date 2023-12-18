from odoo import models, fields, api

class WarehouseSubdivision(models.Model):
    _name= "cyclic.warehouse.subdivision"
    _description="Subdivision Bodega"


    area_code = fields.Char(string="Area", default="A1")


    #Computed Fields
    storage_type = fields.Char(string="Tipo Almacenamiento") #Percha, Suelo, Cajon etc...
    physical_location = fields.Char(string="Ubicacion Fisica") #Percha A, B, C, etc...
    side = fields.Char(string="Lado") #Frontal, Izq, Derecha, Trasero
    level = fields.Char(string="Nivel") #TOPE, FONDO, N1,N2,N3...

    #Related Fields
    subdiv_type = fields.Char(string="Tipo de Subdivision")#Many2one("cyclic.subdivision.type",string="Tipo de Subdivision")
    warehouse_id = fields.Many2one("cyclic.warehouse", "Bodega")
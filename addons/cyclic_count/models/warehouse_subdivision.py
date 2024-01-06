from odoo import models, fields, api

class WarehouseSubdivision(models.Model):
    _name= "cyclic.warehouse.subdivision"
    _description="Subdivision Bodega"


    name = fields.Char(compute="_compute_name", store=True)
    area_code = fields.Many2one("cyclic.warehouse.subdivision.area") #Char(string="Area")

    #Computed Fields
    storage_type = fields.Many2one("cyclic.warehouse.subdivision.stype")#Char(string="Tipo Almacenamiento") #Percha, Suelo, Cajon etc...
    physical_location = fields.Many2one("cyclic.warehouse.subdivision.plocation")#Char(string="Ubicacion Fisica") #Percha A, B, C, etc...
    side = fields.Many2one("cyclic.warehouse.subdivision.side")#Char(string="Lado") #Frontal, Izq, Derecha, Trasero
    level = fields.Many2one("cyclic.warehouse.subdivision.level")#Char(string="Nivel") #TOPE, FONDO, N1,N2,N3...

    #Related Fields
    subdiv_type = fields.Char(string="Tipo de Subdivision")#Many2one("cyclic.subdivision.type",string="Tipo de Subdivision")
    warehouse_id = fields.Many2one("cyclic.warehouse", "Bodega",readonly=True)

    @api.depends('area_code','storage_type','physical_location', 'side', 'level')
    def _compute_name(self):
        for record in self:
            record.name = "%s - %s - %s - %s - %s" %(record.area_code.name or "?", record.storage_type.name or "?", record.physical_location.name or "?", record.side.name or "?", record.level.name or "?" ) 


class SubdivisionArea(models.Model):
    _name= "cyclic.warehouse.subdivision.area"
    _description="Area Subdivision"
    name = fields.Char(string="Área")
class SubdivisionSType(models.Model):
    _name= "cyclic.warehouse.subdivision.stype"
    _description="Tipo Almacenamiento Subdivision"
    name = fields.Char(string="Tipo de Almacenamiento")
    
    
class SubdivisionPLocation(models.Model):
    _name= "cyclic.warehouse.subdivision.plocation"
    _description="Physical Location in Subdivision"
    name = fields.Char(string="Ubicación Física")

    
class SubdivisionSide(models.Model):
    _name= "cyclic.warehouse.subdivision.side"
    _description="Subdivision Side"
    name = fields.Char(string="Lado")
    
class SubdivisionLevel(models.Model):
    _name= "cyclic.warehouse.subdivision.level"
    _description="Subdivision Level"
    name = fields.Char(string="Nivel")
    
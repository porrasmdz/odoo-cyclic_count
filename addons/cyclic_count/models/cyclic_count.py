# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class CyclicCount(models.Model):
    _name = 'cyclic.count'
    _description = 'Conteo Cíclico'

    name = fields.Char(string="Nombre", default="Nuevo Conteo")
    start_date = fields.Date(string="Fecha de conteo",default=fields.Datetime.today()+relativedelta(days=2))
    end_date= fields.Date(string="Fecha límite",default=fields.Datetime.today()+relativedelta(weeks=2,days=2))
    status = fields.Selection([('first','Primer Conteo'),('second','Segundo Conteo'),('third','Tercer Conteo'),('corrections','Conciliaciones'),('finished','Completado')])
    total_items = fields.Integer(string="Registros Sistema Totales")
    total_real_items = fields.Integer(string="Registros Contados Totales")
    total_difference = fields.Integer(string="Diferencia Total")
    total_system_cost = fields.Float(string="Costos Sistema")
    total_real_cost = fields.Float(string="Costos Real")
    difference_cost = fields.Float(string="Costo Diferencia")
    
    #Computed Fields
    company= fields.Char(string="Compañía", default="Compania Test")
    
    #Related Fields
    asignee_ids= fields.Many2many('res.users',string="Encargados")
    product_ids = fields.Many2many('cyclic.product.registry', string="Productos en Bodega")
    warehouse_id= fields.Many2one('cyclic.warehouse',string="Bodega")
    


# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class CyclicCount(models.Model):
    _name = 'cyclic.count'
    _description = 'Conteo Cíclico'
    _inherit= 'mail.thread'
    ref= fields.Char(string="Reference", default=lambda self: ('Nuevo Conteo'))
    active = fields.Boolean(default=True , tracking=True)

    name = fields.Char(string="Nombre", default="Nombre", tracking=True)
    start_date = fields.Date(string="Fecha de conteo",default=fields.Datetime.today()+relativedelta(days=2))
    end_date= fields.Date(string="Fecha límite",default=fields.Datetime.today()+relativedelta(weeks=2,days=2))

    approval_state=fields.Selection([('available','Abierto'),('review','En Revision'),('unavailable', 'Cerrado')], default="available" , tracking=True)

    status = fields.Selection([('first','Primer Conteo'),('second','Segundo Conteo'),
                               ('third','Tercer Conteo'),('corrections','Conciliaciones'),
                               ('finished','Completado')], default=lambda self: ('first'), tracking=True)#, compute="_compute_status")
    total_items = fields.Integer(string="Registros Sistema Totales", compute="_compute_total_items")
    total_real_items = fields.Integer(string="Registros Contados Totales", compute="_compute_real_items")
    units_difference = fields.Integer(string="Diferencia Total", compute="_compute_units_diff")
    total_system_cost = fields.Float(string="Costos Sistema", compute="_compute_system_cost") 
    total_real_cost = fields.Float(string="Costos Físicos", compute="_compute_real_cost")
    difference_cost = fields.Float(string="Costo Diferencia", compute="_compute_diff_cost")
    whtype_id = fields.Many2one('cyclic.warehouse.type', string="Tipo de Bodega", compute="_compute_wh_type")

    #Computed Fields
    company= fields.Many2one("res.company",string="Compañía", compute="_compute_wh_company")
    
    #Related Fields
    prev_ccount = fields.Many2one('cyclic.count', string="Conteo Previo")
    asignee_ids= fields.Many2many('res.users',string="Encargados")
    
    product_ids = fields.One2many('cyclic.product','ccount_id','Productos')#Many2many('cyclic.product', string="Productos en Bodega")
    warehouse_id= fields.Many2one('cyclic.warehouse',string="Bodega")
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['ref']= self.env['ir.sequence'].next_by_code('cyclic.count')
        return super(CyclicCount, self).create(vals_list)

    @api.depends('product_ids')
    def _compute_total_items(self):
        for record in self:
            if(record.product_ids):
                for prec in record.product_ids:
                    record.total_items += prec.system_units 
            else:
                record.total_items = 0
    
    @api.depends('product_ids')
    def _compute_real_items(self):
        for record in self:
            if(record.product_ids):
                for prec in record.product_ids:
                    record.total_real_items += prec.real_units 
            else:
                record.total_real_items = 0


    @api.depends('product_ids')
    def _compute_units_diff(self):
        for record in self:
            if(record.product_ids):
                for prec in record.product_ids:
                    record.units_difference += prec.difference
            else:
                record.units_difference = 0
    

    
    @api.depends('product_ids')
    def _compute_system_cost(self):
        for record in self:
            if(record.product_ids):
                for prec in record.product_ids:
                    record.total_system_cost += prec.system_units * prec.unit_cost
            else:
                record.total_system_cost = 0
                
    @api.depends('product_ids')
    def _compute_real_cost(self):
        for record in self:
            if(record.product_ids):
                for prec in record.product_ids:
                    record.total_real_cost += prec.real_units * prec.unit_cost 
            else:
                record.total_real_cost = 0

    @api.depends('warehouse_id')
    def _compute_wh_type(self):
        for record in self:
            if(record.warehouse_id):
                record.whtype_id = record.warehouse_id.whtype_id 
            else:
                record.whtype_id = None

    @api.depends('product_ids')
    def _compute_diff_cost(self):
        for record in self:
            if(record.product_ids):
                for prec in record.product_ids:
                    record.difference_cost += prec.difference * prec.unit_cost 
            else:
                record.difference_cost = 0
       
  
    @api.depends('warehouse_id')
    def _compute_wh_company(self):
        for record in self:
            if(record.warehouse_id):
                record.company = record.warehouse_id.company_id
            else:
                record.company = "Seleccione una bodega"
            
             
    
    @api.depends('prev_ccount')
    def _compute_status(self):
        for record in self:
            if(record.prev_ccount):
                record.status = 'second'
            else:
                record.status = "first"
    
    def duplicate_self(self):
        new_rec_id = list(self.copy({'approval_state':'unavailable', 'active' : False ,'ref': self.ref, 'name': "%s | (%s)" % (self.name, self.status)}).get_external_id().keys())[0]
        self.prev_ccount = new_rec_id
        

    def remove_even_products(self):
        # This is done once cyclic count has archived itself
        # Even prods are not removed just archived
        diff_prods = self.get_differences()
        self.archive_even_products()
        self.product_ids = diff_prods

    def archive_even_products(self):
         even_prods = self.get_evens()
         self.prev_ccount.product_ids = even_prods

    def action_finish_count(self):
        
        match self.status:
            case 'first':
                
                if self.has_differences(): 
                    self.duplicate_self()
                    self.remove_even_products()
                    self.status = 'second'
                else:
                    self.duplicate_self()
                    self.approval_state = 'unavailable'
                    self.status = 'finished'
                return
            case 'second':
                if self.has_differences(): 
                    
                    
                    self.duplicate_self()
                    self.remove_even_products()
                    self.status = 'third'
                else:
                    
                    self.duplicate_self()
                    
                    self.approval_state = 'unavailable'
                    self.status = 'finished'
                return
            case 'third':
                self.duplicate_self()
                self.archive_even_products()
                self.approval_state = 'unavailable'
                self.status = 'finished'
                return
            case _:
                self.status = 'first'
                return
        
    
    def action_continue_count(self):
        match self.status:
            case _:
                self.status = 'first'
                self.approval_state = 'available'
        return
    
    @api.depends('product_ids')
    def has_differences(self):
        for product in self.product_ids:
            if product.status == 'difference':
                return True
        return False
    @api.depends('product_ids')
    def get_differences(self):
        diff_products = []
        for product in self.product_ids:
           if product.status == 'difference':
               diff_products.append(list(product.get_external_id().keys())[0])
             
        return diff_products
    
    @api.depends('product_ids')
    def get_evens(self):
        even_products = []
        for product in self.product_ids:
           if product.status == 'even':
               even_products.append(list(product.get_external_id().keys())[0])
              
        return even_products
        


    def action_set_available(self):
        if(self.approval_state != 'available'):
            self.approval_state = 'available'
        return


    
   
        
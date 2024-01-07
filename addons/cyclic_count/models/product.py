
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class Product(models.Model):
    _name= "cyclic.product"
    _description="Producto"
    _order= "product_code"
    _inherit= 'mail.thread'

    product_code = fields.Char(string="Codigo de Producto" ,tracking=True)
    sku = fields.Char(string="Sku" ) 
    name= fields.Char(string="Nombre" ,tracking=True)
    unit_cost = fields.Float(string="Costo Unitario" ,tracking=True)

    #Computed fields
    location_code = fields.Char(string="Codigo Ubicacion", compute="_compute_location_code", store=True)
    
    is_supervisor = fields.Boolean(compute="_compute_is_supervisor")
    #Related fields
    ccount_id= fields.Many2one("cyclic.count",string="Conteo")
    
    # active= fields.Boolean(compute="_compute_active")
    
    warehouse_id= fields.Many2one("cyclic.warehouse",string="Bodega", tracking=True)
    whlocation_id = fields.Many2one("cyclic.warehouse.subdivision",string="Subdivision de Bodega", tracking=True)
    mu_id = fields.Many2one("cyclic.measure.unit", string="Unidades de Medida")
    category_id = fields.Many2one("cyclic.product.category", string="Categoría")

    is_edittable = fields.Boolean(compute="_compute_edittable_state") #Invisible
    system_units = fields.Integer(default=0, string="Unidades Sistema",tracking=True )
    real_units = fields.Integer(default=0, string="Unidades Reales",tracking=True)
    
    #Computed fields
    difference = fields.Integer(default=0, string="Diferencia", compute="_compute_difference")
    status = fields.Selection([('even','Cuadrado'),('difference','Diferencia'),('corrected','Conciliado')], compute="_compute_status")
    
    @api.depends('system_units', 'real_units')
    def _compute_difference(self):
        for record in self:
            record.difference = record.system_units - record.real_units
            
    @api.depends('difference')
    def _compute_status(self):
        for record in self:
            match record.difference:
                case 0:
                    record.status = 'even'
                case _:
                    record.status = 'difference'
    @api.depends('ccount_id', 'ccount_id.approval_state')
    def _compute_edittable_state(self):
        for record in self:
            if record.ccount_id and record.ccount_id.approval_state:
                
                if record.ccount_id.approval_state == 'unavailable':
                    record.is_edittable = False
                else:
                    record.is_edittable = True
            else:
                record.is_edittable = False


    def _compute_is_supervisor(self):
        for record in self:
            if(self.user_has_groups('cyclic_count.group_cyclic_supervisor,cyclic_count.group_cyclic_admin,cyclic_count.group_cyclic_director')):
                record.is_supervisor = True
            else:
                record.is_supervisor = False
                
    # @api.depends('ccount_id', 'ccount_id.active')
    # def _compute_active(self):
    #     for record in self:
    #         if record.ccount_id:
                
    #             record.active = record.ccount_id.active
               
    #         else:
    #             record.active = True
    
   

    @api.depends('whlocation_id','warehouse_id')
    def _compute_location_code(self):
        for record in self:
            if record.whlocation_id and len(record.whlocation_id.name) > 0:
                locationcode_tokens = [whloc.strip() for whloc in record.whlocation_id.name.split('-')]
                record.location_code = "%s%s%s%s%s" %(locationcode_tokens[0] or '?',locationcode_tokens[1][0] or '?',locationcode_tokens[2] or '?',locationcode_tokens[3][0] or '?',locationcode_tokens[4] or '?')
            else:
                record.location_code = ""
    
    
    @api.onchange('warehouse_id')
    def onchange_warehouse_id(self):
        self.whlocation_id = None
        self.location_code = None

    
import os

# Define the modules structure and content
modules = {
    "supplement_base": {
        "__init__.py": "from . import models",
        "__manifest__.py": """{
    'name': 'Base para Cotización de Suplementos',
    'version': '1.0',
    'summary': 'Estructura básica para cotizaciones.',
    'depends': ['base'],
    'data': [
        'views/quotation_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False
}""",
        "models/__init__.py": "from . import quotation",
        "models/quotation.py": """
from odoo import models, fields

class SupplementQuotation(models.Model):
    _name = 'supplement.quotation'
    _description = 'Cotización de Suplementos Alimenticios'

    name = fields.Char(string=\"Referencia\", required=True, default=\"Nueva Cotización\")
    customer_id = fields.Many2one('res.partner', string=\"Cliente\", required=True)
    capsule_qty = fields.Integer(string=\"Cantidad de Cápsulas\", required=True)
""",
        "views/quotation_views.xml": """
<odoo>
    <record id="view_supplement_quotation_form" model="ir.ui.view">
        <field name="name">supplement.quotation.form</field>
        <field name="model">supplement.quotation</field>
        <field name="arch" type="xml">
            <form string="Cotización de Suplementos Alimenticios">
                <sheet>
                    <group>
                        <field name="name"/>
                        <field name="customer_id"/>
                        <field name="capsule_qty"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>
</odoo>
""",
        "security/ir.model.access.csv": """id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_supplement_quotation,supplement.quotation,model_supplement_quotation,,1,1,1,1
""",
    },
    "supplement_costs": {
        "__init__.py": "from . import models",
        "__manifest__.py": """{
    'name': 'Cálculo de Costos para Suplementos',
    'version': '1.0',
    'summary': 'Añade cálculo de costos a cotizaciones.',
    'depends': ['supplement_base'],
    'installable': True,
    'application': False
}""",
        "models/__init__.py": "from . import costs",
        "models/costs.py": """
from odoo import models, fields

class SupplementQuotation(models.Model):
    _inherit = 'supplement.quotation'

    raw_material_cost = fields.Float(string=\"Costo Materias Primas\", required=True)
    encapsulation_cost = fields.Float(string=\"Costo Encapsulado\", compute=\"_compute_encapsulation_cost\", store=True)

    def _compute_encapsulation_cost(self):
        for record in self:
            record.encapsulation_cost = (record.capsule_qty / 1000) * 10.0  # Ejemplo
""",
    },
    "supplement_invoices": {
        "__init__.py": "from . import models",
        "__manifest__.py": """{
    'name': 'Facturación para Suplementos',
    'version': '1.0',
    'summary': 'Añade facturación estimada y anticipos.',
    'depends': ['account', 'supplement_base'],
    'installable': True,
    'application': False
}""",
        "models/__init__.py": "from . import invoices",
        "models/invoices.py": """
from odoo import models, fields

class SupplementQuotation(models.Model):
    _inherit = 'supplement.quotation'

    advance_payment = fields.Boolean(string=\"Anticipo Pagado\", default=False)

    def create_advance_invoice(self):
        for record in self:
            advance_amount = record.capsule_qty * 0.5  # Ejemplo de cálculo
            self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': record.customer_id.id,
                'invoice_line_ids': [(0, 0, {'name': 'Anticipo', 'price_unit': advance_amount})],
            })
""",
    },
}

# Directory to save the modules
base_dir = os.path.join(os.getcwd(), "custom-modules")

# Create each module and its files
for module_name, module_files in modules.items():
    module_path = os.path.join(base_dir, module_name)
    os.makedirs(module_path, exist_ok=True)
    for file_path, content in module_files.items():
        full_path = os.path.join(module_path, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)

print(f"Modules created in: {base_dir}")
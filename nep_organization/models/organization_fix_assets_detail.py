from odoo import api, models, fields


class FixAssetsModel(models.Model):
    _name = "organization.fix.assets"
    _description = "Organization Fix Assets Details"
    
    asset_name = fields.Many2one("org.asset.master", string="Asset Name")
    location_of_asset = fields.Char("Asset Location")
    asset_number = fields.Char("Asset Quantity")
    asset_total_cost = fields.Char("Asset Total Cost")
    no_of_rooms = fields.Char("Number of Room")
    house_block_number = fields.Char("Total Block Number")
    total_kitta_number = fields.Char("Total Kitta Number")
    vehicle_type = fields.Char("Vehicle Type")
    # Page reference
    asset_ref_id = fields.Many2one("organization.information")
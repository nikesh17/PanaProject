from odoo import api, fields, models


class Beneficiary(models.Model):
    _name = "upabhokta.samiti.beneficiary"
    _description = "Upabhokta Samiti beneficiary model"

    total_family_numbers = fields.Integer(
        string="Total Family Numbers", compute="_total_family_number"
    )
    total_population = fields.Integer(
        string="Total Population",compute="_total_population"
    )
    total_male_population = fields.Integer(
        string="Total Male Population", compute="_total_male_population"
    )
    total_female_population = fields.Integer(
        string="Total Female Population", compute="_total_female_population"
    )

    tribal_family_number = fields.Integer(string="Tribal Family Number")
    tribal_male_population = fields.Integer(string="Tribal Male Population")
    tribal_female_population = fields.Integer(string="Tribal Female Population")

    dalit_family_number = fields.Integer(string="Dalit Family Population")
    dalit_male_population = fields.Integer(string="Dalit Male Population")
    dalit_female_population = fields.Integer(string="Dalit Female Population")

    total_child_population = fields.Integer(string="Total Child Population", compute="_total_child_pop")
    children_male_population = fields.Integer(string="Children Male Population")
    children_female_population = fields.Integer(string="Children Female Population")

    other_community_family_number = fields.Integer(
        string="Other Community Family Numbers"
    )
    other_community_male_population = fields.Integer(
        string="Other Community Male Population"
    )
    other_community_female_population = fields.Integer(
        string="Other Community Female Population"
    )

    # Upabhokta Samiti Info Notebook Page Reference Id
    upabhokta_samiti_notebook_page_reference_id = fields.Many2one(
        "upabhokta.samiti.info"
    )

    # Total Child Population
    @api.depends("children_female_population","children_male_population")
    def _total_child_pop(self):
        for record in self:
            child_total=record.children_female_population + record.children_male_population
            self.total_child_population=child_total
            
    # Total Population
    @api.depends("total_male_population", "total_female_population")
    def _total_population(self):
        for record in self:
            total_pop = self.total_male_population + self.total_female_population
            self.total_population = total_pop

    # Total Male Population
    @api.depends(
        "tribal_male_population",
        "dalit_male_population",
        "other_community_male_population",
    )
    def _total_male_population(self):
        for record in self:
            total_male_pop = (
                record.tribal_male_population
                + record.dalit_male_population
                + record.other_community_male_population
            )
            self.total_male_population = total_male_pop

    # Total Female Population
    @api.depends(
        "tribal_female_population",
        "dalit_female_population",
        "other_community_female_population",
    )
    def _total_female_population(self):
        for record in self:
            total_female_pop = (
                record.tribal_female_population
                + record.dalit_female_population
                + record.other_community_female_population
            )
            self.total_female_population = total_female_pop

    # Total Family Number
    @api.depends(
        "tribal_family_number", "dalit_family_number", "other_community_family_number"
    )
    def _total_family_number(self):
        for record in self:
            _total_family_number = (
                record.tribal_family_number
                + record.dalit_family_number
                + record.other_community_family_number
            )
            self.total_family_numbers = _total_family_number

    # Total Population
    @api.depends("total_male_population","total_female_population")
    def _total_population(self):
        for record in self:
            total_pop=self.total_male_population + self.total_female_population
            self.total_population=total_pop
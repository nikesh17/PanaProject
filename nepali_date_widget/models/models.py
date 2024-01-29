# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime
import nepali_datetime

class NepaliDateMixin(models.AbstractModel):
    _name = 'nepalidate.mixin'
    _description = "Nepali and English date computation"

    @api.depends("ad_date")
    def _compute_nepali_date(self):
        for record in self:
            if not record.ad_date:
                record.bs_date = nepali_datetime.date.today()
            else:
                record.bs_date = nepali_datetime.date.from_datetime_date(record.ad_date)


    @api.depends("bs_date")
    def _compute_english_date(self):
        for record in self:
            if not record.bs_date:
                record.ad_date = datetime.date.today()
            else:
                nepali_date = nepali_datetime.datetime.strptime(record.bs_date, '%Y-%m-%d')
                english_date = nepali_date.to_datetime_date()
                record.ad_date = english_date


    bs_date = fields.Char(string="Date(BS)", compute='_compute_nepali_date', store=True, readonly=False)
    ad_date = fields.Date(string="Date(AD)", compute='_compute_english_date', store=True, readonly=False)
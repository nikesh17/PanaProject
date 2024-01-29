from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo import tools

# Number to Words

# Main Logic
ones = ('Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine')

twos = ('Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen')

tens = ('Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety', 'Hundred')

suffixes = ('', 'Thousand', 'Lakhs', 'Crore')

def process(number, index):
    
    if number=='0':
        return 'Zero'
    
    length = len(number)
    
    if(length > 3):
        return False
    
    number = number.zfill(3)
    words = ''
 
    hdigit = int(number[0])
    tdigit = int(number[1])
    odigit = int(number[2])
    
    words += '' if number[0] == '0' else ones[hdigit]
    words += ' Hundred ' if not words == '' else ''
    
    if(tdigit > 1):
        words += tens[tdigit - 2]
        words += ' '
        words += ones[odigit]
    
    elif(tdigit == 1):
        words += twos[(int(tdigit + odigit) % 10) - 1]
        
    elif(tdigit == 0):
        words += ones[odigit]

    if(words.endswith('Zero')):
        words = words[:-len('Zero')]
    else:
        words += ' '
     
    if(not len(words) == 0):    
        words += suffixes[index]
        
    return words;
    
def getWords(number):
    length = len(str(number))
    
    if length>12:
        return 'This program supports upto 12 digit numbers.'
    
    words = []
    words.append(process(str(number)[-3:], 0))
    count = length // 3 if length % 3 == 0 else length // 3 + 1
    copy = count+1

    for i in range(length - 4, -1, -2):
        words.append(process(str(number)[0 if i - 2 < 0 else i - 1 : i + 1], copy - count))
        count -= 1;

    final_words = ''
    for s in reversed(words):
        temp = s + ' '
        final_words += temp
    
    return final_words
# End Main Logic


class AccMove(models.Model):
    _inherit='account.move'

    payment_method = fields.Char('Payment Method',compute='_compute_payment_method')

    def _compute_payment_method(self):
        for record in self:
            if record.invoice_payments_widget and 'content' in record.invoice_payments_widget.keys() and len(record.invoice_payments_widget['content'])>0:
                record.payment_method = record.invoice_payments_widget['content'][0]['journal_name']
            else:
                record.payment_method = 'Unpaid'

    total_word = fields.Char("Total in words",compute='_compute_tot_word')

    def _compute_tot_word(self):
        for record in self:
            record.total_word = getWords(int(record.tax_totals['amount_total']))

    total_word_untaxed = fields.Char("Total in words",compute='_compute_untaxed_tot_word')

    def _compute_untaxed_tot_word(self):
        for record in self:
            record.total_word_untaxed = getWords(int(record.tax_totals['amount_untaxed']))

    s_no = fields.Char(compute='_get_serial_numbers', string='S.No.',readonly=False, default=False)
    discount_amt = fields.Monetary('Discount Amount',
                    compute='_compute_discount_amt', 
                    currency_field='currency_id')
    total_amt = fields.Monetary("taxable ")


    @api.depends('invoice_line_ids')
    def _compute_discount_amt(self):
        for record in self:
            temp = False
            for line in record.invoice_line_ids:
                if line.discount>0:
                    temp += line.price_unit * line.quantity * (line.discount / 100.0)
            record.discount_amt = temp

    def _get_serial_numbers(self):
        s_num = 1	
        eng2nep={0:'०',1:'१',2:'२',3:'३',4:'४',5:'५',6:'६',7:'७',8:'८',9:'९'}
        if self._context['lang']=='ne_NP':
            for rec in self:
                temp=''
                temp2=s_num
                while temp2>0:
                    temp=str(eng2nep[temp2%10])+temp
                    temp2=int(temp2/10)
                rec.s_no=temp
                s_num+=1
        else:
            for rec in self:
                rec.s_no=str(s_num)
                s_num+=1

class AccMoveLines(models.Model):
    _inherit='account.move.line'

    s_no = fields.Char(compute='_get_serial_numbers', string='S.No.',readonly=False, default=False)

    def _get_serial_numbers(self):
        s_num = 1	
        eng2nep={0:'०',1:'१',2:'२',3:'३',4:'४',5:'५',6:'६',7:'७',8:'८',9:'९'}
        if self._context['lang']=='ne_NP':
            for rec in self:
                temp=''
                temp2=s_num
                while temp2>0:
                    temp=str(eng2nep[temp2%10])+temp
                    temp2=int(temp2/10)
                rec.s_no=temp
                s_num+=1
        else:
            for rec in self:
                rec.s_no=str(s_num)
                s_num+=1
            
    actual_price = fields.Monetary(
        string='Total',
        compute='_compute_actual_price',
        currency_field='currency_id',
    )
    
    @api.depends('quantity','price_unit')
    def _compute_actual_price(self):
        for record in self:
            record.actual_price = record.quantity*record.price_unit
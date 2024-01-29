/** @odoo-module **/

import { registerPatch } from '@mail/model/model_core';
import { attr, many, one, char } from '@mail/model/model_field';
import { clear, insert } from '@mail/model/model_field_command';
import { addLink, htmlToTextContentInline, parseAndTransform } from '@mail/js/utils';

import { session } from '@web/session';

import { getLangDatetimeFormat, str_to_datetime } from 'web.time';

const { markup } = owl;

let month_map = {
"जनवरी":"बैशाख",
"फेब्रुवरी":"जेठ",
"मार्च":"असार",
"अप्रिल":"श्रावण",
"मई":"भदौ",
"जुन":"आश्विन", 
"जुलाई":"कार्तिक",
"अगष्ट":"मंसिर",
"सेप्टेम्बर":"पुष",
"अक्टोबर":"माघ",
"नोभेम्बर":"फाल्गुन",
"डिसेम्बर":"चैत्र"
}

registerPatch({
    name: 'Message',

    recordMethods:{
        _OnChangeDateToNepaliDateForm() {
            let temp = this.dateDay.split(' ')
            if(temp.length>1){
                temp[1] = month_map[temp[1]]
                // this._dateDay = temp.join(' ')
                Object.defineProperty(this, "dateDay", { value: temp.join(' ') });
            }
        },    
    },
    onChanges:[
        {
            dependencies: ['dateDay'],
            methodName: '_OnChangeDateToNepaliDateForm',
        }
    ]
});

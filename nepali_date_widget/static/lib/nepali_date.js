/** @odoo-module **/
import { registry } from "@web/core/registry";
const {Component, onError, onMounted,  xml, useRef} = owl;
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { DateField } from "@web/views/fields/date/date_field"
import { DatePicker } from "@web/core/datepicker/datepicker";
import {
    formatDate,
    momentToLuxon,
} from "@web/core/l10n/dates";


export class NepaliDateWidget extends DateField {
    setup(){
        super.setup();
        console.log(this.props)
        this.inputel = useRef("nepali-datepicker")
        this.new_id = this.props.id+"aa";
        let bs_dict={},ad_dict=false,temp,ad,bs;
        bs_dict =this.props.value.c
        if(this.props.value){
            if(this.props.value){
                ad_dict = NepaliFunctions.BS2AD(bs_dict)
                // this.props.update(momentToLuxon(moment(ad,"YYYY/MM/DD")).setLocale('ne-NP'));
            }
            this.ad_date = Object.values(ad_dict).slice(0,3).join('/');
            this.bs_date = Object.values(bs_dict).slice(0,3).join('/');
        }
        console.log(this.ad_date)
        console.log(this.bs_date)
        let err = false;
        onError((e) => {
            this.err=true;
            console.log('hi');
            console.log(e);
        });
        
        onMounted(() => {
            // handling the nonscrolling behaviour of the datepicker
            if(err){
                return;
            }
            // console.log(this.bs_date)
            // console.log(Object.values(NepaliFunctions.AD2BS(bs_dict)).slice(0,3).join('/'))
            if(!document.getElementById(this.props.id)){
                // not form view
                // let date_fields = Array.from(document.querySelectorAll(`div[name="${this.props.name}"]`))

                // date_fields.forEach(each=>{
                //     each.getElementsByTagName('span')[0].innerHTML =`${Object.values(NepaliFunctions.AD2BS(bs_dict)).slice(0,3).join('/')} (${this.bs_date})` 
                // })
                return
            }
            if(this.ad_date){
                console.log("***")
                document.getElementById(this.props.id).value=this.ad_date;
            }
            let first_click= {},curr_top={};
            first_click[this.props.id] = true;
            window.$(document.getElementById(this.props.id).parentElement).on('change.datetimepicker',(ev)=>{
                console.log("?????")
                let ad_dict = {},bs_dict= {},temp;
                temp = momentToLuxon(ev.date).setLocale('ne-NP')['c']
                ad_dict['year']= temp['year']
                ad_dict['month']= temp['month']
                ad_dict['day']= temp['day']
                bs_dict = NepaliFunctions.AD2BS(ad_dict)
                this.inputel.value=Object.values(bs_dict).join('/');
                this.bs_date=Object.values(bs_dict).join('/');
                // this.props.update(momentToLuxon(moment(ev.ad,'YYYY-MM-DD')).setLocale('ne-NP'));
            })
            document.getElementById(this.props.id+'aa').addEventListener('click',event=>{
                if(document.querySelector('.modal-dialog.modal-lg')){
                    return;
                }
                if(document.getElementById('ndp-nepali-box')){
                    if(first_click[this.props.id]){
                        curr_top[this.props.id] = document.getElementById('ndp-nepali-box').style.top;
                        curr_top[this.props.id] = Number(curr_top[this.props.id].slice(0,curr_top[this.props.id].length-2));
                        first_click[this.props.id]=false;
                    }
                    let scroll_dist = document.getElementsByClassName('o_content')[0].scrollTop;
                    document.getElementById('ndp-nepali-box').style.top = (curr_top[this.props.id]-scroll_dist)+'px';
                    document.getElementsByClassName('o_content')[0].addEventListener('scroll',e=>{
                        if(document.getElementById('ndp-nepali-box')){
                            scroll_dist = document.getElementsByClassName('o_content')[0].scrollTop;
                            document.getElementById('ndp-nepali-box').remove();
                        //     document.getElementById('ndp-nepali-box').style.top = (curr_top-scroll_dist)+'px'
                        //     console.log(document.getElementById('ndp-nepali-box').style.top)
                        }
                    })
                }
            })
            /* Initialize Datepicker with options */
            this.inputel.el.nepaliDatePicker({
                ndpYear: true,
                ndpMonth: true,
                onChange: (ev)=>{
                    let ad = ev.ad.slice(0,4)+'/'+ev.ad.slice(5,7)+'/'+ev.ad.slice(8,11)
                    document.getElementById(this.props.id).value=ad;
                    this.bs_date = ev.bs.replaceAll('-','/')
                    let ad_dict = {},bs_dict= {},temp;
                    temp = ad.split('/')
                    ad_dict["year"] = Number(temp[0])
                    ad_dict["month"] = Number(temp[1])
                    ad_dict["day"] = Number(temp[2])
                    temp = this.bs_date.split('/')
                    bs_dict["year"] = Number(temp[0])
                    bs_dict["month"] = Number(temp[1])
                    bs_dict["day"] = Number(temp[2])
                    this.bs_date.split('/')
                    // document.getElementById(this.props.id).parentElement.children[1].value=ad;
                    this.props.update(momentToLuxon(moment(ev.ad)).setLocale('ne-NP'));
                }
            });
        });
    }
}

NepaliDateWidget.template = 'nepali_date_widget.NepaliDateField';
NepaliDateWidget.components = {
    DatePicker,
};
NepaliDateWidget.props = {
    ...standardFieldProps,
    pickerOptions: { type: Object, optional: true },
    placeholder: { type: String, optional: true },
};
NepaliDateWidget.supportedTypes = ['date', 'datetime'];

registry.category('fields').content.date[1]=NepaliDateWidget;
registry.category("fields").add("nepali_datewidget", NepaliDateWidget);
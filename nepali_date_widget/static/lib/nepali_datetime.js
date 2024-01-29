/** @odoo-module **/
import { registry } from "@web/core/registry";
const {Component, onError, onMounted,  xml, useRef} = owl;
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { DateTimeField } from "@web/views/fields/datetime/datetime_field"
import { DateTimePicker } from "@web/core/datepicker/datepicker";
import {
    formatDate,
    momentToLuxon,
} from "@web/core/l10n/dates";


export class NepaliDateTimeWidget extends DateTimeField {
    setup(){
        super.setup();
        this.inputel = useRef("nepali-datepicker")
        this.new_id = this.props.id+"aa";
        let bs_dict={},ad_dict=false,temp,ad,bs;
        bs_dict =this.props.value.c
        if(this.props.value){
            if(this.props.value){
                ad_dict = NepaliFunctions.BS2AD(bs_dict)
                // this.props.update(momentToLuxon(moment(ad,"YYYY/MM/DD")).setLocale('ne-NP'));
            }
            // console.log(ad_dict)
            // console.log(bs_dict)
            this.ad_date = Object.values(ad_dict).slice(0,3).join('/');
            this.bs_date = Object.values(bs_dict).slice(0,3).join('/');
            this.time = Object.values(bs_dict).slice(3,6).join(':');
            this.hour = bs_dict['hour']
            this.minute = bs_dict['minute']
            this.second = bs_dict['second']
        }
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
                document.getElementById(this.props.id).value=this.ad_date+' '+this.time;
            }
            let first_click= {},curr_top={};
            first_click[this.props.id] = true;
            window.$(document.getElementById(this.props.id).parentElement).on('change.datetimepicker',(ev)=>{
                let ad_dict = {},bs_dict= {},temp;
                temp = momentToLuxon(ev.date).setLocale('ne-NP')['c']
                this.time = Object.values(temp).slice(3,6).join(':');
                this.hour = temp['hour']
                this.minute = temp['minute']
                this.second = temp['second']
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
                    let timeDiv = document.createElement('div')
                    timeDiv.className = 'd-flex'
                    let hour = document.createElement('input')
                    hour.setAttribute('id','datetime-hour')
                    hour.setAttribute('type','number')
                    hour.setAttribute('min',0)
                    hour.setAttribute('max',23)
                    hour.setAttribute('value',this.hour)
                    hour.addEventListener('input',e=>{
                        console.log(e.value)
                        if(e.value>23)
                            e.value = 23
                        if(e.value<0)
                            e.value = 0
                    })
                    let min = document.createElement('input')
                    min.setAttribute('id','datetime-min')
                    min.setAttribute('type','number')
                    min.setAttribute('min',0)
                    min.setAttribute('max',59)
                    min.setAttribute('value',this.minute)
                    min.addEventListener('input',e=>{
                        if(e.value>59)
                            e.value = 59
                        if(e.value<0)
                            e.value = 0
                    })
                    let sec = document.createElement('input')
                    sec.setAttribute('id','datetime-sec')
                    sec.setAttribute('type','number')
                    sec.setAttribute('min',0)
                    sec.setAttribute('max',59)
                    sec.setAttribute('value',this.second)
                    sec.addEventListener('input',e=>{
                        if(e.value>59)
                            e.value = 59
                        if(e.value<0)
                            e.value = 0
                    })
                    let confirm = document.createElement('i')
                    confirm.className = 'fa fa-check btn btn-sm btn-secondary'
                    confirm.addEventListener('click',e=>{
                        this.onNepaliTimeChange(e)
                    })
                    timeDiv.appendChild(hour)
                    timeDiv.appendChild(min)
                    timeDiv.appendChild(sec)
                    timeDiv.appendChild(confirm)
                    document.getElementById('ndp-nepali-box').appendChild(timeDiv)
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
                onChange: (ev)=>this.onNepaliDateChange(ev)
            });


            this.onNepaliDateChange = (ev)=>{
                let ad = ev.ad.slice(0,4)+'/'+ev.ad.slice(5,7)+'/'+ev.ad.slice(8,11)
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
                
                this.hour = document.getElementById('datetime-hour').value
                this.min = document.getElementById('datetime-min').value
                this.sec = document.getElementById('datetime-sec').value

                this.time = this.hour+':'+this.min+':'+this.sec

                // document.getElementById(this.props.id).parentElement.children[1].value=ad;

                let temp_ad = momentToLuxon(moment(ev.ad+' '+this.time)).setLocale('ne-NP')

                // temp_ad.c['hour'] = Number(this.hour);
                // temp_ad.c['minute'] = Number(this.min);
                // temp_ad.c['second'] = Number(this.sec);

                this.props.update(temp_ad);
                document.getElementById(this.props.id).value=ad+' '+this.time;
            }

            this.onNepaliTimeChange = (ev)=>{        
                if(document.getElementById('datetime-hour').value>23)
                    document.getElementById('datetime-hour').value = 23        
                else if(document.getElementById('datetime-hour').value<0)
                    document.getElementById('datetime-hour').value = 0       
                if(document.getElementById('datetime-min').value>59)
                    document.getElementById('datetime-min').value = 59        
                else if(document.getElementById('datetime-min').value<0)
                    document.getElementById('datetime-min').value = 0       
                if(document.getElementById('datetime-sec').value>59)
                    document.getElementById('datetime-sec').value = 59        
                else if(document.getElementById('datetime-sec').value<0)
                    document.getElementById('datetime-sec').value = 0       
                this.hour = document.getElementById('datetime-hour').value
                this.min = document.getElementById('datetime-min').value
                this.sec = document.getElementById('datetime-sec').value

                this.time = this.hour+':'+this.min+':'+this.sec

                // document.getElementById(this.props.id).parentElement.children[1].value=ad;

                let temp_ad = momentToLuxon(moment(this.ad_date+' '+this.time)).setLocale('ne-NP')

                // temp_ad.c['hour'] = Number(this.hour);
                // temp_ad.c['minute'] = Number(this.min);
                // temp_ad.c['second'] = Number(this.sec);

                this.props.update(temp_ad);
                document.getElementById(this.props.id).value=this.ad_date+' '+this.time;
                document.getElementById('ndp-nepali-box').remove();
            }


        });
    }
}

NepaliDateTimeWidget.template = 'nepali_date_widget.NepaliDateTimeField';
NepaliDateTimeWidget.components = {
    DateTimePicker,
};
NepaliDateTimeWidget.props = {
    ...standardFieldProps,
    pickerOptions: { type: Object, optional: true },
    placeholder: { type: String, optional: true },
};
NepaliDateTimeWidget.supportedTypes = ['date', 'datetime'];

registry.category('fields').content.datetime[1]=NepaliDateTimeWidget;
console.log(registry.category('fields').content)
// registry.category("fields").add("nepali_datewidget", NepaliDateTimeWidget);
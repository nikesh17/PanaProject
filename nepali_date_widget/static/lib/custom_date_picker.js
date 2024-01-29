/** @odoo-module **/
import { registry } from "@web/core/registry";
const {Component, onError, onMounted,  xml, useRef} = owl;
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class NepaliDateWidget extends Component {
    setup(){
        super.setup();
        this.inputel = useRef("nepali-datepicker")
        onError((e) => {
            console.log(e);
        });

        onMounted(() => {
            // handling the nonscrolling behaviour of the datepicker
            let first_click= {},curr_top={};
            first_click[this.props.id] = true;
            console.log(this.props.id)
            document.getElementById(this.props.id).addEventListener('click',event=>{
                if(document.querySelector('.modal-dialog.modal-lg')){
                    console.log("#")
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
                    let ad = ev.ad.slice(5,7)+'/'+ev.ad.slice(8,11)+'/'+ev.ad.slice(0,5)
                    this.props.update(ev.bs);
                }
            });
        });
    }
}

NepaliDateWidget.template = xml`
     <input type="text" class="o_input" t-att-id="props.id" t-att-value="props.value" name="date" t-ref="nepali-datepicker" readonly="true"/>
`;

NepaliDateWidget.props = {
    ...standardFieldProps,
};
NepaliDateWidget.supportedTypes = ["char"];

registry.category("fields").add("nepali_datepicker", NepaliDateWidget);
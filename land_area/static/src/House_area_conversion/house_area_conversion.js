/** @odoo-module */

import { registry } from "@web/core/registry"
import { Many2OneField } from "@web/views/fields/many2one/many2one_field"
import { Many2XAutocomplete, useOpenMany2XRecord } from "@web/views/fields/relational_utils";

const { useState } = owl

class HouseAreaConversionViewController extends Many2OneField {
    setup() {
        super.setup()
        this.state = useState({

        })
        // onMounted(()=>{            
        // })
    }

    async openTree() {
        //await this.props.update([2])
        await this.createmodal()
    }

    closeTree() {
        document.getElementById("house_area_conversion_view_modal").remove();
    }

    async createmodal() {
        const body = document.getElementsByTagName('body')[0]

        let modal = document.createElement('div');
        modal.className = "modal d-block o_technical_modal";
        modal.role = "dialog";
        modal.tabIndex = "-1"
        modal.id = "house_area_conversion_view_modal"
        let modal_dialog = document.createElement('div');
        modal_dialog.className = "modal-dialog modal-md";
        modal_dialog.role = "document";
        let modal_content = document.createElement('div');
        modal_content.className = "modal-content"
        let modal_header = document.createElement('div')
        modal_header.className = 'modal-header'
        let close = document.createElement('button')
        close.type = "button";
        close.className = "btn-close";
        close.id = "close_house_area_conversion_view_modal";
        close.tabIndex = "-1";
        let header_text = document.createElement('span')
        header_text.textContent = 'तल्ला/छेत्रफल सम्बन्धि विवरण :'
        let modal_body = document.createElement('div')
        modal_body.className = 'modal-body'
        /*Search block*/
        let search_container = document.createElement('div')
        search_container.className = "search-container rounded";
        search_container.style = "width:95%; margin-left:auto;margin-right:auto;margin-bottom:15px;margin-top:5px";
        let search_input = document.createElement('input');
        search_input.type = 'search'
        search_input.className = "form-control"
        search_input.placeholder = 'Search Here...'
        search_input.id = 'search-input'
        // search_input.setAttribute('t-ref','search-input')
        // search_input.setAttribute('t-on-keyup','event=>this.search(event)')
        let search_refresh = document.createElement('span')
        search_refresh.className = "btn btn-secondary";
        search_refresh.id = "search-refresh";
        let refresh_i = document.createElement('i');
        refresh_i.className = 'fa fa-refresh'
        search_refresh.appendChild(refresh_i)
        search_container.appendChild(search_input)
        search_container.appendChild(search_refresh)
        let modal_footer = document.createElement('div')
        modal_footer.className = 'modal-footer'
        //modal_footer.textContent='footer'

        let form_container = document.createElement('form')
        form_container.classList.add("container")
        form_container.id = 'form_container_id'

        //div1
        let div1 = document.createElement('div')
        div1.id = 'length_id'
        div1.classList.add("row")


        let divA = document.createElement('div');
        divA.classList.add('col-md-2');
        divA.id = 'length';

        let label_length = document.createElement('label');
        label_length.style = "margin-top: 25px";
        label_length.for = 'label_length';
        label_length.textContent = 'Length';

        div1.appendChild(divA);
        divA.appendChild(label_length);


        let divB = document.createElement('div');
        divB.classList.add('col-md-3');
        divB.id = 'feet';

        let input_length_feet = document.createElement('input');
        input_length_feet.type = 'number';
        input_length_feet.id = 'input_length_feet';

        let label_length_feet = document.createElement('label');
        label_length_feet.style = "margin-left: 40px";
        label_length_feet.for = 'label_length_feet';
        label_length_feet.textContent = 'Feet';

        div1.appendChild(divB);
        divB.appendChild(label_length_feet);
        divB.appendChild(input_length_feet);


        let divC = document.createElement('div');
        divC.classList.add('col-md-3');
        divC.id = 'inch';

        let input_length_inch = document.createElement('input');
        input_length_inch.type = 'number';
        input_length_inch.id = 'input_length_inch';

        let label_length_inch = document.createElement('label');
        label_length_inch.style = "margin-left: 40px";
        label_length_inch.for = 'label_length_inch';
        label_length_inch.textContent = 'Inch';

        div1.appendChild(divC);
        divC.appendChild(label_length_inch);
        divC.appendChild(input_length_inch);


        let divD = document.createElement('div');
        divD.classList.add('col-md-3');
        divD.id = 'meter';

        let input_length_meter = document.createElement('input');
        input_length_meter.type = 'number';
        input_length_meter.id = 'input_length_meter';
        let label_length_meter = document.createElement('label');
        label_length_meter.style = "margin-left: 40px";
        label_length_meter.for = 'label_length_meter';
        label_length_meter.textContent = 'Meter';

        div1.appendChild(divD);
        divD.appendChild(label_length_meter);
        divD.appendChild(input_length_meter);
        form_container.appendChild(div1)

        //div2
        let div2 = document.createElement('div')
        div2.id = 'breadth_id'
        div2.classList.add("row")


        let divE = document.createElement('div');
        divE.classList.add('col-md-2');
        divE.id = 'breadth';

        let label_breadth = document.createElement('label');
        label_breadth.style = "margin-top: 25px";
        label_breadth.for = 'label_breadth';
        label_breadth.textContent = 'Breadth';

        div2.appendChild(divE);
        divE.appendChild(label_breadth);

        let divF = document.createElement('div');
        divF.classList.add('col-md-3');
        divF.id = 'feet';

        let input_breadth_feet = document.createElement('input');
        input_breadth_feet.type = 'number';
        input_breadth_feet.id = 'input_breadth_feet';
        input_breadth_feet.style = "margin-top: 20px";


        div2.appendChild(divF);
        divF.appendChild(input_breadth_feet);


        let divG = document.createElement('div');
        divG.classList.add('col-md-3');
        divG.id = 'inch';

        let input_breadth_inch = document.createElement('input');
        input_breadth_inch.type = 'number';
        input_breadth_inch.id = 'input_breadth_inch';
        input_breadth_inch.style = "margin-top: 20px";

        div2.appendChild(divG);
        divG.appendChild(input_breadth_inch);


        let divH = document.createElement('div');
        divH.classList.add('col-md-3');
        divH.id = 'inch';

        let input_breadth_meter = document.createElement('input');
        input_breadth_meter.type = 'number';
        input_breadth_meter.id = 'input_breadth_meter';
        input_breadth_meter.style = "margin-top: 20px";

        div2.appendChild(divH);
        divH.appendChild(input_breadth_meter);
        form_container.appendChild(div2)



        //div3
        let div3 = document.createElement('div')
        div3.id = 'height_id'
        div3.classList.add("row")


        let divI = document.createElement('div');
        divI.classList.add('col-md-2');
        divI.id = 'height';

        let label_height = document.createElement('label');
        label_height.style = "margin-top: 25px";
        label_height.for = 'label_height';
        label_height.textContent = 'Height';

        div3.appendChild(divI);
        divI.appendChild(label_height);


        let divJ = document.createElement('div');
        divJ.classList.add('col-md-3');
        divJ.id = 'inch';

        let input_height_feet = document.createElement('input');
        input_height_feet.type = 'number';
        input_height_feet.id = 'input_height_feet';
        input_height_feet.style = "margin-top: 20px";

        div3.appendChild(divJ);
        divJ.appendChild(input_height_feet);


        let divK = document.createElement('div');
        divK.classList.add('col-md-3');
        divK.id = 'inch';

        let input_height_inch = document.createElement('input');
        input_height_inch.type = 'number';
        input_height_inch.id = 'input_height_inch';
        input_height_inch.style = "margin-top: 20px";

        div3.appendChild(divK);
        divK.appendChild(input_height_inch);


        let divL = document.createElement('div');
        divL.classList.add('col-md-3');
        divL.id = 'inch';

        let input_height_meter = document.createElement('input');
        input_height_meter.type = 'number';
        input_height_meter.id = 'input_height_meter';
        input_height_meter.style = "margin-top: 20px";

        div3.appendChild(divL);
        divL.appendChild(input_height_meter);
        form_container.appendChild(div3)


        //div4
        let div4 = document.createElement('div')
        div4.id = 'area_id'
        div4.classList.add("row")


        let divM = document.createElement('div');
        divM.classList.add('col-md-2');
        divM.id = 'area';

        let label_area = document.createElement('label');
        label_area.style = "margin-top: 25px";
        label_area.for = 'label_area';
        label_area.textContent = 'Area';

        div4.appendChild(divM);
        divM.appendChild(label_area);

        let divN = document.createElement('div');
        divN.classList.add('col-md-3');
        divN.id = 'feet';


        let input_area_feet = document.createElement('input');
        input_area_feet.type = 'number';
        input_area_feet.id = 'input_area_feet';
        input_area_feet.style = "margin-top: 20px";

        div4.appendChild(divN);
        divN.appendChild(input_area_feet);


        let divO = document.createElement('div');
        divO.classList.add('col-md-3');
        divO.id = 'inch';

        div4.appendChild(divO);


        let divP = document.createElement('div');
        divP.classList.add('col-md-3');
        divP.id = 'meter';

        let input_area_meter = document.createElement('input');
        input_area_meter.type = 'number';
        input_area_meter.id = 'input_area_meter';
        input_area_meter.style = "margin-top: 20px";

        div4.appendChild(divP);
        divP.appendChild(input_area_meter);
        form_container.appendChild(div4)

        //div 5
        let checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = 'check_box';
        checkbox.name = 'check_box';
        checkbox.value = '1';
        checkbox.style = "margin-top: 25px";

        let label = document.createElement('label');
        label.htmlFor = 'check_box';
        label.textContent = 'I agree to the terms and conditions';

        form_container.appendChild(checkbox);
        form_container.appendChild(label);

        //div 6
        let div6 = document.createElement('div')
        div6.id = 'save_discard_id'
        div6.classList.add("row")

        let divT = document.createElement('div');
        divT.classList.add('col-md-12');
        divT.id = 'submit';
        divT.style = "margin-top: 10px; text-align: center";

        let buttonCalculate = document.createElement('button');
        buttonCalculate.type = 'submit';
        buttonCalculate.id = 'button_calculate';
        buttonCalculate.textContent = 'Calculate';
        buttonCalculate.style = "margin-right: 15px";
        buttonCalculate.style.backgroundColor = "#2196F3";
        buttonCalculate.disabled = true;

        let buttonReset = document.createElement('button');
        buttonReset.type = 'reset';
        buttonReset.id = 'button_reset';
        buttonReset.textContent = 'Reset';
           

        div6.appendChild(divT);
        divT.appendChild(buttonCalculate);
        divT.appendChild(buttonReset);
        form_container.appendChild(div6);


        modal_body.appendChild(form_container)
        modal_header.appendChild(header_text)
        modal_header.appendChild(close)
        modal_content.appendChild(modal_header)
        modal_content.appendChild(modal_body)
        modal_content.appendChild(modal_footer)
        modal_dialog.appendChild(modal_content)
        modal.appendChild(modal_dialog)
        body.appendChild(modal)

        //event listeners
        document.getElementById('close_house_area_conversion_view_modal').addEventListener('click', () => {
            this.closeTree();
        });

        //code to reset
        document.getElementById('button_reset').addEventListener('click',()=>{
            document.getElementById('form_container_id').reset();    
        }); 

        document.getElementById('check_box').addEventListener('click',()=>{
            // alert();
            if(document.getElementById('check_box').checked == true){
            document.getElementById('button_calculate').removeAttribute('disabled'); 
            }else{
                document.getElementById("button_calculate").setAttribute("disabled", "disabled");
            }      
        }); 


        //Length
        document.getElementById('input_length_feet').addEventListener('change', () => {
            var L_feet = document.getElementById('input_length_feet').value;
            var L_inch = document.getElementById('input_length_inch').value;
            if(L_inch == ''){
                var L_inch = 0;
            }
            var L_ItoF = house_area_conversion_calc.InchToFeet(L_inch);
            var Total_F = parseFloat(L_feet)+parseFloat(L_ItoF);

            var F_to_M = house_area_conversion_calc.FeetToMeter(Total_F);

            document.getElementById('input_length_meter').value = F_to_M;
            
        });

        document.getElementById('input_length_inch').addEventListener('change', () => {
        // debugger;
          
            var L_inch = document.getElementById('input_length_inch').value;
            var L_feet = document.getElementById('input_length_feet').value;
            if(L_feet == ''){
                var L_feet = 0;
            }

            var I_to_F = house_area_conversion_calc.InchToFeet(L_inch);
            var Total_F = parseFloat(L_feet)+parseFloat(I_to_F);
            var F_to_M = house_area_conversion_calc.FeetToMeter(Total_F);

            document.getElementById('input_length_meter').value = F_to_M;           

        // convert meter to feet&inch
            var M_to_F = house_area_conversion_calc.MeterToFeet(F_to_M);            
            document.getElementById('input_length_feet').value = M_to_F._feet;
            document.getElementById('input_length_inch').value = M_to_F._inch;

        });

        document.getElementById('input_length_meter').addEventListener('change', () => {
            var L_meter = document.getElementById('input_length_meter').value;

            var M_to_F = house_area_conversion_calc.MeterToFeet(L_meter);
            

            document.getElementById('input_length_feet').value = M_to_F._feet;
            document.getElementById('input_length_inch').value = M_to_F._inch;
        });

        
        //Breadth
        document.getElementById('input_breadth_feet').addEventListener('change', () => {
            var B_feet = document.getElementById('input_breadth_feet').value;
            var B_inch = document.getElementById('input_breadth_inch').value;
            if(B_inch == ''){
                var B_inch = 0;
            }
            var B_ItoF = house_area_conversion_calc.InchToFeet(B_inch);
            var Total_F = parseFloat(B_feet)+parseFloat(B_ItoF);


            var F_to_M = house_area_conversion_calc.FeetToMeter(Total_F);

            document.getElementById('input_breadth_meter').value = F_to_M;          
        });

        document.getElementById('input_breadth_inch').addEventListener('change', () => {
            debugger;
            var B_inch = document.getElementById('input_breadth_inch').value;
            var B_feet = document.getElementById('input_breadth_feet').value;
            if(B_feet == ''){
                var B_feet = 0;
            }

            var I_to_F = house_area_conversion_calc.InchToFeet(B_inch);
            var Total_F = parseFloat(B_feet)+parseFloat(I_to_F);
            var F_to_M = house_area_conversion_calc.FeetToMeter(Total_F);

            document.getElementById('input_breadth_meter').value = F_to_M;    

            var M_to_F = house_area_conversion_calc.MeterToFeet(F_to_M);            
            document.getElementById('input_breadth_feet').value = M_to_F._feet;
            document.getElementById('input_breadth_inch').value = M_to_F._inch;       
           

        });

        document.getElementById('input_breadth_meter').addEventListener('change', () => {
            var B_meter = document.getElementById('input_breadth_meter').value;

            var M_to_F = house_area_conversion_calc.MeterToFeet(B_meter);

            document.getElementById('input_breadth_feet').value = M_to_F._feet;
            document.getElementById('input_breadth_inch').value = M_to_F._inch;
        }); 


        //Height
        document.getElementById('input_height_feet').addEventListener('change', () => {
              var H_feet = document.getElementById('input_height_feet').value;
            var H_inch = document.getElementById('input_height_inch').value;
            if(H_inch == ''){
                var H_inch = 0;
            }
            var B_ItoF = house_area_conversion_calc.InchToFeet(H_inch);
            var Total_F = parseFloat(H_feet)+parseFloat(B_ItoF);


            var F_to_M = house_area_conversion_calc.FeetToMeter(Total_F);

            document.getElementById('input_height_meter').value = F_to_M;        
        });

        document.getElementById('input_height_inch').addEventListener('change', () => {
            var H_inch = document.getElementById('input_height_inch').value;
            var H_feet = document.getElementById('input_height_feet').value;
            if(H_feet == ''){
                var H_feet = 0;
            }

            var I_to_F = house_area_conversion_calc.InchToFeet(H_inch);
            var Total_F = parseFloat(H_feet)+parseFloat(I_to_F);
            var F_to_M = house_area_conversion_calc.FeetToMeter(Total_F);

            document.getElementById('input_height_meter').value = F_to_M;    

            var M_to_F = house_area_conversion_calc.MeterToFeet(F_to_M);            
            document.getElementById('input_height_feet').value = M_to_F._feet;
            document.getElementById('input_height_inch').value = M_to_F._inch;           
        });

        document.getElementById('input_height_meter').addEventListener('change', () => {
            var H_meter = document.getElementById('input_height_meter').value;

            var M_to_F = house_area_conversion_calc.MeterToFeet(H_meter);

            document.getElementById('input_height_feet').value = M_to_F._feet;
            document.getElementById('input_height_inch').value = M_to_F._inch;
        });  
        
        
        //Area
        document.getElementById('input_area_feet').addEventListener('change', () => {
            var A_feet = document.getElementById('input_area_feet').value;

            var F_to_M = house_area_conversion_calc.Sq_FeetToSq_Meter(A_feet);

            document.getElementById('input_area_meter').value = F_to_M;          
        });

        document.getElementById('input_area_meter').addEventListener('change', () => {
            var A_meter = document.getElementById('input_area_meter').value;

            var M_to_F = house_area_conversion_calc.Sq_MeterToSq_Feet(A_meter);

            document.getElementById('input_area_feet').value = M_to_F;          
        });


        document.getElementById('button_calculate').addEventListener('click', () => {
            var l_meter = document.getElementById('input_length_meter').value;
            var b_meter = document.getElementById('input_breadth_meter').value;
          
            var s_m = l_meter*b_meter
            var F_to_mtr = house_area_conversion_calc.Sq_MeterToSq_Feet(s_m);

            document.getElementById('input_area_meter').value = s_m.toFixed(2);         
            document.getElementById('input_area_feet').value = parseFloat(F_to_mtr).toFixed(2);         
        });
    }
}


HouseAreaConversionViewController.template = "tax_measurement.HouseAreaConversion_View"
HouseAreaConversionViewController.components = { Many2OneField, Many2XAutocomplete }

registry.category("fields").add("House_Area_Conversion", HouseAreaConversionViewController)
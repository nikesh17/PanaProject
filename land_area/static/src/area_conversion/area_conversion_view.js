/** @odoo-module */

import { registry } from "@web/core/registry"
import { FloatField } from "@web/views/fields/float/float_field";
import { Many2OneField } from "@web/views/fields/many2one/many2one_field";
import { Many2XAutocomplete, useOpenMany2XRecord } from "@web/views/fields/relational_utils";

const { useState,onMounted } = owl

// const model_info={
//     'default':[
//         'parent_id',
//         ["id","parent_id","name_en","name_np","code","active"]
//     ],
//     'rate.business.sanitation.eval':[
//         'rate.business.sanitation.eval',
//         ["id","name","name_np","code","active"],
//         "squareMeter"
//     ],   
// }

class AreaConversionViewController extends FloatField {
    setup(){
        super.setup()
        this.state=useState({
        })
        onMounted(async ()=> {
            // building product group submenu
            // this.buildDataSubmenu();
            // this.createDataParentChildrenList();

            //adding event listeners 
            document.getElementById('refresh_all').addEventListener('click',()=>{
                disableInputs();
                document.getElementById('form_container_id').reset();              
           });         
   
        //    document.getElementById('close-area-conversion-view-modal').addEventListener('click',()=>{
        //        this.closeTree();
        //    });

        let inputIDs=['bkdkk','rapd','hecter','acre','SqMeter','SqFeet','kanwa_kanwain']

        let disableInputs=()=>{
            inputIDs.forEach(id=>{
                if(!document.getElementById(id).classList.contains('disabled'))
                    document.getElementById(id).classList.add('disabled') 
            })
        }

        document.getElementById('input_type_select').addEventListener('change',(e)=>{
            disableInputs();
            if(e.target.value=='')
                return;
            document.getElementById(e.target.value).classList.remove('disabled');
        })

        document.getElementById('kanwa_kanwain_input').addEventListener('click',e=>{
            console.log(e.target.value)
            if(e.target.value=='on')
                document.getElementById('kanwa_kanwain').classList.remove('disabled');
            else
                document.getElementById('kanwa_kanwain').classList.add('disabled');

        })

        document.getElementById('rapd').addEventListener("change", ()=>{
            var Ropani = document.getElementById('input_ropani').value;   
            var Aana = document.getElementById('input_aana').value;   
            var Paisa = document.getElementById('input_paisa').value;   
            var Dam = document.getElementById('input_dam').value;   

            var R_Sf = area_conversion.RopaniToSquareFeet(Ropani);
            var A_Sf = area_conversion.AnnaToSquareFeet(Aana);
            var P_Sf = area_conversion.PaisaToSquareFeet(Paisa);
            var D_Sf = area_conversion.DamToSquareFeet(Dam);
            
            var total_Sf = R_Sf + A_Sf + P_Sf + D_Sf ;
            total_Sf = parseFloat(total_Sf).toFixed(4);
            squarefeettoall(total_Sf)

        });
        document.getElementById('bkdkk').addEventListener("change", ()=>{
            var Bigha = document.getElementById('input_bigha').value;   
            var Kattha = document.getElementById('input_kattha').value;   
            var Dhur = document.getElementById('input_dhur').value;   
            var Kanwa = document.getElementById('input_kanwa').value;   
            var Kanwain = document.getElementById('input_kanwain').value; 

            var Bigha_Sf = area_conversion.BighaToSquareFeet(Bigha);
            var Kattha_Sf = area_conversion.KathaToSquareFeet(Kattha);
            var Dhur_Sf = area_conversion.DhurToSquareFeet(Dhur);
            var Kanwa_Sf = area_conversion.KanwaToSquareFeet(Kanwa);
            var Kanwain_Sf = area_conversion.KanwainToSquareFeet(Kanwain);

            var total_Bsf = Bigha_Sf + Kattha_Sf + Dhur_Sf + Kanwa_Sf + Kanwain_Sf;
            total_Bsf = parseFloat(total_Bsf).toFixed(2);
            squarefeettoall(total_Bsf)           
        });
        document.getElementById('input_hecter').addEventListener("change", ()=>{
            var Hecter = document.getElementById('input_hecter').value; 
            var Hecter_Sf = area_conversion.HecterToSquareFeet(Hecter);           
            squarefeettoall(Hecter_Sf)            
        });   
        document.getElementById('input_acre').addEventListener("change", ()=>{
            var Acre = document.getElementById('input_acre').value; 
            var Acre_Sf = area_conversion.AcerToSquareFeet(Acre);           
            squarefeettoall(Acre_Sf)            
        });     
        document.getElementById('input_SqMeter').addEventListener("change", ()=>{
            var SqMeter = document.getElementById('input_SqMeter').value; 
            var SqMeter_Sf = area_conversion.SquareMeterToSquareFeet(SqMeter);           
            squarefeettoall(SqMeter_Sf)            
        });     

        document.getElementById('input_SqFeet').addEventListener("change", ()=>{
            var SqFeet = document.getElementById('input_SqFeet').value; 
            squarefeettoall(SqFeet)    

        }); 

        })
        let squarefeettoall =(total_Sf)=>{
            this.props.update(Number(total_Sf));
            var sf_h = area_conversion.SquareFeetToHecter(total_Sf);
            var sf_a = area_conversion.SquareFeetToAcer(total_Sf);
            var sf_Sm = area_conversion.SquareFeetToSquareMeter(total_Sf);     
    
            let curr_unit = document.getElementById('input_type_select').value;

            if(curr_unit=='hecter')
                document.getElementById('input_hecter').value = sf_h;  
            else if(curr_unit=='acre')
                document.getElementById('input_acre').value = sf_a;
            else if(curr_unit=='SqMeter')
                document.getElementById('input_SqMeter').value = sf_Sm;
            // else if(curr_unit=='SqFeet')              
            //     document.getElementById('input_SqFeet').value = total_Sf;   
            else if(curr_unit=='bkdkk'){
                var Bsf_bigha = area_conversion.SquareFeetToBighaWithKanwa(total_Sf);  
                document.getElementById('input_bigha').value = Bsf_bigha._bigha;   
                document.getElementById('input_kattha').value = Bsf_bigha._kattha;   
                document.getElementById('input_dhur').value = Bsf_bigha._dhur;   
                document.getElementById('input_kanwa').value = Bsf_bigha._kanwa;   
                document.getElementById('input_kanwain').value = Bsf_bigha._kanwain; 
            }
            else if(curr_unit=='rapd'){
                var Bsf_ropani = area_conversion.SquareFeetToRopaniObj(total_Sf);  
                document.getElementById('input_ropani').value = Bsf_ropani._ropani;   
                document.getElementById('input_aana').value = Bsf_ropani._aana;   
                document.getElementById('input_paisa').value = Bsf_ropani._paisa;   
                document.getElementById('input_dam').value = Bsf_ropani._dam; 
            }
    
        } 
    }

    async openTree(){
        //await this.props.update([2])
        await this.createmodal()
    }

    closeTree(){
        document.getElementById("area-conversion-view-modal").remove();
    }  
  
    // async createmodal(){
    //     const body=document.getElementsByTagName('body')[0]

    //     let modal=document.createElement('div');
    //     modal.className="modal d-block o_technical_modal";
    //     modal.role="dialog";
    //     modal.tabIndex="-1"
    //     modal.id="area-conversion-view-modal"
    //     let modal_dialog=document.createElement('div');
    //     modal_dialog.className="modal-dialog modal-lg";
    //     modal_dialog.role="document";
    //     let modal_content=document.createElement('div');
    //     modal_content.className="modal-content"
    //     let modal_header=document.createElement('div')
    //     modal_header.className='modal-header'
    //     let close=document.createElement('button')
    //     close.type="button";
    //     close.className="btn-close";
    //     close.id="close-area-conversion-view-modal";
    //     close.tabIndex="-1";

    //     let header_text=document.createElement('span')
    //     header_text.className= "header"
    //     header_text.textContent='Area Calculation :' 
    //     let modal_body=document.createElement('div')
    //     modal_body.className='modal-body'
    
    //     // let search_refresh=document.createElement('span')
    //     // search_refresh.className="btn btn-secondary";
    //     // search_refresh.id="search-refresh";
    //     let refresh_btn=document.createElement('button');  
    //     refresh_btn.id= "refresh_all";
    //     refresh_btn.className='btn btn-primary'
    //     // search_refresh.appendChild(refresh_btn) 
    //     refresh_btn.textContent='re-set'     

    //     let modal_footer=document.createElement('div')
    //     modal_footer.className='modal-footer'
    //     //refresh_btn.textContent='footer'
       
    //     // let form_container=document.createElement('form')
    //     // form_container.id='form_container_id'        
    //     // form_container.classList.add("container")        
       
    //     // //div1
    //     // let div1=document.createElement('div')         
    //     // div1.id='bkdkk'
    //     // div1.classList.add("row")

    //     // let divA=document.createElement('div') 
    //     // divA.id='bigha'        
    //     // divA.classList.add('col-md-2')
    //     // let input_bigha=document.createElement('input')
    //     // input_bigha.type="number"
    //     // input_bigha.id="input_bigha"       
    //     // let label_bigha=document.createElement('label')
    //     // label_bigha.for='input_bigha'    
    //     // label_bigha.textContent='Bigha'
    //     // div1.appendChild(divA)
    //     // divA.appendChild(label_bigha)
    //     // divA.appendChild(input_bigha)

    //     // let divB = document.createElement('div')         
    //     // divB.id='kattha'   
    //     // divB.classList.add('col-md-2')    
    //     // let input_kattha=document.createElement('input')
    //     // input_kattha.type="number"
    //     // input_kattha.id="input_kattha"
    //     // let label_kattha=document.createElement('label')       
    //     // label_kattha.for='input_kattha'    
    //     // label_kattha.textContent='Kattha'
    //     // div1.appendChild(divB)
    //     // divB.appendChild(label_kattha)
    //     // divB.appendChild(input_kattha)

    //     // let divC = document.createElement('div')         
    //     // divC.id='dhur' 
    //     // divC.classList.add('col-md-2')
    //     // let input_dhur=document.createElement('input')
    //     // input_dhur.type="number"
    //     // input_dhur.id="input_dhur"
    //     // let label_dhur=document.createElement('label')        
    //     // label_dhur.for='input_dhur'    
    //     // label_dhur.textContent='dhur'
    //     // div1.appendChild(divC)
    //     // divC.appendChild(label_dhur)
    //     // divC.appendChild(input_dhur)


    //     // let divD = document.createElement('div')         
    //     // divD.id='kanwa'
    //     // divD.classList.add('col-md-2')
    //     // let input_kanwa=document.createElement('input')
    //     // input_kanwa.type="number"
    //     // input_kanwa.id="input_kanwa"
    //     // let label_kanwa=document.createElement('label')
    //     // label_kanwa.for='input_kanwa'    
    //     // label_kanwa.textContent='Kanwa'
    //     // div1.appendChild(divD)
    //     // divD.appendChild(label_kanwa)
    //     // divD.appendChild(input_kanwa)

    //     // let divE = document.createElement('div')         
    //     // divE.id='kanwain'
    //     // divE.classList.add('col-md-2')
    //     // let input_kanwain=document.createElement('input')
    //     // input_kanwain.type="number"
    //     // input_kanwain.id="input_kanwain"
    //     // let label_kanwain=document.createElement('label')
    //     // label_kanwain.for='input_kanwain'    
    //     // label_kanwain.textContent='Kanwain'
    //     // div1.appendChild(divE)
    //     // divE.appendChild(label_kanwain)
    //     // divE.appendChild(input_kanwain)
    //     // form_container.appendChild(div1)
               
    //     // // div2
    //     // let div2=document.createElement('div')         
    //     // div2.id='rapd'
    //     // div2.classList.add("row")

    //     // let divM=document.createElement('div') 
    //     // divM.id='ropani'   
    //     //  divM.classList.add("col-md-2")    
    //     // let input_ropani=document.createElement('input')
    //     // input_ropani.type="number"
    //     // input_ropani.id="input_ropani"
    //     // let label_ropani=document.createElement('label')
    //     // label_ropani.for='input_ropani'    
    //     // label_ropani.textContent='Ropani'
    //     // div2.appendChild(divM)
    //     // divM.appendChild(label_ropani)
    //     // divM.appendChild(input_ropani)

    //     // let divN = document.createElement('div')         
    //     // divN.id='aana'       
    //     // divN.classList.add("col-md-2")    
    //     // let input_aana=document.createElement('input')
    //     // input_aana.type="number"
    //     // input_aana.id="input_aana"
    //     // let label_aana=document.createElement('label')       
    //     // label_aana.for='input_aana'    
    //     // label_aana.textContent='Aana'
    //     // div2.appendChild(divN)
    //     // divN.appendChild(label_aana)
    //     // divN.appendChild(input_aana)

    //     // let divO = document.createElement('div')         
    //     // divO.id='paisa' 
    //     // divO.classList.add("col-md-2")    
    //     // let input_paisa=document.createElement('input')
    //     // input_paisa.type="number"
    //     // input_paisa.id="input_paisa"
    //     // let label_paisa=document.createElement('label')        
    //     // label_paisa.for='input_paisa'    
    //     // label_paisa.textContent='Paisa'
    //     // div2.appendChild(divO)
    //     // divO.appendChild(label_paisa)
    //     // divO.appendChild(input_paisa)

    //     // let divP = document.createElement('div')         
    //     // divP.id='dam'
    //     // divP.classList.add("col-md-2")    
    //     // let input_dam=document.createElement('input')
    //     // input_dam.type="number"
    //     // input_dam.id="input_dam"
    //     // let label_dam=document.createElement('label')
    //     // label_dam.for='input_dam'    
    //     // label_dam.textContent='Dam'
    //     // div2.appendChild(divP)
    //     // divP.appendChild(label_dam)
    //     // divP.appendChild(input_dam)   
    //     // form_container.appendChild(div2)

    //     // // div3
    //     // let div3=document.createElement('div')         
    //     // div3.id='hass'
    //     // div3.classList.add("row")

    //     // let divS=document.createElement('div') 
    //     // divS.id='hecter'       
    //     // divS.classList.add("col-md-2")    
    //     // let input_hecter=document.createElement('input')
    //     // input_hecter.type="number"
    //     // input_hecter.id="input_hecter"
    //     // let label_hecter=document.createElement('label')
    //     // label_hecter.for='input_hecter'    
    //     // label_hecter.textContent='Hecter'
    //     // div3.appendChild(divS)
    //     // divS.appendChild(label_hecter)
    //     // divS.appendChild(input_hecter)

    //     // let divT = document.createElement('div')         
    //     // divT.id='acre'       
    //     // divT.classList.add("col-md-2")    
    //     // let input_acre=document.createElement('input')
    //     // input_acre.type="number"
    //     // input_acre.id="input_acre"
    //     // let label_acre=document.createElement('label')       
    //     // label_acre.for='input_acre'    
    //     // label_acre.textContent='Acre'
    //     // div3.appendChild(divT)
    //     // divT.appendChild(label_acre)
    //     // divT.appendChild(input_acre)

    //     // let divU = document.createElement('div')         
    //     // divU.id='SqMeter' 
    //     // divU.classList.add("col-md-2")    
    //     // let input_SqMeter=document.createElement('input')
    //     // input_SqMeter.type="number"
    //     // input_SqMeter.id="input_SqMeter"
    //     // let label_SqMeter=document.createElement('label')        
    //     // label_SqMeter.for='input_SqMeter'    
    //     // label_SqMeter.textContent='Square-Meter'
    //     // div3.appendChild(divU)
    //     // divU.appendChild(label_SqMeter)
    //     // divU.appendChild(input_SqMeter)

    //     // let divV = document.createElement('div')         
    //     // divV.id='SqFeet' 
    //     // divV.classList.add("col-md-2")    
    //     // let input_SqFeet=document.createElement('input')
    //     // input_SqFeet.type="number"
    //     // input_SqFeet.id="input_SqFeet"
    //     // let label_SqFeet=document.createElement('label')        
    //     // label_SqFeet.for='input_SqFeet'    
    //     // label_SqFeet.textContent='Square-Feet'
    //     // div3.appendChild(divV)
    //     // divV.appendChild(label_SqFeet)
    //     // divV.appendChild(input_SqFeet)  
    //     // form_container.appendChild(div3)

    //     // modal_footer.appendChild(refresh_btn)        

    //     // modal_body.appendChild(form_container)
    //     // modal_header.appendChild(header_text)
    //     // modal_header.appendChild(close)
    //     // modal_content.appendChild(modal_header)
    //     // modal_content.appendChild(modal_body)
    //     // modal_content.appendChild(modal_footer)
    //     // modal_dialog.appendChild(modal_content)
    //     // modal.appendChild(modal_dialog)
    //     // body.appendChild(modal)

    //     //event listeners
    //     // document.getElementById('refresh_all').addEventListener('click',()=>{
    //     //      document.getElementById('form_container_id').reset();
           
    //     // });          

    //     // document.getElementById('close-area-conversion-view-modal').addEventListener('click',()=>{
    //     //     this.closeTree();
    //     // });       
          
    //     // document.getElementById('rapd').addEventListener("change", ()=>{
    //     //     var Ropani = document.getElementById('input_ropani').value;   
    //     //     var Aana = document.getElementById('input_aana').value;   
    //     //     var Paisa = document.getElementById('input_paisa').value;   
    //     //     var Dam = document.getElementById('input_dam').value;   

    //     //     var R_Sf = area_conversion.RopaniToSquareFeet(Ropani);
    //     //     var A_Sf = area_conversion.AnnaToSquareFeet(Aana);
    //     //     var P_Sf = area_conversion.PaisaToSquareFeet(Paisa);
    //     //     var D_Sf = area_conversion.DamToSquareFeet(Dam);
            
    //     //     var total_Sf = R_Sf + A_Sf + P_Sf + D_Sf ;
    //     //         total_Sf = parseFloat(total_Sf).toFixed(4);
    //     //         squarefeettoall(total_Sf)

    //     // });

    //     // document.getElementById('bkdkk').addEventListener("change", ()=>{
    //     //     var Bigha = document.getElementById('input_bigha').value;   
    //     //     var Kattha = document.getElementById('input_kattha').value;   
    //     //     var Dhur = document.getElementById('input_dhur').value;   
    //     //     var Kanwa = document.getElementById('input_kanwa').value;   
    //     //     var Kanwain = document.getElementById('input_kanwain').value; 

    //     //     var Bigha_Sf = area_conversion.BighaToSquareFeet(Bigha);
    //     //     var Kattha_Sf = area_conversion.KathaToSquareFeet(Kattha);
    //     //     var Dhur_Sf = area_conversion.DhurToSquareFeet(Dhur);
    //     //     var Kanwa_Sf = area_conversion.KanwaToSquareFeet(Kanwa);
    //     //     var Kanwain_Sf = area_conversion.KanwainToSquareFeet(Kanwain);

    //     //     var total_Bsf = Bigha_Sf + Kattha_Sf + Dhur_Sf + Kanwa_Sf + Kanwain_Sf;
    //     //     total_Bsf = parseFloat(total_Bsf).toFixed(2);
    //     //     squarefeettoall(total_Bsf)           
    //     // });

    //     // document.getElementById('input_hecter').addEventListener("change", ()=>{
    //     //     var Hecter = document.getElementById('input_hecter').value; 
    //     //     var Hecter_Sf = area_conversion.HecterToSquareFeet(Hecter);           
    //     //     squarefeettoall(Hecter_Sf)            
    //     // });   
    //     // document.getElementById('input_acre').addEventListener("change", ()=>{
    //     //     var Acre = document.getElementById('input_acre').value; 
    //     //     var Acre_Sf = area_conversion.AcerToSquareFeet(Acre);           
    //     //     squarefeettoall(Acre_Sf)            
    //     // });     
    //     // document.getElementById('input_SqMeter').addEventListener("change", ()=>{
    //     //     var SqMeter = document.getElementById('input_SqMeter').value; 
    //     //     var SqMeter_Sf = area_conversion.SquareMeterToSquareFeet(SqMeter);           
    //     //     squarefeettoall(SqMeter_Sf)            
    //     // });     

    //     // document.getElementById('input_SqFeet').addEventListener("change", ()=>{
    //     //     var SqFeet = document.getElementById('input_SqFeet').value; 
    //     //     squarefeettoall(SqFeet)            


    //     // }); 

    //     // activateEventListener()
    //     //     const arrowButtons=document.querySelectorAll('.arrowIcon')
    //     //     arrowButtons.forEach(
    //     //         btn=>{
    //     //             btn.addEventListener('click',(event)=>{
    //     //                 event.target.classList.toggle('fa-rotate-90');
    //     //                 event.target.parentElement.classList.toggle('disabled')
    //     //             })
    //     //         }
    //     //     )

    //     // function squarefeettoall(total_Sf){
    //     //     var sf_h = area_conversion.SquareFeetToHecter(total_Sf);
    //     //     var sf_a = area_conversion.SquareFeetToAcer(total_Sf);
    //     //     var sf_Sm = area_conversion.SquareFeetToSquareMeter(total_Sf);     
    
    //     //     document.getElementById('input_hecter').value = sf_h;  
    //     //     document.getElementById('input_acre').value = sf_a;             
    //     //     document.getElementById('input_SqMeter').value = sf_Sm;              
    //     //     document.getElementById('input_SqFeet').value = total_Sf;   
    
    //     //     var Bsf_bigha = area_conversion.SquareFeetToBighaWithKanwa(total_Sf);  
    //     //     // debugger;
    //     //     document.getElementById('input_bigha').value = Bsf_bigha._bigha;   
    //     //     document.getElementById('input_kattha').value = Bsf_bigha._kattha;   
    //     //     document.getElementById('input_dhur').value = Bsf_bigha._dhur;   
    //     //     document.getElementById('input_kanwa').value = Bsf_bigha._kanwa;   
    //     //     document.getElementById('input_kanwain').value = Bsf_bigha._kanwain; 
    
    //     //     var Bsf_ropani = area_conversion.SquareFeetToRopaniObj(total_Sf);  
    //     //     document.getElementById('input_ropani').value = Bsf_ropani._ropani;   
    //     //     document.getElementById('input_aana').value = Bsf_ropani._aana;   
    //     //     document.getElementById('input_paisa').value = Bsf_ropani._paisa;   
    //     //     document.getElementById('input_dam').value = Bsf_ropani._dam; 
    
    //     // } 
    // }    


}
AreaConversionViewController.template = "tax_measurement.AreaConversionEvalView"
AreaConversionViewController.components = { Many2OneField,Many2XAutocomplete,FloatField  }
//AreaConversionViewController.supportedTypes = ["char"]

registry.category("fields").add("area_conversion",  AreaConversionViewController)

class area_conversion
{

static  RopaniToSquareFeet(Ropani) {
    if (Ropani) {
        var SqFeet = 0;
        if (Ropani < 1)
            SqFeet = (5476 * Ropani).toFixed(4);
        else
            SqFeet = (5476 * Ropani).toFixed(4);

        return Number(SqFeet);
    }
    return 0;
}
static AnnaToSquareFeet(anna) {
    if (anna) {
        var SqFeet = (342.25 * anna).toFixed(4);
        return Number(SqFeet);
    }
    return 0;
}
static PaisaToSquareFeet(paisa) {
    if (paisa) {
        var SqFeet = (85.56 * paisa).toFixed(4);
        return Number(SqFeet);
    }
    return 0;
}
static DamToSquareFeet (dam)
{ 
    if (dam) {
        var SqFeet = (21.39 * dam).toFixed(4);
        return Number(SqFeet);
    }
    return 0;
}

/*bigha calculation*/

static BighaToSquareFeet(Bigha) {
    if (Bigha) {
        var SqFeet = 0;
        SqFeet = (72900 * Bigha);
        return Number(SqFeet);
    }
    return 0;

}
static KathaToSquareFeet(Katha) {
    if (Katha) {
        var SqFeet = 0;
        SqFeet = (3645 * Katha);
        return Number(SqFeet);
    }
    return 0;
}
static DhurToSquareFeet(Dhur) {
    if (Dhur) {
        var SqFeet = (182.25 * Dhur).toFixed(4);
        return Number(SqFeet);
    }
    return 0;
}
static KanwaToSquareFeet(Kanwa) {
    if (Kanwa) {
        var SqFeet = (11.390625 * Kanwa).toFixed(4);
        return Number(SqFeet);
    }
    return 0;
}
static KanwainToSquareFeet(Kanwain) {
    if (Kanwain) {
        var SqFeet = (0.7119140625 * Kanwain).toFixed(4);
        return Number(SqFeet);
    }
    return 0;
}

// /*Hector-acre*/

static HecterToSquareFeet(Hecter) {
    if (Hecter) {
        var SqFeet = (107639.104167 * Hecter).toFixed(4);
        return Number(SqFeet);
    }
    return 0;
}
static AcerToSquareFeet(Acer) {
    if (Acer) {
        var SqFeet = (1076.3910417 * Acer).toFixed(4);
        return Number(SqFeet);
    }
    return 0;
}
static SquareMeterToSquareFeet(SquareMeter) {
    if (SquareMeter) {
        var SqFeet = (10.763910417 * SquareMeter).toFixed(5); //92.903 ma 1000 aauni ma point ayera ho
        return Number(SqFeet);
    }
    return 0;
}

// /*Hector-acre*/
static SquareFeetToHecter(SquareFeet) {
    var Hecter = ((1 / 107639.10417) * SquareFeet).toFixed(4);
    return Number(Hecter);
}

static SquareFeetToAcer(SquareFeet) {
    var Acer = ((1 / 1076.3910417) * SquareFeet).toFixed(4);
    return Number(Acer);
}
static SquareFeetToSquareMeter(SquareFeet) {
    var SquareMeter = (0.09290304 * SquareFeet).toFixed(4);
    return Number(SquareMeter);
}

static SquareFeetToRopaniObj(SquareFeet) {
    var me = this;   

    var objRopani = this;    
    var SquareFeet = SquareFeet;

    var d_ropani = (SquareFeet / 5476);
    if (d_ropani > 0) {
        // var rop = Math.round(d_ropani);
        objRopani._ropani = Math.trunc(d_ropani);

        var d_aana = ((d_ropani - objRopani._ropani) * 16);

        var _aanas = d_aana.toFixed(2)
        objRopani._aana = Math.trunc(_aanas);

        var d_paisa = ((d_aana - objRopani._aana) * 4);
        var paisas = me.customRound(d_paisa, 2);
        // var paisas = d_paisa.toFixed(2)
        var original_paisa = Math.trunc(paisas);
        //objRopani.Paisa = decimal.Truncate(Math.Round(d_paisa, _roundPlace));//-- calcualtion wrong
        objRopani._paisa = Math.abs(original_paisa);

        var d_dam = ((d_paisa - original_paisa) * 4);

        var orginal_dam = Math.round(d_dam, 4);
        // orginal_dam = d_dam.toFixed(2);

        objRopani._dam = Math.abs(orginal_dam);
SquareFeet
        if (objRopani._dam < 0) {
            // LogTrace.WriteInfoLog("Negative Value for daam while converting " + SquareFeet.ToString() + " sq.ft.");
        }
    }
    return objRopani;
}
static SquareFeetToRopaniDEC(SquareFeet) {
    //--1Ropani =5476 SqFeet
    return (SquareFeet / 5476);
}
static SquareFeetToBigha(SquareFeet) {    
    var me = this,
        objBigha = new KhatthaBase();
    //--1Bigah = 72900 SqFeet
    var d_bigha = (SquareFeet / 72900);
    if (d_bigha > 0) {

        /* old new use decimal custome
        objBigha._bigha = Math.trunc(d_bigha);
        var d_kattha = ((d_bigha - objBigha._bigha).toFixed(4) * 20);
        var _tempKattha = d_kattha.toFixed(2);
        objBigha._kattha = Math.trunc(_tempKattha);
        var d_dhur = ((d_kattha - objBigha._kattha) * 20);
        */

        objBigha._bigha = Math.trunc(d_bigha);
        var d_kattha = (me.custome_decimal(new Decimal((d_bigha - objBigha._bigha) * 20), (d_bigha - objBigha._bigha) * 20));
        var _tempKattha = d_kattha.toFixed(4);
        objBigha._kattha = Math.trunc(_tempKattha);
        var d_dhur = (me.custome_decimal(new Decimal((d_kattha - objBigha._kattha) * 20), (d_kattha - objBigha._kattha) * 20));

        objBigha._dhur = d_dhur;

        if (me._roundPlace != 4) {
            //objBigha._dhur = d_dhur.toFixed(me._roundPlace);
            if (d_dhur % 1 != 0) {
                objBigha._dhur = parseFloat(d_dhur.toFixed(me._roundPlace));
            } else {
                objBigha._dhur = parseFloat(d_dhur);
            }
        } else {
            if (d_dhur % 1 != 0) {
                objBigha._dhur = parseFloat(d_dhur.toFixed(4));
            } else {
                objBigha._dhur = parseFloat(d_dhur);
            }
        }
    }
    return objBigha;
}

static SquareFeetToBighaWithKanwa(SquareFeet) {
    var me = this,
        // objBigha = new KhatthaBase();
        objBigha = this;
    //--1Bigah = 72900 SqFeet
    var d_bigha = (SquareFeet / 72900);
    if (d_bigha > 0) {

        /* old new use decimal custome
        objBigha._bigha = Math.trunc(d_bigha);
        var d_kattha = ((d_bigha - objBigha._bigha).toFixed(4) * 20);
        var _tempKattha = d_kattha;
        objBigha._kattha = Math.trunc(_tempKattha);
        var d_dhur = ((d_kattha - objBigha._kattha) * 20);
        */

        objBigha._bigha = Math.trunc(d_bigha);
        var d_kattha = (me.custome_decimal(new Decimal((d_bigha - objBigha._bigha) * 20), (d_bigha - objBigha._bigha) * 20));
        var _tempKattha = d_kattha.toFixed(4);
        objBigha._kattha = Math.trunc(_tempKattha);
        var d_dhur = (me.custome_decimal(new Decimal((d_kattha - objBigha._kattha) * 20), (d_kattha - objBigha._kattha) * 20));
        var d_dhur = d_dhur.toFixed(4);
        // if (GlobalResourses.LAND_AREA_SHOW_KANWA.toString() == 'True')
        //     objBigha._dhur = Math.trunc(d_dhur);
        // else
            objBigha._dhur = d_dhur;

        //var d_kanwa = ((d_dhur - objBigha._dhur) * 4);
        var d_kanwa = (me.custome_decimal(new Decimal((d_dhur - objBigha._dhur) * 4), (d_dhur - objBigha._dhur) * 4));

        if (me._roundPlace != 4) {
            // if (GlobalResourses.LAND_AREA_SHOW_KANWA.toString() == 'True')
                objBigha._kanwa = d_kanwa.toFixed(me._roundPlace);
        } else {
            // if (GlobalResourses.LAND_AREA_SHOW_KANWA.toString() == 'True')
                objBigha._kanwa = d_kanwa.toFixed(4);
        }
    }
    return objBigha;
}
// SquareFeetToBighaWithKanwaDEC(SquareFeet) {
//     //--1Bigah = 72900 SqFeet
//     return (SquareFeet / 72900);
// }
// SquareFeetToBighaWithKanwain(SquareFeet) {

//     var me = this,
//         objBigha = new KhatthaBase();
//     //--1Bigah = 72900 SqFeet
//     var d_bigha = (SquareFeet / 72900);
//     if (d_bigha > 0) {

//         objBigha._bigha = Math.trunc(d_bigha);

//         var d_kattha = (me.custome_decimal(new Decimal((d_bigha - objBigha._bigha) * 20), (d_bigha - objBigha._bigha) * 20));
//         var _tempKattha = d_kattha.toFixed(4);

//         objBigha._kattha = Math.trunc(_tempKattha);
//         var d_dhur = (me.custome_decimal(new Decimal((d_kattha - objBigha._kattha) * 20), (d_kattha - objBigha._kattha) * 20));


//         if (me._roundPlace != 4) {
//             //objBigha._dhur = d_dhur.toFixed(me._roundPlace);
//             if (d_dhur % 1 != 0) {
//                 objBigha._dhur = parseFloat(d_dhur.toFixed(me._roundPlace));
//             } else {
//                 objBigha._dhur = parseFloat(d_dhur);
//             }
//         } else {
//             if (d_dhur % 1 != 0) {
//                 objBigha._dhur = parseFloat(d_dhur.toFixed(4));
//             } else {
//                 objBigha._dhur = parseFloat(d_dhur);
//             }
//         }

//         if (GlobalResourses.LAND_AREA_SHOW_KANWA.toString() == 'True')
//             objBigha._dhur = Math.trunc(objBigha._dhur);
//         else
//             objBigha._dhur = d_dhur;

//         //var d_kanwa = ((d_dhur - objBigha._dhur) * 16);
//         var d_kanwa = (me.custome_decimal(new Decimal((d_dhur - objBigha._dhur) * 16), (d_dhur - objBigha._dhur) * 16));
//         var _tempd_kanwa = d_kanwa.toFixed(4);

//         if (GlobalResourses.LAND_AREA_SHOW_KANWA.toString() == 'True')
//             objBigha._kanwa = Math.trunc(_tempd_kanwa);

//         ///var d_kanwain = ((d_kanwa - objBigha._kanwa) * 16);
//         var d_kanwain = (me.custome_decimal(new Decimal((d_kanwa - objBigha._kanwa) * 16), (d_kanwa - objBigha._kanwa) * 16));

//         if (me._roundPlace != 4) {
//             if (GlobalResourses.LAND_AREA_SHOW_KANWA.toString() == 'True')
//                 objBigha._kanwain = (d_kanwain).toFixed(0);
//         } else {
//             if (GlobalResourses.LAND_AREA_SHOW_KANWA.toString() == 'True')
//                 objBigha._kanwain = (d_kanwain).toFixed(0);
//         }
//     }
//     return objBigha;
// }

// Land_area_convert_string(value, landMeasureUnit) {
//     switch (landMeasureUnit) {
//         case 1:
//             var ropaniobj = AreaConversion.SquareFeetToRopaniObj(value);
//             value = ropaniobj._ropani + '-' + ropaniobj._aana + '-' + ropaniobj._paisa + '-' + ropaniobj._dam;
//             break;
//         case 2:
//             if (SessionData.app_setting.land_area_show_kanwa == true) {
//                 var bighaobj = AreaConversion.SquareFeetToBighaWithKanwain(value);
//                 value = bighaobj._bigha + '-' + bighaobj._kattha + '-' + bighaobj._dhur + '-' + bighaobj._kanwa + '-' + bighaobj._kanwain;

//             } else {
//                 var bighaobj = AreaConversion.SquareFeetToBigha(value);
//                 value = bighaobj._bigha + '-' + bighaobj._kattha + '-' + bighaobj._dhur;
//             }

//             break;
//         case 3:
//             var hectorobj = AreaConversion.SquareFeetToHecter(value);
//             value = hectorobj;
//             break;
//         case 4:
//             var acerobj = AreaConversion.SquareFeetToAcer(value);
//             value = acerobj;
//             break;
//         case 5:
//             var sqaremeterobj = AreaConversion.SquareFeetToSquareMeter(value);
//             value = sqaremeterobj;
//             break;
//         case 6:
//             value = value;
//             break;
//     }
//     return value;
// }
static customRound(number, precision) {
    if (number === 0.9992695398100804) {
        return 1;
    }
    var cusnum = parseInt(number.toPrecision(precision));
    return cusnum;
}
static custome_decimal(obj, default_value) {
    var value = 0;
    var text = '';
    if (obj.e < 0) {
        if (obj.s < 0)
            return 0;

        for (var i = 0; i < Math.abs(obj.e) - 1; i++) {
            text = text + "0";
        }
        value = '0.' + text;
        //add value
        var temp = parseFloat(obj.d[0]);
        value = value + temp; //obj.d[0];
    } else {
        value = default_value;
    }
    return parseFloat(value);
}


}



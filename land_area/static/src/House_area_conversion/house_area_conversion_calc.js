class house_area_conversion_calc {
    static InchToMeter(Inch) {
        var Meter = ((0.304803319025215 / 12) * Inch).toFixed(2);
        return Number(Meter);
    }
    static InchToFeet(Inch) {
        var Feet = (Inch / 12).toFixed(2);
        return Number(Feet);
    }
    static MeterToInch(Meter) {
        var Inch = ((1 / 39.3700787402) * Meter).toFixed(2);
        return Number(Inch);
    }
    static MeterToFeet(Meter) {
        var ObjM=this;
        var calc_feet = ((1 / 0.304803319025215) * Meter);

        if (calc_feet > 0) {
            ObjM._feet = Math.trunc(calc_feet);
    
            var calc_inch = ((calc_feet - ObjM._feet) * 12);
    
            ObjM._inch = calc_inch.toFixed(2);
        }
        return ObjM;
    }

    static Sq_MeterToSq_Feet(Meter) {
        var calc_feet_area = 10.7639;
        return Number(Meter*calc_feet_area).toFixed(2);
    }
    
    static FeetToInch(Feet) {
        var Inch = (Feet * 12).toFixed(2);
        return Number(Inch);
    }

    static Sq_FeetToSq_Meter(Feet) {
        var Meter = 0.092903;
        return Number(Feet*Meter).toFixed(2);
    }

     static FeetToMeter(Feet) {
         var Meter = (0.304803319025215 * Feet).toFixed(2);
         return Number(Meter);
     }
}
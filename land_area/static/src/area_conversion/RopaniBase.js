
     var _ropani= 0;
     var _paisa= 0;
     var _dam= 0;
     var _aana= 0;
    function constructor (ropani, aana, paisa, dam) {
        var me = this;
        if (typeof(ropani) != 'undefined') {
            me._ropani = ropani;
        }
        if (typeof(aana) != 'undefined') {
            me._aana = aana;
        }
        if (typeof(paisa) != 'undefined') {
            me._paisa = paisa;
        }
        if (typeof(dam) != 'undefined') {
            me._dam = dam;
        }
    }
    function toRopaniBase () {
        var me = this,
            temp_paisa = 0,
            temp_aana = 0,
            temp_ropani = 0;

        //Convert To paisa
        temp_paisa = ((me._dam / 4) + me._paisa);
        //Convert To Aana
        temp_aana = ((temp_paisa / 4) + me._aana);
        //Convert To Ropani
        temp_ropani = ((temp_aana / 16) + me._ropani);
        return temp_ropani;
    }
    function RopaniBase (r1, r2) {
        //RopaniBase temp = new RopaniBase();
        temp = new toRopaniBase();
        var addVal = 0;

        temp.Dam = r1._dam + r2._dam;
        if (temp._dam >= 4) {
            temp._dam = temp.__dam - 4;
            addVal = 1;
        } else
            addVal = 0;

        temp._paisa = r1._paisa + r2._paisa + addVal;
        if (temp._paisa >= 4) {
            temp._paisa = temp._paisa - 4;
            addVal = 1;
        } else
            addVal = 0;

        temp.Aana = r1._aana + r2._aana + addVal;
        if (temp._aana >= 16) {
            temp._aana = temp._aana - 16;
            addVal = 1;
        } else
            addVal = 0;

        temp.Ropani = r1._ropani + r2._ropani + addVal;
        return temp;
    }

    function CompareTo (other) {
        var me = this;
        if (me.toRopaniBase() == other.toRopaniBase())
            return 0;
        else if (me.toRopaniBase() > other.toRopaniBase())
            return 1;
        else
            return -1;
    }

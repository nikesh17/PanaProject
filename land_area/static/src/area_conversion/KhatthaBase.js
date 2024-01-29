
	 var _bigha=0;
	 var _kattha=0;
	 var _dhur=0;
	 var _kanwa=0;
	 var _kanwain=0;

	 function constructor(bigha, kattha, dhur, kanwa, kanwain) {
		var me = this;
		me._bigha = bigha || 0;
		me._kattha = kattha || 0;
		me._dhur = dhur || 0;
		me._kanwa = kanwa || 0;
		me._kanwain = kanwain || 0;
	}
	function toKatthaBase () {
		var me = this,
			temp_dhur = 0,
			temp_kattha = 0,
			temp_kanwa = 0;

			temp_kanwa = (me._kanwain / 16) + me._kanwa;
			temp_dhur = (temp_kanwa / 16) + me._dhur;
			temp_kattha = (temp_dhur / 20) + me._kattha;

			temp_kattha = me.custome_decimal(new Decimal(temp_kattha),temp_kattha);

		if (me._bigha !== 0) 
		{
			 temp_kattha = me._bigha * 20 + temp_kattha;
		}
		return temp_kattha;
	}
	function toBighaBase () {
		var me = this,
			temp_kanwa = 0,
			temp_dhur = 0,
			temp_kattha = 0,
			temp_bigha = 0;
			temp_kanwa = (me._kanwain / 16) + me._kanwa;
			temp_dhur = (temp_kanwa / 16) + me._dhur;
			temp_kattha = (temp_dhur / 20) + me._kattha;

			temp_kattha = me.custome_decimal(new Decimal(temp_kattha), temp_kattha);
			temp_bigha = (temp_kattha / 20) + me._bigha;
		return temp_bigha;
	}
	function KhatthaBase (r1, r2) {
		temp = {};
		temp.Kanwain = this._Kanwain;
		temp.Kanwa = this._Kanwa;
		temp.Dhur = this._Dhur;
		temp.Kattha = this._Kattha;
		temp.Bigha = this._Bigha;

		var addVal = 0;

		temp.Kanwain = r1.Kanwain + r2.Kanwain;
		if (temp.Kanwain >= 4) {
			temp.Kanwain = temp.Kanwain - 4;
			addVal = 1;
		} else {
			addVal = 0;
		}

		temp.Kanwa = r1.Kanwa + r2.Kanwa;
		if (temp.Kanwa >= 4) {
			temp.Kanwa = temp.Kanwa - 4;
			addVal = 1;
		} else
			addVal = 0;

		temp.Dhur = r1.Dhur + r2.Dhur + addVal;
		if (temp.Dhur >= 20) {
			temp.Dhur = temp.Dhur - 20;
			addVal = 1;
		} else
			addVal = 0;

		temp.Kattha = r1.Kattha + r2.Kattha + addVal;
		if (temp.Kattha >= 20) {
			temp.Kattha = temp.Kattha - 20;
			addVal = 1;
		} else
			addVal = 0;

		temp.Bigha = r1.Bigha + r2.Bigha + addVal;
		return temp;
	}
	function ToString () {
		var me = this,
			retStr;// = new String();
		retStr.concat(me._bigha.toString('0'));
		retStr.concat("-");
		retStr.concat(me._kattha.toString('0'));
		retStr.concat("-");

		if (GlobalResourses.LAND_AREA_SHOW_KANWA.toString() == '0') {
			if (me._kanwa > 0) {
				retStr.Append("-");
				retStr.Append(_kanwa.toString("0"));
			}
			if (me._kanwain > 0) {
				retStr.concat("-");
				retStr.concat(me._kanwain.toString("0.00"));
			}
		} else {
			retStr.concat("-");
			retStr.concat(me._kanwa.toString("0"));
			retStr.concat("-");
			retStr.concat(me._kanwain.toString("0"));
		}
		return retStr.toString();
	}
	function ToBigaKathaDhur () {
		var me = this,
			retStr;// = new String();
		retStr.concat(me._bigha.toString("0"));
		retStr.concat("-");
		retStr.concat(me._kattha.toString("0"));
		retStr.concat("-");
		retStr.concat(Math.trunc(me._dhur).toString("0"));
		//--Commented Since Kanwain included
		if (GlobalResourses.LAND_AREA_SHOW_KANWA.toString() == '0') {
				var _dhurInitial = (me._dhur.toString("0.00")).toFixed(2),
				_dhurTmp = Math.trunc(me._dhur),
				_kanwaTmp = (_dhurInitial - _dhurTmp);

				if (_kanwaTmp == 0.025) {
					retStr.concat("1/4");
				} else if (_kanwaTmp == 0.50) {
					retStr.concat("1/2");
				} else if (_kanwaTmp == 0.75) {
					retStr.concat("3/4");
				} else {
					var newval = [];
					newval = _kanwaTmp.toString().split('.');
					var SecVal;
					if (newval.length > 1) {
						SecVal = newval[1];
					} else {
						SecVal = "00";
					}
					retStr.concat("." + SecVal);
				}
		}
		else {
			retStr.concat("-");
			retStr.concat(me._kanwa.toString("0"));
			retStr.concat("-");
			retStr.concat(me._kanwain.toString("0.00"));
		}
		return retStr.toString();
	}
	function ToBigaKathaDhurKanwai (){
		var me=this,		
		retStr;// = new String();
		
		//retStr.Remove(0, retStr.Length);
		retStr.concat(me._bigha.toString("0"));
		retStr.concat("-");
		retStr.concat(me._kattha.toString("0"));
		retStr.concat("-");
		retStr.concat(Math.trunc(me._dhur).toString("0"));

		var _dhurInitial = (_dhur.toString()).toFixed(2),
		_dhurTmp = Math.trunc(me._dhur),
		_kanwaTmp = _dhurInitial - _dhurTmp;

		if (_kanwaTmp == 0.25)
		{
		   retStr.concat("1/4");
		}
		else if (_kanwaTmp == 0.50)
		{
		   retStr.concat("1/2");
		}
		else if (_kanwaTmp == 0.75)
		{
		   retStr.concat("3/4");
		}
		else
		{
		   var newval=[];
		   newval = _kanwaTmp.toString().split('.');
		   var SecVal;
		   if (newval.Length > 1)
		   {
		       SecVal = newval[1];
		   }
		   else
		   {
		       SecVal = "00";
		   }
		   retStr.concat("." + SecVal);
		}

		return retStr.toString();
	}
	function CompareTo (other) {
		if (this.toKatthaBase() == other.toKatthaBase())
			return 0;
		else if (this.toKatthaBase() > other.toKatthaBase())
			return 1;
		else
			return -1;

	}

     function custome_decima (obj, default_value)
    {
        var value=0;
        var text='';
        if (obj.e <0)
        {
          if (obj.s<0)
            return 0;
                    
            for (var i = 0;i< Math.abs(obj.e)-1;i++)
            {
                text=text+"0";
            }
            value='0.' + text;
            //add value
            var temp = parseFloat(obj.d[0]);
            value = value + temp; //obj.d[0];
        }
        else
        {
            value = default_value;
        }
        return parseFloat(value);
    }
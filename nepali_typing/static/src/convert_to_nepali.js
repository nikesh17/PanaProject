odoo.define('nepali_typing.nepali_typing',async function(require){
	"use strict";
	let core = require('web.core');
	let ajax = require('web.ajax');
	let rpc = require('web.rpc');
    var session = require('web.session');
	let QWeb = core.qweb;
	let _t = core._t;

    let fonts = ['preeti','pcs nepali','kantipur'];


    function Convert(text,font,char_map,post_rules) {
        if(font=='english'){
          return text;
        }
        font = font.toLowerCase();
      
        var output = '';
        for (var w = 0; w < text.length; w++) {
          var letter = text[w];
          output += char_map[letter] || letter;
        }
        for (var r = 0; r < post_rules.length; r++) {
          output = output.replace(new RegExp(post_rules[r][0], 'g'), post_rules[r][1]);
        }
        return output;
    }

    async function readData(model,domain=[],value=['id','display_name']){
        let data = await rpc.query({
            model: model,
            method: 'search_read',
            args: [domain,value],
        });
        return data;
    }

    let char_map,post_rules;

    let keyboards = await readData('user.keyboard',[],['id','display_name','name','char_map','post_rules'])
    let rules = {};
    keyboards.forEach(each => {
        rules[each['name'].toLowerCase()]={
            'name': each['name'],
            'char_map': JSON.parse(each['char_map']),
            'post_rules': JSON.parse(each['post_rules']),
        }
    });
    document.addEventListener("input",async (event) => {
        // let font = 'preeti';
        if (event.target.type === "text" && event.target.id.indexOf("date") === -1 && event.target.className.indexOf("o_datepicker_input") === -1){
            let data = await readData('res.users',[['id','=',session.uid]],['id','display_name','prefered_keyboard'])
            let font = data[0]['prefered_keyboard'][1]
            if(!font)
                font='english'
            if(font.toLowerCase()=='english'){
                return true
            }
            // let keyboard_id = data[0]['prefered_keyboard'][0]
            // let keyboard = await readData('user.keyboard',[['id','=',keyboard_id]],['id','display_name','name','char_map','post_rules'])

            if(rules[font.toLowerCase()]['char_map'])
                char_map = rules[font.toLowerCase()]['char_map'];
            else
                char_map = {};
            if(rules[font.toLowerCase()]['post_rules'])
                post_rules = rules[font.toLowerCase()]['post_rules'];
            else
                post_rules = [];
            let text = event.target.value;
            let convert = Convert(text,font,char_map,post_rules);
            event.target.value = convert;
            return true;
        }
    });
})


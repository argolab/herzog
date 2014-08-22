define(function(require, exports, module){

var tpler = {};

function tmpl(fmt, data, buf){
    var html =
        (typeof fmt == "function") ?
        fmt(data) :
        fmt.replace(/{(\w+|\$)(?:\|(\w+))?}/g, function(all, name, tpl){
            return tpl ?
                ((tpler[tpl] == "function") ?
                 tpler[tpl](name==='$'?data:data[name]) :
                 tmpl(tpler[tpl], name==='$'?data:data[name])) :
            name==='$'?data:data[name];
        });
    return buf ? (buf.push(html), buf) : html;
}

tpler.title = '<input type="text" data-name="title" value="{$}" class="title-inputer" />';
tpler.text = '<textarea data-name="text" class="text-inputer">{$}</textarea>';
tpler.img = '<input type="text" data-name="img" value="{$}" class="img-inputer" />';
tpler.href = '<input type="text" data-name="href" value="{$}" class="href-inputer" />';

var field_name = {
    title : '文字',
    text : '文本',
    img : '图片',
    href : '链接',
    list : '清单'
}

tpler.item = function(data){
    var buf = tmpl('<div class="item" data-type="item" data-name>', null, []);
    for(var name in data){
        if(data.hasOwnProperty(name)){
            var part = data[name];
            tmpl('<div class="part" data-type="part" data-name="{$}"><div class="partname">{$}</div><div class="fields">', name, buf);
            ['title', 'href', 'img', 'text', 'list'].forEach(function(type){
                if(part.hasOwnProperty(type)){
                    tmpl('<span class="field field-'+type+'">' + field_name[type] + ' : ', null, buf);
                    tmpl(tpler[type], part[type], buf);
                    tmpl('</span>', null, buf);
                }
            });
            if(part.hasOwnProperty('desc')){
                tmpl('<div class="desc">{desc}</div>', part, buf);
            }
            tmpl('</div></div>', null, buf);
        }
    }
    buf.push('</div>')
    return buf.join('');
}

tpler.list = function(data){
    var buf = tmpl('<div class="list-inputer" data-type="list" data-name="list">', null, []);
    data.forEach(function(item){
        tmpl('<div class="item-wrapper">', null, buf);
        tmpl(tpler.item, item, buf);
        tmpl('<a href="javascript:;" class="item-remove" data-action="remove">移除</a></div>', null, buf);
    });
    tmpl('<a href="javascript:;" class="item-add" data-action="add">添加</a></div>', null, buf);
    return buf.join('');
}

tpler.ResourceEditor = function(data){
    var buf = tmpl('<div class="resource-editor">', null, []);
    tmpl(tpler.item, data, buf);
    tmpl('</div>', null, buf);
    return buf.join('');
}

var f = document.createElement('div');
function html2node(html){
    f.innerHTML = html;
    return f.childNodes[0];
}

function ResourceEditor(root){
    this._root = root;
    var self = this;
    var onaction = function(e){ return self.onaction(e); };
    root.addEventListener('click', onaction);
}

function rf(start){
    do{
        start = start.parentNode;
    }while(start && !start.hasOwnProperty('_repdata'));
    return start;
}

rep = ResourceEditor.prototype;

rep.bind = function(data){
    this._root.innerHTML = tmpl(tpler.ResourceEditor, data);
}

rep.dump = function(){
    var ds = this._root.querySelectorAll('[data-name]');
    var data = ds[0]._repdata = {};
    for(var i=1; i<ds.length; ++i){
        var d = ds[i];
        var name = d.getAttribute('data-name');
        var type = d.getAttribute('data-type');
        if(type == 'part'){
            d._repdata = rf(d)._repdata[name] = {};
        }else if(type == 'list'){
            d._repdata = rf(d)._repdata[name] = [];
        }else if(type == 'item'){
            d._repdata = {};
            rf(d)._repdata.push(d._repdata);
        }else{
            rf(d)._repdata[name] = d.value;
        }
    }
    return data;
}    

rep.onaction = function(e){
    var target = e.target;
    var action = target.getAttribute('data-action');
    if(action == 'add'){
        target.parentNode.insertBefore(
            target.parentNode.childNodes[0].cloneNode(),
            target);
    }
    else if(action == 'remove'){
        if(target.parentNode.parentNode.childNodes.length > 2){
            target.parentNode.remove();
        }else{
            alert('不能移除最后一个项！');
        }
    }
}

var allatts = {
    title : true,
    text : true,
    href : true,
    img : true,
    desc : true,
    list : true
};

ResourceEditor.verify = function(data){
    var key;
    if(!(typeof data == 'object')){
        throw {
            error : 'No a object',
            data : data
        }
    }
    for(key in data){
        if(data.hasOwnProperty(key)){
            var fields = data[key];
            if(!(typeof fields=="object")){
                throw {
                    error : 'No a object fields',
                    key : key,
                    fields : fields
                }
            }
            for(var attr in fields){
                if(fields.hasOwnProperty(attr)){
                    if(!allatts.hasOwnProperty(attr)){
                        throw {
                            error : 'unknow attr',
                            attr : attr,
                            data : data
                        }
                    }
                    if(attr == 'list'){
                        var lists = fields[attr];
                        for(var i=0; i<lists.length; ++i){
                            ResourceEditor.verify(lists[i]);
                        }
                    }
                }
            }
        }
    }
    return true;                    
}

exports = module.exports = ResourceEditor;

});

// re = (new ResourceEditor(document.body));
// re.bind({
//     '站点名称' : {
//         title : 'ABC',
//         href : '#',
//         img : 'img',
//         desc: '说明文字',
//         list : [
//             {
//                 '站点名称' : {
//                          title : 'ABC',
//                          href : '#',
//                          img : 'img',
//                          desc: '说明文字',
//                 }
//             }
//         ]
//     }
// });

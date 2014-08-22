define(function(require, exports, module){

    require('jquery');
    var Form = require('form');
    
    $(function(){
        ResourceEditor = require('ResourceEditor');
        try{
            ResourceEditor.verify(INIT_DATA);
        }catch(e){
            alert(e.error);
            console.error(e);
            throw e;
        }
        
        re = (new ResourceEditor(document.getElementById('re')));
        re.bind(INIT_DATA);

        new Form({
            el : '#box',
            cookParams : function(params){
                var ds = re.dump();
                try{
                    ResourceEditor.verify(ds);
                }catch(e){
                    alert(JSON.stringify(e));
                    throw e;
                };
                params.ds = JSON.stringify(ds);
            },
            onsuccess : function(data){
                alert('添加成功！');
                location = '/page/manage';
            },
            onfail : function(data){
                console.log(data);
                alert(data.msg);
            }
        });
        
    });
        
});

define(function(require, exports, module){

    require('jquery');

    var ResourceEditor = require('ResourceEditor');

    var Form = require('form');
    var handler = {
        more : function(data, t){
            t.parent().parent().addClass('open');
            t.parent().remove();
        }
    }
    $('body').click(function(e){
        if(e.target.hasAttribute('data-do')){
            e.preventDefault();
            var e = $(e.target);
            handler[e.data('do')](e.data(), e);
        }else if((e.target.tagName == 'SPAN') &&
                 (e.target.parentNode.hasAttribute('data-do'))){
            e.preventDefault();
            var e = $(e.target.parentNode);
            handler[e.data('do')](e.data(), e);
        }
    });
    $(function(){
        new Form({
            el : '#add-resource',
            cookParams : function(params){
                try{
                    ResourceEditor.verify($.parseJSON(params.ds));
                }catch(e){
                    alert(JSON.stringify(e));
                    throw e;
                };
            },
            onsuccess : function(data){
                alert('添加成功！');
                location.reload(true);
            },
            onfail : function(data){
                console.log(data);
                alert(data.msg);
            }
        });
    });

});

define(function(require, exports, module){
    require('jquery');
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
            el : '#editor-newpost',
            cookParams : function(params){
                params.content = this.el.find('div.editarea').html();
            },
            onsuccess : function(data){
                location.href = "/t/" + data.tid;
            },
            onfail : function(data){
                console.log(data);
                alert(data.msg);
            }
        });
        $('#inputer-title').focus();
    });
});


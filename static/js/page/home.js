define(function(require, exports, module){
    require('jquery');
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
    
});


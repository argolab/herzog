define(function(require, exports, module){
    require('jquery');
    var handler = {
        "go-tab" : function(data, t){
            $("div.mod-sections-tabs a.text-iter").removeClass("text-iter");
            t.addClass("text-iter");
            $("div.mod-sections-tabs div.open").removeClass("open");
            $("#tab-"+data.secnum).addClass("open");
            location.hash = "t-" + data.secnum;
        },
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
    (function(){
        var str = location.hash;
        var m = str.match(/t-(\d)/);
        if(m){
            $('#tb-'+m[1]).click();
        }else{
            $('#tb-0').click();
        }
    })();    
});


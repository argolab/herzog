define(function(require, exports, module){

    require('jquery');

    var WidgetClass = require('widget');

    var ReplyEditer = WidgetClass({
        _events : {
            'div.submit' : {
                'click' : function(e, target){
                }
            }
        }
    });

    new ReplyEditer({
        el : '#editor-reply'
    });
    
});

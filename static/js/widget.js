define(function(require, exports, module){

    require('jquery');
    var template = require('artTemplate');

    function BaseWidget(){}

    BaseWidget.prototype = {
        buildElement : function(options){
            this._options = options;
            if(options._container){
                this.el = (this.render == "function") ?
                    this.render(options, options._container) :
                    $((options._tpl ?
                       template(options._tpl, options) :
                       template.render(this.render, options))) ;
                this.el.appendTo($(options._container));                        
            }else{
                this.el = $(options.el);
            }
            this.listen_event();
        },
        render : '',
        listen_event : function(){
            var e = this._options._events || this._events;
            var self = this;
            if(e){
                for(var k in e){
                    if(e.hasOwnProperty(k)){
                        var d = this.el.find(k);
                        var es = e[k];
                        for(var n in es){
                            if(es.hasOwnProperty(n)){
                                (function(){
                                    var f = es[n];
                                    d.on(n, function(e){
                                        return f.call(self, e, this);
                                    });
                                })();
                            }
                        }
                    }
                }
            }
        },
    }

    function WidgetClass(new_methods){
        function Widget(options){
            this._options = null;
            this.buildElement(options);
        }
        Widget.prototype = new BaseWidget;
        Widget.prototype.constructor = Widget;
        $.extend(Widget.prototype, new_methods);
        return Widget;
    }

    module.exports = WidgetClass;
    
});

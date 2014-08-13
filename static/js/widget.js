define(function(require, exports, module){

    require('jquery');
    var template = require('artTemplate');

    function BaseWidget(){}

    BaseWidget.prototype = {
        beforeBuild : null,
        afterBuild : null,
        buildElement : function(options){
            if(this.beforeBuild){
                this.beforeBuild(options);
            }
            this._options = options;
            if(options._container){
                this.el = (this.render == "function") ?
                    this.render(options, options._container) :
                    jQuery((options._tpl ?
                       template(options._tpl, options) :
                       template.render(this.render, options))) ;
                this.el.appendTo(jQuery(options._container));                        
            }else{
                this.el = jQuery(options.el);
            }
            this.listen_event();
            if(this.afterBuild){
                this.afterBuild();
            }
        },
        render : '',
        _setupFromOptions : function(arr){
            for(var i=0; i<arr.length; ++i){
                if(this._options.hasOwnProperty(arr[i])){
                    this[arr[i]] = this._options[arr[i]];
                }
            }
        },
        listen_event : function(base){
            var e = this._options._events || this._events;
            var self = this;
            var base = base || this.el;
            if(e){
                for(var k in e){
                    if(e.hasOwnProperty(k)){
                        var d = base.find(k);
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
        jQuery.extend(Widget.prototype, new_methods);
        return Widget;
    }

    module.exports = WidgetClass;
    
});

define(function(require, exports, module){

    var WidgetClass = require('widget');

    var Form = WidgetClass({
        validator : {
        },
        _events : {
            '[name]' : {
                'change' : function(e, target){
                    var name = $(target).attr('name');
                    if(this.validator.hasOwnProperty(name)){
                        if(!this.validator[name].apply(this, target)){
                            this.disableSubmit();
                        }
                    }
                }
            },
            'form' : {
                'submit' : function(e, target){
                    e.preventDefault();
                    this.submit();
                }
            },
            '.submit' : {
                'click' : function(e, target){
                    e.preventDefault();
                    this.submit();
                }
            }
        },
        afterBuild : function(){
            this._setupFromOptions(['onsuccess', 'onfail', 'onstartpost', 'onafterpost', 'disableSubmit', 'enableSubmit', 'cookParams']);
        },
        disableSubmit : function(){
        },
        enableSubmit : function(){
        },
        dumpField : function(d){
            console.log(d);
            if(typeof d == 'string'){
                d = this.el[0].getElementsByName(d);
            }
            return d.value;
        },
        submit : function(){
            var action = this.el.data('action') || this._options.action
                || this.el.attr('action');
            if(!action){
                return;
            }
            var params = {};
            var self = this;
            self.el.find('[name]').each(function(index, element){
                params[$(element).attr('name')] = self.dumpField(element);
            });
            if(self.cookParams){
                params = self.cookParams.call(this, params) || params;
            }
            self.disableSubmit();
            if(self.onstartpost){
                self.onstartpost();
            }
            $.post(action, params, function(data){
                if(data.success){
                    self.onsuccess(data);
                }else{
                    self.onfail(data);
                }
                if(self.onfinishpost){
                    self.onfinishpost(data);
                }
                self.enableSubmit();
            });
        }
    });

    module.exports = Form;

})

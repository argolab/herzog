define(function(require, exports, module){

    require('jquery');
    var Form = require('form');
    var template = require('artTemplate');

    $('#reset-reply').click(function(){
        $('#editarea-reply').html('').focus();
    });

    $(function(){
        new Form({
            el : '#editor-reply',
            cookParams : function(params){
                params.tid = this.el.data('tid');
                params.content = this.el.find('div.editarea').html();
            },
            onsuccess : function(data){
                console.log('reply success %s', this.el.data('tid'),
                            data);
                $.get(this.el.data('fetch'),
                      { rid : data.rid },
                      function(data){
                          console.log('fetch---', data);
                          console.log(template('tpl-reply', data));
                          var d = $(template('tpl-reply', data));
                          d.appendTo('#replys');
                          $('html, body').animate({
                              scrollTop: d.offset().top
                          }, 1000);
                          $('#editarea-reply').html('');
                      });
                this.el.find('div.editarea').html('');                    
            },
            onfail : function(data){
                console.log(data);
                alert(data.msg);
            }
        });
    });
    
});

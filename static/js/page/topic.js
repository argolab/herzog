define(function(require, exports, module){

    require('jquery');
    var Form = require('form');
    var template = require('artTemplate');

    $('#reset-reply').click(function(){
        $('#editarea-reply').html('').focus();
    });

    $.fn.focusEnd = function() {
        $(this).focus();
        var tmp = $('<span />').appendTo($(this)),
        node = tmp.get(0),
        range = null,
        sel = null;

        if (document.selection) {
            range = document.body.createTextRange();
            range.moveToElementText(node);
            range.select();
        } else if (window.getSelection) {
            range = document.createRange();
            range.selectNode(node);
            sel = window.getSelection();
            sel.removeAllRanges();
            sel.addRange(range);
        }
        tmp.remove();
        return this;
    }
    
    function cancelComment(rid){
        var comments = $('#reply-' + rid + ' div.comments');
        if(comments.hasClass('has-editor')){
            comments.removeClass('has-editor');
            comments.find('.editor-comment').remove();
            return;
        }
    }

    function comment(rid, data){
        var comments = $('#reply-' + rid + ' div.comments');
        if(comments.hasClass('has-editor')){
            return;
        }
        var d = $(template('tpl-comment-editor', data)).appendTo(comments);
        console.log(d);
        comments.addClass('has-editor');
        d.find('div.editarea').focusEnd();
        return new Form({
            el : d,
            cookParams : function(params){
                params.replyid = this.el.data('replyid');
                params.content = this.el.find("div.editarea").html();
            },
            onsuccess : function(data){
                var self = this;
                console.log('comment success %s', this.el.data('replyid'),
                            data);
                $.get(this.el.data('fetch'),
                      { rid : data.rid },
                      function(data){
                          console.log('fetch---', data);
                          var d = $(template('tpl-comment', data));
                          self.el.remove();
                          d.appendTo(comments);
                          $('html, body').animate({
                              scrollTop: d.offset().top - 40
                          }, 500);
                      });
                this.el.find('div.editarea').html('');                    
            },
            onfail : function(data){
                console.error(data);
                alert(data.msg);
            }
        });
    }        

    var handler = {
        comment : function(data){
            cancelComment(data.rid);
            comment(data.rid, data);
        },
        cancelComment : function(data){
            var rid = data.rid;
            cancelComment(rid);
        },
        postComment : function(data){
            var rid = data.rid;
            var comments = $('#reply-' + rid + ' div.comments');
        },
        commentComment : function(data){
            var brid = data.brid;
            cancelComment(brid);
            comment(data.brid, data);
        },
        good : function(data, e){
            data = data.tid ? { tid : data.tid } : { rid : data.rid }
            $.post('/ajax/post/upvote', data,
                   function(data){
                       if(data.success){
                           e.removeClass('good').addClass('ungood').data('do', 'ungood');
                           var num = e.find('span.n');
                           num.text(+num.text() +1);
                           e.find('span.t').text('已赞');
                       }
                   });
        },
        ungood : function(data, e){
            data = data.tid ? { tid : data.tid } : { rid : data.rid }
            $.post('/ajax/post/unvote', data,
                   function(data){
                       if(data.success){
                           e.removeClass('ungood').addClass('good').data('do', 'good');
                           var num = e.find('span.n');
                           num.text(+num.text() -1);
                           e.find('span.t').text('赞');
                       }
                   });
        },
        star : function(data, e){
            data = data.tid ? { tid : data.tid } : { rid : data.rid }
            $.post('/ajax/post/star', data,
                   function(data){
                       if(data.success){
                           e.removeClass('star').addClass('unstar').data('do', 'unstar');
                           e.find('span.t').text('已关注');
                       }
                   });
        },
        unstar : function(data, e){
            data = data.tid ? { tid : data.tid } : { rid : data.rid }
            $.post('/ajax/post/unstar', data,
                   function(data){
                       if(data.success){
                           e.removeClass('unstar').addClass('star').data('do', 'star');
                           e.find('span.t').text('关注');
                       }
                   });
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
                          var d = $(template('tpl-reply', data));
                          d.appendTo('#replys');
                          $('html, body').animate({
                              scrollTop: d.offset().top - 40
                          }, 500);
                          $('#editarea-reply').html('');
                      });
                this.el.find('div.editarea').html('');                    
            },
            onfail : function(data){
                console.error(data);
                alert(data.msg);
            }
        });
    });
    
});

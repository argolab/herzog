seajs.config({
    base : '/static/js',
    alias : {
        "jquery" : "jquery/jquery-1.11.1.min",
    },
    map: [
        [".js", ".js?" + new Date().getTime()]
    ],
    debug : true
})
        

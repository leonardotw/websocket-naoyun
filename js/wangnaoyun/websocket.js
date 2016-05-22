;(function(undefined) {
    'use strict';

    var websocketmanager = function(param){
        console.log('Websocket Manager Loaded')
    }
    this.websocketmanager = websocketmanager;
    websocketmanager.prototype.start = function(url,custom_open,custom_message,custom_close,custom_error) {
        var socket = new WebSocket(url);
        var wsinstance = this;
        socket.onopen = function(f){
            if(custom_open != undefined){
              custom_open(f);
            }
        }
        socket.onmessage = function(m){
            if(custom_message != undefined){
             custom_message(m);
            }
        }
        socket.onclose = function(e){ 
            if(custom_close != undefined){
              custom_close(e);
            }
            wsinstance.start();
        }
        socket.onerror = function(e){
            if(custom_error != undefined) {
              custom_error(e);
            }
            socket.close();
            wsinstance.start();
        }
    }
}).call(this);
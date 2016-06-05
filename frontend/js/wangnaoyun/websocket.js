;(function(undefined) {
    'use strict';

    var websocketmanager = function(param){
        console.log('Websocket Manager Loaded')
        var socket = undefined;
    }
   
    this.websocketmanager = websocketmanager;
    websocketmanager.prototype.socket = undefined;
    websocketmanager.prototype.start = function(url,custom_open,custom_message,custom_close,custom_error) {
        this.url = url
        this.socket = new WebSocket(url);
        
        var wsinstance = this;
        this.socket.onopen = function(f){
            if(custom_open != undefined){
              custom_open(f);
            }
        }
        this.socket.onmessage = function(m){
            if(custom_message != undefined){
             custom_message(m);
            }
        }
        this.socket.onclose = function(e){ 
            if(custom_close != undefined){
              custom_close(e);
            }
            wsinstance.start(wsinstance.url,custom_open,custom_message,custom_close,custom_error);
        }
        this.socket.onerror = function(e){
            if(custom_error != undefined) {
              custom_error(e);
            }
            socket.close();
            wsinstance.start(wsinstance.url,custom_open,custom_message,custom_close,custom_error);

        }
    }
}).call(this);

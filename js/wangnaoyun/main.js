;(function(undefined) {
    'use strict';

    var naoyun = function(param){
        console.log('Naoyun Loaded')
    }

    naoyun.prototype.createUser = function(screenName, attributes) {
        return {
                id: screenName,
                label: '@'+ screenName,
                x: Math.random(),
                y: Math.random(),
                size: 10,
                color: '#BB0000',
                type: 'circle',
                active: false/*,
                image: {
                  url: urls[Math.floor(Math.random() * urls.length)],
                  // scale/clip are ratio values applied on top of 'size'
                  scale: 1.3,
                  clip: 0.85
                }*/
              }
    }

    this.naoyun = naoyun;

}).call(this);
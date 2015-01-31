$(function(){
  "use strict";
  var m = {
    init: function(){
      m.tid = null,
      m.interval = null;
      m.bindEvents();
    },
    bindEvents: function(){
      $('#ok').on('click', function(){
        var width = screen.width,
            height = screen.height;
        $.ajax({
          type: 'POST',
          url: '/genimg',
          data: {width: width, height: height}
        }).done(function(data){
          console.log(data);
          if(data.success){
            progressJs().setOptions({overlayMode: true, theme: 'blueOverlay'}).start();
            m.tid = data.task_id;
            m.interval = setInterval(m.checkFinish, 3000);
          }
        });
      });

      $('#save').on('click', function(){
        m.downloadCanvas(this, 'canvas', 'test.png');
      });
    },
    checkFinish: function(){
      $.ajax({
        type: 'GET',
        url: '/task_result/' + m.tid
      }).done(function(data){
        if(data.ready){
          clearInterval(m.interval);

          progressJs().setOptions({overlayMode: true, theme: 'blueOverlay'}).end();

          $('#canvas').show();
          document.getElementById("img").src = '/img/' + m.tid;

          m.loadCanvas('/img/' + m.tid);

        }
        else{
            if (data.current !== 0) progressJs().setOptions({overlayMode: true, theme: 'blueOverlay'}).set(data.current*100)
        }
      });
    },
    loadCanvas: function(dataURL){
      var canvas = document.getElementById('canvas');
      var context = canvas.getContext('2d');

      // load image from data url
      var imageObj = new Image();
      imageObj.onload = function() {
        context.drawImage(this, 0, 0);
      };

      imageObj.src = dataURL;
    },
    downloadCanvas: function(link, canvasId, filename) {
      link.href = document.getElementById(canvasId).toDataURL();
      link.download = filename;
    }
  };

  m.init();
});

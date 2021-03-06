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
          if(data.success){
            progressJs().setOptions({overlayMode: true, theme: 'blueOverlay'}).start();
            m.tid = data.task_id;
            m.interval = setInterval(m.checkFinish, 3000);
          }
        });
      });

      $('#save').on('click', function(){
        // m.downloadCanvas(this, 'canvas', 'test.png');
        var canvas = document.getElementById("canvas"), ctx = canvas.getContext("2d");
        // draw to canvas...
        canvas.toBlob(function(blob) {
          saveAs(blob, "wallpaper.jpg");
        });
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

          // m.loadCanvas('/img/' + m.tid);
          fabric.Image.fromURL('/img/' + m.tid, function(img) {
            var oImg = img.set({ left: 20, top: 10})
            window.canvas.add(oImg).renderAll();
            window.canvas.setActiveObject(oImg);
          });

        }
        else{
            if (+(data.current) !== 0) progressJs().setOptions({overlayMode: true, theme: 'blueOverlay'}).set(data.current*100)
        }
      });
    },
    loadCanvas: function(dataURL){
      var canvas = document.getElementById('canvas');
      var context = canvas.getContext('2d');

      // load image from data url
      var imageObj = new Image();
      imageObj.onload = function() {
        context.drawImage(this, 0, 0, $('#canvas').attr('width'), $('#canvas').attr('height'));
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

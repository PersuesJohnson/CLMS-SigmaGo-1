/* ===========================================================
 * jquery-label_better.js v1.1
 * ===========================================================
 * Copyright 2013 Pete Rojwongsuriya.
 * http://www.thepetedesign.com
 *
 * Label your form input like a boss with 
 * beautiful animation and without taking up space
 *
 * https://github.com/peachananr/label_better
 *
 * ========================================================== */

!function($){
  
  var defaults = {
    position: 'top',
    animationTime: 500,
    easing: "ease-in-out",
    offset: 4,
    hidePlaceholderOnFocus: false
	};
	
  $.fn.animateLabel = function(settings, btn) {
    var position = btn.data("position")  || settings.position,
    posx = 0,
    posy = 0;
    
    
    $(this).css({
      "left": "auto",
      "position": "absolute",
      "-webkit-transition": "all " + settings.animationTime + "ms " + settings.easing,
      "-moz-transition": "all " + settings.animationTime + "ms " + settings.easing,
      "-ms-transition": "all " + settings.animationTime + "ms " + settings.easing,
      "transition": "all " + settings.animationTime + "ms " + settings.easing
    });
    
    switch (position) { 
      case 'top':
        posx = 0;
        posy = ($(this).height() + settings.offset) * -1;
        
        $(this).css({
          "top": "0",
          "opacity": "1",
          "-webkit-transform": "translate3d(" + posx + ", " + posy + "px, 0)", 
          "-moz-transform": "translate3d(" + posx + ", " + posy + "px, 0)", 
          "-ms-transform": "translate3d(" + posx + ", " + posy + "px, 0)", 
          "transform": "translate3d(" + posx + ", " + posy + "px, 0)"
        });
      break;
    }
  }
  
  $.fn.removeAnimate = function(settings, btn) {
    var position = btn.data("position")  || settings.position,
    posx = 0,
    posy = 0;
  
    $(this).css({
      "top": "0",
      "opacity": "0",
      "-webkit-transform": "translate3d(" + posx + ", " + posy + "px, 0)", 
      "-moz-transform": "translate3d(" + posx + ", " + posy + "px, 0)", 
      "-ms-transform": "translate3d(" + posx + ", " + posy + "px, 0)", 
      "transform": "translate3d(" + posx + ", " + posy + "px, 0)"
    });
    
  }
  
  $.fn.label_better = function(options){
    var settings = $.extend({}, defaults, options),
        el = $(this),
        triggerIn = "focus",
        triggerOut = "blur";  
    if(settings.easing == "bounce") settings.easing = "cubic-bezier(0.175, 0.885, 0.420, 1.310)"   
    
    el.each(function( index, value ) {
      var btn = $(this),
          position = btn.data("position")  || settings.position;
      btn.wrapAll("<div class='lb_wrap' style=' position:absolute; right:26vw; display:inline;'></div>")
      
      if( btn.val().length > 0) {
        var text = btn.data("new-placeholder")  || btn.attr("placeholder");
        $("<div class='lb_label " + position + "'>"+ text + "</div>").css("opacity", "0").insertAfter(btn).animateLabel(settings, btn);
      }
      btn.triggerInFunc = function() {
        if(btn.val().length < 1) {
          var text = btn.data("new-placeholder")  || btn.attr("placeholder"),
           position = btn.data("position")  || settings.position;
          $("<div class='lb_label " + position + "'>"+ text + "</div>").css("opacity", "0").insertAfter(btn).animateLabel(settings, btn);
        }
        if (settings.hidePlaceholderOnFocus == true) {
          btn.data("default-placeholder", btn.attr("placeholder"))
          btn.attr("placeholder", "") 
        }
        btn.parent().find(".lb_label").addClass("active");
      };
      btn.triggerOutFunc = function() {
        if(btn.val().length < 1) {
          btn.parent().find(".lb_label").bind("transitionend webkitTransitionEnd oTransitionEnd MSTransitionEnd", function(){ $(this).remove(); }).removeAnimate(settings, btn)
        }
        if (settings.hidePlaceholderOnFocus == true) {
          btn.attr("placeholder", btn.data("default-placeholder")) 
          btn.data("default-placeholder", "")
        }
        btn.parent().find(".lb_label").removeClass("active");
      };
      btn.bind(triggerIn, btn.triggerInFunc).bind(triggerOut, btn.triggerOutFunc);
    });
  }
}(window.jQuery);


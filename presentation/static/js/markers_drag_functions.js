// drag related variables
var dragok = false;
var startX;
var startY;

export function rect(figure) {
    let vertXsum = 0;
    let vertYsum = 0;
    for(var i=1;i<figure.vertexes.length + 1;i++){
        window.ctx.beginPath();
        if(i === figure.vertexes.length){
            window.ctx.moveTo(figure.vertexes[i-1].x,figure.vertexes[i-1].y);
            window.ctx.lineTo(figure.vertexes[0].x,figure.vertexes[0].y);
        }else{
           window.ctx.moveTo(figure.vertexes[i-1].x,figure.vertexes[i-1].y);
           window.ctx.lineTo(figure.vertexes[i].x,figure.vertexes[i].y);
           vertXsum += figure.vertexes[i].x;
           vertYsum += figure.vertexes[i].y;
        }
        window.ctx.stroke();
        if(i === 1){
            vertXsum += figure.vertexes[i-1].x;
            vertYsum += figure.vertexes[i-1].y;
        }
    }
    window.ctx.beginPath();
    let xm = vertXsum / figure.vertexes.length;
    let ym = vertYsum / figure.vertexes.length;
    window.ctx.fillStyle = "#FFF";
    window.ctx.textBaseline = "center";
    window.ctx.textAlign = "center";
    window.ctx.font = 'bold 26px sans-serif';
    window.ctx.fillText(window.marker_name, xm, ym);
    window.ctx.fill();
    window.ctx.lineWidth=1;
    window.ctx.strokeStyle = "#000";
    window.ctx.strokeText(window.marker_name, xm, ym);
    window.ctx.stroke();
    window.ctx.strokeStyle = "#000";
}

// clear the canvas
export function clear() {
    window.ctx.clearRect(0, 0, WIDTH, HEIGHT);
}

// redraw the scene
export function draw_rect(change_val=true) {
    clear();
    // redraw each rect in the rects[] array
    for (var [key, value] of window.zones) {
        var r=value;
        window.ctx.strokeStyle=r.fill;
        window.ctx.lineWidth=3;
        rect(r);
        if(r.selected){
            draw_selection(key)
        }
        if(change_val){
            let str_to_show = ""
            for(var j=0;j<r.vertexes.length;j++){
                str_to_show += r.vertexes[j].x + "," + r.vertexes[j].y + ";"
            }
            window.textareaCoords.value = str_to_show;
        }
    }
}
export function draw_selection(key) {
    for(var i=0;i<window.zones.get(key).vertexes.length;i++){
        window.ctx.fillStyle="#ff0000";
        window.ctx.strokeStyle="#ffffff";
        window.ctx.lineWidth=3;
        window.ctx.beginPath();
        window.ctx.arc(window.zones.get(key).vertexes[i].x,window.zones.get(key).vertexes[i].y,window.vertexRadius,2*Math.PI,false);
        window.ctx.stroke();
        window.ctx.closePath();
        window.ctx.fill();
    }
}

export function circle(figure) {
    window.ctx.beginPath();
    window.ctx.arc(figure.x, figure.y, figure.radius, 0, 2 * Math.PI, false);
    window.ctx.stroke();
    window.ctx.beginPath();
    window.ctx.fillStyle = "#FFF";
    window.ctx.textBaseline = "center";
    window.ctx.textAlign = "center";
    window.ctx.font = 'bold 26px sans-serif';
    window.ctx.fillText(window.marker_name, figure.x, figure.y);
    window.ctx.fill();
    window.ctx.lineWidth=1;
    window.ctx.strokeStyle = "#000";
    window.ctx.strokeText(window.marker_name, figure.x, figure.y);
    window.ctx.stroke();
    window.ctx.strokeStyle = "#000";
}
export function draw_circle(change_val=true) {
    clear();
    // redraw each rect in the rects[] array
    for(var [key, value] of window.zones) {
        var c=value;
        window.ctx.strokeStyle="#ffffff";
        window.ctx.lineWidth=3;
        circle(c);
        if(c.selected){
            // draw_selection()
        }
        if(change_val){
            window.textareaCoords.value = c.x + "," + c.y + "," + c.radius;
        }
    }
}

// handle mousedown events
export function myDown(e){

    // tell the browser we're handling this mouse event
    e.preventDefault();
    e.stopPropagation();

    // get the current mouse position
    window.scrolloffsetY = document.getElementsByClassName("content")[0].scrollTop;
    /*
    let canvasOffset = canvas.getBoundingClientRect().top + window.scrolloffsetY - 449.375
        if (canvasOffset > 0)
            canvasOffset -=  200;
     */
    let canvasOffset = 0;
    var mx=parseInt(e.clientX-window.offsetX);
    var my=parseInt(e.clientY-offsetY+window.scrolloffsetY);
    //if (my < 0)
    //    my += 210;

    window.selectedOption = window.zoneType.options[window.zoneType.selectedIndex];
    if(window.selectedOption.getAttribute('key') === "polygon") {
        // test each rect to see if mouse is inside
        dragok = false;
        for (var [key, value] of window.zones) {
            var r = value;
            let vertexSelected = false;
            let vertXsum = 0;
            let vertYsum = 0;
            if (r.selected) {
                for (var j = 0; j < r.vertexes.length; j++) {
                    if (Math.pow(mx - r.vertexes[j].x, 2) + Math.pow(my - (r.vertexes[j].y+canvasOffset), 2) <= Math.pow(window.vertexRadius, 2)) {
                        r.vertexes[j].v = true;
                        vertexSelected = true;
                    }
                }
            }
            for (j = 0; j < r.vertexes.length; j++) {
                vertXsum += r.vertexes[j].x;
                vertYsum += r.vertexes[j].y;
            }

            let xm = vertXsum / r.vertexes.length;
            let ym = vertYsum / r.vertexes.length // + canvasOffset;
            /*
            console.log(window.scrolloffsetY)
            console.log(mx, my)
            console.log(canvasOffset)
            console.log(xm, ym)
            */
            if (mx > xm - 32 && mx < xm + 32 && my > ym - 15 && my < ym + 15 || vertexSelected === true) {
                // if yes, set that rects isDragging=true
                dragok = true;
                if (!vertexSelected)
                    r.isDragging = true;
                r.selected = true;
                r.fill = "#ffffff";
            } else {
                r.selected = false;
            }
        }
        draw_rect();
    } else if(window.selectedOption.getAttribute('key') === "circle") {
        dragok = false;
        for (var [key, value] of window.zones) {
            let c = value
            if (mx > c.x - 32 && mx < c.x + 32 && my > c.y - 15 && my < c.y + 15) {
                dragok = true;
                c.isDragging = true;
                c.selected = true;
                c.fill = "#ffffff";
            } else {
                c.selected = false;
            }
        }
        draw_circle();
    }
    // save the current mouse position
    startX = mx;
    startY = my;
}


// handle mouseup events
export function myUp(e){
    // tell the browser we're handling this mouse event
    e.preventDefault();
    e.stopPropagation();

    window.selectedOption = window.zoneType.options[window.zoneType.selectedIndex];
    if(window.selectedOption.getAttribute('key') === "polygon") {
        // clear all the dragging flags
        for (var [key, value] of window.zones) {
            var r=value;
            r.isDragging=false;
            r.fill="#444444";
            for (var j = 0; j < r.vertexes.length; j++) {
                r.vertexes[j].v = false
            }
        }
        draw_rect();
    } else if(window.selectedOption.getAttribute('key') === "circle") {
        for (var [key, value] of window.zones) {
            var c=value;
            c.isDragging=false;
            c.fill="#444444";
        }
        draw_circle();
    }
}


// handle mouse moves
export function myMove(e){
    // if we're dragging anything...
    if (dragok){

      // tell the browser we're handling this mouse event
      e.preventDefault();
      e.stopPropagation();

      // get the current mouse position
      window.scrolloffsetY = document.getElementsByClassName("content")[0].scrollTop;
      var mx=parseInt(e.clientX-window.offsetX);
      var my=parseInt(e.clientY-offsetY+window.scrolloffsetY);

      // calculate the distance the mouse has moved
      // since the last mousemove
      var dx=mx-startX;
      var dy=my-startY;

      window.selectedOption = window.zoneType.options[window.zoneType.selectedIndex];
      if(window.selectedOption.getAttribute('key') === "polygon") {
          // move each rect that isDragging
          // by the distance the mouse has moved
          // since the last mousemove
          for (var [key, value] of window.zones) {
              var r=value;
            for (var j = 0; j < r.vertexes.length; j++) {
                if (r.vertexes[j].v) {
                    r.vertexes[j].x+=dx;
                    r.vertexes[j].y+=dy;
                }
            }
            if(r.isDragging){
                for (j = 0; j < r.vertexes.length; j++) {
                    r.vertexes[j].x+=dx;
                    r.vertexes[j].y+=dy;
                }
              }
          }
          // redraw the scene with the new rect positions
          draw_rect();
      } else if(window.selectedOption.getAttribute('key') === "circle") {
          for(var [key, value] of window.zones) {
            let c=value;
            if(c.isDragging){
                c.x+=dx;
                c.y+=dy;
              }
          }
          draw_circle();
      }

      // reset the starting mouse position for the next mousemove
      startX=mx;
      startY=my;

    }
}
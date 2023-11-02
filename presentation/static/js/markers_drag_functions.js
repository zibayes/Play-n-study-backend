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
    window.ctx.fillText(figure.marker_name, xm, ym);
    window.ctx.fill();
    window.ctx.lineWidth=1;
    window.ctx.strokeStyle = "#000";
    window.ctx.strokeText(figure.marker_name, xm, ym);
    window.ctx.stroke();
    window.ctx.strokeStyle = "#000";
}

// clear the canvas
export function clear() {
    window.ctx.clearRect(0, 0, WIDTH, HEIGHT);
}

// redraw the scene
export function draw_figures(change_val=true) {
    clear();
    // перерисовка всех фигур
    for (var [key, value] of window.zones) {
        if (value.x === undefined) {
            window.ctx.strokeStyle = value.fill;
            window.ctx.lineWidth = 3;
            rect(value);
            if (value.selected && value.x === undefined) {
                draw_selection(value)
            }
            if (change_val) {
                let str_to_show = ""
                for (var j = 0; j < value.vertexes.length; j++) {
                    str_to_show += value.vertexes[j].x + "," + value.vertexes[j].y + ";"
                }
                value.textareaCoords.value = str_to_show;
            }
        } else{
            window.ctx.strokeStyle = "#ffffff";
            window.ctx.lineWidth = 3;
            circle(value);
            if (value.selected) {
                // draw_selection()
            }
            if (change_val) {
                value.textareaCoords.value = value.x + "," + value.y + "," + value.radius;
            }
        }
    }
}

// отображение выделения
export function draw_selection(figure) {
    for(var i=0;i<figure.vertexes.length;i++){
        window.ctx.fillStyle="#ff0000";
        window.ctx.strokeStyle="#ffffff";
        window.ctx.lineWidth=3;
        window.ctx.beginPath();
        window.ctx.arc(figure.vertexes[i].x,figure.vertexes[i].y,window.vertexRadius,2*Math.PI,false);
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
    window.ctx.fillText(figure.marker_name, figure.x, figure.y);
    window.ctx.fill();
    window.ctx.lineWidth=1;
    window.ctx.strokeStyle = "#000";
    window.ctx.strokeText(figure.marker_name, figure.x, figure.y);
    window.ctx.stroke();
    window.ctx.strokeStyle = "#000";
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

    dragok = false;
    for (var [key, value] of window.zones) {
        if (value.x === undefined){
            let vertexSelected = false;
            let vertXsum = 0;
            let vertYsum = 0;
            if (value.selected) {
                for (var j = 0; j < value.vertexes.length; j++) {
                    if (Math.pow(mx - value.vertexes[j].x, 2) + Math.pow(my - (value.vertexes[j].y+canvasOffset), 2) <= Math.pow(window.vertexRadius, 2)) {
                        value.vertexes[j].v = true;
                        vertexSelected = true;
                    }
                }
            }
            for (j = 0; j < value.vertexes.length; j++) {
                vertXsum += value.vertexes[j].x;
                vertYsum += value.vertexes[j].y;
            }

            let xm = vertXsum / value.vertexes.length;
            let ym = vertYsum / value.vertexes.length + window.ctx.canvas.offsetTop // + canvasOffset;

            console.log(window.ctx.canvas.offsetTop)
            console.log(mx, my)
            console.log(xm, ym)

            if (mx > xm - 32 && mx < xm + 32 && my > ym - 15 && my < ym + 15 || vertexSelected === true) {
                // if yes, set that rects isDragging=true
                dragok = true;
                if (!vertexSelected)
                    value.isDragging = true;
                value.selected = true;
                value.fill = "#ffffff";
            } else {
                value.selected = false;
            }
            draw_figures();
        } else{
            if (mx > value.x - 32 && mx < value.x + 32 && my > value.y - 15 && my < value.y + 15) {
            dragok = true;
            value.isDragging = true;
            value.selected = true;
            value.fill = "#ffffff";

            } else {
                value.selected = false;
            }
            draw_figures();
        }
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

    for (var [key, value] of window.zones) {
        if (value.x === undefined){
            value.isDragging=false;
            value.fill="#444444";
            for (var j = 0; j < value.vertexes.length; j++) {
                value.vertexes[j].v = false
            }
            draw_figures();
        } else {
            value.isDragging=false;
            value.fill="#444444";
            draw_figures();
        }
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

      for (var [key, value] of window.zones) {
          if (value.x === undefined){
            for (var j = 0; j < value.vertexes.length; j++) {
                if (value.vertexes[j].v) {
                    value.vertexes[j].x+=dx;
                    value.vertexes[j].y+=dy;
                }
            }
            if(value.isDragging){
                for (j = 0; j < value.vertexes.length; j++) {
                    value.vertexes[j].x+=dx;
                    value.vertexes[j].y+=dy;
                }
                draw_figures();
            } else {
                draw_figures(false);
            }
          } else {
            if(value.isDragging){
                value.x+=dx;
                value.y+=dy;
                draw_figures();
            } else {
                draw_figures(false);
            }
          }
      }

      // reset the starting mouse position for the next mousemove
      startX=mx;
      startY=my;

    }
}
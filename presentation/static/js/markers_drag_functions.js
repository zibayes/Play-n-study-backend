// drag related variables
var dragok = false;
var startX;
var startY;

export function rect(figure, ctx) {
    let vertXsum = 0;
    let vertYsum = 0;
    for(var i=1;i<figure.vertexes.length + 1;i++){
        ctx.beginPath();
        if(i === figure.vertexes.length){
            ctx.moveTo(figure.vertexes[i-1].x,figure.vertexes[i-1].y);
            ctx.lineTo(figure.vertexes[0].x,figure.vertexes[0].y);
        }else{
           ctx.moveTo(figure.vertexes[i-1].x,figure.vertexes[i-1].y);
           ctx.lineTo(figure.vertexes[i].x,figure.vertexes[i].y);
           vertXsum += figure.vertexes[i].x;
           vertYsum += figure.vertexes[i].y;
        }
        ctx.stroke();
        if(i === 1){
            vertXsum += figure.vertexes[i-1].x;
            vertYsum += figure.vertexes[i-1].y;
        }
    }
    ctx.beginPath();
    let xm = vertXsum / figure.vertexes.length;
    let ym = vertYsum / figure.vertexes.length;
    ctx.fillStyle = "#FFF";
    ctx.textBaseline = "center";
    ctx.textAlign = "center";
    ctx.font = 'bold 26px sans-serif';
    ctx.fillText(figure.marker_name, xm, ym);
    ctx.fill();
    ctx.lineWidth=1;
    ctx.strokeStyle = "#000";
    ctx.strokeText(figure.marker_name, xm, ym);
    ctx.stroke();
    ctx.strokeStyle = "#000";
}

// clear the canvas
export function clear(ctx) {
    ctx.clearRect(0, 0, window.WIDTH, window.HEIGHT);
}

// redraw the scene
export function draw_figures(canvas, change_val=true, drop_selection=false) {
    // перерисовка всех фигур
    if (typeof canvas === "string") {
        canvas = window.canvases.get(canvas.substring(0, canvas.indexOf("-")))
    }
    let ctx=canvas.canvas.getContext("2d");
    clear(ctx);
    /*
    const image = new Image();
    image.src = image_load;
    ctx.drawImage(image, 0, 0, width, height);
    TODO: добавть у канваса хранение фонового изображения
     */
    if (canvas.background !== undefined)
        ctx.drawImage(canvas.background, 0, 0, canvas.canvas.width, canvas.canvas.height);
    let zones = canvas.zones
    for (var [key, value] of zones) {
        if (value.x === undefined) {
            ctx.strokeStyle = value.fill;
            ctx.lineWidth = 3;
            rect(value, ctx);
            if (value.selected && !drop_selection) {
                draw_selection(value, ctx)
            } else {
                value.selected = false
                value.isDragging = false
            }
            if (change_val) {
                let str_to_show = ""
                for (var j = 0; j < value.vertexes.length; j++) {
                    str_to_show += value.vertexes[j].x + "," + value.vertexes[j].y + ";"
                }
                value.textareaCoords.value = str_to_show;
            }
        } else {
            ctx.strokeStyle = "#ffffff";
            ctx.lineWidth = 3;
            circle(value, ctx);
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
export function draw_selection(figure, ctx) {
    for(var i=0;i<figure.vertexes.length;i++){
        // ctx.fillStyle="#ff0000";
        // ctx.strokeStyle="#ffffff";
        ctx.lineWidth=3;
        ctx.beginPath();
        ctx.arc(figure.vertexes[i].x,figure.vertexes[i].y,window.vertexRadius,2*Math.PI,false);
        ctx.stroke();
        ctx.fill();
    }
}

export function circle(figure, ctx) {
    ctx.beginPath();
    ctx.arc(figure.x, figure.y, figure.radius, 0, 2 * Math.PI, false);
    ctx.stroke();
    ctx.beginPath();
    ctx.fillStyle = "#FFF";
    ctx.textBaseline = "center";
    ctx.textAlign = "center";
    ctx.font = 'bold 26px sans-serif';
    ctx.fillText(figure.marker_name, figure.x, figure.y);
    ctx.fill();
    ctx.lineWidth=1;
    ctx.strokeStyle = "#000";
    ctx.strokeText(figure.marker_name, figure.x, figure.y);
    ctx.stroke();
    ctx.strokeStyle = "#000";
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
    let canvasOffset = 280 + window.scrolloffsetY + this.getBoundingClientRect().top - 891.125; // TODO: -200 - editor // standard: window.scrolloffsetY + window.ctx.canvas.getBoundingClientRect().top = 891.125
    var mx=parseInt(e.clientX-window.offsetX);
    var my=parseInt(e.clientY-offsetY+window.scrolloffsetY);
    //if (my < 0)
    //    my += 210;

    let zones = window.canvases.get(this.id.substring(this.id.indexOf("-")+1)).zones
    dragok = false;
    for (var [key, value] of zones) {
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
            let ym = vertYsum / value.vertexes.length + canvasOffset;

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
        } else{
            if (mx > value.x - 32 && mx < value.x + 32 && my > value.y + canvasOffset - 15 && my < value.y + canvasOffset + 15) {
            dragok = true;
            value.isDragging = true;
            value.selected = true;
            value.fill = "#ffffff";

            } else {
                value.selected = false;
            }
        }
        draw_figures(window.canvases.get(this.id.substring(this.id.indexOf("-")+1)));
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

    let zones = window.canvases.get(this.id.substring(this.id.indexOf("-")+1)).zones
    for (var [key, value] of zones) {
        if (value.x === undefined){
            value.isDragging=false;
            value.fill="#444444";
            for (var j = 0; j < value.vertexes.length; j++) {
                value.vertexes[j].v = false
            }
            draw_figures(window.canvases.get(this.id.substring(this.id.indexOf("-")+1)));
        } else {
            value.isDragging=false;
            value.fill="#444444";
            draw_figures(window.canvases.get(this.id.substring(this.id.indexOf("-")+1)));
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

      let zones = window.canvases.get(this.id.substring(this.id.indexOf("-")+1)).zones
      for (var [key, value] of zones) {
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
                draw_figures(window.canvases.get(this.id.substring(this.id.indexOf("-")+1)));
            } else {
                draw_figures(window.canvases.get(this.id.substring(this.id.indexOf("-")+1)), false);
            }
          } else {
            if(value.isDragging){
                value.x+=dx;
                value.y+=dy;
                draw_figures(window.canvases.get(this.id.substring(this.id.indexOf("-")+1)));
            } else {
                draw_figures(window.canvases.get(this.id.substring(this.id.indexOf("-")+1)), false);
            }
          }
      }

      // reset the starting mouse position for the next mousemove
      startX=mx;
      startY=my;

    }
}
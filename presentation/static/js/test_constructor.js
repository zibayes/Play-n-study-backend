import { addDragoverEventListener, addQuestionListener } from './test_constructor_functions.js';

let questions_list = document.getElementById("questionsList")
addDragoverEventListener(questions_list, `question_div`);
// Добавление вопроса
let addBtn = document.getElementById("addQuestion");
window.questionIndex = 1;
window.answerIndex = 0;
addQuestionListener(addBtn);

var canvas=document.getElementById("canvas");
var ctx=canvas.getContext("2d");
var BB=canvas.getBoundingClientRect();
var scrollOffsetY = document.getElementsByClassName("content")[0].scrollTop;
var offsetX=BB.left;
var offsetY=BB.top;
var WIDTH = canvas.width;
var HEIGHT = canvas.height;
var vertexRadius = 6
let marker_name = "";
let zoneFigure = document.getElementById("ZoneFigure");
let selectedOption;

// drag related variables
var dragok = false;
var startX;
var startY;

// an array of objects that define different rectangles
var rects=[];
rects.push({vertexes:[{x:10,y:10,v:false},{x:10,y:60,v:false},{x:60,y:60,v:false},{x:60,y:10,v:false}],isDragging:false,selected:false});
let circles=[];
circles.push({x:60,y:60,radius:40,isDragging:false,selected:false})

// listen for mouse events
canvas.onmousedown = myDown;
canvas.onmouseup = myUp;
canvas.onmousemove = myMove;

// call to draw the scene
draw_rect();

// draw a single rect
function rect(figure) {
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
ctx.fillText(marker_name, xm, ym);
ctx.fill();
ctx.lineWidth=1;
ctx.strokeStyle = "#000";
ctx.strokeText(marker_name, xm, ym);
ctx.stroke();
ctx.strokeStyle = "#000";
}

// clear the canvas
function clear() {
ctx.clearRect(0, 0, WIDTH, HEIGHT);
}

// redraw the scene
function draw_rect(change_val=true) {
clear();
// redraw each rect in the rects[] array
for(var i=0;i<rects.length;i++){
    var r=rects[i];
    ctx.strokeStyle=r.fill;
    ctx.lineWidth=3;
    rect(r);
    if(r.selected){
        draw_selection()
    }
    if(change_val){
        let coordinates = document.getElementById("coordinates");
        let str_to_show = ""
        for(var j=0;j<r.vertexes.length;j++){
            str_to_show += r.vertexes[j].x + "," + r.vertexes[j].y + ";"
        }
        coordinates.value = str_to_show;
    }
}
}
function draw_selection() {
for(var i=0;i<rects[0].vertexes.length;i++){
    ctx.fillStyle="#ff0000";
    ctx.strokeStyle="#ffffff";
    ctx.lineWidth=3;
    ctx.beginPath();
    ctx.arc(rects[0].vertexes[i].x,rects[0].vertexes[i].y,vertexRadius,2*Math.PI,false);
    ctx.stroke();
    ctx.closePath();
    ctx.fill();
}
}

function circle(figure) {
ctx.beginPath();
ctx.arc(figure.x, figure.y, figure.radius, 0, 2 * Math.PI, false);
ctx.stroke();
ctx.beginPath();
ctx.fillStyle = "#FFF";
ctx.textBaseline = "center";
ctx.textAlign = "center";
ctx.font = 'bold 26px sans-serif';
ctx.fillText(marker_name, figure.x, figure.y);
ctx.fill();
ctx.lineWidth=1;
ctx.strokeStyle = "#000";
ctx.strokeText(marker_name, figure.x, figure.y);
ctx.stroke();
ctx.strokeStyle = "#000";
}
function draw_circle(change_val=true) {
clear();
// redraw each rect in the rects[] array
for(var i=0;i<circles.length;i++){
    var c=circles[i];
    ctx.strokeStyle="#ffffff";
    ctx.lineWidth=3;
    circle(c);
    if(c.selected){
        // draw_selection()
    }
    if(change_val){
        let coordinates = document.getElementById("coordinates");
        coordinates.value = c.x + "," + c.y + "," + c.radius;
    }
}
}


// handle mousedown events
function myDown(e){

// tell the browser we're handling this mouse event
e.preventDefault();
e.stopPropagation();

// get the current mouse position
scrollOffsetY = document.getElementsByClassName("content")[0].scrollTop;
var mx=parseInt(e.clientX-offsetX);
var my=parseInt(e.clientY-offsetY+scrollOffsetY);

selectedOption = zoneFigure.options[zoneFigure.selectedIndex];
if(selectedOption.getAttribute('key') === "polygon") {
    // test each rect to see if mouse is inside
    dragok = false;
    for (var i = 0; i < rects.length; i++) {
        var r = rects[i];
        let vertexSelected = false;
        let vertXsum = 0;
        let vertYsum = 0;
        if (r.selected) {
            for (var j = 0; j < r.vertexes.length; j++) {
                if (Math.pow(mx - r.vertexes[j].x, 2) + Math.pow(my - r.vertexes[j].y, 2) <= Math.pow(vertexRadius, 2)) {
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
        let ym = vertYsum / r.vertexes.length;
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
} else if(selectedOption.getAttribute('key') === "circle") {
    dragok = false;
    for (i = 0; i < circles.length; i++) {
        let c = circles[i]
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
function myUp(e){
// tell the browser we're handling this mouse event
e.preventDefault();
e.stopPropagation();

selectedOption = zoneFigure.options[zoneFigure.selectedIndex];
if(selectedOption.getAttribute('key') === "polygon") {
    // clear all the dragging flags
    for(var i=0;i<rects.length;i++){
        var r=rects[i];
        r.isDragging=false;
        r.fill="#444444";
        for (var j = 0; j < r.vertexes.length; j++) {
            r.vertexes[j].v = false
        }
    }
    draw_rect();
} else if(selectedOption.getAttribute('key') === "circle") {
    for(i=0;i<circles.length;i++){
        var c=circles[i];
        c.isDragging=false;
        c.fill="#444444";
    }
    draw_circle();
}
}


// handle mouse moves
function myMove(e){
// if we're dragging anything...
if (dragok){

  // tell the browser we're handling this mouse event
  e.preventDefault();
  e.stopPropagation();

  // get the current mouse position
  scrollOffsetY = document.getElementsByClassName("content")[0].scrollTop;
  var mx=parseInt(e.clientX-offsetX);
  var my=parseInt(e.clientY-offsetY+scrollOffsetY);

  // calculate the distance the mouse has moved
  // since the last mousemove
  var dx=mx-startX;
  var dy=my-startY;

  selectedOption = zoneFigure.options[zoneFigure.selectedIndex];
  if(selectedOption.getAttribute('key') === "polygon") {
      // move each rect that isDragging
      // by the distance the mouse has moved
      // since the last mousemove
      for(var i=0;i<rects.length;i++){
          var r=rects[i];
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
  } else if(selectedOption.getAttribute('key') === "circle") {
      for(i=0;i<circles.length;i++){
        let c=circles[i];
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

let marker = document.getElementById("marker");
marker.addEventListener('input', function (evt) {
marker_name = marker.value;
selectedOption = zoneFigure.options[zoneFigure.selectedIndex];
if(selectedOption.getAttribute('key') === "polygon") {
    draw_rect();
} else if(selectedOption.getAttribute('key') === "circle") {
    draw_circle();
}
});

zoneFigure.addEventListener('change', function (evt) {
selectedOption = zoneFigure.options[zoneFigure.selectedIndex];
if(selectedOption.getAttribute('key') === "polygon") {
    draw_rect();
}else if(selectedOption.getAttribute('key') === "circle") {
    draw_circle()
}
});

let buttonAddBackground = document.getElementById("addBackgroundImage");
buttonAddBackground.addEventListener('click', function (evt) {
let customFile = document.getElementById("customFile");
let file = customFile.files[0];
let canvas = document.getElementById("canvas");
let canvasContainer = document.getElementById("canvasContainer");
let reader = new FileReader();
reader.onload = function(event) {
    const image = new Image();
    image.src = event.target.result;
    image.onload = function () {
        let height = this.height;
        let width = this.width;
        if(width > 1036){
            let ratio = height / width;
            width = 1036;
            height = width * ratio;
            ImageTools.resize(file, {
                width: width,
                height: height
            }, function(blob, didItResize) {
                canvas.height = height;
                canvas.width = width;
                canvasContainer.setAttribute("height", height + "px");
                canvasContainer.setAttribute("width", width + "px");
                $('#canvas').css('background-image', 'url(' + window.URL.createObjectURL(blob) + ')');
            });
        }else{
            canvas.height = height;
            canvas.width = width;
            canvasContainer.setAttribute("height", height + "px");
            canvasContainer.setAttribute("width", width + "px");
            $('#canvas').css('background-image', 'url(' + image.src + ')');
        }
    };
};
reader.readAsDataURL(file);
});

let coordinates = document.getElementById("coordinates");
coordinates.addEventListener('input', function (evt) {
let string = coordinates.value;

selectedOption = zoneFigure.options[zoneFigure.selectedIndex];
if(selectedOption.getAttribute('key') === "polygon") {
    let coordsAmount = coordinates.value.match(/;/g).length;
    let delimiter, coords, comma;
    rects[0].vertexes = []
    for(let i = 0; i < coordsAmount; i++){
        if(i > 0){
            delimiter = string.indexOf(";");
            string = string.slice(delimiter+1);
        }
        delimiter = string.indexOf(";");
        if(delimiter > 0)
            coords = string.slice(0, delimiter);
        else
            coords = string
        comma = coords.indexOf(",");
        let new_x = parseInt(coords.slice(0, comma));
        let new_y = parseInt(coords.slice(comma+1));
        rects[0].vertexes.push({x:new_x, y: new_y, v:false})
    }
    draw_rect(false);
} else if(selectedOption.getAttribute('key') === "circle") {
    let delimiter = string.indexOf(",");
    circles[0].x = parseInt(string.slice(0, delimiter));
    string = string.slice(delimiter+1);
    delimiter = string.indexOf(",");
    circles[0].y = parseInt(string.slice(0, delimiter));
    string = string.slice(delimiter+1);
    circles[0].radius = parseInt(string);
    draw_circle();
}
});
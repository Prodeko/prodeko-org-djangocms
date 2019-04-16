/**
 * crop thingy
 * (c) Henrik Aarnio
 **/

function SimpleCrop(element, settings){
    settings = settings ? settings : {};
    settings.backgroundColor = settings.backgroundColor ? settings.backgroundColor : "lightgrey";
    settings.textColor = settings.textColor ? settings.textColor : "darkgrey";
    settings.uploadText = settings.uploadText ? settings.uploadText : "Lataa kuva napauttamalla";
    settings.aspectRatio = settings.aspectRatio ? settings.aspectRatio : 1;
    settings.minZoom = settings.minZoom ? settings.minZoom : 0.1;
    settings.outputWidth = settings.outputWidth ? settings.outputWidth : 200;
    settings.width = settings.width ? settings.width : element.clientWidth;
    settings.height = settings.height ? settings.height : element.clientHeight;

    var div = document.createElement('div');
    div.style.position = 'relative';
    div.style.marginLeft = "auto";
    div.style.marginRight = "auto";
    div.style.width = "100%";
    div.style.height = "100%";

    var wholeCanvas = document.createElement('canvas');
    var ctx = wholeCanvas.getContext('2d');
    wholeCanvas.style.top = "0px";
    wholeCanvas.style.width = "100%";
    wholeCanvas.style.display = "inline-block";

    var zoomcontrolDiv = document.createElement('div');
    zoomcontrolDiv.style.display = "inline-block";
    zoomcontrolDiv.style.top = "94%";
    zoomcontrolDiv.style.width = "100%";
    zoomcontrolDiv.style.transform = "translate(-50%, 0%)";


    var zoomslider = document.createElement('input');
    zoomslider.type = 'range';
    zoomslider.style.display = "inline-block";
    zoomslider.style.width = "92%"
    zoomslider.min = "0";
    zoomslider.max = "1";
    zoomslider.step = "0.01";


    div.appendChild(wholeCanvas);
    zoomcontrolDiv.appendChild(document.createTextNode("-  "));
    zoomcontrolDiv.appendChild(zoomslider);
    zoomcontrolDiv.appendChild(document.createTextNode("  +"));
    zoomcontrolDiv.style.display = "inline-block";
    zoomcontrolDiv.style.marginLeft = "50%";
    div.appendChild(zoomcontrolDiv);
    element.appendChild(div);


    var selectionW, selectionH, selectionLeft, selectionRight, selectionUp, selectionDown;

    var width = wholeCanvas.width = settings.outputWidth / 0.5;
    var height = wholeCanvas.height = settings.outputWidth * settings.aspectRatio / 0.5;
    wholeCanvas.style.width = settings.width + "px";
    wholeCanvas.style.height = settings.height + "px";

    if(wholeCanvas.width > wholeCanvas.height){
        selectionW = wholeCanvas.width*0.5;
        selectionH = selectionW * settings.aspectRatio;
    } else {
        selectionH = wholeCanvas.height*0.5;
        selectionW = selectionH / settings.aspectRatio;
    }
    selectionLeft = wholeCanvas.width * 0.5 - selectionW*0.5;
    selectionRight = wholeCanvas.width * 0.5 + selectionW*0.5;
    selectionUp = wholeCanvas.height * 0.5 - selectionH*0.5;
    selectionDown = wholeCanvas.height*0.5 + selectionH*0.5;

    function updateCanvasSize(initial){
        if(!initial){
            wholeCanvas.style.width = element.clientWidth + "px";
            wholeCanvas.style.height = element.clientHeight + "px";
        }
    }
    updateCanvasSize(true);

    var uploadButton = document.createElement('input');
    var originalImage;
    var imageLocation = {x: wholeCanvas.width/2, y: wholeCanvas.height/2};
    var imageScale = 1;

    var minimumScaleFactor;
    var maximumScaleFactor;

    uploadButton.type = 'file';
    uploadButton.accept = "image/*";
    uploadButton.addEventListener('change', function(event){
        originalImage = new Image();
        originalImage.onload = function(){
            imageScale = Math.max(wholeCanvas.width/originalImage.width, wholeCanvas.height/originalImage.height)
            minimumScaleFactor = Math.max(selectionW/originalImage.width, selectionH/originalImage.height)
            maximumScaleFactor =  minimumScaleFactor / settings.minZoom;
            updateZoomslider();
            updateImage();
        }
        originalImage.src = URL.createObjectURL(uploadButton.files[0]);
    });

    function putImageInsideBounds(){
        if(originalImage.width * imageScale < selectionW){
            imageScale = selectionW / originalImage.width;
        }
        if(originalImage.height * imageScale < selectionH){
            imageScale = selectionH / originalImage.height;
        }

        if(imageLocation.x - originalImage.width/2 * imageScale > selectionLeft){
            imageLocation.x = selectionLeft + originalImage.width/2 * imageScale;
        }
        if(imageLocation.x + originalImage.width/2 * imageScale < selectionRight){
            imageLocation.x = selectionRight - originalImage.width/2 * imageScale;
        }
        if(imageLocation.y - originalImage.height/2 * imageScale > selectionUp){
            imageLocation.y = selectionUp + originalImage.height/2 * imageScale;
        }
        if(imageLocation.y + originalImage.height/2 * imageScale < selectionDown){
            imageLocation.y = selectionDown - originalImage.height/2 * imageScale;
        }
    }
    function updateImage(){
        if(originalImage){
            putImageInsideBounds();
            ctx.fillStyle = settings.backgroundColor;
            ctx.fillRect(0, 0, wholeCanvas.width, wholeCanvas.height);
            var w = imageScale*originalImage.width;
            var h = imageScale*originalImage.height;

            ctx.fillStyle = "#888888";
            ctx.fillRect(imageLocation.x - w*0.5, imageLocation.y - h*0.5, w, h);

            ctx.fillStyle = "#ffffff";
            ctx.fillRect(selectionLeft, selectionUp, selectionW, selectionH);

            ctx.globalCompositeOperation = "multiply";
            ctx.drawImage(originalImage, imageLocation.x - w*0.5, imageLocation.y - h*0.5, w, h);
            ctx.globalCompositeOperation = "source-over";
        } else {
            drawEmptyCanvas();
        }
    }


    function drawEmptyCanvas(){
        ctx.fillStyle = settings.backgroundColor;
        ctx.fillRect(0, 0, wholeCanvas.width, wholeCanvas.height);

        ctx.fillStyle = settings.textColor;
        ctx.textBaseline = "middle";
        ctx.textAlign = "center";
        ctx.font = wholeCanvas.height / 20 + "px Arial";
        ctx.fillText(settings.uploadText, wholeCanvas.width/2, wholeCanvas.height/2);
    }

    drawEmptyCanvas();

    wholeCanvas.addEventListener('click', function(event){
        if(!originalImage){
            uploadButton.click();
        }
    });

    var clickCoordinates;
    wholeCanvas.addEventListener('mousedown', function(event){
        if(originalImage){
            clickCoordinates = {x:event.screenX, y:event.screenY};
        }
    });
    wholeCanvas.addEventListener('mousemove', function(event){
        if(clickCoordinates){
            newClickCoordinates = {x:event.screenX, y:event.screenY};
            imageLocation.x -= (clickCoordinates.x - newClickCoordinates.x) * wholeCanvas.width / wholeCanvas.clientWidth;
            imageLocation.y -= (clickCoordinates.y - newClickCoordinates.y) * wholeCanvas.height / wholeCanvas.clientHeight;
            clickCoordinates = newClickCoordinates;

            updateImage();
        }
    });
    wholeCanvas.addEventListener('mouseup', function(event){
        clickCoordinates = null;
    });
    wholeCanvas.addEventListener('mouseout', function(event){
        clickCoordinates = null;
    });

    wholeCanvas.addEventListener('wheel', function(event){
        event.preventDefault();
        if(event.deltaY > 0) scaleUp();
        else scaleDown();
    });

    function scaleUp(){
        var scaleFactor = Math.min(imageScale*1.1, maximumScaleFactor)/imageScale;
        imageScale *= scaleFactor;
        imageLocation.x -= wholeCanvas.width / 2; imageLocation.y -= wholeCanvas.height / 2;
        imageLocation.x *= scaleFactor;           imageLocation.y *= scaleFactor;
        imageLocation.x += wholeCanvas.width / 2; imageLocation.y += wholeCanvas.height / 2;
        updateImage();
        updateZoomslider();
    }
    function scaleDown(){
        var scaleFactor = Math.max(imageScale/1.1, minimumScaleFactor)/imageScale;
        imageScale *= scaleFactor;
        imageLocation.x -= wholeCanvas.width / 2; imageLocation.y -= wholeCanvas.height / 2;
        imageLocation.x *= scaleFactor;           imageLocation.y *= scaleFactor;
        imageLocation.x += wholeCanvas.width / 2; imageLocation.y += wholeCanvas.height / 2;
        updateImage();
        console.log(imageScale)
        updateZoomslider();
    }

    zoomslider.addEventListener('input', function(){
        imageScale = Number(zoomslider.value) * (maximumScaleFactor - minimumScaleFactor) + minimumScaleFactor;
        updateImage();
    })
    function updateZoomslider(){
        zoomslider.value = (imageScale - minimumScaleFactor) / (maximumScaleFactor - minimumScaleFactor);
    }

    if(settings.confirmButton){
        settings.confirmButton.addEventListener('click', function(){
            var resultCanvas = document.createElement('canvas');
            var resCtx = resultCanvas.getContext('2d');
            resultCanvas.width = settings.outputWidth;
            resultCanvas.height = settings.outputWidth * settings.aspectRatio;
            resCtx.drawImage(wholeCanvas, selectionLeft, selectionUp, selectionW, selectionH, 0, 0, resultCanvas.width, resultCanvas.height)

            var reader = new FileReader();

            if(settings.outputData){
                resultCanvas.toBlob(function(blob){
                    settings.outputData.data = blob;
                })
            }

            if(settings.outputImage){
                settings.outputImage.src = resultCanvas.toDataURL()
            }
        })
    }
}

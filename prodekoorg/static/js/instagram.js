const ACCESS_TOKEN = "2398789603.1677ed0.0f8cf3e0b2684743a9ea6b9a9636dadb";
var num = 4
if(window.innerWidth >= 576) {
   num = 6;
}
window.onload = fetch(`https://api.instagram.com/v1/users/self/media/recent/?access_token=${ACCESS_TOKEN}&count=${num}`)
    .then(function (response) {
        return response.json();
    })
    .then(function (myJson) {
        //console.log(JSON.stringify(myJson));
        console.log(JSON.stringify(myJson.data));
        myJson.data.map(image => $('div#instagram').append(`<a href=${image.link} target= "_blank"><img src=${image.images.low_resolution.url}></img></a>`));
    });

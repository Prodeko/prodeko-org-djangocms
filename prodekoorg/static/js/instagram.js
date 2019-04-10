const ACCESS_TOKEN = "2398789603.1677ed0.2175ddadc380435f9a837eac1a212d0c";
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

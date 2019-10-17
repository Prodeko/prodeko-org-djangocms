const ACCESS_TOKEN = '2398789603.1677ed0.d61f066776bb4a068b1952be09c2265d';
var num = 4;

if (window.innerWidth >= 576) {
  num = 8;
}

window.onload = fetch(
  `https://api.instagram.com/v1/users/self/media/recent/?access_token=${ACCESS_TOKEN}&count=${num}`
)
  .then(function(response) {
    return response.json();
  })
  .then(function(json) {
    json.data.map(image =>
      $('div#instagram').append(
        `<a href=${image.link} target= "_blank"><img src=${image.images.low_resolution.url}></img></a>`
      )
    );
  });

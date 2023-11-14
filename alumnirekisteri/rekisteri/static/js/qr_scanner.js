let scanner = new Instascan.Scanner({
  video: document.getElementById('qr-video'),
  mirror: false,
});
scanner.addListener('scan', function (content) {
  sendQRData(content);
});

Instascan.Camera.getCameras()
  .then(function (cameras) {
    if (cameras.length > 0) {
      scanner.start(cameras[0]);
    } else {
      console.error('No cameras found.');
    }
  })
  .catch(function (e) {
    console.error(e);
  });

function sendQRData(qrData) {
  const message_elem = document.getElementById('scanner-message');
  const url = '/fi/matrikkeli/api/scanner/';
  const sheetId = window.localStorage.getItem('sheet-id');
  if (!sheetId) {
    message_elem.innerHTML = 'Sheetin ID:tä ei ole asetettu.';
    return;
  }
  const data = {
    sessionKey: qrData,
    sheetId,
  };

  fetch(url, {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data.active) {
        document.getElementById('scanned-email').innerHTML = data.email;
        document.getElementById('scanned-name').innerHTML = data.name;
        document.getElementById('scanned-type').innerHTML = data.member_type;
      }
      message_elem.innerHTML = data.message;
    })
    .catch((error) => {
      message_elem.innerHTML = 'Tapahtui virhe!';
      return console.error(error);
    });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document
  .getElementById('submit-spreadsheet-id')
  .addEventListener('click', function () {
    const spreadsheetId = document.getElementById('spreadsheet-id').value;
    localStorage.setItem('sheet-id', spreadsheetId);
  });

function showSpinner() {
  document.getElementById('load-modal').classList.remove('hidden');
  document.getElementById('load-modal').classList.add('flex');

}
function hideSpinner() {
  document.getElementById('load-modal').classList.remove('flex');
  document.getElementById('load-modal').classList.add('hidden');
};

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Si esta cookie comienza con el nombre que buscamos
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
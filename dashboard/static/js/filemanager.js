  // Kontekst menyu funksiyasi
  const contextMenu = document.getElementById('contextMenu');
  let selectedFile = null;

  document.addEventListener('contextmenu', function (e) {
      e.preventDefault();

      const target = e.target.closest('.file-item');
      if (target) {
          selectedFile = target.dataset.name;
          const isDir = target.dataset.isDir === 'true';

          // Paste faqat papka uchun chiqadi
          document.querySelector('.context-paste').style.display = isDir ? 'block' : 'none';

          contextMenu.style.display = 'block';
          contextMenu.style.left = `${e.pageX}px`;
          contextMenu.style.top = `${e.pageY}px`;
      } else {
          contextMenu.style.display = 'none';
      }
  });

  document.addEventListener('click', function () {
      contextMenu.style.display = 'none';
  });

  // Tahrirlash
  document.querySelector('.context-rename').addEventListener('click', function () {
      const newName = prompt('Faylning yangi nomini kiriting:', selectedFile);
      if (newName) {
          fetch('/filemanager/rename/', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': getCSRFToken()
              },
              body: JSON.stringify({ old_name: selectedFile, new_name: newName })
          }).then(res => res.json())
              .then(data => alert(data.message || 'Fayl tahrirlandi!'))
              .catch(err => alert('Xatolik yuz berdi!'));
      }
  });

  // O'chirish
  document.querySelector('.context-delete').addEventListener('click', function () {
      if (confirm(`Faylni o'chirish: ${selectedFile}?`)) {
          fetch('/filemanager/delete/', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': getCSRFToken()
              },
              body: JSON.stringify({ name: selectedFile })
          }).then(res => res.json())
              .then(data => alert(data.message || 'Fayl o‘chirildi!'))
              .catch(err => alert('Xatolik yuz berdi!'));
      }
  });

  // Nusxalash
  document.querySelector('.context-copy').addEventListener('click', function () {
      fetch('/filemanager/copy/', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCSRFToken()
          },
          body: JSON.stringify({ name: selectedFile })
      }).then(res => res.json())
          .then(data => alert(data.message || 'Fayl nusxalandi!'))
          .catch(err => alert('Xatolik yuz berdi!'));
  });

  // Joylashtirish
  document.querySelector('.context-paste').addEventListener('click', function () {
      fetch('/filemanager/paste/', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCSRFToken()
          }
      }).then(res => res.json())
          .then(data => alert(data.message || 'Fayl joylashtirildi!'))
          .catch(err => alert('Xatolik yuz berdi!'));
  });

  function getCSRFToken() {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.startsWith('csrftoken=')) {
              return cookie.substring('csrftoken='.length);
          }
      }
      return '';
  }
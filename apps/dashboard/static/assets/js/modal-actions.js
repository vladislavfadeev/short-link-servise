// Create csrf const for POST AJAX requests
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

//  Modal window
const modal = new ItcModal();
document.addEventListener('click', (e) => {
    if (e.target.closest('[data-toggle="img-modal"]')) {
        const btn = e.target.closest('[data-toggle="img-modal"]');

        modal.setTitle(btn.dataset.title);
        modal.setBody(
            `<div style="display: flex; gap: 1rem;">
              <div style="flex: 1 0 50%;">
              <img src="${btn.dataset.img}" style="display: block; height: auto; max-width: 50%; margin: 0 auto;">
              </div>
          </div>
          <div class="text-center my-2">
              <a href="${btn.dataset.img}?mime=png" class="btn btn-primary px-4">Скачать PNG</a>
              <a href="${btn.dataset.img}?mime=svg" class="btn btn-primary px-4">Скачать SVG</a>
          </div>`
        );
        modal.show();
    }
    if (e.target.closest('[data-toggle="del-modal"]')) {
        const btn = e.target.closest('[data-toggle="del-modal"]');
        modal.setTitle(`${btn.dataset.title}?`);
        modal.setBody(
            `<div class="text-center my-2 mx-2">
              <button class="btn btn-primary px-4" data-url="${btn.dataset.url}" data-toggle="del-confirm">Удалить</button>
              <button class="btn btn-primary px-4" data-toggle="modal-close">Отменить</button>
          </div>`
        );
        modal.show();
    }
    if (e.target.closest('[data-toggle="del-confirm"]')) {
        const btn = e.target.closest('[data-toggle="del-confirm"]');
        e.preventDefault();
        const request = new XMLHttpRequest();
        request.open('POST', btn.dataset.url);
        request.setRequestHeader('X-CSRFToken', csrftoken);
        request.send();
        request.onload = () => {
            if (request.status === 204) {
                location.reload()
            } else {
                modal.setTitle('Отклонено')
                modal.setBody(
                    `<div class="text-center my-2">
                      <span> 
                          Произошла ошибка, попробуйте снова. 
                          Если проблема повторяется - сообщите администратору.
                      </span>
                  </div>`
                )
            }
        };
    }
    if (e.target.closest('[data-toggle="share-modal"]')) {
        const btn = e.target.closest('[data-toggle="share-modal"]');
        modal.setTitle(btn.dataset.title);
        modal.setBody(`
        <div class="col text-center">
          <a href="https://vk.com/share.php?url=${btn.dataset.share}" target="_blank" rel="nofollow noopener" title="Вконтакте">
            <img src="/static/assets/images/vk-logo.png" style="height: 3em;">
          </a>          
          <a href="https://connect.ok.ru/offer?url=${btn.dataset.share}" target="_blank" rel="nofollow noopener" title="Одноклассники">
            <img src="/static/assets/images/ok-logo.png" style="height: 3em;">
          </a>
          <a href="https://connect.mail.ru/share?url=${btn.dataset.share}" target="_blank" rel="nofollow noopener" title="Мой Мир">
            <img src="/static/assets/images/moimir-logo.png" style="height: 3em;">
          </a>
          <a href="https://t.me/share/url?url=${btn.dataset.share}" target="_blank" rel="nofollow noopener" title="Telegram">
            <img src="/static/assets/images/telegram-logo.png" style="height: 3em;">
          </a>
          <a href="https://api.whatsapp.com/send?text=${btn.dataset.share}" target="_blank" rel="nofollow noopener" title="WhatsApp">
            <img src="/static/assets/images/whatsapp-logo.png" style="height: 3em;">
          </a>
          <a href="https://twitter.com/intent/tweet?url=${btn.dataset.share}" target="_blank" rel="nofollow noopener" title="Twitter">
            <img src="/static/assets/images/twitter-logo.png" style="height: 3em;">
          </a>
        </div
      `);
        modal.show();
    }
    if (e.target.closest('[data-toggle="modal-close"]')) {
        modal.hide();
    }

});


// Hide tooltips when the modal window show
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
$('[data-bs-toggle="tooltip"]').on('click', function (e) {
    $(this).blur();
});
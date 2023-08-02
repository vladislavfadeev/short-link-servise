class ItcModal {
  #elem;
  #template = (
    `<div class="itc-modal-backdrop modal-dialog-centered">
      <div class="itc-modal-content px-3">
        <div class="itc-modal-header ">
          <div class="itc-modal-title">{{title}}</div>
          <span class="itc-modal-btn-close pl-5" title="Закрыть">×</span>
        </div>
        <div class="itc-modal-body">{{content}}</div>
        {{footer}}
        </div>
      </div>`);
  #templateFooter = '<div class="itc-modal-footer">{{buttons}}</div>';
  #templateBtn = '<button type="button" class="{{class}}" data-action={{action}}>{{text}}</button>';
  #eventShowModal = new Event('show.itc.modal', { bubbles: true });
  #eventHideModal = new Event('hide.itc.modal', { bubbles: true });
  #disposed = false;

  constructor(options = []) {
    this.#elem = document.createElement('div');
    this.#elem.classList.add('itc-modal');
    let html = this.#template.replace('{{title}}', options.title || 'Новое окно');
    html = html.replace('{{content}}', options.content || '');
    const buttons = (options.footerButtons || []).map((item) => {
      let btn = this.#templateBtn.replace('{{class}}', item.class);
      btn = btn.replace('{{action}}', item.action);
      return btn.replace('{{text}}', item.text);
    });
    const footer = buttons.length ? this.#templateFooter.replace('{{buttons}}', buttons.join('')) : '';
    html = html.replace('{{footer}}', footer);
    this.#elem.innerHTML = html;
    document.body.append(this.#elem);
    this.#elem.addEventListener('click', this.#handlerCloseModal.bind(this));
  }

  #handlerCloseModal(e) {
    if (e.target.closest('.itc-modal-btn-close') || e.target.classList.contains('itc-modal-backdrop')) {
      this.hide();
    }
  }

  show() {
    if (this.#disposed) {
      return;
    }
    this.#elem.classList.add('itc-modal-show');
    this.#elem.dispatchEvent(this.#eventShowModal);
  }

  hide() {
    this.#elem.classList.remove('itc-modal-show');
    this.#elem.dispatchEvent(this.#eventHideModal);
  }

  dispose() {
    this.#elem.remove(this.#elem);
    this.#elem.removeEventListener('click', this.#handlerCloseModal);
    this.#disposed = true;
  }

  setBody(html) {
    this.#elem.querySelector('.itc-modal-body').innerHTML = html;
  }

  setTitle(text) {
    this.#elem.querySelector('.itc-modal-title').innerHTML = text;
  }

}

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
      request.setRequestHeader('X-CSRFToken',csrftoken);
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
      modal.setBody();
      modal.show();
  }
  if (e.target.closest('[data-toggle="modal-close"]')) {
      modal.hide();
  }

});
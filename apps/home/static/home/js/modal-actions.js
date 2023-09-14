const modal = new ItcModal();
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

async function sendForm(force) {
  try {
    const form = new FormData(document.forms.link_form);
    if (force === true) {
      form.set('force', true);
    }

    const response = await fetch(document.forms.link_form.action, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
      },
      body: form,
    });

    if (!response.ok) {
      throw new Error('Something went wrong');
    }

    const responseData = await response.json();
    spinnerActions('on');
    getStatus(responseData.task_id);
  } catch (error) {
    spinnerActions('off');
    modal.setTitle('Что-то пошло не так..');
    modal.setBody(error.message);
    modal.show();
  }
}

async function getStatus(task_id) {
  try {
    const response = await fetch(`task_status/${task_id}`);
    if (response.status === 200) {
      location.reload();
    } else if (response.status === 202) {
      setTimeout(() => getStatus(task_id), 1000);
    } else {
      const data = await response.json();
      spinnerActions('off');
      modal.setTitle(`Возникла ошибка`);
      modal.setBody(
        `${data.task_result},
        <p class=mb-2><b>Все равно сохранить?</b></p>
        <div class="text-center my-2 mx-2">
          <button class="btn btn-primary px-4" data-toggle="force_save">Сохранить</button>
          <button class="btn btn-primary px-4" data-toggle="modal-close">Отменить</button>
        </div>`
      );
      modal.show();
    }
  } catch (error) {
    spinnerActions('off');
    modal.setTitle('Ошибка');
    modal.setBody('Произошла ошибка при обработке запроса.');
    modal.show();
  }
}

function spinnerActions(action) {
  var button = document.forms.link_form.querySelector('[type="submit"]')
  var spinner = document.forms.link_form.querySelector('.submit-spinner')

  if (action === 'on') {
    button.disabled = true;
    spinner.classList.remove('submit-spinner_hide');
  }
  if (action === 'off') {
    button.disabled = false;
    spinner.classList.add('submit-spinner_hide');
  }
}

document.forms.link_form.addEventListener('submit', (e) => {
  e.preventDefault();
  sendForm(false);
});

document.addEventListener('click', (e) => {
  if (e.target.closest('[data-toggle="force_save"]')) {
    e.preventDefault();
    sendForm(true);
    modal.hide();
  }
  if (e.target.closest('[data-toggle="modal-close"]')) {
    modal.hide();
  }
});


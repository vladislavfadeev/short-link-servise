
function copyToClipboard(inputId) {
    var notification = document.getElementById('notification');
    var copyButton = document.getElementById(`btn${inputId}`);
    var input = document.getElementById(inputId);
    
    var tempInput = document.createElement("input");
    tempInput.setAttribute("type", "text");
    tempInput.setAttribute("value", input.value);
    document.body.appendChild(tempInput);
    
    tempInput.select();
    
    document.execCommand("copy");
    document.body.removeChild(tempInput);

    if (copyButton) {
        copyButton.innerText = "Скопировано!";
        setTimeout(function() {
            copyButton.innerText = "Копировать";
        }, 2000);
    }
    if (notification) {
        notification.style.display = 'block';
        setTimeout(() => {
            notification.style.display = 'none';
        }, 1000);
    };
  }
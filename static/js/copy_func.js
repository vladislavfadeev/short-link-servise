
function copyToClipboard(inputId) {
    var copyButton = document.getElementById("copy-button");
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
        }, 3000);
    }
  }
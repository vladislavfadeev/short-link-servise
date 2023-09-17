var navbar = document.getElementById('sidebar')
var collapseButton = document.getElementById('mobile-collapse')

var cookieValue = document.cookie.split("; ").find((row) => row.startsWith("navbarCollapse="))?.split("=")[1];
if (cookieValue === 'True') {
    navbar.classList.add('navbar-collapsed');
} else if (cookieValue === undefined) {
    document.cookie = "navbarCollapse=False; path=/; SameSite=None; Secure";
}

function changeCollapseStatus() {
    var cookieValue = document.cookie.split("; ").find((row) => row.startsWith("navbarCollapse="))?.split("=")[1];
    if (cookieValue === 'True') {
        document.cookie = "navbarCollapse=False; path=/; SameSite=None; Secure";
    } else if (cookieValue === 'False') {
        document.cookie = "navbarCollapse=True; path=/; SameSite=None; Secure";
    }
}

collapseButton.addEventListener('click', function () {
    changeCollapseStatus()
});

window.addEventListener("scroll", function() {
    let navbar = document.getElementById("navbar");
    if (window.scrollY > 50) {
        navbar.classList.add("scrolled");
    } else {
        navbar.classList.remove("scrolled");
    }
});

document.querySelectorAll('.custom-btn').forEach(function(button) {
    button.addEventListener('click', function() {
        button.classList.toggle('active');
    });
});

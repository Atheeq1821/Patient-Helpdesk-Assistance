window.addEventListener('scroll', function() {
    const navbar = document.getElementById('navbar');
    if (window.scrollY > 50) { 
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

var typed = new Typed('#t2', {
    strings: ["We're GLAD YOU'RE Here...."],
    typeSpeed: 30,
    loop: false,
    showCursor: false,
    startDelay: 1000,
  });
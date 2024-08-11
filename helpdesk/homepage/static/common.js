window.addEventListener('scroll', function() {
    const navbar = document.getElementById('navbar');
    if (window.scrollY > 50) { 
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry)=> {
      console.log(entry)
      if(entry.isIntersecting){
        entry.target.classList.add('show')
      }else{
        entry.target.classList.remove('show')
      }
    })
  })
  const hiddenElements = document.querySelectorAll('.hidden')
  hiddenElements.forEach((el) => observer.observe(el))


  const observer_lr = new IntersectionObserver((entries) => {
    entries.forEach((entry)=> {
      console.log(entry)
      if(entry.isIntersecting){
        entry.target.classList.add('show-lr')
      }else{
        entry.target.classList.remove('show-lr')
      }
    })
  })
  const hiddenElements_lr = document.querySelectorAll('.hidden-lr')
  hiddenElements_lr.forEach((el) => observer_lr.observe(el))

  const observer_rl = new IntersectionObserver((entries) => {
    entries.forEach((entry)=> {
      console.log(entry)
      if(entry.isIntersecting){
        entry.target.classList.add('show-rl')
      }else{
        entry.target.classList.remove('show-rl')
      }
    })
  })
  const hiddenElements_rl = document.querySelectorAll('.hidden-rl')
  hiddenElements_rl.forEach((el) => observer_rl.observe(el))
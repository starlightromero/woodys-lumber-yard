const slider = document.querySelector('.slider')
const remember = document.getElementById('remember')

slider.addEventListener('click', () => {
  remember.checked ? remember.checked = false : remember.checked = true
})

const searchBtn = document.querySelector('.search-btn')
const searchForm = document.querySelector('.search-form')

searchBtn.addEventListener('click', () => {
  searchBtn.classList.toggle('slideOutRight')
  searchForm.style.display = 'flex'
  searchForm.classList.toggle('fadeIn')
})

const adminButton = document.getElementById('admin-button')

adminButton.addEventListener('click', () => {
  window.location.href = '/admin'
})

const cart = document.querySelector('.cart')
const addToCart = document.querySelector('button[name=\'add-to-cart\']')

addToCart.addEventListener('click', () => {
  alert('added')
})

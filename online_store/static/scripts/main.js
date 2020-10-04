const searchBtn = document.querySelector('.search-btn')
const searchForm = document.querySelector('.search-form')

searchBtn.addEventListener('click', () => {
  searchBtn.classList.toggle('slideOutRight')
  searchForm.style.display = 'flex'
  searchForm.classList.toggle('fadeIn')
})

// const cart = document.querySelector('.cart')
// const addToCart = document.querySelector('button[name=\'add-to-cart\']')
//
// addToCart.addEventListener('click', () => {
//   alert('added')
// })

const searchBtn = document.querySelector('.search-btn')
const searchForm = document.querySelector('.search-form')

searchBtn.addEventListener('click', () => {
  searchBtn.classList.toggle('slideOutRight')
  searchForm.style.display = 'flex'
  searchForm.classList.toggle('fadeIn')
})

const cartTotal = document.querySelector('.cart-total')

const addToCart = productId => {
  axios.put('/cart/' + productId)
    .then(function (response) {
      cartTotal.innerHTML = +cartTotal.innerHTML + 1
    })
    .catch(function (error) {
      console.log(error)
    })
}

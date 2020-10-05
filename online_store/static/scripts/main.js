const searchBtn = document.querySelector('.search-btn')
const searchForm = document.querySelector('.search-form')

searchBtn.addEventListener('click', () => {
  searchBtn.classList.toggle('slideOutRight')
  searchForm.style.display = 'flex'
  searchForm.classList.toggle('fadeIn')
})

const cart = document.querySelector('.cart')

const addToCart = productId => {
  axios.put('/cart/' + productId)
    .then(function (response) {
      console.log(response)
    })
    .catch(function (error) {
      console.log(error)
    })
}

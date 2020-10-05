const searchBtn = document.querySelector('.search-btn')
const searchForm = document.querySelector('.search-form')

searchBtn.addEventListener('click', () => {
  searchBtn.classList.toggle('slideOutRight')
  searchForm.style.display = 'flex'
  searchForm.classList.toggle('fadeIn')
})

const cartTotal = document.querySelector('.cart-total')

const addToCart = productId => {
  const productItem = document.getElementById(productId)
  axios.put('/cart/' + productId)
    .then(function (response) {
      cartTotal.innerHTML = +cartTotal.innerHTML + 1
      const newQuantity = +productItem.getAttribute('data-quantity') - 1
      productItem.setAttribute('data-quantity', newQuantity)
      checkQuantityInStock()
    })
    .catch(function (error) {
      console.log(error)
    })
}

const productItems = document.querySelectorAll('.product-item')

const checkQuantityInStock = () => {
  for (const prod of productItems) {
    const addToCart = prod.querySelector('.add-to-cart')
    if (+prod.getAttribute('data-quantity') === 0) {
      addToCart.disabled = true
      addToCart.style.backgroundColor = '#B09C7D'
      addToCart.innerHTML = 'Sold Out'
    }
  }
}

checkQuantityInStock()

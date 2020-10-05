/*  global
    axios
*/

const formQuantity = document.querySelector('.form-quantity')
const inStock = document.querySelector('.in-stock')
const addToCartBtn = document.querySelector('.add-to-cart')

const checkQuantity = () => {
  const quantity = +formQuantity.value
  if (quantity > +inStock.innerHTML || quantity < 1) {
    addToCartBtn.disable = true
    addToCartBtn.style.backgroundColor = '#B09C7D'
  } else {
    addToCartBtn.disable = false
    addToCartBtn.style.backgroundColor = '#634C29'
  }
}

formQuantity.addEventListener('keydown', checkQuantity)
formQuantity.addEventListener('keyup', checkQuantity)
formQuantity.addEventListener('change', checkQuantity)

const addManyToCart = productId => {
  const quantity = +formQuantity.value
  axios.put('/cart/' + productId, {
    quantity: quantity
  })
    .then(function (response) {
      cartTotal.innerHTML = +cartTotal.innerHTML + quantity
    })
    .catch(function (error) {
      console.log(error)
    })
}

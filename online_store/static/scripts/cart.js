/*  global
    axios
*/

const removeFromCart = productId => {
  const product = document.getElementById(productId)
  const price = product.querySelector('.price')
  const quantityInCart = product.querySelector('.quantity-in-cart')
  const totalProducts = document.getElementById('total-products')
  const subtotal = document.getElementById('subtotal')
  const quantity = +quantityInCart.innerHTML
  axios.delete('/cart/' + productId)
    .then(function (response) {
      cartTotal.innerHTML = +cartTotal.innerHTML - quantity
      product.remove()
      totalProducts.innerHTML = +totalProducts.innerHTML - quantity
      subtotal.innerHTML = +subtotal.innerHTML - ((quantity * +price.innerHTML).toFixed(2))
    })
    .catch(function (error) {
      console.log(error)
    })
}

const clearCart = () => {
  const allProducts = document.querySelectorAll('.cart-products')
  const totalProducts = document.getElementById('total-products')
  const subtotal = document.getElementById('subtotal')
  axios.delete('/cart')
    .then(function (response) {
      cartTotal.innerHTML = 0
      for (const product of allProducts) {
        product.remove()
      }
      totalProducts.innerHTML = 0
      subtotal.innerHTML = '0.00'
    })
    .catch(function (error) {
      console.log(error)
    })
}

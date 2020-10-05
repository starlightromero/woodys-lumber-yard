/*  global
    axios
*/

const addToCart = productId => {
  const formQuantity = document.querySelector('.form-quantity')
  const quantity = +formQuantity.innerHTML
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

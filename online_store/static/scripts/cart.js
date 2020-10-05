/*  global
    axios
*/

const removeFromCart = productId => {
  console.log('delete')
  const product = document.getElementById(productId)
  const quantity = product.querySelector('h3')
  axios.delete('/cart/' + productId)
    .then(function (response) {
      cartTotal.innerHTML = +cartTotal.innerHTML - +quantity.innerHTML
    })
    .catch(function (error) {
      console.log(error)
    })
}

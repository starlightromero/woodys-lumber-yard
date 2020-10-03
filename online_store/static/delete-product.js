/*  global
    axios
*/

const deleteProduct = productId => {
  axios.delete('/admin/' + productId)
    .then(function (response) {
      console.log(response)
      window.location.href = '/admin'
    })
    .catch(function (error) {
      console.log(error)
      window.location.href = '/admin'
    })
}

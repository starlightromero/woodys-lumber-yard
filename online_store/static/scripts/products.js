/*  global
    axios
*/

const deleteProduct = productId => {
  axios.delete('/admin/products/' + productId)
    .then(function (response) {
      console.log(response)
      window.location.href = '/admin/products'
    })
    .catch(function (error) {
      console.log(error)
      window.location.href = '/admin/products'
    })
}

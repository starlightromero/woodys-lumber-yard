/*  global
    axios
*/

const deleteCategory = categoryId => {
  axios.delete('/admin/category/' + categoryId)
    .then(function (response) {
      console.log(response)
      window.location.href = '/admin/category'
    })
    .catch(function (error) {
      console.log(error)
      window.location.href = '/admin/category'
    })
}

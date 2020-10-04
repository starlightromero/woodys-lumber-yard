/*  global
    axios
*/

const updateCategory = categoryId => {
  const categoryName = document.querySelector(`[data-id='${categoryId}']`)
  axios.put('/admin/categories/' + categoryId, {
    name: categoryName.value
  })
    .then(function (response) {
      console.log(response)
      window.location.href = '/admin/categories'
    })
    .catch(function (error) {
      console.log(error)
      window.location.href = '/admin/categories'
    })
}

const deleteCategory = categoryId => {
  axios.delete('/admin/categories/' + categoryId)
    .then(function (response) {
      console.log(response)
      window.location.href = '/admin/categories'
    })
    .catch(function (error) {
      console.log(error)
      window.location.href = '/admin/categories'
    })
}

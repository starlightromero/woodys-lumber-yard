/*  global
    axios
*/

const updateCategory = categoryId => {
  const categoryName = document.querySelector(`[data-id='${categoryId}']`)
  axios.put('/admin/category/' + categoryId, {
    name: categoryName.value
  })
    .then(function (response) {
      console.log(response)
      window.location.href = '/admin/category'
    })
    .catch(function (error) {
      console.log(error)
      window.location.href = '/admin/category'
    })
}

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

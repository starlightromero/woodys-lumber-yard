const goToUrl = (url) => {
  window.location.href = url
}

const productsBtn = document.getElementById('products')
const findProductsBtn = document.getElementById('find-products')
const addProductsBtn = document.getElementById('add-products')
const deleteProductsBtn = document.getElementById('delete-products')
const deleteAllBtn = document.getElementById('delete-all')

productsBtn.addEventListener('click', goToUrl.bind(this, '/admin/products'))
findProductsBtn.addEventListener('click', goToUrl.bind(this, '/admin/find-products'))
addProductsBtn.addEventListener('click', goToUrl.bind(this, '/admin/add-products'))
deleteProductsBtn.addEventListener('click', goToUrl.bind(this, '/admin/delete-products'))

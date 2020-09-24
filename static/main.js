const searchBtn = document.querySelector('.search-btn')
const searchForm = document.querySelector('.search-form')

searchBtn.addEventListener('click', () => {
  searchBtn.classList.toggle('slideOutRight')
  searchForm.style.display = 'flex'
  searchForm.classList.toggle('fadeIn')
})

const adminButton = document.getElementById('admin-button')

adminButton.addEventListener('click', function () {
  window.location.href = '/admin'
})

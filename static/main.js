const searchBtn = document.querySelector('.search-btn')
const searchForm = document.querySelector('.search-form')

searchBtn.addEventListener('click', () => {
  searchBtn.classList.toggle('slideOutRight')
  searchForm.style.display = 'flex'
  searchForm.classList.toggle('fadeIn')
})

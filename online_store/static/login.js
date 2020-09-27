const login = document.querySelector('.login')
const signup = document.querySelector('.signup')
const goToLogin = document.getElementById('goToLogin')
const goToSignup = document.getElementById('goToSignup')

goToSignup.addEventListener('click', () => {
  login.style.display = 'none'
  signup.style.display = 'block'
})

goToLogin.addEventListener('click', () => {
  signup.style.display = 'none'
  login.style.display = 'block'
})

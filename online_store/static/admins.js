/*  global
    axios
*/

const revoke = adminId => {
  axios.put('/admin/admins/' + adminId)
    .then(function (response) {
      console.log(response)
      window.location.href = '/admin/admins'
    })
    .catch(function (error) {
      console.log(error)
      window.location.href = '/admin/admins'
    })
}

const grant = userId => {
  axios.put('/admin/admins/' + userId)
    .then(function (response) {
      console.log(response)
      window.location.href = '/admin/admins'
    })
    .catch(function (error) {
      console.log(error)
      window.location.href = '/admin/admins'
    })
}

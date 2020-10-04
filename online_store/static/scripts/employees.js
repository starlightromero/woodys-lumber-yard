/*  global
    axios
*/

const revoke = id => {
  axios.put('/admin/employees/' + id)
    .then(function (response) {
      console.log(response)
      window.location.href = '/admin/employees'
    })
    .catch(function (error) {
      console.log(error)
      window.location.href = '/admin/employees'
    })
}

const grant = id => {
  axios.put('/admin/employees/' + id)
    .then(function (response) {
      console.log(response)
      window.location.href = '/admin/employees'
    })
    .catch(function (error) {
      console.log(error)
      window.location.href = '/admin/employees'
    })
}

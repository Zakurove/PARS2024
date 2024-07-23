function approved(par_id) {
    let elem = document.getElementById(par_id);
    elem.style.color = '9e9e9e';
    let data = {par_id: par_id, action: 'approved' };
    console.log(data);
    edit_par(data);
}

function pending(par_id) {
    let elem = document.getElementById(par_id);
    elem.style.color = 'black';
    let data = {par_id: par_id, action: 'pending' };
    edit_par(data);
}

function edit_par(data) {
    let req = axios({
    method: 'post',
    url: '/api/edit_par/',
    xsrfCookieName: 'csftoken',
    xsrffHeaderName: 'X-CSRFTOKEN',
    data: data,
    headers: {
        'X-CSRFTOKEN': 'csftoken'
        }
    }).then((response) => {
        this.par = response.data;
        console.log(response);
    });
    return;
}
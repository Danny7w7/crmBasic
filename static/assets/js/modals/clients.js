document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.view-client').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const id = this.dataset.id;
            if (id) {
                viewRemitter(id);
            }
        });
    });
});

function viewRemitter(id) {
    fetch(`/getRemitterDetail/${id}/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const r = data.data;
                document.getElementById('modal-r-full-name').textContent = r.full_name || '';
                document.getElementById('modal-r-address').textContent = r.address || '';
                document.getElementById('modal-r-city').textContent = r.city || '';
                document.getElementById('modal-r-country').textContent = r.country || '';
                document.getElementById('modal-r-phone').textContent = r.phone_number || '';
                document.getElementById('modal-r-email').textContent = r.email || '';
                document.getElementById('modal-r-cod').textContent = r.cod_number || '';
                document.getElementById('modal-r-created').textContent = r.created_at || '';
            } else {
                alert('No se pudo obtener la información del remitente.');
            }
        })
        .catch(err => {
            alert('Error al obtener datos del remitente.');
            console.error(err);
        });
}

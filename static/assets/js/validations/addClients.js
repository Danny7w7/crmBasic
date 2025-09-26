// selects.js
document.addEventListener('DOMContentLoaded', function () {

    console.log('QUI ANDAMOS')

    // ----- REMITENTE -----
    const remitenteSelect = new TomSelect('#client-nombre', {
        placeholder: 'Escriba el nombre...',
        valueField: 'id',
        labelField: 'full_name',
        searchField: 'full_name',
        load: function (query, callback) {
            if (!query.length) return callback();

            fetch(`/findClient/?search=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => callback(data.data || []))
                .catch(() => callback());
        },
    });

    document.querySelector('#client-nombre').addEventListener('change', async function () {
        const clientId = this.value;
        try {
            const response = await fetch(`/searchClientData/?id=${clientId}`);
            const data = await response.json();

            if (data.success) {
                const d = data.data;
                document.querySelector('#client-direccion').value = d.address || '';
                document.querySelector('#client-telefono').value = d.phone_number || '';
                document.querySelector('#client-id').value = d.id || '';
            } else {
                alert('Error: ' + data.error);
            }
        } catch (error) {
            alert('Error al obtener los datos del remitente.');
        }

        checkForm();
    });

    
});

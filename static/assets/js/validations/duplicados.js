document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('#clientForm') || document.querySelector('#receiverForm');

    if (!form) return;

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const isRemitter = form.id === 'clientForm';
        const type = isRemitter ? 'remitter' : 'receiver';

        const data = {
            type: type,
            full_name: form.querySelector('[name="full_name"]').value.trim(),
            address: form.querySelector('[name="address"]').value.trim(),
            city: form.querySelector('[name="city"]').value.trim(),
            country: form.querySelector('[name="country"]').value.trim(),
            phone_number: form.querySelector('[name="phone_number"]').value.trim(),
            email: form.querySelector('[name="email"]').value.trim()
        };

        const queryParams = new URLSearchParams(data).toString();

        try {
            const response = await fetch(`/checkPersonExists/?${queryParams}`);
            const result = await response.json();

            if (result.exists) {
                Swal.fire({
                    icon: 'warning',
                    title: 'Duplicado',
                    text: `Ya existe un ${type === 'remitter' ? 'remitente' : 'destinatario'} con esa información.`,
                    confirmButtonText: 'Entendido'
                });
                return;
            }else {
                form.submit(); // ✅ No existe, continuar con el envío real
            }
        } catch (error) {
            alert("Hubo un error al validar la existencia del registro.");
        }
    });
});

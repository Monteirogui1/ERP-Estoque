// Função para destacar o item ativo no sidebar com base na URL atual
document.addEventListener('DOMContentLoaded', () => {
    const sidebarLinks = document.querySelectorAll('.sidebar nav ul li a');
    const currentPath = window.location.pathname;

    sidebarLinks.forEach(link => {
        // Remove a barra final do href e do currentPath para comparação
        const linkPath = link.getAttribute('href').replace(/\/$/, '');
        const normalizedCurrentPath = currentPath.replace(/\/$/, '');

        // Verifica se o link corresponde à URL atual
        if (linkPath === normalizedCurrentPath) {
            link.parentElement.classList.add('active');
        }
    });
});

// Funcionalidade do botão de logout (apenas um exemplo)
// document.querySelector('.logout-btn')?.addEventListener('click', () => {
//     alert('Você saiu do sistema!');
// });

// Funcionalidade de exclusão (exemplo genérico, precisa de integração com backend)
document.querySelectorAll('.btn-delete').forEach(button => {
    button.addEventListener('click', () => {
        const id = button.getAttribute('data-id');
        if (confirm('Tem certeza que deseja excluir este item?')) {
            // Aqui você pode fazer uma requisição AJAX para excluir o item
            alert(`Item com ID ${id} seria excluído (funcionalidade de exemplo).`);
            // Exemplo de requisição (descomente e ajuste conforme necessário):
            /*
            fetch(`/delete-url/${id}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            }).then(response => {
                if (response.ok) {
                    button.closest('tr').remove();
                }
            });
            */
        }
    });
});

// Função para toggle de senha na página de login
function togglePassword() {
    const passwordField = document.getElementById('password');
    const toggleIcon = document.getElementById('toggleIcon');
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash');
    } else {
        passwordField.type = 'password';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    }
}


document.addEventListener('DOMContentLoaded', () => {
    const notificationIcon = document.querySelector('.notification-icon');
    const notificationDropdown = document.querySelector('#notificationDropdown');

    if (notificationIcon && notificationDropdown) {
        notificationIcon.addEventListener('click', (e) => {
            e.preventDefault();
            notificationDropdown.style.display =
                notificationDropdown.style.display === 'block' ? 'none' : 'block';
        });

        document.addEventListener('click', (e) => {
            if (!notificationIcon.contains(e.target) && !notificationDropdown.contains(e.target)) {
                notificationDropdown.style.display = 'none';
            }
        });
    }
});
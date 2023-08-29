$(document).ready(function () {
    $('#login').click(function () {
        facebookLogin();
    });

    function facebookLogin() {
        FB.login(function (response) {
            if (response.authResponse) {
                getFacebookData();
            }
        }, { scope: 'email, public_profile' });
    }

    function getFacebookData() {
        FB.api('/me', { fields: 'name' }, function (response) {
            $('#login').after('<div id="facebook-session">' +
                '<strong>Bienvenido: ' + response.name + '</strong>' +
                '<a href="#" id="logout" class="btn btn-danger">Cerrar sesión</a>' +
                '</div>');
            $('#login').remove();
        });
    }

    $(document).on('click', '#logout', function (e) {
        e.preventDefault();
        if (confirm("¿Está seguro?")) {
            FB.logout(function (response) {
                $('#facebook-session').before('<button type="button" id="login" class="btn btn-outline-primary flex-grow-1 mr-2 d-flex align-items-center justify-content-center"><i class="fab fa-facebook-f lead mr-2"></i> Facebook</button>');
                $('#facebook-session').remove();
            });
        }
    });
});

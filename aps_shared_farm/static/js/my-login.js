/******************************************
 * My Login
 *
 * Bootstrap 4 Login Page
 *
 * @author          Muhamad Nauval Azhar
 * @uri            https://nauval.in
 * @copyright       Copyright (c) 2018 Muhamad Nauval Azhar
 * @license         My Login is licensed under the MIT license.
 * @github          https://github.com/nauvalazhar/my-login
 * @version         1.2.0
 *
 * Help me to keep this project alive
 * https://www.buymeacoffee.com/mhdnauvalazhar
 *
 ******************************************/

'use strict';

$(function () {

    // // author badge :)
    // var author = '<div style="position: fixed;bottom: 0;right: 20px;background-color: #fff;box-shadow: 0 4px 8px rgba(0,0,0,.05);border-radius: 3px 3px 0 0;font-size: 12px;padding: 5px 10px;">By <a href="https://twitter.com/mhdnauvalazhar">@mhdnauvalazhar</a> &nbsp;&bull;&nbsp; <a href="https://www.buymeacoffee.com/mhdnauvalazhar">Buy me a Coffee</a></div>';
    // $("body").append(author);

    $("input[type='password'][data-eye]").each(function (i) {
        var $this = $(this),
            id = 'eye-password-' + i,
            el = $('#' + id);

        $this.wrap($("<div/>", {
            style: 'position:relative',
            id: id
        }));

        $this.css({
            paddingRight: 60
        });
        $this.after($("<div/>", {
            html: 'Show',
            class: 'btn btn-primary btn-sm',
            id: 'passeye-toggle-' + i,
        }).css({
            position: 'absolute',
            right: 10,
            top: ($this.outerHeight() / 2) - 12,
            padding: '2px 7px',
            fontSize: 12,
            cursor: 'pointer',
        }));

        $this.after($("<input/>", {
            type: 'hidden',
            id: 'passeye-' + i
        }));

        var invalid_feedback = $this.parent().parent().find('.invalid-feedback');

        if (invalid_feedback.length) {
            $this.after(invalid_feedback.clone());
        }

        $this.on("keyup paste", function () {
            $("#passeye-" + i).val($(this).val());
        });
        $("#passeye-toggle-" + i).on("click", function () {
            if ($this.hasClass("show")) {
                $this.attr('type', 'password');
                $this.removeClass("show");
                $(this).removeClass("btn-outline-primary");
            } else {
                $this.attr('type', 'text');
                $this.val($("#passeye-" + i).val());
                $this.addClass("show");
                $(this).addClass("btn-outline-primary");
            }
        });
    });

    $(".my-login-validation").submit(function () {
        var form = $(this);
        if (form[0].checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.addClass('was-validated');
    });
});

const togglePassword = document.querySelector('#togglePassword');
const signUpTogglePassword = document.querySelector('#signUpTogglePassword1');
const signUpTogglePassword1 = document.querySelector('#signUpTogglePassword2');
const resetTogglePassword1 = document.querySelector('#resetTogglePassword1');
const resetTogglePassword2 = document.querySelector('#resetTogglePassword2');
const password = document.querySelector('#id_password');
const password1 = document.querySelector('#id_password1');
const password2 = document.querySelector('#id_password2');
const resetPassword1 = document.querySelector('#id_new_password1');
const resetPassword2 = document.querySelector('#id_new_password2');
document.body.addEventListener('click', event => {
    if (event.target === togglePassword) {
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';

        password.setAttribute('type', type);
        // toggle the eye / eye slash icon
        if (togglePassword.classList.contains("fa-eye-slash")) {
            togglePassword.classList.toggle('fa-eye', true);
            togglePassword.classList.toggle('fa-eye-slash', false);
        } else {
            togglePassword.classList.toggle('fa-eye', false);
            togglePassword.classList.toggle('fa-eye-slash', true);
        }
    } else if (event.target === signUpTogglePassword) {

        const type = password1.getAttribute('type') === 'password' ? 'text' : 'password';
        console.log(type);
        password1.setAttribute('type', type);
        // toggle the eye / eye slash icon
        if (signUpTogglePassword.classList.contains("fa-eye-slash")) {
            signUpTogglePassword.classList.toggle('fa-eye', true);
            signUpTogglePassword.classList.toggle('fa-eye-slash', false);
        } else {
            signUpTogglePassword.classList.toggle('fa-eye', false);
            signUpTogglePassword.classList.toggle('fa-eye-slash', true);
        }


    } else if (event.target === signUpTogglePassword1) {
        // toggle the type attribute
        const type = password2.getAttribute('type') === 'password' ? 'text' : 'password';

        password2.setAttribute('type', type);
        // toggle the eye / eye slash icon
        if (signUpTogglePassword1.classList.contains("fa-eye-slash")) {
            signUpTogglePassword1.classList.toggle('fa-eye', true);
            signUpTogglePassword1.classList.toggle('fa-eye-slash', false);
        } else {
            signUpTogglePassword1.classList.toggle('fa-eye', false);
            signUpTogglePassword1.classList.toggle('fa-eye-slash', true);
        }
    }
    else if (event.target === resetTogglePassword1) {
        // toggle the type attribute
        const type = resetPassword1.getAttribute('type') === 'password' ? 'text' : 'password';

        resetPassword1.setAttribute('type', type);
        // toggle the eye / eye slash icon
        if (resetTogglePassword1.classList.contains("fa-eye-slash")) {
            resetTogglePassword1.classList.toggle('fa-eye', true);
            resetTogglePassword1.classList.toggle('fa-eye-slash', false);
        } else {
            resetTogglePassword1.classList.toggle('fa-eye', false);
            resetTogglePassword1.classList.toggle('fa-eye-slash', true);
        }
    }
    else if (event.target === resetTogglePassword2) {
        // toggle the type attribute
        const type = resetPassword2.getAttribute('type') === 'password' ? 'text' : 'password';

        resetPassword2.setAttribute('type', type);
        // toggle the eye / eye slash icon
        if (resetTogglePassword2.classList.contains("fa-eye-slash")) {
            resetTogglePassword2.classList.toggle('fa-eye', true);
            resetTogglePassword2.classList.toggle('fa-eye-slash', false);
        } else {
            resetTogglePassword2.classList.toggle('fa-eye', false);
            resetTogglePassword2.classList.toggle('fa-eye-slash', true);
        }
    }
    else {
        console.log('no event listener')
    }
    //handle click
});
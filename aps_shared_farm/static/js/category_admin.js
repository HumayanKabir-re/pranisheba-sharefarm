


window.addEventListener("load", function() {
    (function ($) {
        $(function () {
            var selectField = $('#id_category'),
                verified = $('.general_css'),
                verified_menu = $('.shariah_css');

            function toggleVerified(value) {
                if (value === 'general') {
                    verified.show();
                    verified_menu.hide();
                } else {
                    verified.hide();
                    verified_menu.show();
                }
            }

            // show/hide on load based on pervious value of selectField
            toggleVerified(selectField.val());

            // show/hide on change
            selectField.change(function () {
                toggleVerified($(this).val());
            });
        });
    })(django.jQuery);
});
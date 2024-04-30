// script.js

$(document).ready(function() {
    // Form validation
    $('form').on('submit', function(event) {
        let isValid = true;

        // Validate location
        const location = $('#location').val().trim();
        if (location === '') {
            alert('Please enter a location.');
            isValid = false;
        }

        // Validate year
        const year = parseInt($('#year').val());
        if (isNaN(year) || year < 1901 || year > new Date

().getFullYear()) {
            alert('Please enter a valid year between 1901 

and ' + new Date().getFullYear());
            isValid = false;
        }

        // If form is not valid, prevent submission
        if (!isValid) {
            event.preventDefault();
        }
    });

    // Additional JavaScript can be added here for 

other interactions
});
$(document).ready(function() {
    // Activate the carousel with options
    $('#testimonialCarousel').carousel({
        interval: 5000, // Auto slide every 5 seconds
        pause: 'hover' // Pause on hover
    });

    // Enable manual sliding with carousel navigation buttons
    $('.carousel-control-prev').click(function() {
        $('#testimonialCarousel').carousel('prev');
    });

    $('.carousel-control-next').click(function() {
        $('#testimonialCarousel').carousel('next');
    });
});

$(document).ready(function() {
    $(".flash-message").each(function() {
        $(this).css("opacity", "1"); // Fade in
        setTimeout(() => {
            $(this).fadeTo(500, 0, function() { // Start fade out after 3 seconds
                $(this).remove();
            });
        }, 3000);
    });
});
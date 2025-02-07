$(document).ready(function() {
    $('#chat-form').on('submit', function(event) {
        event.preventDefault();

        $.ajax({
            url: '', // The current URL will handle the POST request
            type: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                $('#chat-container').append(
                    '<div class="chat-message bot"><p>' + response.response + '</p></div>'
                );
                $('#prompt-input').val(''); // Clear the input field
                $('#chat-container').scrollTop($('#chat-container')[0].scrollHeight); // Auto-scroll
            },
            error: function(xhr, errmsg, err) {
                console.error(xhr.status + ": " + xhr.responseText);
            }
        });
    });
});
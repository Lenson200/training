$(document).ready(function() {
    $('#mark-complete-btn').click(function() {
        // Get CSRF token from cookie
        var csrftoken = getCookie('csrftoken');
        
        // Assume you have these variables defined somewhere
        var module_id_value = 'module-id';
        var trainee_id_value = 'trainee-id';
        var progress_value =100 ; 
        
        // Log variables to console to ensure they have expected values
        console.log('csrftoken:', csrftoken);
        console.log('module_id_value:', module_id_value);
        console.log('trainee_id_value:', trainee_id_value);
        console.log('progress_value:', progress_value);
        
        // AJAX request to mark module complete
        $.ajax({
            url: '/mark_module_complete/',
            type: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken  // Include CSRF token in headers
            },
            data: {
                'module_id': module_id_value,
                'trainee_id': trainee_id_value,
                'progress': progress_value
            },
            success: function(response) {
                alert(response.message);
                // Update UI based on response, e.g., show completion status
                if (response.message === 'Module marked as complete.') {
                    // Update UI to reflect completion
                    $('#module-' + module_id).addClass('completed');  // Example: add a CSS class
                     $('#module-' + module_id + ' .status').text('Completed');
                     //success page after marking complete
                     window.location.href = '{% url "success_page" %}';
                } else {
                    // Update UI to indicate not completed
                    $('#module-' + module_id).removeClass('completed');  // remove a CSS class
                   $('#module-' + module_id + ' .status').text('Not Completed');
                }
            },
            error: function(xhr, status, error) {
                alert('Error: ' + xhr.responseText);
                // Handle error
                console.error('Error marking module as complete:', error);
               alert('Error marking module as complete. Please try again.');
            }
        });
    });

    // Function to get CSRF token from cookie
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});


// document.addEventListener("DOMContentLoaded", function() {
//     var progressData = document.getElementById("progress-data");

//     if (!progressData) {
//         console.error("Element with ID 'progress-data' not found.");
//         return;
//     }

//     var totalPages = progressData.getAttribute("data-total-pages");
//     var traineeId = progressData.getAttribute("data-trainee-id");
//     var moduleId = progressData.getAttribute("data-module-id");
//     var csrfToken = progressData.getAttribute("data-csrf-token");

//     function markPageAsRead(pageNum) {
//         // Calculate progress percentage
//         var progress = Math.round((pageNum / totalPages) * 100);

//         // AJAX call to update progress
//         $.ajax({
//             url: progressData.getAttribute("data-url"),
//             type: 'POST',
//             data: {
//                 'trainee_id': traineeId,
//                 'module_id': moduleId,
//                 'progress': progress,
//                 'csrfmiddlewaretoken': csrfToken
//             },
//             success: function(data) {
//                 console.log('Progress updated successfully.');
//             },
//             error: function(xhr, errmsg, err) {
//                 console.log('Error updating progress.');
//             }
//         });
//     }

//     // Example usage:
//     // markPageAsRead(1);
// });
// module_detail.js

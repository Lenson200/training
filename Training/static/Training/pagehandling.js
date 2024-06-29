$(document).ready(function() {
    $('#mark-complete-btn').click(function() {
        var moduleId = $('#module-id').val();  // Assuming you have input fields or hidden inputs for these values
        var traineeId = $('#trainee-id').val();

        // AJAX call to mark module as completed
        $.ajax({
            url: '/mark_module_complete/',  // Replace with your actual URL
            type: 'POST',
            data: {
                'module_id': moduleId,
                'trainee_id': traineeId,
                'progress': 100,  // Set progress to 100
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(data) {
                console.log('Module marked as completed.');
                // Optionally update UI or perform other actions upon success
            },
            error: function(xhr, errmsg, err) {
                console.error('Error marking module as completed.');
            }
        });
    });
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

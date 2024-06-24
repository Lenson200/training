document.addEventListener("DOMContentLoaded", function() {
    var progressData = document.getElementById("progress-data");

    var totalPages = progressData.getAttribute("data-total-pages");
    var traineeId = progressData.getAttribute("data-trainee-id");
    var moduleId = progressData.getAttribute("data-module-id");
    var csrfToken = progressData.getAttribute("data-csrf-token");

    function markPageAsRead(pageNum) {
        // Calculate progress percentage
        var progress = Math.round((pageNum / totalPages) * 100);

        // AJAX call to update progress
        $.ajax({
            url: progressData.getAttribute("data-url"),
            type: 'POST',
            data: {
                'trainee_id': traineeId,
                'module_id': moduleId,
                'progress': progress,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(data) {
                console.log('Progress updated successfully.');
            },
            error: function(xhr, errmsg, err) {
                console.log('Error updating progress.');
            }
        });
    }

    // Example usage:
    // markPageAsRead(1);
});

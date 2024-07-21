document.addEventListener('DOMContentLoaded', function() {
    const progressRange = document.getElementById('progressRange');
    const progressValue = document.getElementById('progressValue');

    progressRange.addEventListener('input', function() {
        const progress = this.value;
        progressValue.textContent = progress + '%';
        updateProgress(window.examId, progress);
    });

    function updateProgress(examId, progress) {
        fetch(`/update_progress/${examId}/${progress}/`)
            .then(response => response.json())
            .then(data => {
                if (data.status !== 'ok') {
                    console.error('Failed to update progress');
                }
            })
            .catch(error => console.error('Error:', error));
    }

    // Set initial progress value
    progressRange.value = window.progressValue;
    progressValue.textContent = window.progressValue + '%';
});

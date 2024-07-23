document.addEventListener('DOMContentLoaded', function() {
    // Prevent default form submission and handle step transitions
    document.getElementById('formStep1').addEventListener('submit', function(e) {
        e.preventDefault();
        document.getElementById('step1').style.display = 'none';
        document.getElementById('step2').style.display = 'block';
    });

    document.getElementById('formStep2').addEventListener('submit', function(e) {
        e.preventDefault();
        document.getElementById('step2').style.display = 'none';
        document.getElementById('step3').style.display = 'block';
    });

    document.getElementById('formStep3').addEventListener('submit', function(e) {
        e.preventDefault();
        document.getElementById('step3').style.display = 'none';
        document.getElementById('step4').style.display = 'block';
    });

    document.getElementById('formStep4').addEventListener('submit', function(e) {
        e.preventDefault();
        // Implement what happens after the last step is completed
        alert('Onboarding completed!');
    });
});
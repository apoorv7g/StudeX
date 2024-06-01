document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('signupForm');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');

    form.addEventListener('submit', function(event) {
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;

        if (!validatePassword(password)) {
            event.preventDefault(); // Prevent form submission
            alert('Password must be at least 8 characters long, contain a capital letter and a number.');
        } else if (password !== confirmPassword) {
            event.preventDefault(); // Prevent form submission
            alert('Passwords do not match. Please try again.');
        }
    });

    confirmPasswordInput.addEventListener('paste', function(event) {
        event.preventDefault();
        alert('Pasting is not allowed in the confirm password field.');
    });

    function validatePassword(password) {
        const minLength = 8;
        const hasUpperCase = /[A-Z]/.test(password);
        const hasNumber = /\d/.test(password);
        return password.length >= minLength && hasUpperCase && hasNumber;
    }
});

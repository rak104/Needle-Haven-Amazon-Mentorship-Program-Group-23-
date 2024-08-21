document.getElementById('changePasswordBtn').addEventListener('click', function() {
    var changePasswordSection = document.getElementById('changePasswordSection');
    if (changePasswordSection.style.display === 'none' || changePasswordSection.style.display === '') {
        changePasswordSection.style.display = 'block';
    } else {
        changePasswordSection.style.display = 'none';
    }
});

const dropdown = document.getElementById('learning_menu');
dropdown.addEventListener('change', function() {
    // Get the selected option value
    const selectedOption = dropdown.value;
    
    // Set the selected option value to the hidden input
    document.getElementById('learner').value = selectedOption;
});

function resetDropdown() {
    dropdown.selectedIndex = 0; // Set the selected index to 0 (default option)
}

// Call resetDropdown() function after the form is submitted
document.querySelector('.search-form').addEventListener('submit', function() {
    resetDropdown(); // Reset the dropdown menu
});

// videos.js

document.addEventListener('DOMContentLoaded', function() {
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

    window.openTab = function(event, tabId) {
        var i, tabcontent, tablinks;
        tabcontent = document.getElementsByClassName('tab-content');
        for (i = 0; i < tabcontent.length; i++) {
            tabcontent[i].classList.remove('active');
        }
        tablinks = document.getElementsByClassName('tab');
        for (i = 0; i < tablinks.length; i++) {
            tablinks[i].classList.remove('active');
        }
        document.getElementById(tabId).classList.add('active');
        event.currentTarget.classList.add('active');
    }

    // Open the first tab by default
    document.querySelector('.tab').click();
});

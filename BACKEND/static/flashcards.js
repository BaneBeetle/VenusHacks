// static/flashcards.js

document.addEventListener('DOMContentLoaded', function() {
    const dropdown = document.getElementById('learning_menu');
    dropdown.addEventListener('change', function() {
        // Get the selected option value
        const selectedOption = dropdown.value;
        
        // Set the selected option value to the hidden input
        document.getElementById('learner').value = selectedOption;
    });

    document.querySelectorAll('.flashcard').forEach(card => {
        card.addEventListener('click', () => {
            card.classList.toggle('is-flipped');
        });
        card.addEventListener('mouseleave', () => {
            card.classList.remove('is-flipped');
        });
    });
});

// scripts.js
document.querySelectorAll('.flashcard').forEach(card => {
    card.addEventListener('click', () => {
        card.querySelector('.flashcard-inner').classList.toggle('is-flipped');
    });
});

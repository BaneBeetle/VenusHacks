// static/scripts.js
document.querySelectorAll('.flashcard').forEach(card => {
    card.addEventListener('click', () => {
        card.classList.toggle('is-flipped');
    });
    card.addEventListener('mouseleave', () => {
        card.classList.remove('is-flipped');
    });
});

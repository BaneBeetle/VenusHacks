// document.addEventListener('DOMContentLoaded', function() {
//     const form = document.querySelector('form');
//     const playlistContainer = document.getElementById('playlist-container');
//     const messageContainer = document.getElementById('no-playlist-message');

//     form.addEventListener('submit', function(event) {
//         event.preventDefault();  // Prevent the form from submitting traditionally

//         const formData = new FormData(form);
//         fetch('/templates/music.html', {  // '/music.html' is Flask route handling the POST request
//             method: 'POST',
//             body: formData
//         })
//         .then(response => response.text())
//         .then(playlists => {
//             if (playlists.length > 0) {
//                 updatePlaylists(playlists);
//                 messageContainer.innerHTML = playlists; // Hide the "no playlists" message
//             } else {
//                 playlistContainer.innerHTML = ''; // Clear previous results
//                 messageContainer.style.display = 'block'; // Show "no playlists" message
//             }
//             localStorage.setItem('playlists', playlistContainer.innerHTML); // Save to local storage
//             console.log('local storage reached')
//         })
//         .catch(error => {
//             console.error('Error fetching playlists:', error);
//             messageContainer.textContent = 'Failed to load playlists. Please try again.';
//             messageContainer.style.display = 'block';
//         });
//     });

//     // Function to update the playlist display
//     function updatePlaylists(playlists) {
//         playlistContainer.innerHTML = playlists.map(playlist => `
//             <div>
//                 <h5>${playlist.title}</h5>
//                 <a href="${playlist.url}" target="_blank">Watch on YouTube</a>
//             </div>
//         `).join('');
//     }

//     // Load playlists from local storage on page load
//     function loadPlaylists() {
//         const savedPlaylists = localStorage.getItem('playlists');
//         if (savedPlaylists) {
//             playlistContainer.innerHTML = savedPlaylists;
//             messageContainer.style.display = 'none'; // Ensure no playlist message is hidden if playlists exist
//         }
//     }

//     loadPlaylists(); // Call loadPlaylists to display any saved playlists on page load
// });

// document.addEventListener('DOMContentLoaded', function() {
//     const form = document.getElementById('musicForm');
//     const resultsContainer = document.getElementById('results'); // Ensure you have this ID in your HTML

//     // Load playlist data from local storage if available
//         if (localStorage.getItem('playlists')) {
//             resultsContainer.innerHTML = localStorage.getItem('playlists');
//         }
//     form.addEventListener('submit', function(event) {
//         event.preventDefault(); // Prevent default form submission which causes page reload

//         const formData = new FormData(form);
//         fetch('/music.html', { // Adjust this URL to match your Flask route
//             method: 'POST',
//             body: formData
//         })
//         .then(response => response.text()) // Expecting HTML, so use `.text()` instead of `.json()`
//         .then(htmlContent => {
//             resultsContainer.innerHTML = htmlContent; // Insert the HTML into the DOM
//         })
//         .catch(error => {
//             console.error('Error fetching HTML content:', error);
//             resultsContainer.innerHTML = '<p>Error loading content.</p>'; // Display error in the DOM
//         });
//     });
// });


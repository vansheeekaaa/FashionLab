// Example JavaScript code to handle upvoting
const upvoteBtns = document.querySelectorAll('.upvote-btn');

upvoteBtns.forEach(upvoteBtn => {
    upvoteBtn.addEventListener('click', function() {
        const designId = upvoteBtn.getAttribute('data-design-id');
        fetch(`/design/${designId}/upvote/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'), // Ensure CSRF token is included
                'Content-Type': 'application/json'
            },
        })
        .then(response => response.json())
        .then(data => {
            // Update the UI to reflect the updated vote count for this specific design
            const votesElement = document.querySelector(`#votes-${designId}`);
            if (votesElement) {
                votesElement.textContent = data.votes;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


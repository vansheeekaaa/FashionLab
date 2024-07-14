const upvoteBtns = document.querySelectorAll('.upvote-btn');

upvoteBtns.forEach(upvoteBtn => {
    upvoteBtn.addEventListener('click', function() {
        const designId = upvoteBtn.getAttribute('data-design-id');
        fetch(`/design/${designId}/upvote/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'), 
                'Content-Type': 'application/json'
            },
        })
        .then(response => response.json())
        .then(data => {
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

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', () => {
    const closetButtons = document.querySelectorAll('.closet-btn');

    closetButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const messageDiv = button.nextElementSibling; 
            messageDiv.style.display = 'block'; 
            setTimeout(() => {
                messageDiv.style.display = 'none'; 
            }, 1000); 
        });
    });
});

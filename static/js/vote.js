document.addEventListener('DOMContentLoaded', function () {
    const upvoteBtns = document.querySelectorAll('.upvote-btn');
    const addToClosetBtns = document.querySelectorAll('.closet-btn');

    upvoteBtns.forEach(upvoteBtn => {
        upvoteBtn.addEventListener('click', function () {
            const designId = upvoteBtn.getAttribute('data-design-id');
            const isUpvoted = upvoteBtn.getAttribute('data-upvoted') === 'true';

            fetch(`/design/${designId}/upvote/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
            })
            .then(response => {
                if (response.status === 401) {
                    window.location.href = '/signup/';
                } else {
                    return response.json();
                }
            })
            .then(data => {
                if (data) {
                    const votesElement = document.querySelector(`#votes-${designId}`);
                    if (votesElement) {
                        votesElement.textContent = data.votes;
                    }
                    const heartIcon = upvoteBtn.querySelector('i');
                    heartIcon.classList.toggle('fa-solid', !isUpvoted);
                    heartIcon.classList.toggle('fa-regular', isUpvoted);
                    upvoteBtn.setAttribute('data-upvoted', !isUpvoted);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });

    addToClosetBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            const designId = btn.closest('.design-box').id.split('-')[1];

            fetch(`/design/${designId}/add-to-closet/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const message = btn.nextElementSibling;
                    if (message) {
                        message.style.display = 'block'; // Show "Added to Closet!" message
                        setTimeout(() => {
                            message.style.display = 'none'; // Hide after 2 seconds
                        }, 2000);
                    }
                } else {
                    alert('Failed to add design to closet.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
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

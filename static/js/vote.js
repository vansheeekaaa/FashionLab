const upvoteBtns = document.querySelectorAll('.upvote-btn');

upvoteBtns.forEach(upvoteBtn => {
    upvoteBtn.addEventListener('click', function() {
        const designId = upvoteBtn.getAttribute('data-design-id');
        const isUpvoted = upvoteBtn.getAttribute('data-upvoted') === 'true';

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
            const heartIcon = upvoteBtn.querySelector('i');
            heartIcon.classList.toggle('fa-solid', !isUpvoted);
            heartIcon.classList.toggle('fa-regular', isUpvoted);
            upvoteBtn.setAttribute('data-upvoted', !isUpvoted);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

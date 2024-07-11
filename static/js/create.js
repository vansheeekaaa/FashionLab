async function fetchAvatar() {
    const gender = document.getElementById('gender').value;
    const style = document.getElementById('style').value;
    const url = `https://api.readyplayer.me/v1/avatars?gender=${gender}&style=${style}`;

    try {
        const response = await fetch(url);
        if (response.ok) {
            const data = await response.json();
            const avatarUrl = data.avatar_url; // Adjust according to actual response structure
            document.getElementById('avatar-container').innerHTML = `<img src="${avatarUrl}" alt="Avatar">`;
        } else {
            console.error('Error fetching avatar:', response.status, response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

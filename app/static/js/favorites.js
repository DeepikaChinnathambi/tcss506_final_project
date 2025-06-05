document.querySelectorAll('.favorite-btn', '.remove-favorite').forEach(button => {
  // Attach a click listener to this specific 
  button.addEventListener('click', async (e) => {
    const btn = e.currentTarget;
    const eventId = btn.dataset.eventId;
    try {
        const response = await fetch(`/events/${eventId}/favorite`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
        if (response.ok) {
            // Toggle button appearance
            btn.classList.toggle('btn-outline-primary');
            btn.classList.toggle('btn-primary');

            const isFavorited = btn.classList.contains('btn-primary');
            btn.innerHTML = `<i class="fas fa-heart"></i> ${isFavorited ? '❤️ Favorited' : 'Favorite'}`;
        } else {
            alert(data.error);
        }
    } catch (error) {
        alert('Error updating favorites');
    }
})
});
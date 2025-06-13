document.querySelectorAll('.favorite-btn, .remove-favorite-btn').forEach(button => {
  button.addEventListener('click', async (e) => {
    const btn = e.currentTarget;
    const eventId = btn.dataset.eventId;
    const icon = btn.querySelector('i');

    try {
      const response = await fetch(`/events/${eventId}/favorite`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await response.json();

      if (response.ok) {
        const isFavorited = data.favorited;

        icon.classList.toggle('trash', !isFavorited);
        icon.classList.toggle('fas', isFavorited);
        icon.classList.toggle('far', !isFavorited);

        btn.classList.toggle('btn-primary', isFavorited);
        btn.classList.toggle('btn-outline-primary', !isFavorited);
        btn.innerHTML = `<i class="${isFavorited ? 'fas' : 'far'} fa-heart"></i> ${isFavorited ? 'Favorited' : 'Favorite'}`;

        // Optionally update the favorite heart icon
        const rsvpBtn = document.querySelector(`.rsvp-btn[data-event-id="${eventId}"]`);
        if (rsvpBtn && isFavorited) {
            rsvpBtn.classList.remove('btn-primary');
            rsvpBtn.classList.add('btn-outline-primary');
            rsvpBtn.innerHTML = '<i class="far fa-square"></i> RSVP';
        }

      } else {
        alert(data.error || 'Error toggling favorite');
      }
    } catch (err) {
      alert('Network error');
    }
  });
});
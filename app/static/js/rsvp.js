document.querySelectorAll('.rsvp-btn, .remove-rsvp').forEach(button => {
  button.addEventListener('click', async (e) => {
    const btn = e.currentTarget;
    const eventId = btn.dataset.eventId;
    const icon = btn.querySelector('i');

    try {
      const response = await fetch(`/events/${eventId}/rsvp`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });

      const data = await response.json();

      if (response.ok) {
        const isGoing = icon.classList.contains('fas'); // RSVP'd

        // Update RSVP button
        btn.classList.toggle('btn-primary', data.rsvp_status);
        btn.classList.toggle('btn-outline-primary', !data.rsvp_status);
        btn.innerHTML = `${data.rsvp_status ? '<i class="fas fa-check-square"></i> I\'m going!' : '<i class="far fa-square"></i> RSVP'}`;

        // Optionally update the favorite heart icon
        const favBtn = document.querySelector(`.favorite-btn[data-event-id="${eventId}"]`);
        if (favBtn) {
            favBtn.classList.add('btn-primary');
            favBtn.classList.remove('btn-outline-primary');
            favBtn.innerHTML = '<i class="fas fa-heart"></i> Favorited';
        }

      } else {
        alert(data.error || 'Error updating RSVP');
      }
    } catch (error) {
      alert('Error updating RSVP');
    }
  });
});

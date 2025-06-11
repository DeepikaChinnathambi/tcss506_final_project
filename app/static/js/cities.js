document.addEventListener('DOMContentLoaded', () => {
  const cityInput = document.getElementById('city');
  const stateInput = document.getElementById('state');
  const suggestions = document.createElement('div');
  suggestions.classList.add('autocomplete-suggestions');
  document.body.appendChild(suggestions);

  let cities = [];

  // Fetch city data
  fetch('/static/js/cities.json')
    .then(res => res.json())
    .then(data => {
      cities = data;
    });

  function closeSuggestions() {
    suggestions.innerHTML = '';
    suggestions.style.display = 'none';
  }

  function createSuggestion(cityData) {
    const div = document.createElement('div');
    div.classList.add('autocomplete-suggestion');
    div.textContent = `${cityData.city}, ${cityData.state_id}`;
    div.addEventListener('click', () => {
      cityInput.value = cityData.city;
      stateInput.value = cityData.state_id;
      closeSuggestions();
    });
    return div;
  }

  cityInput.addEventListener('input', () => {
    const val = cityInput.value.trim().toLowerCase();
    if (!val) {
      closeSuggestions();
      return;
    }

    const matches = cities
      .filter(c => c.city.toLowerCase().startsWith(val))
      .slice(0, 5);

    suggestions.innerHTML = '';
    if (matches.length > 0) {
      matches.forEach(match => {
        suggestions.appendChild(createSuggestion(match));
      });
      const rect = cityInput.getBoundingClientRect();
      suggestions.style.display = 'block';
      suggestions.style.position = 'absolute';
      suggestions.style.top = rect.bottom + window.scrollY + 'px';
      suggestions.style.left = rect.left + window.scrollX + 'px';
      suggestions.style.width = rect.width + 'px';
    } else {
      closeSuggestions();
    }
  });

  document.addEventListener('click', e => {
    if (!suggestions.contains(e.target) && e.target !== cityInput) {
      closeSuggestions();
    }
  });
});

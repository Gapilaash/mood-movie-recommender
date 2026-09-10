// Shared across index.html, favorites.html, watchlist.html.
// Keeps favorites/watchlist storage, theme, and toast logic in one place
// so all three pages stay in sync.

let favoritesArr = JSON.parse(localStorage.getItem('mmr_favorites') || '[]');
let watchlistArr = JSON.parse(localStorage.getItem('mmr_watchlist') || '[]');

function movieKey(m) { return `${m.title}__${m.year || ''}`; }

// ---------- Theme ----------
function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  const icon = document.getElementById('theme-icon');
  if (!icon) return;
  if (theme === 'light') {
    icon.innerHTML = '<path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/>';
  } else {
    icon.innerHTML = '<circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>';
  }
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
  const next = current === 'light' ? 'dark' : 'light';
  localStorage.setItem('mmr_theme', next);
  applyTheme(next);
}

// ---------- Toast ----------
function showToast(msg) {
  const t = document.getElementById('toast');
  if (!t) return;
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2600);
}

// ---------- Favorites ----------
function isFavorited(m) {
  return favoritesArr.some(f => movieKey(f) === movieKey(m));
}

function removeFavorite(key) {
  favoritesArr = favoritesArr.filter(f => movieKey(f) !== key);
  localStorage.setItem('mmr_favorites', JSON.stringify(favoritesArr));
  updateFavCount();
  renderFavorites();
  if (typeof currentMovies !== 'undefined' && typeof renderResults === 'function') renderResults();
}

function updateFavCount() {
  const el = document.getElementById('fav-count-label');
  if (!el) return;
  el.textContent = favoritesArr.length ? `Favorites (${favoritesArr.length})` : 'Favorites';
}

function renderFavorites() {
  const el = document.getElementById('favorites-list');
  if (!el) return;
  if (!favoritesArr.length) {
    el.innerHTML = '<div class="fav-empty">No favorites saved yet — tap the heart on any pick to save it here.</div>';
    return;
  }
  el.innerHTML = favoritesArr.map(m => `
    <div class="fav-item">
      <div class="fav-item-body">
        <div class="fav-item-title">${m.title}${m.year ? ` (${m.year})` : ''}</div>
        <div class="fav-item-meta">${m.genre || ''}${m.savedMood ? ` · saved for "${m.savedMood}"` : ''}</div>
      </div>
      <button class="icon-btn save-btn active" title="Remove from favorites" onclick="removeFavorite('${movieKey(m).replace(/'/g, "\\'")}')">
        <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24"><path d="M12 21s-6.7-4.35-9.3-8.1C.86 10.2 1.6 6.6 4.6 5.1 7 3.9 9.6 4.7 12 7.3c2.4-2.6 5-3.4 7.4-2.2 3 1.5 3.74 5.1 1.9 7.8C18.7 16.65 12 21 12 21z"/></svg>
      </button>
    </div>
  `).join('');
}

// ---------- Watchlist ----------
function isInWatchlist(m) {
  return watchlistArr.some(w => movieKey(w) === movieKey(m));
}

function removeFromWatchlist(key) {
  watchlistArr = watchlistArr.filter(w => movieKey(w) !== key);
  localStorage.setItem('mmr_watchlist', JSON.stringify(watchlistArr));
  updateWatchlistCount();
  renderWatchlist();
  if (typeof currentMovies !== 'undefined' && typeof renderResults === 'function') renderResults();
}

function updateWatchlistCount() {
  const el = document.getElementById('watchlist-count-label');
  if (!el) return;
  el.textContent = watchlistArr.length ? `Watchlist (${watchlistArr.length})` : 'Watchlist';
}

function renderWatchlist() {
  const el = document.getElementById('watchlist-list');
  if (!el) return;
  if (!watchlistArr.length) {
    el.innerHTML = '<div class="fav-empty">Nothing here yet — tap the bookmark on any pick to save it for later.</div>';
    return;
  }
  el.innerHTML = watchlistArr.map(m => `
    <div class="fav-item">
      <div class="fav-item-body">
        <div class="fav-item-title">${m.title}${m.year ? ` (${m.year})` : ''}</div>
        <div class="fav-item-meta">${m.genre || ''}${m.savedMood ? ` · saved for "${m.savedMood}"` : ''}</div>
      </div>
      <button class="icon-btn watchlist-btn active" title="Remove from watchlist" onclick="removeFromWatchlist('${movieKey(m).replace(/'/g, "\\'")}')">
        <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24"><path d="M6 2a2 2 0 00-2 2v18l8-5 8 5V4a2 2 0 00-2-2H6z"/></svg>
      </button>
    </div>
  `).join('');
}

// ---------- Init (runs on every page that loads this file) ----------
applyTheme(localStorage.getItem('mmr_theme') || 'dark');
updateFavCount();
updateWatchlistCount();
renderFavorites();
renderWatchlist();

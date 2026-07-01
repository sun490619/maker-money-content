// Init Lucide icons
document.addEventListener('DOMContentLoaded', () => {
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }

  // === Hamburger Menu ===
  const hamburgerBtn = document.getElementById('hamburger-btn');
  const menuDropdown = document.getElementById('menu-dropdown');

  if (hamburgerBtn && menuDropdown) {
    hamburgerBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = menuDropdown.classList.contains('open');
      if (isOpen) {
        menuDropdown.classList.remove('open');
        menuDropdown.hidden = true;
      } else {
        menuDropdown.classList.add('open');
        menuDropdown.hidden = false;
        // Re-render icons inside dropdown
        if (typeof lucide !== 'undefined') lucide.createIcons();
      }
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
      if (!menuDropdown.contains(e.target) && !hamburgerBtn.contains(e.target)) {
        menuDropdown.classList.remove('open');
        menuDropdown.hidden = true;
      }
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && menuDropdown.classList.contains('open')) {
        menuDropdown.classList.remove('open');
        menuDropdown.hidden = true;
        hamburgerBtn.focus();
      }
    });
  }
});

// Theme toggle
(function(){
  const saved = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', saved);

  document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('theme-toggle');
    if (!btn) return;
    updateThemeLabel(saved);
    btn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
      updateThemeLabel(next);
      // Re-render icons after theme change
      if (typeof lucide !== 'undefined') {
        setTimeout(() => lucide.createIcons(), 50);
      }
    });
  });

  function updateThemeLabel(theme) {
    const btn = document.getElementById('theme-toggle');
    if (!btn) return;
    const icon = btn.querySelector('svg');
    const label = btn.querySelector('span');
    // Replace the SVG icon
    if (icon) {
      const newIcon = document.createElement('i');
      newIcon.setAttribute('data-lucide', theme === 'dark' ? 'sun' : 'moon');
      icon.replaceWith(newIcon);
    }
    if (label) {
      label.textContent = theme === 'dark' ? 'Light' : 'Dark';
    }
    if (typeof lucide !== 'undefined') {
      lucide.createIcons();
    }
  }
})();

// Category filter
function filterCat(cat, el) {
  document.querySelectorAll('.cat-tab').forEach(t => t.classList.remove('active'));
  if (el) el.classList.add('active');
  const cards = document.querySelectorAll('.article-card[data-cat]');
  cards.forEach(c => {
    c.style.display = (cat === 'all' || c.dataset.cat === cat) ? '' : 'none';
  });
}

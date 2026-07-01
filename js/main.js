// 主题切换
(function(){
  const saved = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', saved);
  
  document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('theme-toggle');
    if (!btn) return;
    updateIcon(saved);
    btn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
      updateIcon(next);
    });
  });

  function updateIcon(theme) {
    const btn = document.getElementById('theme-toggle');
    if (!btn) return;
    btn.textContent = theme === 'dark' ? '☀️' : '🌙';
  }
})();

// 分类筛选（首页）
function filterCat(cat, el) {
  document.querySelectorAll('.cat-tab').forEach(t => t.classList.remove('active'));
  if (el) el.classList.add('active');
  const cards = document.querySelectorAll('.article-card[data-cat]');
  cards.forEach(c => {
    c.style.display = (cat === 'all' || c.dataset.cat === cat) ? '' : 'none';
  });
}

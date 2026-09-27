/* Terminal activity reflects the actual browser session. Hover is context only;
   backend API requests are logged independently after they complete. */
(() => {
  const areas = new Set(['home','upload','dashboard','scada','integrity','safeguards','ai','devsecops','compliance','reports','monitoring','audit','evidence','detections']);
  const area = () => {
    const name = location.hash.replace(/^#\//, '').split('?')[0] || 'home';
    return areas.has(name) ? name : 'home';
  };
  const hovered = new Set();
  function report(action, name) {
    if (!areas.has(name)) return;
    if (action === 'hover' && hovered.has(name)) return;
    if (action === 'hover') hovered.add(name);
    fetch('/api/console-interaction', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({action, area: name}), keepalive: true
    }).catch(() => {});
  }
  window.addEventListener('hashchange', () => { hovered.clear(); report('view', area()); });
  document.addEventListener('pointerover', event => {
    const target = event.target.closest('#topnav a, .hero-actions a, .observability-launch a');
    if (!target || target.contains(event.relatedTarget)) return;
    report('hover', target.dataset.route || area());
  }, {passive: true});
  report('view', area());
})();

(function () {
  if (window.__ipblGlobalTooltipV2) return;
  window.__ipblGlobalTooltipV2 = true;

  var tip = document.createElement('div');
  tip.id = 'ipbl-global-tooltip';
  tip.setAttribute('role', 'tooltip');
  document.body.appendChild(tip);

  var active = null;

  function textFor(el) {
    return (el.getAttribute('data-tip') || el.getAttribute('aria-label') || el.getAttribute('title') || '').trim();
  }

  function removeNativeTitle(el) {
    if (el && el.hasAttribute('title')) {
      if (!el.hasAttribute('data-tip') && !el.hasAttribute('aria-label')) {
        el.setAttribute('data-ipbl-tooltip-text', el.getAttribute('title') || '');
      }
      el.removeAttribute('title');
    }
  }

  function getText(el) {
    return textFor(el) || (el.getAttribute('data-ipbl-tooltip-text') || '').trim();
  }

  function place(el) {
    if (!el || tip.style.display === 'none') return;
    var r = el.getBoundingClientRect();
    var gap = 9;
    var pad = 12;
    var w = tip.offsetWidth;
    var h = tip.offsetHeight;
    var x = r.left + r.width / 2 - w / 2;
    x = Math.max(pad, Math.min(x, window.innerWidth - w - pad));
    var y = r.top - h - gap;
    if (y < pad) y = r.bottom + gap;
    if (y + h > window.innerHeight - pad) y = Math.max(pad, window.innerHeight - h - pad);
    tip.style.left = Math.round(x) + 'px';
    tip.style.top = Math.round(y) + 'px';
  }

  function show(el) {
    if (!el) return;
    removeNativeTitle(el);
    var txt = getText(el);
    if (!txt) return;
    active = el;
    tip.textContent = txt;
    tip.style.display = 'block';
    place(el);
  }

  function hide(el) {
    if (el && active && el !== active) return;
    active = null;
    tip.style.display = 'none';
  }

  document.addEventListener('mouseover', function (ev) {
    var el = ev.target && ev.target.closest ? ev.target.closest('.info-tip') : null;
    if (el && el !== active) show(el);
  }, true);

  document.addEventListener('mouseout', function (ev) {
    var el = ev.target && ev.target.closest ? ev.target.closest('.info-tip') : null;
    if (!el) return;
    var related = ev.relatedTarget;
    if (!related || !el.contains(related)) hide(el);
  }, true);

  document.addEventListener('focusin', function (ev) {
    var el = ev.target && ev.target.closest ? ev.target.closest('.info-tip') : null;
    if (el) show(el);
  }, true);

  document.addEventListener('focusout', function (ev) {
    var el = ev.target && ev.target.closest ? ev.target.closest('.info-tip') : null;
    if (el) hide(el);
  }, true);

  window.addEventListener('scroll', function () { if (active) place(active); }, true);
  window.addEventListener('resize', function () { if (active) place(active); });
})();

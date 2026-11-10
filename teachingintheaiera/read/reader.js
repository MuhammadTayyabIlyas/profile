/* Reader for Teaching in the AI Era.
   EPUB: epub.js over the unpacked book in ./book/ (chapters load one at a time).
   Online reading only: the book is sold, so there is no PDF tab and no download button.
   Everything the reader remembers lives in localStorage on this device only. */
(function () {
  'use strict';
  var BASE = '/teachingintheaiera/';
  // edition stamp: change it whenever the EPUB is replaced, so no browser reuses a cached copy
  var ED = '?v=20261110';
  var KEY = 'tiae-reader-v1';
  var FIRST = 'text/title_page.xhtml';
  var $ = function (id) { return document.getElementById(id); };

  var state = load();
  function load() {
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; }
  }
  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* private mode: reading still works */ }
  }

  /* ---------- theme and text size ---------- */
  var mq = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  function theme() { return state.theme || (mq && mq.matches ? 'dark' : 'light'); }
  function applyTheme() {
    var t = theme();
    document.documentElement.setAttribute('data-theme', t);
    $('btn-theme').setAttribute('aria-pressed', String(t === 'dark'));
    $('btn-theme').lastChild.textContent = ' Dark';
    if (rendition) rendition.themes.select(t);
  }
  $('btn-theme').addEventListener('click', function () {
    state.theme = theme() === 'dark' ? 'light' : 'dark';
    save(); applyTheme();
  });
  if (mq && mq.addEventListener) mq.addEventListener('change', function () { if (!state.theme) applyTheme(); });

  var SIZES = [85, 100, 115, 130, 150, 175];
  if (SIZES.indexOf(state.size) === -1) state.size = 100;
  function step(dir) {
    var i = Math.max(0, Math.min(SIZES.length - 1, SIZES.indexOf(state.size) + dir));
    state.size = SIZES[i]; save();
    if (rendition) rendition.themes.fontSize(state.size + '%');
  }
  function closeSettings() {
    if ($('settings').hidden) return;
    $('settings').hidden = true;
    $('btn-settings').setAttribute('aria-expanded', 'false');
  }
  $('btn-settings').addEventListener('click', function (e) {
    e.stopPropagation();
    var open = $('settings').hidden;
    $('settings').hidden = !open;
    $('btn-settings').setAttribute('aria-expanded', String(open));
    if (open) $('btn-smaller').focus();
  });
  $('settings').addEventListener('click', function (e) { e.stopPropagation(); });
  document.addEventListener('click', closeSettings);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeSettings(); });
  $('btn-smaller').addEventListener('click', function () { step(-1); });
  $('btn-larger').addEventListener('click', function () { step(1); });

  /* ---------- EPUB ---------- */
  var book, rendition, toc = [];
  function epubStatus(msg, pct, done) {
    $('epub-msg').textContent = msg;
    if (pct != null) document.querySelector('#epub-status .bar i').style.width = pct + '%';
    $('epub-status').hidden = !!done;
  }

  function openEpub() {
    if (book) return;
    if (!window.ePub) { epubStatus('The reader could not load. Please reload the page.', 0); return; }
    epubStatus('Opening the book…', 20);
    // open the package file directly: one round trip fewer than META-INF/container.xml
    book = window.ePub(BASE + 'read/book/EPUB/content.opf' + ED, { openAs: 'opf' });
    rendition = book.renderTo('viewer', {
      width: '100%', height: '100%', flow: 'scrolled-doc', spread: 'none', allowScriptedContent: false
    });
    rendition.themes.register('light', {
      'html, body': { 'background': '#FBFAF6 !important', 'color': '#1B2233 !important' },
      'body': { 'padding': '0 1rem 2rem !important', 'max-width': '40em', 'margin': '0 auto !important', 'line-height': '1.6 !important', 'font-family': 'Charter, "Iowan Old Style", Georgia, serif !important' },
      'a': { 'color': '#1D4ED8 !important' },
      'img': { 'max-width': '100% !important', 'height': 'auto !important' }
    });
    rendition.themes.register('dark', {
      'html, body': { 'background': '#10151F !important', 'color': '#E6E8EE !important' },
      'body': { 'padding': '0 1rem 2rem !important', 'max-width': '40em', 'margin': '0 auto !important', 'line-height': '1.6 !important', 'font-family': 'Charter, "Iowan Old Style", Georgia, serif !important' },
      'a': { 'color': '#F5B841 !important' },
      'img': { 'max-width': '100% !important', 'height': 'auto !important', 'background': '#fff' },
      'table, th, td': { 'border-color': '#3A4560 !important' }
    });
    rendition.themes.fontSize(state.size + '%');
    applyTheme();

    book.loaded.navigation.then(function (nav) { toc = nav.toc; buildToc(); }).catch(function () {});
    book.ready.then(function () {
      epubStatus('Opening the book…', 60);
      return rendition.display(startTarget());
    }).then(function () {
      epubStatus('', 100, true);
    }).catch(function (err) {
      console.error(err);
      state.cfi = null; save();
      epubStatus('The book could not open here. Please reload the page.', 0);
    });

    var t;
    rendition.on('relocated', function (loc) {
      updateWhere(loc);
      clearTimeout(t);
      t = setTimeout(function () {
        // show the chapter in the address bar, so a copied link opens the same chapter
        var m = /(ch\d{3})\.xhtml/.exec(loc.start.href || '');
        state.cfi = loc.start.cfi; state.ch = m ? m[1] : null; save();
        if (m && location.hash !== '#' + m[1]) history.replaceState(null, '', '#' + m[1]);
      }, 400);
    });
    rendition.on('keyup', keys);

    // scrolled-doc mode does not report scrolling, so save the exact place ourselves
    var st2;
    function onScroll() {
      clearTimeout(st2);
      st2 = setTimeout(function () {
        var loc = rendition.currentLocation();
        if (loc && loc.start && loc.start.cfi) { state.cfi = loc.start.cfi; save(); }
      }, 500);
    }
    rendition.on('rendered', function () {
      var c = document.querySelector('#viewer .epub-container');
      if (c && !c._tiae) { c._tiae = true; c.addEventListener('scroll', onScroll, { passive: true }); }
    });
  }

  function hashChapter() {
    var m = /^#(ch\d{3})$/.exec(location.hash);
    return m ? 'text/' + m[1] + '.xhtml' : null;
  }
  function startTarget() {
    var h = hashChapter();
    // a reload of the reader's own chapter link resumes at the saved place, not the chapter start
    if (h && state.cfi && state.ch && h === 'text/' + state.ch + '.xhtml') return state.cfi;
    return h || state.cfi || FIRST;
  }

  function label(href) {
    var file = href.split('#')[0];
    for (var i = 0; i < toc.length; i++) if (toc[i].href.split('#')[0] === file) return toc[i].label.trim();
    if (/title_page/.test(file)) return 'Title page';
    if (/nav\.xhtml/.test(file)) return 'Contents';
    return '';
  }
  function updateWhere(loc) {
    var href = loc.start.href;
    $('where').textContent = label(href);
    $('prev').disabled = !!loc.atStart;
    $('next').disabled = !!loc.atEnd;
    var links = document.querySelectorAll('#toc-list > li > a');
    for (var i = 0; i < links.length; i++) {
      links[i].setAttribute('aria-current', String(links[i].getAttribute('data-href').split('#')[0] === href));
    }
  }
  function go(dir) {
    if (!rendition) return;
    (dir > 0 ? rendition.next() : rendition.prev()).then(function () {
      var v = document.querySelector('#viewer .epub-container');
      if (v) v.scrollTop = 0;
    });
  }
  $('prev').addEventListener('click', function () { go(-1); });
  $('next').addEventListener('click', function () { go(1); });

  function keys(e) {
    if (e.target && /INPUT|TEXTAREA/.test(e.target.tagName)) return;
    if (tab !== 'epub') return;
    if (e.key === 'ArrowRight') go(1);
    if (e.key === 'ArrowLeft') go(-1);
  }
  document.addEventListener('keyup', keys);

  function link(item) {
    var a = document.createElement('a');
    a.href = '#';
    a.textContent = item.label.trim();
    a.setAttribute('data-href', item.href);
    a.addEventListener('click', function (e) {
      e.preventDefault();
      closeToc();
      rendition.display(item.href);
    });
    return a;
  }
  function buildToc() {
    var list = $('toc-list');
    list.textContent = '';
    toc.forEach(function (item) {
      if (/title_page|cover|#toc$/.test(item.href)) return;
      var li = document.createElement('li');
      li.appendChild(link(item));
      if (item.subitems && item.subitems.length) {
        var d = document.createElement('details');
        var s = document.createElement('summary');
        s.textContent = 'Sections';
        d.appendChild(s);
        var ol = document.createElement('ol');
        item.subitems.forEach(function (sub) {
          var sli = document.createElement('li');
          sli.appendChild(link(sub));
          ol.appendChild(sli);
        });
        d.appendChild(ol);
        li.appendChild(d);
      }
      list.appendChild(li);
    });
  }
  function openToc() {
    $('toc').hidden = false; $('scrim').hidden = false;
    $('btn-toc').setAttribute('aria-expanded', 'true');
    var cur = document.querySelector('#toc-list a[aria-current="true"]') || document.querySelector('#toc-list a');
    if (cur) cur.focus();
  }
  function closeToc() {
    if ($('toc').hidden) return;
    $('toc').hidden = true; $('scrim').hidden = true;
    $('btn-toc').setAttribute('aria-expanded', 'false');
    $('btn-toc').focus();
  }
  $('btn-toc').addEventListener('click', function () { $('toc').hidden ? openToc() : closeToc(); });
  $('toc-close').addEventListener('click', closeToc);
  $('scrim').addEventListener('click', closeToc);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeToc(); });

  /* ---------- deep links: #ch003 opens a chapter ---------- */
  window.addEventListener('hashchange', function () {
    var ch = hashChapter();
    if (ch && rendition) rendition.display(ch);
  });

  applyTheme();
  openEpub();
})();

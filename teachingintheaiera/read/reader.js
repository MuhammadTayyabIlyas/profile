/* Reader for Teaching in the AI Era.
   EPUB: epub.js over the unpacked book in ./book/ (chapters load one at a time).
   PDF:  PDF.js, loaded only when the PDF tab is opened; pages render as they scroll into view.
   Everything the reader remembers lives in localStorage on this device only. */
(function () {
  'use strict';
  var BASE = '/teachingintheaiera/';
  var FILES = { epub: BASE + 'files/teaching-in-the-ai-era.epub', pdf: BASE + 'files/teaching-in-the-ai-era.pdf' };
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
    if (tab === 'pdf') return zoom(dir);
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

  /* ---------- tabs ---------- */
  var tab = 'epub';
  function showTab(name, focus) {
    tab = name;
    ['epub', 'pdf'].forEach(function (n) {
      var on = n === name;
      $('tab-' + n).setAttribute('aria-selected', String(on));
      $('tab-' + n).tabIndex = on ? 0 : -1;
      $('pane-' + n).hidden = !on;
    });
    $('btn-toc').hidden = name !== 'epub';
    $('btn-dl').href = FILES[name];
    $('btn-smaller').querySelector('.sr').textContent = name === 'pdf' ? 'Zoom out' : 'Smaller text';
    $('btn-larger').querySelector('.sr').textContent = name === 'pdf' ? 'Zoom in' : 'Larger text';
    state.tab = name; save();
    if (name === 'pdf') openPdf(); else openEpub();
    if (focus) $('tab-' + name).focus();
  }
  $('tab-epub').addEventListener('click', function () { showTab('epub'); history.replaceState(null, '', location.pathname); });
  $('tab-pdf').addEventListener('click', function () { showTab('pdf'); });
  document.querySelector('.tabs').addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') showTab(tab === 'epub' ? 'pdf' : 'epub', true);
  });

  /* ---------- EPUB ---------- */
  var book, rendition, toc = [];
  function epubStatus(msg, pct, done) {
    $('epub-msg').textContent = msg;
    if (pct != null) document.querySelector('#epub-status .bar i').style.width = pct + '%';
    $('epub-status').hidden = !!done;
  }

  function openEpub() {
    if (book) return;
    if (!window.ePub) { epubStatus('The reader could not load. Please use the Download button above.', 0); return; }
    epubStatus('Opening the book…', 20);
    // open the package file directly: one round trip fewer than META-INF/container.xml
    book = window.ePub(BASE + 'read/book/EPUB/content.opf', { openAs: 'opf' });
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
      epubStatus('The book could not open here. Please use the Download button above, or try the PDF tab.', 0);
    });

    var t;
    rendition.on('relocated', function (loc) {
      updateWhere(loc);
      clearTimeout(t);
      t = setTimeout(function () { state.cfi = loc.start.cfi; save(); }, 400);
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
  function startTarget() { return hashChapter() || state.cfi || FIRST; }

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

  /* ---------- PDF ---------- */
  var pdf, pages = [], scale = state.zoom || 1, io, rendering = {};
  function pdfStatus(msg, pct, done) {
    $('pdf-msg').textContent = msg;
    if (pct != null) document.querySelector('#pdf-status .bar i').style.width = pct + '%';
    $('pdf-status').hidden = !!done;
  }
  function loadScript(src) {
    return new Promise(function (ok, fail) {
      var s = document.createElement('script');
      s.src = src; s.onload = ok; s.onerror = fail;
      document.head.appendChild(s);
    });
  }
  function hashPage() {
    var m = /^#pdf(?:-(\d+))?$/.exec(location.hash);
    return m ? (parseInt(m[1], 10) || 1) : null;
  }

  function openPdf() {
    if (pdf) return;
    pdfStatus('Opening the PDF…', 10);
    loadScript(BASE + 'read/lib/pdf.min.js').then(function () {
      var lib = window.pdfjsLib;
      lib.GlobalWorkerOptions.workerSrc = BASE + 'read/lib/pdf.worker.min.js';
      var task = lib.getDocument({ url: FILES.pdf, rangeChunkSize: 131072, disableAutoFetch: true, disableStream: true });
      // range requests keep reporting progress after the first pages show; ignore those
      task.onProgress = function (p) { if (p.total && !pdf) pdfStatus('Opening the PDF…', 10 + Math.round(80 * p.loaded / p.total)); };
      return task.promise;
    }).then(function (doc) {
      pdf = doc;
      $('page-count').textContent = doc.numPages;
      $('page-input').max = doc.numPages;
      layoutPages();
      pdfStatus('', 100, true);
      jump(hashPage() || state.page || 1);
    }).catch(function (err) {
      console.error(err);
      pdfStatus('The PDF viewer could not load here. You can open the PDF directly instead.', 0);
      var p = $('pdf-msg');
      var a = document.createElement('a');
      a.href = FILES.pdf; a.textContent = ' Open the PDF';
      p.appendChild(a);
    });
  }

  function width() { return Math.min($('pdf-pages').clientWidth - 16, 820) * scale; }
  function layoutPages() {
    var box = $('pdf-pages');
    box.textContent = '';
    pages = [];
    if (io) io.disconnect();
    io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var n = +en.target.getAttribute('data-n');
        if (en.isIntersecting) draw(n); else clear(n);
      });
    }, { root: box, rootMargin: '120% 0px' });
    for (var n = 1; n <= pdf.numPages; n++) {
      var d = document.createElement('div');
      d.className = 'pdf-page';
      d.style.width = width() + 'px';
      d.setAttribute('data-n', n);
      d.setAttribute('role', 'img');
      d.setAttribute('aria-label', 'PDF page ' + n);
      var s = document.createElement('span');
      s.textContent = n;
      d.appendChild(s);
      box.appendChild(d);
      pages.push(d);
      io.observe(d);
    }
  }
  function draw(n) {
    var el = pages[n - 1];
    if (!el || el.querySelector('canvas') || rendering[n]) return;
    rendering[n] = true;
    pdf.getPage(n).then(function (page) {
      var cssW = el.clientWidth;
      var ratio = Math.min(window.devicePixelRatio || 1, 2);
      var vp = page.getViewport({ scale: cssW / page.getViewport({ scale: 1 }).width * ratio });
      var c = document.createElement('canvas');
      c.width = Math.floor(vp.width); c.height = Math.floor(vp.height);
      el.insertBefore(c, el.firstChild);
      return page.render({ canvasContext: c.getContext('2d'), viewport: vp }).promise;
    }).catch(function () {}).then(function () { rendering[n] = false; });
  }
  function clear(n) {
    var c = pages[n - 1] && pages[n - 1].querySelector('canvas');
    if (c && !rendering[n]) { c.width = 0; c.height = 0; c.remove(); }
  }
  function current() {
    var box = $('pdf-pages'), mid = box.scrollTop + box.clientHeight / 3;
    var h = pages.length ? pages[0].offsetHeight + 12 : 1;
    return Math.max(1, Math.min(pages.length, Math.floor(mid / h) + 1));
  }
  function jump(n) {
    n = Math.max(1, Math.min(pdf.numPages, n | 0));
    // scroll only the PDF column; scrollIntoView would also move the page frame on phones
    $('pdf-pages').scrollTop = pages[n - 1].offsetTop - $('pdf-pages').offsetTop - 12;
    $('page-input').value = n;
  }
  var st;
  $('pdf-pages').addEventListener('scroll', function () {
    clearTimeout(st);
    st = setTimeout(function () {
      if (!pages.length) return;
      var n = current();
      if (document.activeElement !== $('page-input')) $('page-input').value = n;
      state.page = n; save();
      history.replaceState(null, '', '#pdf-' + n);
    }, 150);
  });
  $('jump').addEventListener('submit', function (e) { e.preventDefault(); if (pdf) jump(+$('page-input').value); });
  function zoom(dir) {
    if (!pdf) return;
    var n = current();
    scale = Math.max(0.6, Math.min(2.5, Math.round((scale + dir * 0.2) * 10) / 10));
    state.zoom = scale; save();
    pages.forEach(function (p, i) { clear(i + 1); p.style.width = width() + 'px'; });
    jump(n);
  }
  $('zoom-in').addEventListener('click', function () { zoom(1); });
  $('zoom-out').addEventListener('click', function () { zoom(-1); });
  var rt;
  window.addEventListener('resize', function () {
    if (!pdf || tab !== 'pdf') return;
    clearTimeout(rt);
    rt = setTimeout(function () { var n = current(); pages.forEach(function (p, i) { clear(i + 1); p.style.width = width() + 'px'; }); jump(n); }, 200);
  });

  /* ---------- deep links: #ch003 opens a chapter, #pdf-112 opens a PDF page ---------- */
  window.addEventListener('hashchange', function () {
    var ch = hashChapter(), pg = hashPage();
    if (ch) { showTab('epub'); if (rendition) rendition.display(ch); }
    else if (pg) { showTab('pdf'); if (pdf) jump(pg); }
  });

  applyTheme();
  showTab(hashPage() ? 'pdf' : hashChapter() ? 'epub' : (state.tab || 'epub'));
})();

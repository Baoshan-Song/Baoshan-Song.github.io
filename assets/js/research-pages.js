(function () {
  'use strict';
  var nav = document.querySelector('[data-video-nav]');
  var sections = Array.from(document.querySelectorAll('[data-video-section]'));
  if (nav && sections.length) {
    function selectCategory() {
      var target = document.getElementById(window.location.hash.slice(1));
      var selected = target && target.closest('[data-video-section]');
      selected = selected || sections[0];
      sections.forEach(function (section) {
        section.hidden = section !== selected;
        if (section.hidden) section.querySelectorAll('.video-player').forEach(function (player) {
          player.replaceWith(player.originalPreview);
        });
      });
      nav.querySelectorAll('a').forEach(function (link) {
        if (link.hash === '#' + selected.id) link.setAttribute('aria-current', 'true');
        else link.removeAttribute('aria-current');
      });
      if (target && target.classList.contains('video-card')) target.scrollIntoView({block: 'start'});
    }
    nav.addEventListener('click', function (event) {
      var link = event.target.closest('a');
      if (!link || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      history.pushState(null, '', link.hash);
      selectCategory();
    });
    window.addEventListener('hashchange', selectCategory);
    selectCategory();
  }
  document.addEventListener('click', function (event) {
    var preview = event.target.closest('[data-video-id]');
    if (!preview || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    var frame = document.createElement('iframe');
    frame.className = 'video-player';
    frame.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(preview.dataset.videoId) + '?autoplay=1';
    frame.title = preview.dataset.videoTitle;
    frame.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    frame.allowFullscreen = true;
    frame.referrerPolicy = 'strict-origin-when-cross-origin';
    frame.originalPreview = preview;
    preview.replaceWith(frame);
    frame.focus();
  });
}());

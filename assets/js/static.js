/* Standalone enhancements. No WordPress server or build step is required. */
(() => {
  'use strict';
  const base = new URL('../../', document.currentScript.src);
  const SITE_NAME = 'Forsk Technologies';
  const REQUEST_FILENAME = 'forsk-technologies-request.txt';
  const getSearchIndex = () => window.TECHCO_SEARCH || [];

  const ready = () => {
    document.querySelectorAll('.elementor-invisible').forEach(e => e.classList.remove('elementor-invisible'));
    document.querySelectorAll('.e-con.e-parent').forEach(e => e.classList.add('e-lazyloaded'));
    document.querySelectorAll('.odometer[data-count]').forEach(e => { e.textContent = e.dataset.count; });
    document.querySelectorAll('.xb-nav-mobile').forEach(e => {
      e.setAttribute('aria-label', 'Open navigation');
      e.setAttribute('aria-expanded', 'false');
      e.addEventListener('click', () => e.setAttribute('aria-expanded', String(document.querySelector('.xb-header-menu')?.classList.contains('active'))));
    });
    document.querySelectorAll('.xb-menu-close,.xb-menu-toggle').forEach(e => {
      e.setAttribute('role', 'button'); e.tabIndex = 0;
      e.setAttribute('aria-label', e.classList.contains('xb-menu-close') ? 'Close navigation' : 'Toggle submenu');
      e.addEventListener('keydown', event => { if (['Enter',' '].includes(event.key)) { event.preventDefault(); e.click(); } });
    });
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') {
        document.querySelectorAll('.xb-header-menu,.xb-nav-mobile').forEach(n => n.classList.remove('active'));
        document.querySelectorAll('.xb-nav-mobile').forEach(n => n.setAttribute('aria-expanded','false'));
      }
    });
    document.querySelectorAll('form[data-static-form]').forEach(form => {
      form.addEventListener('submit', event => {
        event.preventDefault();
        if (!form.reportValidity()) return;
        if (form.dataset.staticForm === 'search') {
          const query = String(new FormData(form).get('s') || '').trim();
          const dialog = document.createElement('dialog'); dialog.className = 'static-search';
          const heading = document.createElement('h2'); heading.textContent = query ? `Search: ${query}` : 'Search pages';
          const close = document.createElement('button'); close.textContent = 'Close'; close.className='static-button'; close.addEventListener('click',()=>dialog.close());
          const list = document.createElement('ul');
          const words = query.toLowerCase().split(/\s+/).filter(Boolean);
          const results = words.length ? getSearchIndex().filter(p => words.every(w => (p.title+' '+p.text).toLowerCase().includes(w))).slice(0,30) : [];
          results.forEach(p => {const li=document.createElement('li'),a=document.createElement('a');a.href=new URL(p.url,base);a.textContent=p.title;li.append(a);list.append(li);});
          if (!results.length) {const li=document.createElement('li');li.textContent=query?'No matching pages found. Try another keyword.':'Enter a keyword to search.';list.append(li);}
          dialog.append(heading,list,close);document.body.append(dialog);dialog.addEventListener('close',()=>dialog.remove());dialog.showModal();
        } else {
          const fields=[...new FormData(form)].filter(([key])=>!key.startsWith('_'));
          const content=`${SITE_NAME} website request\n\n`+fields.map(([key,value])=>`${key}: ${value}`).join('\n')+'\n\nThis file is a local copy. It has not been sent or subscribed.';
          const url=URL.createObjectURL(new Blob([content],{type:'text/plain;charset=utf-8'}));
          const a=document.createElement('a');a.href=url;a.download=REQUEST_FILENAME;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
          const note = form.querySelector('.static-form-note');
          if (note) note.textContent='Your request was downloaded to your device. Nothing has been sent. Contact the business directly to submit it.';
        }
      });
      if (form.dataset.staticForm === 'contact') form.querySelectorAll('[type="submit"]').forEach(e=>{
        if(e.tagName==='INPUT')e.value='Download request';else if(e.textContent.trim())e.textContent='Download request';
        e.setAttribute('aria-label','Download request');
      });
    });
  };
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',ready);else ready();
})();

/* Standalone enhancements. No WordPress server or build step is required. */
(() => {
  'use strict';
  const base = new URL('../../', document.currentScript.src);
  const ready = () => {
    document.querySelectorAll('.elementor-invisible').forEach(e => e.classList.remove('elementor-invisible'));
    document.querySelectorAll('.e-con.e-parent').forEach(e => e.classList.add('e-lazyloaded'));
    document.querySelectorAll('.odometer[data-count]').forEach(e => { e.textContent = e.dataset.count; });

    /* Shared accessibility hardening without changing the visual layout. */
    if (!document.getElementById('static-a11y-style')) {
      const style = document.createElement('style');
      style.id = 'static-a11y-style';
      style.textContent = `
        :focus-visible{outline:3px solid #fff!important;outline-offset:3px!important;box-shadow:0 0 0 6px #0044eb!important}
        .skip-link{position:fixed;top:8px;left:8px;z-index:100000;padding:10px 14px;border-radius:8px;background:#fff;color:#020842;font-weight:700;transform:translateY(-160%);transition:transform .15s ease}
        .skip-link:focus{transform:translateY(0)}
        .review_bg_box.bg-success .text-white,.badge.bg-secondary{color:#020842!important}
        @media(min-width:992px){.dropdown:focus-within>.dropdown-menu{display:block;transform:translateY(0);z-index:1000}}
        @media(max-width:991px){.xb-menu-toggle,.xb-menu-close,.mobile_menu_btn,.xb-nav-mobile{min-width:44px!important;min-height:44px!important}.xb-menu-toggle{top:2px!important;width:44px!important;height:44px!important;line-height:44px!important}}
        @media(prefers-reduced-motion:reduce){.skip-link{transition:none}}
      `;
      document.head.append(style);
    }

    const main = document.querySelector('#elementor_page_builder');
    if (main) {
      main.setAttribute('role', 'main');
      if (!document.querySelector('.skip-link')) {
        const skip = document.createElement('a');
        skip.className = 'skip-link';
        skip.href = '#elementor_page_builder';
        skip.textContent = 'Skip to main content';
        document.body.prepend(skip);
      }
    }

    document.querySelectorAll('.header-logo a img,.xb-logo-mobile a img').forEach(img => {
      if (!img.getAttribute('alt')?.trim()) img.alt = 'Forsk Technologies';
    });
    document.querySelectorAll('.xb-backtotop a').forEach(link => {
      if (!link.textContent.trim() && !link.hasAttribute('aria-label')) link.setAttribute('aria-label', 'Back to top');
    });

    let lastMenuOpener = null;
    const mobileMenu = document.querySelector('.xb-header-menu');
    if (mobileMenu && !mobileMenu.id) mobileMenu.id = 'site-mobile-navigation';
    document.querySelectorAll('.xb-nav-mobile').forEach(e => {
      e.setAttribute('aria-label', 'Open navigation');
      e.setAttribute('aria-expanded', 'false');
      if (mobileMenu?.id) e.setAttribute('aria-controls', mobileMenu.id);
      e.addEventListener('click', () => {
        lastMenuOpener = e;
        const expanded = Boolean(document.querySelector('.xb-header-menu')?.classList.contains('active'));
        e.setAttribute('aria-expanded', String(expanded));
        e.setAttribute('aria-label', expanded ? 'Close navigation' : 'Open navigation');
        if (expanded) setTimeout(() => document.querySelector('.xb-header-menu.active .xb-menu-close')?.focus(), 0);
      });
    });

    let submenuIndex = 0;
    document.querySelectorAll('.xb-menu-close,.xb-menu-toggle').forEach(e => {
      e.setAttribute('role', 'button');
      e.tabIndex = 0;
      const isClose = e.classList.contains('xb-menu-close');
      e.setAttribute('aria-label', isClose ? 'Close navigation' : 'Toggle submenu');
      if (!isClose) {
        const submenu = e.closest('.menu-item')?.querySelector(':scope > .sub-menu');
        if (submenu) {
          if (!submenu.id) submenu.id = `submenu-${++submenuIndex}`;
          e.setAttribute('aria-controls', submenu.id);
          e.setAttribute('aria-expanded', String(e.classList.contains('active')));
          e.addEventListener('click', () => setTimeout(() => e.setAttribute('aria-expanded', String(e.classList.contains('active'))), 0));
        }
      } else {
        e.addEventListener('click', () => setTimeout(() => {
          document.querySelectorAll('.xb-nav-mobile').forEach(n => {
            n.setAttribute('aria-expanded','false');
            n.setAttribute('aria-label','Open navigation');
          });
          if (lastMenuOpener) lastMenuOpener.focus();
        }, 0));
      }
      e.addEventListener('keydown', event => {
        if (['Enter',' '].includes(event.key)) {
          event.preventDefault();
          e.click();
        }
      });
    });

    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') {
        document.querySelectorAll('.xb-header-menu,.xb-nav-mobile').forEach(n => n.classList.remove('active'));
        document.querySelectorAll('.xb-nav-mobile').forEach(n => {
          n.setAttribute('aria-expanded','false');
          n.setAttribute('aria-label','Open navigation');
        });
        if (lastMenuOpener) lastMenuOpener.focus();
      }
    });

    document.querySelectorAll('label[for]').forEach(label => {
      const control = document.getElementById(label.htmlFor);
      if (!control) return;
      if (!label.textContent.trim()) {
        label.textContent = control.getAttribute('placeholder') || 'Email address';
        label.classList.add('visually-hidden');
      }
      if (label.textContent.trim()) {
        control.removeAttribute('aria-label');
        control.removeAttribute('aria-required');
        if (control.getAttribute('aria-invalid') === 'false') control.removeAttribute('aria-invalid');
      }
      control.addEventListener('invalid', () => control.setAttribute('aria-invalid', 'true'));
      const clearInvalid = () => { if (control.checkValidity()) control.removeAttribute('aria-invalid'); };
      control.addEventListener('input', clearInvalid);
      control.addEventListener('change', clearInvalid);
    });

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      document.querySelectorAll('.swiper').forEach(el => el.swiper?.autoplay?.stop?.());
    }

    document.querySelectorAll('form[data-static-form]').forEach(form => {
      form.addEventListener('submit', event => {
        event.preventDefault();
        if (!form.reportValidity()) return;
        if (form.dataset.staticForm === 'search') {
          const query = String(new FormData(form).get('s') || '').trim();
          const dialog = document.createElement('dialog'); dialog.className = 'static-search';
          const heading = document.createElement('h2');
          heading.id = `static-search-title-${Date.now()}`;
          heading.textContent = query ? `Search: ${query}` : 'Search pages';
          dialog.setAttribute('aria-labelledby', heading.id);
          const close = document.createElement('button'); close.type='button'; close.textContent = 'Close'; close.className='static-button'; close.addEventListener('click',()=>dialog.close());
          const list = document.createElement('ul');
          const words = query.toLowerCase().split(/\s+/).filter(Boolean);
          const results = words.length ? (window.TECHCO_SEARCH || []).filter(p => words.every(w => (p.title+' '+p.text).toLowerCase().includes(w))).slice(0,30) : [];
          results.forEach(p => {const li=document.createElement('li'),a=document.createElement('a');a.href=new URL(p.url,base);a.textContent=p.title;li.append(a);list.append(li);});
          if (!results.length) {const li=document.createElement('li');li.textContent=query?'No matching pages found. Try another keyword.':'Enter a keyword to search.';list.append(li);}
          dialog.append(heading,list,close);document.body.append(dialog);dialog.addEventListener('close',()=>dialog.remove());dialog.showModal();
        } else {
          const fields=[...new FormData(form)].filter(([key])=>!key.startsWith('_'));
          const content='Techco website request\n\n'+fields.map(([key,value])=>`${key}: ${value}`).join('\n')+'\n\nThis file is a local copy. It has not been sent or subscribed.';
          const url=URL.createObjectURL(new Blob([content],{type:'text/plain;charset=utf-8'}));
          const a=document.createElement('a');a.href=url;a.download='techco-request.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
          const note=form.querySelector('.static-form-note');
          if(note) note.textContent='Your request was downloaded to your device. Nothing has been sent. Contact the business directly to submit it.';
        }
      });
      if (form.dataset.staticForm === 'contact') form.querySelectorAll('[type="submit"]').forEach(e=>{
        if(e.tagName==='INPUT') e.value='Download request'; else if(e.textContent.trim()) e.textContent='Download request';
        e.removeAttribute('aria-label');
      });
    });
  };
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',ready);else ready();
})();

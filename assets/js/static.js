/* Standalone enhancements. No WordPress server or build step is required. */
(() => {
  'use strict';

  const base = new URL('../../', document.currentScript.src);
  const SITE_NAME = 'Forsk Technologies';
  const REQUEST_FILENAME = 'forsk-technologies-request.txt';
  const getSearchIndex = () => window.TECHCO_SEARCH || [];
  const OFFICIAL_HEADER_LOGO = new URL(
    'assets/images/logo/forsk-technologies-horizontal-logo-blue-black-green-ai-agi-white-background.png',
    base
  ).href;
  let generatedId = 0;
  let mobileTriggerToRestore = null;

  const ensureId = (element, prefix = 'forsk-nav') => {
    if (!element.id) {
      generatedId += 1;
      element.id = `${prefix}-${generatedId}`;
    }
    return element.id;
  };

  const normalizePath = (value) => {
    try {
      const url = new URL(value, window.location.href);
      let path = decodeURIComponent(url.pathname).replace(/\/{2,}/g, '/');
      if (path.endsWith('/')) path += 'index.html';
      return path.split('/').pop().toLowerCase() || 'index.html';
    } catch (_) {
      return '';
    }
  };

  const isVisible = (element) => Boolean(
    element &&
    !element.closest('[inert]') &&
    element.getClientRects().length
  );

  const getFocusable = (container) => [
    ...container.querySelectorAll(
      'a[href]:not([tabindex="-1"]), button:not([disabled]):not([tabindex="-1"]), input:not([disabled]):not([tabindex="-1"]), select:not([disabled]):not([tabindex="-1"]), textarea:not([disabled]):not([tabindex="-1"]), [tabindex]:not([tabindex="-1"])'
    )
  ].filter(isVisible);

  const applyOfficialHeaderLogo = () => {
    document.querySelectorAll('.site_header .header-logo img, .site_header .xb-logo-mobile img').forEach((image) => {
      image.src = OFFICIAL_HEADER_LOGO;
      image.alt = 'Forsk Technologies';
      image.decoding = 'async';
    });
  };

  const makeStickyCloneIdsUnique = () => {
    document.querySelectorAll('.stricked-menu').forEach((sticky, stickyIndex) => {
      const idMap = new Map();
      sticky.querySelectorAll('[id]').forEach((element, elementIndex) => {
        const oldId = element.id;
        const newId = `sticky-${stickyIndex + 1}-${oldId}-${elementIndex + 1}`;
        idMap.set(oldId, newId);
        element.id = newId;
      });
      sticky.querySelectorAll('[for], [aria-controls], [aria-labelledby], [aria-describedby]').forEach((element) => {
        ['for', 'aria-controls', 'aria-labelledby', 'aria-describedby'].forEach((attribute) => {
          const value = element.getAttribute(attribute);
          if (!value) return;
          const rewritten = value
            .split(/\s+/)
            .map((token) => idMap.get(token) || token)
            .join(' ');
          element.setAttribute(attribute, rewritten);
        });
      });
    });
  };

  const updateActiveNavigation = () => {
    const currentPath = normalizePath(window.location.href);
    const activeClasses = [
      'current-menu-item',
      'current_page_item',
      'current-menu-parent',
      'current_page_parent',
      'current-menu-ancestor',
      'current_page_ancestor'
    ];

    document.querySelectorAll('.site_header nav').forEach((nav) => {
      nav.querySelectorAll('li').forEach((item) => item.classList.remove(...activeClasses));
      nav.querySelectorAll('a[aria-current]').forEach((link) => link.removeAttribute('aria-current'));

      nav.querySelectorAll('a[href]').forEach((link) => {
        const href = link.getAttribute('href');
        if (!href || href === '#' || href.startsWith('javascript:')) return;
        if (normalizePath(link.href) !== currentPath) return;

        link.setAttribute('aria-current', 'page');
        const currentItem = link.closest('li');
        if (!currentItem) return;
        currentItem.classList.add('current-menu-item', 'current_page_item');

        let parent = currentItem.parentElement?.closest('li.menu-item-has-children');
        while (parent && nav.contains(parent)) {
          parent.classList.add('current-menu-ancestor', 'current_page_ancestor');
          parent = parent.parentElement?.closest('li.menu-item-has-children');
        }
      });
    });
  };

  const syncStickyAccessibility = () => {
    document.querySelectorAll('.stricked-menu').forEach((sticky) => {
      const isFixed = sticky.classList.contains('stricky-fixed');
      sticky.setAttribute('aria-hidden', String(!isFixed));
      sticky.inert = !isFixed;

      const original = sticky.parentElement?.querySelector(':scope > .stricky.original');
      if (original) {
        original.setAttribute('aria-hidden', String(isFixed));
        original.inert = isFixed;
      }
    });
  };

  const setupStickyAccessibility = () => {
    syncStickyAccessibility();
    document.querySelectorAll('.stricked-menu').forEach((sticky) => {
      new MutationObserver(syncStickyAccessibility).observe(sticky, {
        attributes: true,
        attributeFilter: ['class']
      });
    });
    window.addEventListener('scroll', syncStickyAccessibility, { passive: true });
  };

  const syncSubmenuToggle = (toggle) => {
    const item = toggle.closest('.menu-item-has-children');
    const submenu = item?.querySelector(':scope > .sub-menu');
    const expanded = Boolean(
      toggle.classList.contains('active') ||
      submenu?.classList.contains('active')
    );
    toggle.setAttribute('aria-expanded', String(expanded));
  };

  const setupMobileSubmenus = () => {
    document.querySelectorAll('.xb-header-menu .menu-item-has-children').forEach((item) => {
      const submenu = item.querySelector(':scope > .sub-menu');
      const toggle = item.querySelector(':scope > .xb-menu-toggle');
      if (!submenu || !toggle) return;

      const label = item.querySelector(':scope > a')?.textContent.trim() || 'submenu';
      const submenuId = ensureId(submenu, 'mobile-submenu');
      toggle.setAttribute('role', 'button');
      toggle.tabIndex = 0;
      toggle.setAttribute('aria-label', `Toggle ${label} submenu`);
      toggle.setAttribute('aria-controls', submenuId);
      toggle.setAttribute('aria-expanded', 'false');

      toggle.addEventListener('click', () => window.requestAnimationFrame(() => syncSubmenuToggle(toggle)));
      toggle.addEventListener('keydown', (event) => {
        if (!['Enter', ' '].includes(event.key)) return;
        event.preventDefault();
        toggle.click();
      });
    });
  };

  const visibleMobileMenu = () => [
    ...document.querySelectorAll('.xb-header-menu.active')
  ].find((menu) => !menu.closest('[inert]') && menu.getClientRects().length) || null;

  const syncMobileNavigation = (focusOnOpen = false) => {
    const activeMenu = visibleMobileMenu();
    const isOpen = Boolean(activeMenu);
    document.body.classList.toggle('forsk-nav-open', isOpen);

    document.querySelectorAll('.xb-nav-mobile').forEach((trigger) => {
      trigger.setAttribute('aria-expanded', String(isOpen));
      trigger.setAttribute('aria-label', isOpen ? 'Close navigation' : 'Open navigation');
    });

    if (isOpen && focusOnOpen) {
      const closeButton = activeMenu.querySelector('.xb-menu-close');
      const firstLink = activeMenu.querySelector('a[href]');
      window.setTimeout(() => (closeButton || firstLink)?.focus(), 0);
    }
  };

  const closeMobileNavigation = ({ restoreFocus = true } = {}) => {
    document.querySelectorAll('.xb-header-menu, .xb-nav-mobile').forEach((element) => element.classList.remove('active'));
    document.querySelectorAll('.xb-nav-mobile').forEach((trigger) => {
      trigger.setAttribute('aria-expanded', 'false');
      trigger.setAttribute('aria-label', 'Open navigation');
    });
    document.body.classList.remove('forsk-nav-open');
    if (restoreFocus && mobileTriggerToRestore) mobileTriggerToRestore.focus();
  };

  const setupMobileNavigation = () => {
    document.querySelectorAll('.xb-header-menu').forEach((menu) => {
      ensureId(menu, 'mobile-navigation');
      menu.setAttribute('aria-label', 'Primary navigation');
    });

    document.querySelectorAll('.xb-nav-mobile').forEach((trigger) => {
      const headerBottom = trigger.closest('.header_bottom');
      const controlledMenu = headerBottom?.querySelector('.xb-header-menu') || document.querySelector('.xb-header-menu');
      trigger.setAttribute('aria-label', 'Open navigation');
      trigger.setAttribute('aria-expanded', 'false');
      if (controlledMenu) trigger.setAttribute('aria-controls', ensureId(controlledMenu, 'mobile-navigation'));

      trigger.addEventListener('click', () => {
        mobileTriggerToRestore = trigger;
        window.requestAnimationFrame(() => syncMobileNavigation(true));
      });
    });

    document.querySelectorAll('.xb-menu-close').forEach((closeButton) => {
      closeButton.setAttribute('role', 'button');
      closeButton.tabIndex = 0;
      closeButton.setAttribute('aria-label', 'Close navigation');
      closeButton.addEventListener('keydown', (event) => {
        if (!['Enter', ' '].includes(event.key)) return;
        event.preventDefault();
        closeButton.click();
      });
      closeButton.addEventListener('click', () => window.requestAnimationFrame(() => {
        syncMobileNavigation(false);
        mobileTriggerToRestore?.focus();
      }));
    });

    document.querySelectorAll('.xb-header-menu-backdrop').forEach((backdrop) => {
      backdrop.addEventListener('click', () => window.requestAnimationFrame(() => syncMobileNavigation(false)));
    });

    document.querySelectorAll('.xb-header-menu a[href]').forEach((link) => {
      link.addEventListener('click', () => {
        const href = link.getAttribute('href');
        if (href && href !== '#') window.setTimeout(() => closeMobileNavigation({ restoreFocus: false }), 0);
      });
    });
  };

  const closeDesktopDropdowns = (except = null) => {
    document.querySelectorAll('.main-menu li.forsk-submenu-open').forEach((item) => {
      if (item === except || item.contains(except)) return;
      item.classList.remove('forsk-submenu-open');
      item.querySelector(':scope > a')?.setAttribute('aria-expanded', 'false');
    });
  };

  const setupDesktopNavigation = () => {
    document.querySelectorAll('.main-menu').forEach((nav) => {
      nav.setAttribute('aria-label', 'Primary navigation');

      nav.querySelectorAll('li.menu-item-has-children').forEach((item) => {
        const link = item.querySelector(':scope > a');
        const submenu = item.querySelector(':scope > .sub-menu');
        if (!link || !submenu) return;

        const submenuId = ensureId(submenu, 'desktop-submenu');
        link.setAttribute('aria-haspopup', 'true');
        link.setAttribute('aria-controls', submenuId);
        link.setAttribute('aria-expanded', 'false');

        const open = () => {
          closeDesktopDropdowns(item);
          item.classList.add('forsk-submenu-open');
          link.setAttribute('aria-expanded', 'true');
        };
        const close = () => {
          item.classList.remove('forsk-submenu-open');
          link.setAttribute('aria-expanded', 'false');
        };

        item.addEventListener('focusin', open);
        item.addEventListener('focusout', () => window.setTimeout(() => {
          if (!item.contains(document.activeElement)) close();
        }, 0));

        link.addEventListener('keydown', (event) => {
          if (event.key === 'ArrowDown') {
            event.preventDefault();
            open();
            submenu.querySelector('a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])')?.focus();
          } else if (event.key === 'Escape') {
            event.preventDefault();
            close();
            link.focus();
          }
        });

        if (link.getAttribute('href') === '#') {
          link.addEventListener('click', (event) => {
            event.preventDefault();
            const opening = !item.classList.contains('forsk-submenu-open');
            closeDesktopDropdowns(opening ? item : null);
            item.classList.toggle('forsk-submenu-open', opening);
            link.setAttribute('aria-expanded', String(opening));
          });
        }
      });

      const topLevelLinks = [
        ...nav.querySelectorAll(':scope > ul > li > a')
      ];
      topLevelLinks.forEach((link, index) => {
        link.addEventListener('keydown', (event) => {
          let nextIndex = null;
          if (event.key === 'ArrowRight') nextIndex = (index + 1) % topLevelLinks.length;
          if (event.key === 'ArrowLeft') nextIndex = (index - 1 + topLevelLinks.length) % topLevelLinks.length;
          if (event.key === 'Home') nextIndex = 0;
          if (event.key === 'End') nextIndex = topLevelLinks.length - 1;
          if (nextIndex === null) return;
          event.preventDefault();
          topLevelLinks[nextIndex]?.focus();
        });
      });
    });

    document.addEventListener('pointerdown', (event) => {
      if (!event.target.closest('.main-menu')) closeDesktopDropdowns();
    });
  };

  const setupKeyboardSafety = () => {
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') {
        if (visibleMobileMenu()) {
          event.preventDefault();
          closeMobileNavigation();
          return;
        }
        closeDesktopDropdowns();
      }

      if (event.key !== 'Tab') return;
      const menu = visibleMobileMenu();
      if (!menu) return;
      const focusable = getFocusable(menu);
      if (!focusable.length) return;

      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });
  };

  const setupStaticForms = () => {
    document.querySelectorAll('form[data-static-form]').forEach((form) => {
      form.addEventListener('submit', (event) => {
        event.preventDefault();
        if (!form.reportValidity()) return;
        if (form.dataset.staticForm === 'search') {
          const query = String(new FormData(form).get('s') || '').trim();
          const dialog = document.createElement('dialog');
          dialog.className = 'static-search';
          const heading = document.createElement('h2');
          heading.textContent = query ? `Search: ${query}` : 'Search pages';
          const close = document.createElement('button');
          close.textContent = 'Close';
          close.className = 'static-button';
          close.addEventListener('click', () => dialog.close());
          const list = document.createElement('ul');
          const words = query.toLowerCase().split(/\s+/).filter(Boolean);
          const results = words.length
            ? getSearchIndex().filter((page) => words.every((word) => `${page.title} ${page.text}`.toLowerCase().includes(word))).slice(0, 30)
            : [];
          results.forEach((page) => {
            const item = document.createElement('li');
            const link = document.createElement('a');
            link.href = new URL(page.url, base);
            link.textContent = page.title;
            item.append(link);
            list.append(item);
          });
          if (!results.length) {
            const item = document.createElement('li');
            item.textContent = query ? 'No matching pages found. Try another keyword.' : 'Enter a keyword to search.';
            list.append(item);
          }
          dialog.append(heading, list, close);
          document.body.append(dialog);
          dialog.addEventListener('close', () => dialog.remove());
          dialog.showModal();
        } else {
          const fields = [...new FormData(form)].filter(([key]) => !key.startsWith('_'));
          const content = `${SITE_NAME} website request\n\n${fields.map(([key, value]) => `${key}: ${value}`).join('\n')}\n\nThis file is a local copy. It has not been sent or subscribed.`;
          const url = URL.createObjectURL(new Blob([content], { type: 'text/plain;charset=utf-8' }));
          const link = document.createElement('a');
          link.href = url;
          link.download = REQUEST_FILENAME;
          link.click();
          window.setTimeout(() => URL.revokeObjectURL(url), 1000);
          const note = form.querySelector('.static-form-note');
          if (note) note.textContent = 'Your request was downloaded to your device. Nothing has been sent. Contact the business directly to submit it.';
        }
      });
      if (form.dataset.staticForm === 'contact') {
        form.querySelectorAll('[type="submit"]').forEach((element) => {
          if (element.tagName === 'INPUT') element.value = 'Download request';
          else if (element.textContent.trim()) element.textContent = 'Download request';
          element.setAttribute('aria-label', 'Download request');
        });
      }
    });
  };

  const ready = () => {
    document.querySelectorAll('.elementor-invisible').forEach((element) => element.classList.remove('elementor-invisible'));
    document.querySelectorAll('.e-con.e-parent').forEach((element) => element.classList.add('e-lazyloaded'));
    document.querySelectorAll('.odometer[data-count]').forEach((element) => { element.textContent = element.dataset.count; });

    makeStickyCloneIdsUnique();
    applyOfficialHeaderLogo();
    updateActiveNavigation();
    setupDesktopNavigation();
    setupMobileSubmenus();
    setupMobileNavigation();
    setupStickyAccessibility();
    setupKeyboardSafety();
    setupStaticForms();
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready);
  else ready();
})();

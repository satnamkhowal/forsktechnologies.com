(() => {
  'use strict';

  const scriptUrl = new URL(document.currentScript.src, window.location.href);
  const siteRoot = new URL('../../', scriptUrl);
  const endpoint = new URL('api/enquiry.php', siteRoot);
  const tokenEndpoint = new URL('api/enquiry-token.php', siteRoot);

  const selectors = {
    name: '[name="name"], #input_name',
    email: '[name="email"], #input_email',
    phone: '[name="phone"], #input_phone',
    company: '[name="company"], #input_company',
    message: '[name="message"], #input_textarea'
  };

  const fieldFor = (form, key) => form.querySelector(selectors[key]);
  const valueFor = (form, key) => String(fieldFor(form, key)?.value || '').trim();

  const ensureStyles = () => {
    if (document.querySelector('link[data-forsk-enquiry-styles]')) return;
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = new URL('assets/css/enquiry-form.css', siteRoot).href;
    link.dataset.forskEnquiryStyles = 'true';
    document.head.append(link);
  };

  const ensureStatus = form => {
    let status = form.querySelector('.forsk-enquiry-status');
    if (!status) {
      status = form.querySelector('.wpcf7-response-output');
      if (status) status.classList.add('forsk-enquiry-status');
    }
    if (!status) {
      status = document.createElement('div');
      status.className = 'forsk-enquiry-status';
      const submit = form.querySelector('[type="submit"]');
      if (submit?.parentNode) submit.parentNode.insertBefore(status, submit);
      else form.append(status);
    }
    status.setAttribute('role', 'status');
    status.setAttribute('aria-live', 'polite');
    status.setAttribute('aria-atomic', 'true');
    status.removeAttribute('aria-hidden');
    return status;
  };

  const showStatus = (form, message, kind = 'error') => {
    const status = ensureStatus(form);
    status.textContent = message;
    status.classList.add('is-visible');
    status.classList.toggle('is-success', kind === 'success');
    status.classList.toggle('is-error', kind !== 'success');
  };

  const clearStatus = form => {
    const status = ensureStatus(form);
    status.textContent = '';
    status.classList.remove('is-visible', 'is-success', 'is-error');
  };

  const ensureError = (form, key) => {
    let error = form.querySelector(`[data-error-for="${key}"]`);
    if (error) return error;
    const field = fieldFor(form, key);
    if (!field) return null;
    error = document.createElement('div');
    error.className = 'forsk-field-error';
    error.dataset.errorFor = key;
    error.setAttribute('aria-live', 'polite');
    field.insertAdjacentElement('afterend', error);
    return error;
  };

  const clearErrors = form => {
    Object.keys(selectors).forEach(key => {
      const field = fieldFor(form, key);
      const error = ensureError(form, key);
      if (field) {
        field.classList.remove('forsk-enquiry-invalid');
        field.removeAttribute('aria-invalid');
        field.removeAttribute('aria-describedby');
      }
      if (error) error.textContent = '';
    });
  };

  const showErrors = (form, errors = {}) => {
    let firstInvalid = null;
    Object.entries(errors).forEach(([key, message]) => {
      const field = fieldFor(form, key);
      const error = ensureError(form, key);
      if (!field || !error) return;
      if (!error.id) error.id = `${form.id || 'forsk-enquiry'}-${key}-error`;
      error.textContent = String(message);
      field.classList.add('forsk-enquiry-invalid');
      field.setAttribute('aria-invalid', 'true');
      field.setAttribute('aria-describedby', error.id);
      if (!firstInvalid) firstInvalid = field;
    });
    firstInvalid?.focus();
  };

  const validate = form => {
    const errors = {};
    const name = valueFor(form, 'name');
    const email = valueFor(form, 'email');
    const phone = valueFor(form, 'phone');
    const company = valueFor(form, 'company');
    const message = valueFor(form, 'message');
    const phoneDigits = phone.replace(/\D/g, '');

    if (name.length < 2) errors.name = 'Please enter your full name.';
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 254) {
      errors.email = 'Please enter a valid email address.';
    }
    if (!/^[0-9+().\s-]{7,25}$/.test(phone) || phoneDigits.length < 7 || phoneDigits.length > 15) {
      errors.phone = 'Please enter a valid phone number.';
    }
    if (company && company.length < 2) {
      errors.company = 'Please enter a valid company name or leave it blank.';
    }
    if (message.length < 10) errors.message = 'Please add a little more detail about how we can help.';
    if (message.length > 3000) errors.message = 'Please keep your message under 3000 characters.';

    return errors;
  };

  const ensureHoneypot = form => {
    let field = form.querySelector('[name="website"]');
    if (field) return field;
    const wrapper = document.createElement('div');
    wrapper.className = 'forsk-enquiry-honeypot';
    wrapper.setAttribute('aria-hidden', 'true');
    const label = document.createElement('label');
    label.textContent = 'Website';
    field = document.createElement('input');
    field.type = 'text';
    field.name = 'website';
    field.tabIndex = -1;
    field.autocomplete = 'off';
    wrapper.append(label, field);
    form.append(wrapper);
    return field;
  };

  const fetchToken = async form => {
    const response = await fetch(tokenEndpoint, {
      method: 'GET',
      credentials: 'same-origin',
      headers: { Accept: 'application/json', 'X-Requested-With': 'XMLHttpRequest' }
    });
    const payload = await response.json().catch(() => ({}));
    if (!response.ok || !payload.csrf) throw new Error(payload.message || 'Could not initialize the secure form.');
    form.dataset.enquiryCsrf = payload.csrf;
    return payload.csrf;
  };

  const prepareForm = form => {
    if (form.dataset.forskEnquiryReady === 'true') return;
    form.dataset.forskEnquiryReady = 'true';
    ensureStyles();
    ensureHoneypot(form);
    ensureStatus(form);

    const legacy = form.matches('[data-static-form="contact"]');
    if (legacy) {
      const action = String(form.getAttribute('action') || '').trim();
      if (action && action !== '#') {
        // A real endpoint was added elsewhere: do not replace or intercept it.
        form.dataset.forskEnquiryReady = 'external-endpoint';
        return;
      }
      form.method = 'post';
      form.action = endpoint.href;
      const note = form.querySelector('.static-form-note');
      if (note) note.textContent = 'Your details will be used only to respond to this enquiry.';
    }

    const name = fieldFor(form, 'name');
    const email = fieldFor(form, 'email');
    const phone = fieldFor(form, 'phone');
    const company = fieldFor(form, 'company');
    const message = fieldFor(form, 'message');
    if (name) { name.autocomplete = 'name'; name.maxLength = 100; }
    if (email) { email.autocomplete = 'email'; email.maxLength = 254; }
    if (phone) { phone.autocomplete = 'tel'; phone.inputMode = 'tel'; phone.maxLength = 25; }
    if (company) { company.autocomplete = 'organization'; company.maxLength = 120; company.required = false; company.removeAttribute('aria-required'); }
    if (message) { message.minLength = 10; message.maxLength = 3000; }

    fetchToken(form).catch(() => {
      // A fresh token is attempted again at submit time; do not expose server detail here.
    });

    form.addEventListener('input', event => {
      const input = event.target;
      if (!(input instanceof HTMLElement)) return;
      input.classList.remove('forsk-enquiry-invalid');
      input.removeAttribute('aria-invalid');
    });

    form.addEventListener('submit', async event => {
      event.preventDefault();
      clearStatus(form);
      clearErrors(form);

      if (!form.reportValidity()) return;
      const clientErrors = validate(form);
      if (Object.keys(clientErrors).length) {
        showErrors(form, clientErrors);
        showStatus(form, 'Please correct the highlighted fields and submit again.');
        return;
      }

      const submit = form.querySelector('[type="submit"]');
      if (submit) {
        submit.disabled = true;
        submit.setAttribute('aria-busy', 'true');
      }

      try {
        const csrf = form.dataset.enquiryCsrf || await fetchToken(form);
        const data = new FormData();
        data.set('_csrf', csrf);
        data.set('name', valueFor(form, 'name'));
        data.set('email', valueFor(form, 'email'));
        data.set('phone', valueFor(form, 'phone'));
        data.set('company', valueFor(form, 'company'));
        data.set('message', valueFor(form, 'message'));
        data.set('source_page', window.location.pathname.slice(0, 255));
        data.set('source_form', String(form.dataset.sourceForm || form.id || 'legacy-contact').slice(0, 80));
        data.set('website', String(form.querySelector('[name="website"]')?.value || ''));

        const response = await fetch(endpoint, {
          method: 'POST',
          body: data,
          credentials: 'same-origin',
          headers: { Accept: 'application/json', 'X-Requested-With': 'XMLHttpRequest' }
        });
        const payload = await response.json().catch(() => ({}));
        form.dataset.enquiryCsrf = '';

        if (!response.ok || !payload.ok) {
          if (payload.errors) showErrors(form, payload.errors);
          showStatus(form, payload.message || 'We could not submit your enquiry right now. Please try again later.');
          fetchToken(form).catch(() => {});
          return;
        }

        form.reset();
        showStatus(form, payload.message || 'Thank you. Your enquiry has been received.', 'success');
        fetchToken(form).catch(() => {});
      } catch (error) {
        showStatus(form, 'We could not submit your enquiry right now. Please check your connection and try again.');
      } finally {
        if (submit) {
          submit.disabled = false;
          submit.removeAttribute('aria-busy');
        }
      }
    });
  };

  const isLegacyEnquiry = form => {
    if (!form.matches('[data-static-form="contact"]')) return false;
    if (form.querySelector('#footer_mail_input, .footer_newslatter')) return false;
    return Boolean(fieldFor(form, 'name') && fieldFor(form, 'email') && fieldFor(form, 'phone') && fieldFor(form, 'message'));
  };

  document.querySelectorAll('form[data-enquiry-form="true"], form[data-static-form="contact"]').forEach(form => {
    if (form.matches('[data-enquiry-form="true"]') || isLegacyEnquiry(form)) prepareForm(form);
  });
})();

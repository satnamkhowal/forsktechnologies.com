# Forsk Technologies enquiry form system

This system converts the existing static website enquiry forms into a secure server-processed flow without changing the public `.html` URLs. It also provides a reusable PHP include for pages that are converted to PHP later.

## Verified field model

The existing website uses these enquiry fields:

- Full name (required)
- Email (required)
- Phone (required)
- Company (present on the homepage; optional in the shared schema)
- Message / project details (required)

The system does not add unverified business facts or unnecessary lead fields. `source_page` and `source_form` are internal context fields added by the client/PHP include.

## Files

- `includes/enquiry-system.php` — server configuration, session/CSRF, validation, sanitization, rate limiting, privacy-conscious logging, optional PDO storage, optional mail notification.
- `includes/enquiry-form.php` — reusable PHP form renderer.
- `api/enquiry-token.php` — same-origin CSRF token endpoint.
- `api/enquiry.php` — POST submission endpoint.
- `assets/js/enquiry-form.js` — client-side validation, error UI and AJAX submission for reusable and legacy forms.
- `assets/css/enquiry-form.css` — accessible error/success/spam-honeypot states.
- `database/enquiries.sql` — optional MySQL/MariaDB table.

## Legacy migration behavior

The current exported contact forms use `action="#"`, `method="get"` and `data-static-form="contact"`. `assets/js/static.js` now detects only full enquiry forms (name + email + phone + message), skips the footer newsletter, and loads `enquiry-form.js`.

`enquiry-form.js` changes only those static demo enquiry forms to the secure POST endpoint at runtime. If a form already has a non-`#` action, it is deliberately left alone so an existing/real endpoint is not broken.

The original `.html` URLs remain unchanged.

## Server configuration

Do not place secrets in HTML, JavaScript, committed PHP config files or the repository. Configure these as hosting/server environment variables instead:

| Variable | Purpose |
| --- | --- |
| `FORSK_ENQUIRY_APP_KEY` | Secret used for privacy-preserving IP hashing. Recommended in production. |
| `FORSK_ENQUIRY_TRUSTED_ORIGINS` | Optional comma-separated additional allowed origins. Same host is allowed automatically. |
| `FORSK_ENQUIRY_RATE_LIMIT` | Maximum submissions per rate window. Default `5`. |
| `FORSK_ENQUIRY_RATE_WINDOW` | Rate window in seconds. Default `900`. |
| `FORSK_ENQUIRY_MIN_FILL_SECONDS` | Minimum time between CSRF issue and submit. Default `2`. |
| `FORSK_ENQUIRY_LOG_PATH` | Optional private server log file path. If absent, minimal events go to the PHP error log. |
| `FORSK_ENQUIRY_DB_DSN` | Optional PDO DSN, e.g. a MySQL DSN. |
| `FORSK_ENQUIRY_DB_USER` | Optional database user. |
| `FORSK_ENQUIRY_DB_PASS` | Optional database password. |
| `FORSK_ENQUIRY_DB_TABLE` | Optional table override. Default `forsk_enquiries`. |
| `FORSK_ENQUIRY_MAIL_TO` | Optional verified notification recipient address. |
| `FORSK_ENQUIRY_MAIL_FROM` | Optional verified server sender address. |

At least one delivery method (database or mail) must be configured. The endpoint returns a clear `503` instead of falsely telling a visitor that an enquiry was sent when neither is configured.

### Database

If database storage is wanted, run `database/enquiries.sql` once against the configured database, then set the PDO environment variables above. Inserts use prepared statements. The database records the submitted enquiry but does not store visitor IP addresses.

### Email

Email notification is enabled only when both `FORSK_ENQUIRY_MAIL_TO` and `FORSK_ENQUIRY_MAIL_FROM` are valid server-side values. The implementation uses PHP's configured mail transport; SMTP usernames/passwords are never sent to or embedded in the browser.

If the hosting environment requires authenticated SMTP instead of PHP mail, add a server-side mail transport/library and continue reading its credentials only from server environment configuration.

## Reusable PHP include

On a PHP page:

```php
<?php
require_once __DIR__ . '/includes/enquiry-form.php';

forsk_render_enquiry_form([
    'id' => 'service-enquiry',
    'source_form' => 'service-page',
    'include_company' => true,
    'button_label' => 'Send Enquiry',
]);
```

The shared renderer uses the current site form classes (`row`, `form-group`, `form-control`, `btn`) so it can fit the established design system rather than introduce a separate visual language.

## Validation and security

Server-side rules are authoritative. JavaScript mirrors them for faster feedback:

- name: required, minimum 2 characters, maximum 100
- email: required, valid email, maximum 254
- phone: required, 7–15 digits with common phone punctuation allowed
- company: optional, maximum 120
- message: required, minimum 10, maximum 3000

Additional controls:

- POST-only submission
- same-origin/origin allow-list check
- session-backed CSRF token
- minimum form-fill timing check
- hidden honeypot
- hashed-IP rate limiting (raw IP is not stored by the form system)
- prepared SQL statements
- CR/LF stripping for mail headers
- normalized control-character filtering and length limits
- generic external errors; internal failure detail is not returned to visitors
- minimal logs contain request id, event type, source page and a short IP hash only — not name, email, phone, company or message

## Deployment checklist

1. Confirm PHP sessions work on the hosting account.
2. Configure `FORSK_ENQUIRY_APP_KEY` with a strong random server-side secret.
3. Configure at least database storage or server mail delivery.
4. If using DB storage, run `database/enquiries.sql` and test insert permissions.
5. If using mail, verify the configured sender is permitted by the hosting mail setup.
6. Submit from the homepage and `contact.html` and confirm clear success/error UI.
7. Test invalid email, short message, invalid phone, repeated submissions and a filled honeypot.
8. Confirm logs do not contain submitted PII.
9. Confirm footer newsletter behavior has not been converted into an enquiry.
10. Once all pages are gradually converted to PHP, use `forsk_render_enquiry_form()` rather than duplicating form markup.

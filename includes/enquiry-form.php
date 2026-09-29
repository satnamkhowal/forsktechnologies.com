<?php

declare(strict_types=1);

require_once __DIR__ . '/enquiry-system.php';

/**
 * Render the reusable Forsk Technologies enquiry form.
 *
 * Options:
 * - id: form id
 * - source_form: analytics/source label
 * - source_page: page path/identifier
 * - include_company: show optional company field (default true)
 * - button_label: submit button text
 */
function forsk_render_enquiry_form(array $options = []): void
{
    $id = preg_replace('/[^A-Za-z0-9_-]/', '', (string) ($options['id'] ?? 'forsk-enquiry-form')) ?: 'forsk-enquiry-form';
    $sourceForm = forsk_enquiry_normalize_text($options['source_form'] ?? 'enquiry', 80);
    $sourcePage = forsk_enquiry_normalize_text($options['source_page'] ?? ($_SERVER['REQUEST_URI'] ?? ''), 255);
    $includeCompany = !array_key_exists('include_company', $options) || (bool) $options['include_company'];
    $buttonLabel = forsk_enquiry_normalize_text($options['button_label'] ?? 'Send Enquiry', 40);
    $csrf = forsk_enquiry_issue_token();

    $escape = static function (string $value): string {
        return htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
    };
    ?>
    <form id="<?= $escape($id) ?>"
          class="forsk-enquiry-form"
          action="/api/enquiry.php"
          method="post"
          data-enquiry-form="true"
          data-source-form="<?= $escape($sourceForm) ?>"
          novalidate>
        <input type="hidden" name="_csrf" value="<?= $escape($csrf) ?>">
        <input type="hidden" name="source_form" value="<?= $escape($sourceForm) ?>">
        <input type="hidden" name="source_page" value="<?= $escape($sourcePage) ?>">
        <div class="forsk-enquiry-honeypot" aria-hidden="true">
            <label for="<?= $escape($id) ?>-website">Website</label>
            <input id="<?= $escape($id) ?>-website" name="website" type="text" tabindex="-1" autocomplete="off">
        </div>

        <div class="row xb-contact-form">
            <div class="col-md-6">
                <div class="form-group">
                    <label class="input_title" for="<?= $escape($id) ?>-name">Full Name</label>
                    <input class="form-control" id="<?= $escape($id) ?>-name" name="name" type="text"
                           autocomplete="name" minlength="2" maxlength="100" required aria-required="true">
                    <div class="forsk-field-error" data-error-for="name" aria-live="polite"></div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="form-group">
                    <label class="input_title" for="<?= $escape($id) ?>-email">Email</label>
                    <input class="form-control" id="<?= $escape($id) ?>-email" name="email" type="email"
                           autocomplete="email" maxlength="254" required aria-required="true">
                    <div class="forsk-field-error" data-error-for="email" aria-live="polite"></div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="form-group">
                    <label class="input_title" for="<?= $escape($id) ?>-phone">Phone</label>
                    <input class="form-control" id="<?= $escape($id) ?>-phone" name="phone" type="tel"
                           autocomplete="tel" inputmode="tel" maxlength="25" required aria-required="true">
                    <div class="forsk-field-error" data-error-for="phone" aria-live="polite"></div>
                </div>
            </div>
            <?php if ($includeCompany): ?>
                <div class="col-md-6">
                    <div class="form-group">
                        <label class="input_title" for="<?= $escape($id) ?>-company">Company <span class="forsk-optional">(optional)</span></label>
                        <input class="form-control" id="<?= $escape($id) ?>-company" name="company" type="text"
                               autocomplete="organization" maxlength="120">
                        <div class="forsk-field-error" data-error-for="company" aria-live="polite"></div>
                    </div>
                </div>
            <?php endif; ?>
            <div class="col-12">
                <div class="form-group">
                    <label class="input_title" for="<?= $escape($id) ?>-message">How can we help?</label>
                    <textarea class="form-control" id="<?= $escape($id) ?>-message" name="message" rows="6"
                              minlength="10" maxlength="3000" required aria-required="true"></textarea>
                    <div class="forsk-field-error" data-error-for="message" aria-live="polite"></div>
                </div>
            </div>
            <div class="col-12">
                <p class="forsk-enquiry-privacy-note">The details you submit will be used to respond to your enquiry.</p>
                <div class="forsk-enquiry-status" role="status" aria-live="polite" aria-atomic="true"></div>
                <button type="submit" class="btn btn-primary">
                    <span class="btn_label"><?= $escape($buttonLabel) ?></span>
                    <span class="btn_icon" aria-hidden="true"><i class="fa-solid fa-arrow-up-right"></i></span>
                </button>
            </div>
        </div>
    </form>
    <?php
}

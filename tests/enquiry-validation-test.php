<?php

declare(strict_types=1);

require_once dirname(__DIR__) . '/includes/enquiry-system.php';

function assert_true(bool $condition, string $message): void
{
    if (!$condition) {
        fwrite(STDERR, "FAIL: {$message}\n");
        exit(1);
    }
}

[$validData, $validErrors] = forsk_enquiry_validate([
    'name' => 'Test User',
    'email' => 'test@example.com',
    'phone' => '+91 98765 43210',
    'company' => 'Example Company',
    'message' => 'We need help with a software project.',
    'source_page' => '/contact.html?email=private@example.com',
    'source_form' => 'contact-page',
]);

assert_true($validErrors === [], 'valid enquiry should pass validation');
assert_true($validData['source_page'] === '/contact.html', 'source page must discard query strings');

[, $invalidErrors] = forsk_enquiry_validate([
    'name' => 'A',
    'email' => 'not-an-email',
    'phone' => '123',
    'message' => 'short',
]);

assert_true(isset($invalidErrors['name']), 'short name should fail');
assert_true(isset($invalidErrors['email']), 'invalid email should fail');
assert_true(isset($invalidErrors['phone']), 'invalid phone should fail');
assert_true(isset($invalidErrors['message']), 'short message should fail');

[$legacyData, $legacyErrors] = forsk_enquiry_validate([
    'text-967' => 'Legacy User',
    'email-191' => 'legacy@example.com',
    'text-968' => '+1 202 555 0100',
    'text-969' => 'Legacy Company',
    'textarea-579' => 'This validates the homepage legacy aliases.',
]);

assert_true($legacyErrors === [], 'legacy homepage aliases should remain compatible');
assert_true($legacyData['name'] === 'Legacy User', 'legacy name should map to canonical name');
assert_true($legacyData['company'] === 'Legacy Company', 'legacy company should map to canonical company');

fwrite(STDOUT, "PASS: enquiry validation smoke checks\n");

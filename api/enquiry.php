<?php

declare(strict_types=1);

require_once dirname(__DIR__) . '/includes/enquiry-system.php';

header('Referrer-Policy: strict-origin-when-cross-origin');
header('Permissions-Policy: interest-cohort=()');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Allow: POST');
    forsk_enquiry_respond(405, [
        'ok' => false,
        'message' => 'Method not allowed.',
    ]);
}

$requestId = 'ENQ-' . gmdate('Ymd') . '-' . strtoupper(bin2hex(random_bytes(4)));
$sourcePage = forsk_enquiry_value($_POST, ['source_page'], 255);

if (!forsk_enquiry_origin_allowed()) {
    forsk_enquiry_log('rejected_origin', $requestId, ['source_page' => $sourcePage]);
    forsk_enquiry_respond(403, [
        'ok' => false,
        'message' => 'This request could not be verified. Please reload the page and try again.',
    ]);
}

if (forsk_enquiry_rate_limited()) {
    forsk_enquiry_log('rate_limited', $requestId, ['source_page' => $sourcePage]);
    forsk_enquiry_respond(429, [
        'ok' => false,
        'message' => 'Too many submissions were received. Please try again later.',
    ]);
}

// Honeypot: respond successfully so automated spam does not learn the rejection rule.
$honeypot = forsk_enquiry_value($_POST, ['website'], 255);
if ($honeypot !== '') {
    forsk_enquiry_log('spam_honeypot', $requestId, ['source_page' => $sourcePage]);
    forsk_enquiry_respond(200, [
        'ok' => true,
        'request_id' => $requestId,
        'message' => 'Thank you. Your enquiry has been received.',
    ]);
}

$csrf = forsk_enquiry_value($_POST, ['_csrf'], 128);
if (!forsk_enquiry_verify_csrf($csrf)) {
    forsk_enquiry_log('rejected_csrf', $requestId, ['source_page' => $sourcePage]);
    forsk_enquiry_respond(403, [
        'ok' => false,
        'message' => 'Your form session expired or could not be verified. Please reload the page and try again.',
    ]);
}

[$data, $errors] = forsk_enquiry_validate($_POST);
if ($errors) {
    forsk_enquiry_log('validation_failed', $requestId, ['source_page' => $data['source_page']]);
    forsk_enquiry_respond(422, [
        'ok' => false,
        'message' => 'Please correct the highlighted fields and submit again.',
        'errors' => $errors,
    ]);
}

$dbResult = ['configured' => false, 'success' => false];
$mailResult = ['configured' => false, 'success' => false];

try {
    $dbResult = forsk_enquiry_store($data, $requestId);
} catch (Throwable $exception) {
    forsk_enquiry_log('database_error', $requestId, ['source_page' => $data['source_page']]);
}

try {
    $mailResult = forsk_enquiry_send_mail($data, $requestId);
} catch (Throwable $exception) {
    forsk_enquiry_log('mail_error', $requestId, ['source_page' => $data['source_page']]);
}

$deliveryConfigured = $dbResult['configured'] || $mailResult['configured'];
$delivered = $dbResult['success'] || $mailResult['success'];

if (!$deliveryConfigured) {
    forsk_enquiry_log('not_configured', $requestId, ['source_page' => $data['source_page']]);
    forsk_enquiry_respond(503, [
        'ok' => false,
        'message' => 'The enquiry service is not configured on this server yet. Please try again after the site configuration is completed.',
    ]);
}

if (!$delivered) {
    forsk_enquiry_log('delivery_failed', $requestId, ['source_page' => $data['source_page']]);
    forsk_enquiry_respond(500, [
        'ok' => false,
        'message' => 'We could not submit your enquiry right now. Please try again later.',
    ]);
}

forsk_enquiry_log('accepted', $requestId, ['source_page' => $data['source_page']]);
forsk_enquiry_respond(200, [
    'ok' => true,
    'request_id' => $requestId,
    'message' => 'Thank you. Your enquiry has been received. We will use the details you provided to respond to your request.',
]);

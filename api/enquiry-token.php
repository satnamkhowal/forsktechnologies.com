<?php

declare(strict_types=1);

require_once dirname(__DIR__) . '/includes/enquiry-system.php';

if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    header('Allow: GET');
    forsk_enquiry_respond(405, [
        'ok' => false,
        'message' => 'Method not allowed.',
    ]);
}

if (!forsk_enquiry_origin_allowed()) {
    forsk_enquiry_respond(403, [
        'ok' => false,
        'message' => 'This request could not be verified.',
    ]);
}

forsk_enquiry_respond(200, [
    'ok' => true,
    'csrf' => forsk_enquiry_issue_token(),
]);

<?php

declare(strict_types=1);

/**
 * Shared enquiry form security, validation, persistence and notification helpers.
 * Secrets/configuration are read from the server environment only.
 */

function forsk_enquiry_env(string $key, ?string $default = null): ?string
{
    $value = getenv($key);
    if ($value === false || trim((string) $value) === '') {
        return $default;
    }

    return trim((string) $value);
}

function forsk_enquiry_config(): array
{
    static $config;
    if (is_array($config)) {
        return $config;
    }

    $trustedOrigins = array_values(array_filter(array_map(
        'trim',
        explode(',', (string) forsk_enquiry_env('FORSK_ENQUIRY_TRUSTED_ORIGINS', ''))
    )));

    $config = [
        'db_dsn' => forsk_enquiry_env('FORSK_ENQUIRY_DB_DSN'),
        'db_user' => forsk_enquiry_env('FORSK_ENQUIRY_DB_USER'),
        'db_pass' => forsk_enquiry_env('FORSK_ENQUIRY_DB_PASS'),
        'db_table' => forsk_enquiry_env('FORSK_ENQUIRY_DB_TABLE', 'forsk_enquiries'),
        'mail_to' => forsk_enquiry_env('FORSK_ENQUIRY_MAIL_TO'),
        'mail_from' => forsk_enquiry_env('FORSK_ENQUIRY_MAIL_FROM'),
        'trusted_origins' => $trustedOrigins,
        'app_key' => forsk_enquiry_env('FORSK_ENQUIRY_APP_KEY'),
        'log_path' => forsk_enquiry_env('FORSK_ENQUIRY_LOG_PATH'),
        'rate_limit' => max(1, (int) forsk_enquiry_env('FORSK_ENQUIRY_RATE_LIMIT', '5')),
        'rate_window' => max(60, (int) forsk_enquiry_env('FORSK_ENQUIRY_RATE_WINDOW', '900')),
        'minimum_fill_seconds' => max(1, (int) forsk_enquiry_env('FORSK_ENQUIRY_MIN_FILL_SECONDS', '2')),
    ];

    return $config;
}

function forsk_enquiry_start_session(): void
{
    if (session_status() === PHP_SESSION_ACTIVE) {
        return;
    }

    $secure = !empty($_SERVER['HTTPS']) && strtolower((string) $_SERVER['HTTPS']) !== 'off';
    session_name('forsk_enquiry');
    session_set_cookie_params([
        'lifetime' => 0,
        'path' => '/',
        'secure' => $secure,
        'httponly' => true,
        'samesite' => 'Lax',
    ]);
    session_start();
}

function forsk_enquiry_issue_token(): string
{
    forsk_enquiry_start_session();
    $now = time();
    $tokens = isset($_SESSION['forsk_enquiry_tokens']) && is_array($_SESSION['forsk_enquiry_tokens'])
        ? $_SESSION['forsk_enquiry_tokens']
        : [];

    foreach ($tokens as $existingToken => $issuedAt) {
        if (!is_int($issuedAt) || $issuedAt < ($now - 3600)) {
            unset($tokens[$existingToken]);
        }
    }

    $token = bin2hex(random_bytes(32));
    $tokens[$token] = $now;
    $_SESSION['forsk_enquiry_tokens'] = array_slice($tokens, -8, null, true);

    return $token;
}

function forsk_enquiry_verify_csrf(string $token): bool
{
    forsk_enquiry_start_session();
    if ($token === '') {
        return false;
    }

    $tokens = isset($_SESSION['forsk_enquiry_tokens']) && is_array($_SESSION['forsk_enquiry_tokens'])
        ? $_SESSION['forsk_enquiry_tokens']
        : [];
    $startedAt = isset($tokens[$token]) ? (int) $tokens[$token] : 0;
    $minimum = (int) forsk_enquiry_config()['minimum_fill_seconds'];

    if ($startedAt <= 0 || (time() - $startedAt) < $minimum) {
        return false;
    }

    unset($tokens[$token]);
    $_SESSION['forsk_enquiry_tokens'] = $tokens;
    return true;
}

function forsk_enquiry_request_wants_json(): bool
{
    $accept = strtolower((string) ($_SERVER['HTTP_ACCEPT'] ?? ''));
    $requestedWith = strtolower((string) ($_SERVER['HTTP_X_REQUESTED_WITH'] ?? ''));

    return strpos($accept, 'application/json') !== false || $requestedWith === 'xmlhttprequest';
}

function forsk_enquiry_respond(int $status, array $payload): void
{
    http_response_code($status);
    header('Cache-Control: no-store');
    header('X-Content-Type-Options: nosniff');

    if (forsk_enquiry_request_wants_json()) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode($payload, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
        exit;
    }

    header('Content-Type: text/html; charset=utf-8');
    $ok = !empty($payload['ok']);
    $message = htmlspecialchars((string) ($payload['message'] ?? 'Unable to process your request.'), ENT_QUOTES, 'UTF-8');
    $title = $ok ? 'Enquiry received' : 'Enquiry not submitted';
    echo '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'
        . htmlspecialchars($title, ENT_QUOTES, 'UTF-8')
        . '</title></head><body><main><h1>' . htmlspecialchars($title, ENT_QUOTES, 'UTF-8') . '</h1><p>' . $message
        . '</p><p><a href="/">Return to website</a></p></main></body></html>';
    exit;
}

function forsk_enquiry_normalize_text($value, int $maxLength): string
{
    if (!is_scalar($value)) {
        return '';
    }

    $value = str_replace(["\r\n", "\r"], "\n", trim((string) $value));
    $value = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $value) ?? '';
    if (function_exists('mb_substr')) {
        return mb_substr($value, 0, $maxLength, 'UTF-8');
    }

    return substr($value, 0, $maxLength);
}

function forsk_enquiry_value(array $input, array $keys, int $maxLength): string
{
    foreach ($keys as $key) {
        if (array_key_exists($key, $input)) {
            return forsk_enquiry_normalize_text($input[$key], $maxLength);
        }
    }

    return '';
}

function forsk_enquiry_clean_source_page($value): string
{
    $value = forsk_enquiry_normalize_text($value, 255);
    $path = parse_url($value, PHP_URL_PATH);
    if (!is_string($path)) {
        $path = '';
    }
    $path = preg_replace('/[^A-Za-z0-9_\.\/-]/', '', $path) ?? '';

    return substr($path, 0, 255);
}

function forsk_enquiry_validate(array $input): array
{
    $data = [
        'name' => forsk_enquiry_value($input, ['name', 'full_name', 'text-264', 'text-967'], 100),
        'email' => strtolower(forsk_enquiry_value($input, ['email', 'email-628', 'email-191'], 254)),
        'phone' => forsk_enquiry_value($input, ['phone', 'text-265', 'text-968'], 25),
        'company' => forsk_enquiry_value($input, ['company', 'text-969'], 120),
        'message' => forsk_enquiry_value($input, ['message', 'textarea-65', 'textarea-579'], 3000),
        'source_page' => forsk_enquiry_clean_source_page($input['source_page'] ?? ''),
        'source_form' => forsk_enquiry_value($input, ['source_form'], 80),
    ];

    $errors = [];
    $nameLength = function_exists('mb_strlen') ? mb_strlen($data['name'], 'UTF-8') : strlen($data['name']);
    if ($nameLength < 2) {
        $errors['name'] = 'Please enter your full name.';
    }

    if (!filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
        $errors['email'] = 'Please enter a valid email address.';
    }

    $digits = preg_replace('/\D+/', '', $data['phone']) ?? '';
    if (!preg_match('/^[0-9+().\s-]{7,25}$/', $data['phone']) || strlen($digits) < 7 || strlen($digits) > 15) {
        $errors['phone'] = 'Please enter a valid phone number.';
    }

    if ($data['company'] !== '') {
        $companyLength = function_exists('mb_strlen') ? mb_strlen($data['company'], 'UTF-8') : strlen($data['company']);
        if ($companyLength < 2) {
            $errors['company'] = 'Please enter a valid company name or leave it blank.';
        }
    }

    $messageLength = function_exists('mb_strlen') ? mb_strlen($data['message'], 'UTF-8') : strlen($data['message']);
    if ($messageLength < 10) {
        $errors['message'] = 'Please add a little more detail about how we can help.';
    }

    return [$data, $errors];
}

function forsk_enquiry_origin_allowed(): bool
{
    $origin = trim((string) ($_SERVER['HTTP_ORIGIN'] ?? ''));
    if ($origin === '') {
        return true;
    }

    $originParts = parse_url($origin);
    $originHost = strtolower((string) ($originParts['host'] ?? ''));
    $requestHost = strtolower((string) ($_SERVER['HTTP_HOST'] ?? ''));
    $requestHost = preg_replace('/:\d+$/', '', $requestHost) ?? $requestHost;
    if ($originHost !== '' && hash_equals($requestHost, $originHost)) {
        return true;
    }

    foreach (forsk_enquiry_config()['trusted_origins'] as $trustedOrigin) {
        if (hash_equals(rtrim($trustedOrigin, '/'), rtrim($origin, '/'))) {
            return true;
        }
    }

    return false;
}

function forsk_enquiry_ip_hash(): string
{
    $ip = (string) ($_SERVER['REMOTE_ADDR'] ?? 'unknown');
    $key = (string) (forsk_enquiry_config()['app_key'] ?: (php_uname('n') . __DIR__));

    return hash_hmac('sha256', $ip, $key);
}

function forsk_enquiry_rate_limited(): bool
{
    $config = forsk_enquiry_config();
    $hash = forsk_enquiry_ip_hash();
    $path = rtrim(sys_get_temp_dir(), DIRECTORY_SEPARATOR) . DIRECTORY_SEPARATOR . 'forsk-enquiry-rate-' . $hash . '.json';
    $now = time();
    $cutoff = $now - (int) $config['rate_window'];
    $handle = @fopen($path, 'c+');
    if ($handle === false) {
        return false;
    }

    try {
        if (!flock($handle, LOCK_EX)) {
            return false;
        }
        $raw = stream_get_contents($handle);
        $timestamps = json_decode($raw ?: '[]', true);
        if (!is_array($timestamps)) {
            $timestamps = [];
        }
        $timestamps = array_values(array_filter($timestamps, static function ($timestamp) use ($cutoff): bool {
            return is_int($timestamp) && $timestamp >= $cutoff;
        }));
        $limited = count($timestamps) >= (int) $config['rate_limit'];
        if (!$limited) {
            $timestamps[] = $now;
        }
        rewind($handle);
        ftruncate($handle, 0);
        fwrite($handle, json_encode($timestamps));
        fflush($handle);
        flock($handle, LOCK_UN);

        return $limited;
    } finally {
        fclose($handle);
    }
}

function forsk_enquiry_log(string $event, string $requestId, array $context = []): void
{
    $safe = [
        'time' => gmdate('c'),
        'event' => $event,
        'request_id' => $requestId,
        'source_page' => forsk_enquiry_clean_source_page($context['source_page'] ?? ''),
        'ip_hash' => substr(forsk_enquiry_ip_hash(), 0, 16),
    ];
    $line = json_encode($safe, JSON_UNESCAPED_SLASHES) . PHP_EOL;
    $path = forsk_enquiry_config()['log_path'];
    if ($path) {
        @file_put_contents($path, $line, FILE_APPEND | LOCK_EX);
        return;
    }

    error_log(rtrim($line));
}

function forsk_enquiry_store(array $data, string $requestId): array
{
    $config = forsk_enquiry_config();
    if (!$config['db_dsn']) {
        return ['configured' => false, 'success' => false];
    }

    $table = (string) $config['db_table'];
    if (!preg_match('/^[A-Za-z0-9_]+$/', $table)) {
        throw new RuntimeException('Invalid enquiry table configuration.');
    }

    $pdo = new PDO((string) $config['db_dsn'], (string) $config['db_user'], (string) $config['db_pass'], [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES => false,
    ]);
    $sql = 'INSERT INTO ' . $table
        . ' (request_id, full_name, email, phone, company, message, source_page, source_form, created_at) '
        . 'VALUES (:request_id, :full_name, :email, :phone, :company, :message, :source_page, :source_form, :created_at)';
    $statement = $pdo->prepare($sql);
    $statement->execute([
        ':request_id' => $requestId,
        ':full_name' => $data['name'],
        ':email' => $data['email'],
        ':phone' => $data['phone'],
        ':company' => $data['company'] !== '' ? $data['company'] : null,
        ':message' => $data['message'],
        ':source_page' => $data['source_page'] !== '' ? $data['source_page'] : null,
        ':source_form' => $data['source_form'] !== '' ? $data['source_form'] : null,
        ':created_at' => gmdate('Y-m-d H:i:s'),
    ]);

    return ['configured' => true, 'success' => true];
}

function forsk_enquiry_send_mail(array $data, string $requestId): array
{
    $config = forsk_enquiry_config();
    if (!$config['mail_to'] || !$config['mail_from']) {
        return ['configured' => false, 'success' => false];
    }

    $to = str_replace(["\r", "\n"], '', (string) $config['mail_to']);
    $from = str_replace(["\r", "\n"], '', (string) $config['mail_from']);
    if (!filter_var($to, FILTER_VALIDATE_EMAIL) || !filter_var($from, FILTER_VALIDATE_EMAIL)) {
        throw new RuntimeException('Invalid mail configuration.');
    }

    $subject = 'Website enquiry ' . $requestId;
    $body = "A new Forsk Technologies website enquiry was received.\n\n"
        . "Request ID: {$requestId}\n"
        . "Name: {$data['name']}\n"
        . "Email: {$data['email']}\n"
        . "Phone: {$data['phone']}\n"
        . "Company: " . ($data['company'] !== '' ? $data['company'] : 'Not provided') . "\n"
        . "Source page: " . ($data['source_page'] !== '' ? $data['source_page'] : 'Not provided') . "\n\n"
        . "Message:\n{$data['message']}\n";
    $headers = [
        'From: ' . $from,
        'Reply-To: ' . str_replace(["\r", "\n"], '', $data['email']),
        'Content-Type: text/plain; charset=UTF-8',
    ];

    return ['configured' => true, 'success' => mail($to, $subject, $body, implode("\r\n", $headers))];
}

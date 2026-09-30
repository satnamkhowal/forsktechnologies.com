<?php
if (!isset($location) || !is_array($location)) {
    http_response_code(404);
    exit('Location not found');
}

$title = 'Forsk Technologies in ' . $location['name'];
$description = 'Software development, web application, mobile app, cloud and technology consulting services from Forsk Technologies in ' . $location['name'] . ', ' . $location['region'] . '.';
$canonical = 'https://forsktechnologies.com/locations/' . rawurlencode($location['slug']) . '.php';

$schema = [
    '@context' => 'https://schema.org',
    '@type' => 'ProfessionalService',
    'name' => 'Forsk Technologies - ' . $location['name'],
    'url' => $canonical,
    'email' => $location['email'],
    'telephone' => $location['phone'],
    'address' => [
        '@type' => 'PostalAddress',
        'streetAddress' => $location['address'],
        'addressLocality' => $location['name'],
        'addressRegion' => $location['region'],
        'postalCode' => $location['postal_code'],
        'addressCountry' => $location['country'],
    ],
];
?>
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><?= htmlspecialchars($title, ENT_QUOTES, 'UTF-8') ?></title>
    <meta name="description" content="<?= htmlspecialchars($description, ENT_QUOTES, 'UTF-8') ?>">
    <link rel="canonical" href="<?= htmlspecialchars($canonical, ENT_QUOTES, 'UTF-8') ?>">
    <link rel="stylesheet" href="../assets/css/bootstrap.min.css">
    <link rel="stylesheet" href="../assets/css/main.css">
    <script type="application/ld+json"><?= json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) ?></script>
    <style>
        .forsk-location-hero{padding:96px 0 72px;background:#020842;color:#fff}.forsk-location-hero h1{font-size:clamp(38px,6vw,72px);line-height:1.05}.forsk-location-section{padding:72px 0}.forsk-location-card{height:100%;padding:28px;border:1px solid #e8eaf1;border-radius:18px;background:#fff}.forsk-location-meta{padding:28px;border-radius:18px;background:#f6f8ff}.forsk-location-cta{padding:56px 0;background:#f6f8ff}.forsk-location-cta a{display:inline-block;padding:14px 24px;border-radius:999px;background:#0044eb;color:#fff;text-decoration:none;font-weight:700}
    </style>
</head>
<body>
<main>
    <section class="forsk-location-hero">
        <div class="container">
            <p>Forsk Technologies • <?= htmlspecialchars($location['name'], ENT_QUOTES, 'UTF-8') ?></p>
            <h1>Software Development & Technology Services in <?= htmlspecialchars($location['name'], ENT_QUOTES, 'UTF-8') ?></h1>
            <p class="lead mt-4">Build, modernize and support digital products with Forsk Technologies.</p>
        </div>
    </section>

    <section class="forsk-location-section">
        <div class="container">
            <div class="row g-4">
                <div class="col-lg-8">
                    <h2>Technology services for businesses in <?= htmlspecialchars($location['name'], ENT_QUOTES, 'UTF-8') ?></h2>
                    <p>Forsk Technologies works with businesses that need custom software, web applications, mobile applications, cloud solutions, UI/UX support and technology consulting.</p>
                    <div class="row g-4 mt-2">
                        <div class="col-md-6"><div class="forsk-location-card"><h3>Custom Software Development</h3><p>Purpose-built applications and systems aligned to business requirements.</p></div></div>
                        <div class="col-md-6"><div class="forsk-location-card"><h3>Web & Mobile Development</h3><p>Responsive web applications and mobile solutions for customer and internal workflows.</p></div></div>
                        <div class="col-md-6"><div class="forsk-location-card"><h3>Cloud & Modernization</h3><p>Cloud migration, modernization and engineering support for scalable systems.</p></div></div>
                        <div class="col-md-6"><div class="forsk-location-card"><h3>Technology Consulting</h3><p>Architecture, product planning and implementation guidance for digital initiatives.</p></div></div>
                    </div>
                </div>
                <div class="col-lg-4">
                    <aside class="forsk-location-meta">
                        <h2>Office</h2>
                        <p><?= htmlspecialchars($location['address'], ENT_QUOTES, 'UTF-8') ?></p>
                        <p><strong>Phone:</strong> <a href="tel:<?= preg_replace('/\s+/', '', $location['phone']) ?>"><?= htmlspecialchars($location['phone'], ENT_QUOTES, 'UTF-8') ?></a></p>
                        <p><strong>Email:</strong> <a href="mailto:<?= htmlspecialchars($location['email'], ENT_QUOTES, 'UTF-8') ?>"><?= htmlspecialchars($location['email'], ENT_QUOTES, 'UTF-8') ?></a></p>
                    </aside>
                </div>
            </div>
        </div>
    </section>

    <section class="forsk-location-cta">
        <div class="container">
            <h2>Discuss your project with Forsk Technologies</h2>
            <p>Tell us what you want to build, improve or modernize.</p>
            <a href="../contact.html">Send an enquiry</a>
        </div>
    </section>
</main>
<?php
$footerBasePath = '../';
require dirname(__DIR__) . '/includes/footer.php';
?>
</body>
</html>

<?php
$locations = require dirname(__DIR__) . '/config/locations.php';
?><!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Forsk Technologies Locations</title>
    <meta name="description" content="Verified Forsk Technologies office locations and contact details.">
    <link rel="canonical" href="https://forsktechnologies.com/locations/">
    <link rel="stylesheet" href="../assets/css/bootstrap.min.css">
    <link rel="stylesheet" href="../assets/css/main.css">
    <style>.forsk-locations{padding:80px 0}.forsk-location-list{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}.forsk-location-item{padding:28px;border:1px solid #e8eaf1;border-radius:18px;background:#fff}.forsk-location-item a{font-weight:700;text-decoration:none}</style>
</head>
<body>
<main class="forsk-locations">
    <div class="container">
        <p>Forsk Technologies</p>
        <h1>Our Locations</h1>
        <p class="lead">Verified office locations for Forsk Technologies.</p>
        <div class="forsk-location-list mt-5">
            <?php foreach ($locations as $location): ?>
                <?php if (empty($location['verified'])) { continue; } ?>
                <article class="forsk-location-item">
                    <h2><?= htmlspecialchars($location['name'], ENT_QUOTES, 'UTF-8') ?></h2>
                    <p><?= htmlspecialchars($location['address'], ENT_QUOTES, 'UTF-8') ?></p>
                    <a href="<?= htmlspecialchars($location['slug'], ENT_QUOTES, 'UTF-8') ?>.php">View <?= htmlspecialchars($location['name'], ENT_QUOTES, 'UTF-8') ?> office</a>
                </article>
            <?php endforeach; ?>
        </div>
    </div>
</main>
<?php
$footerBasePath = '../';
require dirname(__DIR__) . '/includes/footer.php';
?>
</body>
</html>

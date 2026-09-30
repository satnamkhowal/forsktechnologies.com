<?php
$locations = require dirname(__DIR__) . '/config/locations.php';
$location = $locations['jaipur'] ?? null;
require dirname(__DIR__) . '/includes/location-page.php';

<?php
/**
 * Reusable service-page renderer for Forsk Technologies.
 * Outputs only the service-page body so shared head/header/footer includes remain independent.
 */
declare(strict_types=1);

if (!function_exists('forsk_service_escape')) {
    function forsk_service_escape(mixed $value): string {
        return htmlspecialchars((string) $value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
    }
}

if (!function_exists('forsk_service_items')) {
    function forsk_service_items(array $items): string {
        if ($items === []) return '';
        $html = '<ul class="forsk-service-list unordered_list_block">';
        foreach ($items as $item) {
            if (!is_string($item) || trim($item) === '') continue;
            $html .= '<li><span class="forsk-service-check" aria-hidden="true">✓</span><span>' . forsk_service_escape($item) . '</span></li>';
        }
        return $html . '</ul>';
    }
}

if (!function_exists('forsk_service_cards')) {
    function forsk_service_cards(array $items): string {
        if ($items === []) return '';
        $html = '<div class="row g-4">';
        foreach ($items as $item) {
            if (!is_array($item) || empty($item['title'])) continue;
            $html .= '<div class="col-md-6 col-xl-4"><article class="forsk-service-card h-100"><h3>' . forsk_service_escape($item['title']) . '</h3>';
            if (!empty($item['description'])) $html .= '<p>' . forsk_service_escape($item['description']) . '</p>';
            $html .= '</article></div>';
        }
        return $html . '</div>';
    }
}

if (!function_exists('forsk_service_related')) {
    function forsk_service_related(array $items): string {
        if ($items === []) return '';
        $html = '<div class="row g-4">';
        foreach ($items as $item) {
            if (!is_array($item) || empty($item['title']) || empty($item['url'])) continue;
            $html .= '<div class="col-md-6 col-xl-4"><a class="forsk-service-related-card h-100" href="' . forsk_service_escape($item['url']) . '">';
            $html .= '<span class="forsk-service-related-title">' . forsk_service_escape($item['title']) . '</span>';
            if (!empty($item['description'])) $html .= '<span class="forsk-service-related-copy">' . forsk_service_escape($item['description']) . '</span>';
            $html .= '<span class="forsk-service-related-link">Explore service <span aria-hidden="true">→</span></span></a></div>';
        }
        return $html . '</div>';
    }
}

if (!function_exists('forsk_service_faq')) {
    function forsk_service_faq(array $items, string $id): string {
        if ($items === []) return '';
        $html = '<div class="accordion forsk-service-faq" id="' . forsk_service_escape($id) . '">';
        $index = 0;
        foreach ($items as $item) {
            if (!is_array($item) || empty($item['question']) || empty($item['answer'])) continue;
            $index++;
            $collapseId = $id . '-item-' . $index;
            $headingId = $id . '-heading-' . $index;
            $expanded = $index === 1 ? 'true' : 'false';
            $show = $index === 1 ? ' show' : '';
            $collapsed = $index === 1 ? '' : ' collapsed';
            $html .= '<div class="accordion-item"><h3 class="accordion-header" id="' . forsk_service_escape($headingId) . '">';
            $html .= '<button class="accordion-button' . $collapsed . '" type="button" data-bs-toggle="collapse" data-bs-target="#' . forsk_service_escape($collapseId) . '" aria-expanded="' . $expanded . '" aria-controls="' . forsk_service_escape($collapseId) . '">' . forsk_service_escape($item['question']) . '</button></h3>';
            $html .= '<div id="' . forsk_service_escape($collapseId) . '" class="accordion-collapse collapse' . $show . '" aria-labelledby="' . forsk_service_escape($headingId) . '" data-bs-parent="#' . forsk_service_escape($id) . '"><div class="accordion-body"><p>' . forsk_service_escape($item['answer']) . '</p></div></div></div>';
        }
        return $html . '</div>';
    }
}

if (!function_exists('forsk_service_section_heading')) {
    function forsk_service_section_heading(string $eyebrow, string $title, string $copy = ''): string {
        $html = '<div class="forsk-service-section-heading">';
        if ($eyebrow !== '') $html .= '<span class="forsk-service-eyebrow">' . forsk_service_escape($eyebrow) . '</span>';
        $html .= '<h2>' . forsk_service_escape($title) . '</h2>';
        if ($copy !== '') $html .= '<p>' . forsk_service_escape($copy) . '</p>';
        return $html . '</div>';
    }
}

if (!function_exists('forsk_render_service_page')) {
    function forsk_render_service_page(array $service): void {
        $title = trim((string) ($service['title'] ?? ''));
        $summary = trim((string) ($service['summary'] ?? ''));
        if ($title === '' || $summary === '') throw new InvalidArgumentException('Service pages require verified title and summary values.');

        $pageId = preg_replace('/[^a-z0-9-]+/i', '-', strtolower((string) ($service['slug'] ?? $title))) ?: 'service';
        $contactUrl = (string) ($service['contact_url'] ?? 'contact.html');
        $ctaLabel = (string) ($service['cta_label'] ?? 'Discuss your requirement');

        echo '<main class="forsk-service-page" id="service-' . forsk_service_escape($pageId) . '">';
        echo '<div class="breadcrumb service-banner pos-rel forsk-service-hero"><div class="container"><div class="breadcrumb__content text-center">';
        if (!empty($service['eyebrow'])) echo '<span class="forsk-service-eyebrow">' . forsk_service_escape($service['eyebrow']) . '</span>';
        echo '<h1 class="breadcrumb__title">' . forsk_service_escape($title) . '</h1><p class="forsk-service-hero-copy">' . forsk_service_escape($summary) . '</p>';
        echo '<a class="btn btn-primary forsk-service-primary-cta" href="#enquire"><span class="btn_label">' . forsk_service_escape($ctaLabel) . '</span></a></div></div></div>';

        echo '<section class="forsk-service-section"><div class="container"><div class="row g-5 align-items-start"><div class="col-lg-7">';
        echo forsk_service_section_heading('Service overview', 'What this service is', (string) ($service['overview'] ?? $summary));
        echo '</div>';
        if (!empty($service['audience'])) echo '<div class="col-lg-5"><aside class="forsk-service-callout"><span class="forsk-service-eyebrow">Who needs it</span><h2>Best suited for</h2><p>' . forsk_service_escape($service['audience']) . '</p></aside></div>';
        echo '</div></div></section>';

        if (!empty($service['problem']) || !empty($service['challenges'])) {
            echo '<section class="forsk-service-section forsk-service-section-alt"><div class="container">' . forsk_service_section_heading('Business challenges', 'What problem does it solve?', (string) ($service['problem'] ?? '')) . forsk_service_items((array) ($service['challenges'] ?? [])) . '</div></section>';
        }

        if (!empty($service['capabilities'])) {
            echo '<section class="forsk-service-section"><div class="container">' . forsk_service_section_heading('Solutions & capabilities', 'What Forsk Technologies provides') . forsk_service_cards((array) $service['capabilities']) . '</div></section>';
        }

        if (!empty($service['process'])) {
            echo '<section class="forsk-service-section forsk-service-section-alt"><div class="container">' . forsk_service_section_heading('Process', 'How the work moves forward') . '<ol class="forsk-service-process">';
            $step = 0;
            foreach ((array) $service['process'] as $item) {
                if (!is_array($item) || empty($item['title'])) continue;
                $step++;
                echo '<li><span class="forsk-service-process-number">' . str_pad((string) $step, 2, '0', STR_PAD_LEFT) . '</span><div><h3>' . forsk_service_escape($item['title']) . '</h3>';
                if (!empty($item['description'])) echo '<p>' . forsk_service_escape($item['description']) . '</p>';
                echo '</div></li>';
            }
            echo '</ol></div></section>';
        }

        if (!empty($service['technologies'])) {
            echo '<section class="forsk-service-section"><div class="container">' . forsk_service_section_heading('Technology stack', 'Relevant technologies & capabilities', 'Only technologies verified for this service should be listed here.') . '<div class="forsk-service-tags">';
            foreach ((array) $service['technologies'] as $technology) {
                if (is_string($technology) && trim($technology) !== '') echo '<span>' . forsk_service_escape($technology) . '</span>';
            }
            echo '</div></div></section>';
        }

        if (!empty($service['benefits'])) echo '<section class="forsk-service-section forsk-service-section-alt"><div class="container">' . forsk_service_section_heading('Benefits', 'Business value this service is designed to support') . forsk_service_items((array) $service['benefits']) . '</div></section>';
        if (!empty($service['related_services'])) echo '<section class="forsk-service-section"><div class="container">' . forsk_service_section_heading('Related services', 'Explore connected capabilities') . forsk_service_related((array) $service['related_services']) . '</div></section>';
        if (!empty($service['faq'])) echo '<section class="forsk-service-section forsk-service-section-alt"><div class="container">' . forsk_service_section_heading('FAQ', 'Questions before you enquire') . forsk_service_faq((array) $service['faq'], 'service-faq-' . $pageId) . '</div></section>';

        echo '<section class="forsk-service-section forsk-service-enquiry" id="enquire"><div class="container"><div class="forsk-service-enquiry-shell"><div>';
        echo forsk_service_section_heading('Start a conversation', (string) ($service['cta_title'] ?? 'Tell us what you need'), (string) ($service['cta_copy'] ?? 'Share your requirement and the team can review the next practical step.'));
        echo '</div><div class="forsk-service-enquiry-action">';
        if (!empty($service['enquiry_form_renderer']) && is_callable($service['enquiry_form_renderer'])) {
            call_user_func($service['enquiry_form_renderer'], $service);
        } else {
            echo '<a class="btn btn-primary" href="' . forsk_service_escape($contactUrl) . '"><span class="btn_label">' . forsk_service_escape($ctaLabel) . '</span></a>';
            echo '<p class="forsk-service-form-note">A form is shown here only when a verified enquiry handler/include is connected.</p>';
        }
        echo '</div></div></div></section></main>';
    }
}

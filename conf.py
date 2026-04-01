project = 'Qorix Developer Doc-as-Code'
author = 'Qorix Developer Team'

extensions = [
    'sphinx_needs',
    'sphinxcontrib.mermaid',
]

master_doc = 'index'
source_suffix = '.rst'
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    '50-testing/**',
    '60-decisions/**',
    '70-ops/**',
    '80-product_direction/**',
    '98-requirements/**',
    '00-overview/glossary.rst',
    '30-swe.2/example-architecture.rst',
]

needs_types = [
    dict(directive='req', title='Requirement', prefix='REQ_', color='#BFD8D2', style='node'),
    dict(directive='spec', title='Specification', prefix='SPEC_', color='#FEDCD2', style='node'),
]

needs_extra_options = [
    'priority',
    'rationale',
    'verification',
    'jira',
    'domain',
    'cluster',
]

needs_extra_links = [
    {
        'option': 'parent',
        'incoming': 'children',
        'outgoing': 'parent',
        'copy': False,
        'color': '#4A7EBB',
    },
    {
        'option': 'implements',
        'incoming': 'implemented_by',
        'outgoing': 'implements',
        'copy': False,
        'color': '#1B9E77',
    },
]

needs_id_regex = r'^[A-Z0-9-]+$'

html_theme = 'pydata_sphinx_theme'
html_theme_options = {
    'logo': {
        'text': 'Qorix Docs',
    },
    'navbar_start': ['navbar-logo'],
    'navbar_center': ['navbar-nav'],
    'navbar_end': ['theme-switcher', 'navbar-icon-links'],
    'header_links_before_dropdown': 6,
    'navigation_with_keys': True,
    'show_prev_next': True,
    'secondary_sidebar_items': ['page-toc'],
    'icon_links': [
        {
            'name': 'GitHub',
            'url': 'https://github.com/eclipse-score/score',
            'icon': 'fa-brands fa-github',
        },
    ],
}

html_context = {
    'default_mode': 'light',
}

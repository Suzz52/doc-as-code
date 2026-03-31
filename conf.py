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
    '40-swe.3/**',
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

html_theme = 'panda3d'
html_theme_path = ['_themes']

"""
mailbomb/
├── mailbomb/                 # Main application
│   ├── core/                 # Core functionality
│   │   ├── config.py         # Configuration management
│   │   ├── exceptions.py     # Custom exceptions
│   │   └── logging.py        # Logging setup
│   ├── models/               # Data models
│   │   ├── contact.py
│   │   ├── campaign.py
│   │   └── template.py
│   ├── services/             # Business logic
│   │   ├── email.py
│   │   ├── campaign.py
│   │   └── analytics.py
│   ├── repos/         # Data access
│   │   ├── contact.py
│   │   └── campaign.py
│   └── api/                  # External interfaces
│       ├── rest/
│       └── cli/
├── tests/                    # Comprehensive tests
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── scripts/                  # Utility scripts
├── pyproject.toml            # Python virtual env info
├── README.md
└── LICENCE
"""

# Contributing to NuclearShield

Thank you for your interest in contributing to NuclearShield.

NuclearShield is a defensive, read-only cybersecurity assurance project. Contributions should preserve its safety boundaries, evidence-driven design, and focus on explainable defensive analysis.

## Contribution Principles

Contributions should:

- Preserve the defensive and read-only architecture
- Use synthetic or fictional demonstration data
- Maintain clear evidence provenance
- Prefer explainable detection and analysis
- Preserve human authority as the final decision boundary
- Include tests for meaningful functional changes
- Keep documentation aligned with implemented behavior
- Avoid unnecessary dependencies and complexity

## Safety Boundary

Do not contribute:

- Plant-control or command functionality
- Exploit or offensive attack functionality
- Real nuclear facility information
- Real SCADA or I&C credentials
- Sensitive plant topology
- Real safety-system configuration
- Nuclear material-accounting information
- Real physical-access records
- Production industrial telemetry
- Features designed to interfere with operational systems

NuclearShield must not be connected to operational nuclear facilities, SCADA or I&C networks, safety systems, physical-access systems, nuclear material-accounting systems, or production industrial environments.

## Development Setup

Clone the repository:

    git clone https://github.com/ruveeha33/NuclearShield.git
    cd NuclearShield

Create a Python 3.12 virtual environment and install the development dependencies:

    py -3.12 -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install -e ".[dev]"

## Quality Checks

Before submitting a contribution, run:

    pytest -q
    ruff check app tests
    bandit -q -r app -x app/static

All existing tests should pass.

## Docker Validation

For changes affecting deployment or monitoring, validate the Docker Compose configuration:

    docker compose config

Then start the platform when runtime verification is required:

    docker compose up --build -d

Check the running services:

    docker compose ps

Stop the environment when finished:

    docker compose down

## Pull Requests

Keep pull requests focused on one clear change.

A pull request should explain:

- What was changed
- Why the change is needed
- How the change was tested
- Whether documentation was updated
- Whether the change affects the NuclearShield safety boundary

Do not include unrelated formatting or refactoring changes in the same pull request unless necessary.

## Reporting Security Issues

Do not publish sensitive vulnerability details in a public issue.

Follow the repository SECURITY.md guidance when reporting security concerns.

Never include operational nuclear, industrial-control, facility, credential, personnel, or material information in a report.

## License

By contributing to NuclearShield, you agree that your contributions will be distributed under the repository's MIT License.

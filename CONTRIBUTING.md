# Contributing to Voice Bot

Thank you for your interest in contributing to the Voice Bot project!

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make your changes
5. Push to your fork
6. Submit a pull request

## Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/voice-bot.git
cd voice-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dev dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8

# Run tests
pytest tests/

# Format code
black .

# Lint code
flake8 .
```

## Code Style

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Comment complex logic
- Use type hints where possible

## Testing

All pull requests must include tests:

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=.

# Run specific test
pytest tests/test_openai_client.py
```

## Commit Messages

- Use clear, descriptive messages
- Start with a verb (Add, Fix, Update, etc.)
- Keep first line under 50 characters
- Reference issues when applicable

Example:
```
Add speech-to-text processing module

Implemented OpenAI Whisper integration for converting
audio to text. Supports multiple languages and formats.

Fixes #42
```

## Pull Request Process

1. Update documentation
2. Add tests for new features
3. Ensure all tests pass
4. Provide clear description
5. Link related issues
6. Request review from maintainers

## Reporting Issues

When reporting bugs, include:
- Description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details
- Error logs/screenshots

## Feature Requests

Suggest features by creating an issue with:
- Feature description
- Use case/benefit
- Possible implementation approach
- Examples if applicable

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🎉

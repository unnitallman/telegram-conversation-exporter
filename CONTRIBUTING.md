# Contributing to Telegram Conversation Exporter

Thank you for your interest in contributing to the Telegram Conversation Exporter! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear description of the problem
- Steps to reproduce the issue
- Your system information (OS, Python version)
- Any error messages or logs

### Suggesting Features

Feature suggestions are welcome! Please create an issue with:
- A clear description of the feature
- The use case or problem it solves
- Any implementation ideas (optional)

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test your changes**: Ensure all existing tests pass and add tests for new features
5. **Follow code style**: Use consistent formatting and follow Python best practices
6. **Commit your changes**: Use clear, descriptive commit messages
7. **Push to your fork**: `git push origin feature/your-feature-name`
8. **Create a Pull Request**

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/unnitallman/telegram-conversation-exporter.git
   cd telegram-conversation-exporter
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your test environment (optional):
   ```bash
   python setup.py
   ```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Handle errors gracefully

## Testing

Before submitting a PR:
- Test your changes with different conversation types
- Ensure error handling works correctly
- Test with both small and large conversations
- Verify all media types are handled properly

## Questions?

Feel free to open an issue for any questions about contributing!
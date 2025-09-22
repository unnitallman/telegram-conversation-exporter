# Security Policy

## Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

1. **Do NOT** create a public issue
2. Send an email to the repository owner with details of the vulnerability
3. Include steps to reproduce the issue
4. Allow reasonable time for the issue to be resolved before public disclosure

## Security Considerations

### API Credentials
- Never commit your `.env` file or API credentials to version control
- Store API credentials securely using environment variables
- Regenerate API credentials if they are accidentally exposed

### Session Files
- Session files (`.session`) contain authentication tokens
- Keep session files secure and do not share them
- Session files are automatically ignored by `.gitignore`

### Data Protection
- Exported conversations contain personal data
- Store exported data securely
- Be mindful of privacy laws and regulations in your jurisdiction
- Consider encrypting exported data for additional security

### Network Security
- The tool connects to Telegram's servers using encrypted connections
- No data is sent to third-party services
- All operations are performed locally on your machine

## Best Practices

1. **Environment Setup**:
   - Use a virtual environment
   - Keep dependencies up to date
   - Review dependency security advisories

2. **Usage**:
   - Only export conversations you have permission to export
   - Respect privacy rights and local laws
   - Regularly review and clean up old exports

3. **System Security**:
   - Keep your operating system and Python installation updated
   - Use antivirus software
   - Enable firewall protection

## Responsible Disclosure

We appreciate responsible disclosure of security vulnerabilities. We will:
- Acknowledge receipt of your report within 48 hours
- Provide regular updates on our progress
- Credit you in the security advisory (unless you prefer to remain anonymous)
- Work with you to ensure the vulnerability is properly addressed
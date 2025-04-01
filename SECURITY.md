# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.2.x   | :white_check_mark: |
| 1.1.x   | :white_check_mark: |
| 1.0.x   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please follow these steps to report it:

1. **Do not disclose the vulnerability publicly** until it has been addressed by the maintainers.
2. Send an email to security@example.com with a detailed description of the vulnerability, including:
   - The steps to reproduce the issue
   - The potential impact of the vulnerability
   - Any potential solutions or workarounds you're aware of

## Security Best Practices

When using this UML-MCP server in your environment, please follow these security best practices:

### Network Security
- Always run the service behind a secure proxy if exposing it to the internet
- Consider using HTTPS for any exposed endpoints
- Limit access to the server using IP restrictions or VPN when possible

### API Security
- Do not expose the MCP server directly to untrusted networks
- Use API keys or other authentication mechanisms when integrating with other services
- Validate all input coming from external sources

### Server Environment
- Keep all dependencies up to date
- Run the service with minimal required permissions
- Use containerization to isolate the service from other applications

## Dependency Vulnerabilities

We use automated tools to scan for vulnerabilities in our dependencies and update them regularly. Users are encouraged to:

1. Regularly update to the latest version of this project
2. Report any known vulnerabilities in dependencies
3. Submit pull requests to update outdated or vulnerable dependencies

## Responsible Disclosure

We are committed to addressing security issues promptly. We will:

1. Acknowledge receipt of your vulnerability report within 48 hours
2. Provide a timeline for fixing the issue within 5 business days
3. Notify you when the vulnerability has been fixed
4. Acknowledge your contribution (unless you prefer to remain anonymous)

Thank you for helping keep this project secure!

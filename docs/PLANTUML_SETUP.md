# PlantUML Local Setup Guide

This guide helps you set up local PlantUML diagram generation using the bundled plantuml.jar file.

## Why Use Local PlantUML?

- **Offline diagrams**: Generate diagrams without internet connection
- **Better performance**: No network latency
- **Privacy**: Diagram code never leaves your machine
- **Reliability**: No dependency on external services

## Requirements

### Java Runtime Environment (JRE) 11 or higher

PlantUML requires Java to run. The extension will automatically detect Java installation.

## Installation Steps

### 1. Install Java

Choose one of the following options:

#### Option A: Eclipse Adoptium (Recommended)
- **Windows/macOS/Linux**: https://adoptium.net/
- Download and install the latest LTS version (Java 21 or Java 17)
- Follow the installer instructions

#### Option B: Oracle JDK
- https://www.oracle.com/java/technologies/downloads/
- Download and install Java SE Development Kit

#### Option C: Package Manager

**Windows (winget)**:
```powershell
winget install EclipseAdoptium.Temurin.21.JDK
```

**macOS (Homebrew)**:
```bash
brew install openjdk@21
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install openjdk-21-jdk
```

**Linux (Fedora/RHEL)**:
```bash
sudo dnf install java-21-openjdk
```

### 2. Verify Java Installation

Open a terminal/command prompt and run:

```bash
java -version
```

You should see output like:
```
openjdk version "21.0.1" 2023-10-17
OpenJDK Runtime Environment (build 21.0.1+12-29)
```

### 3. Configure Extension

The extension bundles plantuml.jar automatically in `extension/bin/plantuml.jar`.

In Claude Desktop extension settings:
1. Enable **"Use Local PlantUML JAR"** option
2. (Optional) Set custom **"Java Executable Path"** if auto-detection fails
3. (Optional) Set custom **"PlantUML JAR Path"** if using a different version

## Troubleshooting

### Java Not Found

**Error**: `Java Runtime Environment not found`

**Solutions**:
1. Ensure Java is installed (see step 1 above)
2. Verify `java -version` works in terminal
3. Set JAVA_HOME environment variable:

   **Windows**:
   ```powershell
   setx JAVA_HOME "C:\Program Files\Eclipse Adoptium\jdk-21.0.1.12-hotspot"
   ```

   **macOS/Linux (add to ~/.bashrc or ~/.zshrc)**:
   ```bash
   export JAVA_HOME=/Library/Java/JavaVirtualMachines/temurin-21.jdk/Contents/Home
   ```

4. Manually specify Java path in extension settings

### PlantUML.jar Not Found

**Error**: `plantuml.jar not found`

**Solutions**:
1. The extension should bundle plantuml.jar in `extension/bin/plantuml.jar`
2. Download manually from: https://github.com/plantuml/plantuml/releases/latest
3. Place it in one of these locations:
   - `<extension-dir>/bin/plantuml.jar`
   - `~/.plantuml/plantuml.jar`
   - Custom path (set in extension settings)

### Diagram Generation Fails

**Error**: `PlantUML generation failed: [error details]`

**Solutions**:
1. Check diagram syntax is valid PlantUML
2. Check Java has execute permissions on plantuml.jar
3. View logs at `logs/uml_mcp_server_YYYY-MM-DD.log`
4. Try disabling local PlantUML to use Kroki service as fallback

### Performance Issues

If diagram generation is slow:
1. Ensure you're using Java 11 or higher (Java 21 recommended)
2. For large diagrams, increase Java heap size:
   ```bash
   java -Xmx2048m -jar plantuml.jar [...]
   ```
   Note: This requires modifying the PlantUML client code

## Comparison: Local vs Server

| Feature | Local PlantUML | Kroki Service |
|---------|---------------|---------------|
| Internet required | No | Yes |
| Setup complexity | Medium (Java required) | Low (no setup) |
| Performance | Fast (local) | Depends on network |
| Privacy | High (offline) | Medium (sends code to server) |
| Supported formats | PNG, SVG, TXT, PDF, EPS | PNG, SVG, TXT, PDF |
| Diagram types | PlantUML only | 20+ types (PlantUML, Mermaid, D2, etc.) |

## Supported PlantUML Formats

When using local PlantUML, the following output formats are supported:
- **svg** - Scalable Vector Graphics (recommended)
- **png** - Portable Network Graphics
- **txt** - Text-based diagram
- **pdf** - Portable Document Format
- **eps** - Encapsulated PostScript

## Testing Your Setup

1. Enable "Use Local PlantUML JAR" in extension settings
2. Ask Claude to generate a simple diagram:
   ```
   Create a class diagram for a simple User class with name and email properties
   ```
3. Check the response for:
   - "Using local PlantUML client for diagram generation"
   - File path to generated diagram
   - "generated_by": "local_plantuml"

## Version Information

- **Extension PlantUML JAR**: v1.2025.8
- **Minimum Java Version**: 11
- **Recommended Java Version**: 21 (LTS)

## Further Help

If you encounter issues:
1. Check logs in `logs/uml_mcp_server_YYYY-MM-DD.log`
2. Report issues at: https://github.com/ChistokhinSV/uml-mcp/issues
3. Include Java version (`java -version`) and error messages

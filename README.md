# 🤗 Hugging Face Hub Utilities

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

*A comprehensive toolkit for managing your Hugging Face Hub resources*

</div>

---

## 🌟 Features

- 🔄 Organization Management
  - Move repositories between organizations
  - Batch operations support
  - Exception handling for specific repos
- 🔒 Privacy Controls
  - Automatic repository privacy management
  - Secure token handling
- 📊 Detailed Reporting
  - Operation summaries
  - Success rate tracking
  - Debug logging support

## 📦 Installation

```bash
# From source
git clone https://github.com/sumukshashidhar/hf-hub-utils.git
cd hf-hub-utils
pip install .

# Using pip (coming soon)
pip install hf-hub-utils
```

## 🛠️ Available Tools

### Organization Mover

Move datasets and models between Hugging Face organizations with ease.

```bash
# Basic usage
hf-hub-utils org-mover --source source-org --target target-org

# With custom token
hf-hub-utils org-mover --source source-org --target target-org --token your-token

# Exclude specific repositories
hf-hub-utils org-mover --source source-org --target target-org --exceptions exceptions.txt

# Enable detailed logging
hf-hub-utils org-mover --source source-org --target target-org --debug
```

#### Excluding Repositories

Create an `exceptions.txt` file to specify repositories to skip:

```bash
# exceptions.txt
# One repository name per line (without organization prefix)
my-dataset-1
my-model-2
```

#### Features

- ✨ Automatic repository privacy management
- 🔄 Smart conflict resolution with timestamps
- 📝 Detailed logging with progress tracking
- ⚡ Efficient batch operations
- 🎯 Selective migration with exceptions

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Used By |
|----------|-------------|----------|----------|
| `HF_TOKEN` | Hugging Face API token | No (can use --token) | org-mover |

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 💻 Make your changes
4. ✅ Run tests and linting
5. 📝 Update documentation if needed
6. 🔄 Push your changes (`git push origin feature/amazing-feature`)
7. 🎯 Open a Pull Request

### Development Setup

```bash
# Clone the repository
git clone https://github.com/sumukshashidhar/hf-hub-utils.git
cd hf-hub-utils

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Project Structure

```
hf_hub_utils/
├── common/           # Shared utilities
│   ├── logging.py   # Logging configuration
│   └── ...
├── org_mover/       # Organization mover tool
│   ├── cli.py       # Command-line interface
│   ├── mover.py     # Core functionality
│   └── ...
└── cli.py           # Main CLI entry point
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co/) for their amazing platform and APIs
- All our contributors and users

---

<div align="center">
Made with ❤️ by the community
</div>
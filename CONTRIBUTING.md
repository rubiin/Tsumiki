# Contributing to Tsumiki

Thank you for your interest in contributing to Tsumiki ! We welcome contributions and are excited to work together to make this project better. To ensure a smooth collaboration, please follow the guidelines below.

## Table of Contents

- [Contributing to \[Project Name\]](#contributing-to-tsumiki)
  - [Table of Contents](#table-of-contents)
  - [Code of Conduct](#code-of-conduct)
  - [How to Contribute](#how-to-contribute)
    - [Reporting Bugs](#reporting-bugs)
    - [Suggesting Enhancements](#suggesting-enhancements)
    - [Submitting Code Changes](#submitting-code-changes)
    - [Commit Message Guidelines](#commit-message-guidelines)
    - [Pull Request Process](#pull-request-process)
    - [Creating a new widget](#creating-a-new-widget)
  - [Getting Started](#getting-started)
  - [License](#license)

## Code of Conduct

Please note that we have a [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.

## How to Contribute

We welcome various forms of contribution including bug reports, feature requests, and code contributions. Here’s how you can help:

### Reporting Bugs

If you find a bug, please open an issue in the repository with the following information:

- A clear description of the issue.
- Steps to reproduce the issue (if applicable).
- The expected behavior.
- Any relevant logs or error messages.

### Suggesting Enhancements

If you have an idea for a new feature or enhancement, please open an issue with the following:

- A clear description of the feature.
- Why it’s useful.
- Any possible implementation details.

### Submitting Code Changes

If you want to contribute code, follow these steps:

1. Fork the repository.
2. Create a new branch for your changes.
3. Make your changes and add tests if applicable.
4. Ensure all tests pass.
5. Commit your changes with a descriptive commit message.
6. Push to your fork and create a pull request.

### Commit Message Guidelines

We follow a simple and consistent commit message format:
<type>(<scope>): <short description>

Longer description (if needed)

Closes: #issue-number

Types can include:

- **feat**: a new feature
- **fix**: a bug fix
- **docs**: documentation changes
- **style**: code style changes (e.g., formatting)
- **refactor**: code changes that neither fix a bug nor add a feature
- **test**: adding or modifying tests
- **chore**: general maintenance (e.g., upgrading dependencies)

### Pull Request Process

When creating a pull request:

- Ensure your branch is up-to-date with the main branch before submitting.
- Provide a clear description of what your pull request does.
- Add screenshots or examples if your changes include UI modifications.
- Link to any relevant issues or discussions.
- Follow the coding standards of the project.

### Creating a new widget

When creating a new widget:

- Create a new file under `widgets/` directory, and implement your widget class
- The widget class name should have `Widget` suffix for consistency. Ex. `CustomButtonWidget`, `WeatherWidget`
- Add your widget to the imports and `widgets_list` dictionary in `modules/bar.py`
- Add the widget name to the enum list in `tsumiki.schema.json` for validation
- Add default configuration in `utils/constants.py` under `DEFAULT_CONFIG["widgets"]`
- Also add the schema definitions in `tsumiki.schema.json` for autocompletions
- Update example configuration in `example/config.json` to demonstrate usage
- Add widget documentation to the README.md widgets table
- Run `python doc_gen.py` to generate the documentation for the widgets

## Getting Started

To start contributing, you can clone the repository and set up your local development environment:

1. Clone the repo:
2. Install dependencies with pip

## License

By contributing, you agree that your contributions will be licensed under the project’s license.

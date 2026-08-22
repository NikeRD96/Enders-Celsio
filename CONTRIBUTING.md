# Contributing to Enders Celsio Integration

Thank you for considering contributing to the Enders Celsio Home Assistant custom integration!

## How to Contribute

1. **Report Bugs**: Use the [Bug Report](https://github.com/NikeRD96/Enders-Celsio/issues/new?template=bug_report.yml) template. Include your Home Assistant version and raw BLE advertisement bytes if possible.
2. **Suggest Enhancements**: Use the [Feature Request](https://github.com/NikeRD96/Enders-Celsio/issues/new?template=feature_request.yml) template.
3. **Submit Pull Requests**:
   - Fork the repository.
   - Create a feature branch: `git checkout -b feature/my-feature`.
   - Make your changes and write unit tests for any new parser logic or feature.
   - Run tests locally:
     ```bash
     python -m unittest discover -s tests
     ```
   - Commit your changes with clear messages.
   - Push to your branch and submit a Pull Request.

## Code Standards

- Follow Home Assistant development guidelines and PEP 8 style standards.
- Ensure all tests pass.
- Validate `manifest.json` and translation files.

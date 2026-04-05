# Contributing to HackingGPT

Thank you for wanting to contribute to HackingGPT! Your collaboration is essential to improving and expanding this project. Below are the guidelines and workflow for submitting your contributions.

## How can I contribute?

You can help in several ways:

- **Report issues:**
  Found a bug, unexpected behavior, or have a suggestion for improvement? Open an _issue_ in this repository. Please describe the problem in detail, including steps to reproduce it (if applicable).

- **Submit pull requests:**
  Fix a bug, add a feature, or improve the documentation. To do so, follow the workflow below to ensure your contribution integrates well into the project.

- **Test and suggest improvements:**
  Test new features and suggest improvements or optimizations based on your usage experience.

## Pull request workflow

1. **Fork the repository:**
   Click the "Fork" button on the HackingGPT repository to create a copy of the project in your account.

2. **Clone your fork locally:**
   In the terminal, run:
   ```bash
   git clone https://github.com/your-username/HackingGPT.git
   ```

Replace `your-username` with your GitHub username.

3. **Create a branch for your contribution:**
    Choose a descriptive name for your branch:

    ```bash
    git checkout -b feature/your-change-name
    ```

4. **Make your changes:**
    Apply the necessary modifications to the code or documentation.

5. **Testing:**
    Make sure your changes do not break existing functionality. Run the script and validate the behavior.

6. **Commit your changes:**
    Write clear and descriptive commit messages using the imperative mood. For example:

    ```bash
    git commit -m "Add support for DeepSeek API"
    ```

7. **Push your branch to your fork:**

    ```bash
    git push origin feature/your-change-name
    ```

8. **Open a pull request:**
    On GitHub, go to the HackingGPT repository and click "New Pull Request". Select your branch and submit the pull request with a detailed description of the changes and the reasons for them.

## Code and style guidelines

- **Clarity and consistency:**
    Keep the code style clear and consistent. Follow the naming conventions and formatting already used in the project.

- **Commit messages:**
    Write concise and descriptive commit messages using the imperative mood (e.g., "Add", "Remove", "Fix").

- **Documentation:**
    Keep the code well-commented and update the documentation whenever you modify or add features.

- **API key security:**
    Make sure any API keys used in the code are loaded via environment variables and that no key is exposed in the code or in the commit history.

## Code of Conduct

This project adopts a [Code of Conduct](CODE_OF_CONDUCT.md) to ensure a collaborative, respectful, and inclusive environment. All contributors are expected to maintain professional behavior and respect all other community members. Conduct issues will be taken seriously.

## Questions

If you have questions about how to contribute or about the project, open an _issue_ in the repository so we can help.

## Thank you

We appreciate your contribution and interest in being part of the development of HackingGPT!

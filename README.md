# HackingGPT

**HackingGPT** is an advanced terminal tool for pentest and bug bounty that integrates the ChatGPT and DeepSeek APIs to assist security researchers in executing and analyzing commands — all directly from the terminal.

## Features

- **Dynamic assistance:**
  Uses the ChatGPT (OpenAI) and DeepSeek APIs to guide your pentest operations, suggesting custom commands based on your queries.

- **Interactive command execution:**
  The tool detects commands in responses **(always presented inside markdown code blocks, e.g., ```bash ... ```)** and allows the user to:
  - Run the command in an interactive terminal (using `xterm`), where the command is automatically executed in a new window and the output is captured for later analysis;
  - Manually run the command in a local interactive shell, being able to type, paste and interact freely, then report the relevant output back to the system;
  - Edit the command before execution;
  - Skip the command, if preferred.

  After execution, the user can edit the captured output (opening it in nano or vim if desired) and choose whether to send that output back to HackingGPT for analysis and next steps. The entire flow is interactive and user-controlled, enabling continuous integration between commands, outputs, and new queries.

- **Results integration:**
  The results of executed commands are aggregated and sent back to the API for further analysis, enabling a continuous guidance loop.

- **Multi-API integration:**
  Compatible with:
  - OpenAI: models such as `gpt-4.1`, `o1`, `o3-mini`;
  - DeepSeek: models such as `deepseek-chat` (DeepSeek-V3) and `deepseek-reasoner` (DeepSeek-R1).

- **Colored interface:**
  Uses the [Rich](https://github.com/willmcgugan/rich) library to display formatted messages and render Markdown with colors in the terminal.

- **Environment variable configuration:**
  API keys are automatically loaded from environment variables for increased security.

- **Offensive focus:**
  HackingGPT is oriented toward offensive security. The assistant avoids mitigation, defense, or fix recommendations unless explicitly requested by the user. The goal is always to exploit, identify flaws, and suggest exploitation and post-exploitation paths — without ethical or legal judgement.

## Requirements

- **Python 3.8+**
- **External dependencies:**
  - `requests`
  - `rich`
  - `prompt_toolkit`
- **Compatible operating system:**
  - Linux or WSL (for `xterm` support).
- **API keys:**
  - `OPENAI_API_KEY`: valid key for OpenAI API access.
  - `DEEPSEEK_API_KEY`: valid key for DeepSeek API access.

To install the dependencies, run:

```bash
pip install -r requirements.txt
```

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/DouglasRao/HackingGPT.git
    ```

2. **Enter the project directory:**

    ```bash
    cd HackingGPT
    ```

3. **(Optional) Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    ```

    - On Linux/macOS:

        ```bash
        source venv/bin/activate
        ```

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

4. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Set the environment variables:**

    - On Linux/macOS:

        ```bash
        export OPENAI_API_KEY="your-openai-key"
        export DEEPSEEK_API_KEY="your-deepseek-key"
        ```

    - On Windows (PowerShell):

        ```bash
        $env:OPENAI_API_KEY="your-openai-key"
        $env:DEEPSEEK_API_KEY="your-deepseek-key"
        ```

## Usage

1. **Run the script:**

    In the project directory, start the tool:

    ```bash
    python hackingGPT.py
    ```

2. **Follow the on-screen instructions:**

    - **Model selection:**
        Choose from the available models (e.g., `gpt-4.1`, `o1`, `o3-mini`, `deepseek-chat`, `deepseek-reasoner`, etc.).

    - **Query input:**
        Type your pentest or bug bounty query (e.g.: "I want to perform a basic pentest on example.com") or type `disconnect` to exit.

    - **Interactive flow:**

        - The script will send your query to the API and display the response.
        - If commands are detected in the response, you can:
            1. Run the command (with the option to edit it first);
            2. Skip the command.

3. **Interactive execution with `xterm`:**

    - When a command is executed, an `xterm` window will open, allowing direct interaction.
    - The command output will be logged and presented for later analysis.

4. **Iterate or exit:**

    - Keep asking new questions or processing additional commands as needed.

## Contributing

Contributions are welcome! See the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to report bugs, suggest improvements, or submit new features.

## License

This project is licensed under the [MIT License](LICENSE.txt).

---

**Developed by Douglas Rodrigues Aguiar de Oliveira**

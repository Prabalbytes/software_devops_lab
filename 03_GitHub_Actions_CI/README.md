# Experiment 3 — GitHub Actions CI Pipeline

## Aim
To design and implement a Continuous Integration (CI) pipeline using GitHub Actions that automatically performs Python code linting and testing whenever code is pushed to the `main` branch or a pull request is created.

## Objectives
- Understand GitHub Actions and workflow automation.
- Configure a YAML-based CI workflow.
- Automate Python code linting using Flake8.
- Execute automated tests using Pytest.
- Verify that the pipeline detects coding errors and test failures.

## Tools and Technologies
- **GitHub Actions** — CI workflow automation.
- **Python 3.11** — Programming language.
- **Flake8** — Python code linting.
- **Pytest** — Automated testing framework.
- **YAML** — Workflow configuration format.

## Project Structure

```text
devops_lab/
│
├── .github/
│   └── workflows/
│       └── python-ci.yml
│
├── 02_GitHub_CLI_and_VSCode/
│   ├── index.py
│   ├── requirements.txt
│   ├── test_index.py
│   └── test
│
└── 03_GitHub_Actions_CI/
    └── README.md
```

**Note:** The workflow is stored in `.github/workflows/` at the repository root because GitHub Actions requires this location. The workflow executes Python linting and testing inside the `02_GitHub_CLI_and_VSCode/` directory.

## Workflow Configuration

The workflow is defined in:

`.github/workflows/python-ci.yml`

It contains the following stages:

1. **Trigger:** Starts automatically on pushes and pull requests targeting `main`.
2. **Checkout:** Uses `actions/checkout@v4` to access repository files.
3. **Python Setup:** Configures Python 3.11 using `actions/setup-python@v5`.
4. **Dependency Installation:** Installs Flake8 and Pytest from `requirements.txt`.
5. **Linting:** Runs Flake8 to identify Python coding-style errors.
6. **Testing:** Runs Pytest to execute automated test cases.

## Execution Procedure

1. Create the workflow file inside `.github/workflows/`.
2. Configure the workflow using YAML syntax.
3. Add Python dependencies to `requirements.txt`.
4. Set the working directory to `02_GitHub_CLI_and_VSCode`.
5. Commit and push the changes to GitHub.
6. Open the repository's **Actions** tab.
7. Verify the workflow execution and inspect the job results.

## Testing and Verification

The pipeline performs two major checks:

- **Linting:** Flake8 checks the Python source files for coding-style violations.
- **Testing:** Pytest executes the available test cases and reports their results.

The pipeline can also be tested with intentionally incorrect Python code. Such code should cause the linting or testing stage to fail. After correcting the code, the workflow should execute successfully again.

## Expected Result

A YAML-based Continuous Integration pipeline was configured using GitHub Actions. It automatically installs dependencies, checks Python code quality using Flake8, and executes test cases using Pytest on pushes and pull requests targeting the `main` branch.

The successful execution of the workflow demonstrates automated code validation and testing.

## Viva Preparation

**1. What is GitHub Actions?**
GitHub Actions is a platform used to automate software development workflows, including building, testing, and deployment.

**2. What is a runner?**
A runner is a virtual machine that executes the jobs and steps defined in a GitHub Actions workflow.

**3. Why are workflow files stored in `.github/workflows/`?**
GitHub Actions automatically detects workflow YAML files stored in this directory at the repository root.

**4. Why is CI performed on pull requests?**
It helps detect errors before changes are merged into the main branch.

**5. What is the purpose of Flake8?**
Flake8 checks Python code for style violations and common programming errors.

**6. What is the purpose of Pytest?**
Pytest is used to execute automated test cases and verify program functionality.

**7. What are GitHub Secrets?**
GitHub Secrets are encrypted values used to store sensitive information such as access tokens and credentials securely.
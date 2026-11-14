# Experiment 8: Jenkins Freestyle CI Job

## Aim
To create and configure a Jenkins Freestyle project that automatically retrieves source code from GitHub and performs Python linting and testing.

## Tools and Technologies
- Jenkins 2.580.2
- Docker Desktop
- Python 3.13.5
- Git 2.47.3
- Flake8 7.5.0
- pytest 9.2.0
- GitHub

## Project Configuration

**Jenkins Job Name:** `flask-demo-pipeline`

**GitHub Repository:**  
`https://github.com/Prabalbytes/software_devops_lab.git`

**Branch:** `*/main`

**Build Trigger:** Poll SCM

**Polling Schedule:**
```text
H/5 * * * *
```

## Build Steps

The Jenkins Freestyle project executes the following commands:

```bash
cd 02_GitHub_CLI_and_VSCode

python3 -m pip install -r requirements.txt

python3 -m flake8 . --max-line-length=100

python3 -m pytest -v
```

## Execution Results

The Jenkins job successfully performed the following operations:

1. Retrieved the source code from GitHub.
2. Installed the required Python dependencies.
3. Executed Python linting using Flake8.
4. Executed automated tests using pytest.
5. Completed the build successfully.

**Test Result:**
```text
1 passed
Finished: SUCCESS
```

## Jenkins Environment Verification

The following components were verified inside the Jenkins container:

| Component | Version |
|---|---|
| Jenkins | 2.580.2 |
| Python | 3.13.5 |
| pip | 25.1.1 |
| Git | 2.47.3 |
| Flake8 | 7.5.0 |
| pytest | 9.2.0 |

## Screenshots


Attach the following screenshots:

| Screenshot filename | What to capture |
|---|---|
| `01_jenkins_dashboard.png` | Jenkins dashboard showing `flask-demo-pipeline` |
| `02_job_configuration.png` | General configuration and job settings |
| `03_git_configuration.png` | GitHub repository URL and main branch |
| `04_poll_scm_trigger.png` | Poll SCM enabled with schedule |
| `05_build_steps.png` | Execute Shell commands |
| `06_successful_console_output.png` | Console output showing `1 passed` and `Finished: SUCCESS` |
| `07_environment_verification.png` | Terminal output showing Python, pip, Git, Flake8 and pytest versions |

## Conclusion

Successfully configured a Jenkins Freestyle CI job integrated with GitHub. Jenkins retrieved the source code, installed Python dependencies, performed linting with Flake8, and executed automated tests using pytest. The build completed successfully.
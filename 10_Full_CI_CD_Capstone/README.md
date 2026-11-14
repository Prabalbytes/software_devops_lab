# Experiment 10: Full CI/CD Capstone

## 1. Aim

To design and implement an end-to-end CI/CD pipeline using GitHub Actions, Docker Hub and Render. The pipeline automatically tests application code, builds and publishes Docker images, deploys the application, verifies its health and supports automatic rollback when deployment verification fails.

## 2. Technologies Used

- Git and GitHub
- GitHub Actions
- Python and Flask
- Docker and Docker Hub
- Render
- YAML
- PowerShell

## 3. Project Architecture

The CI/CD pipeline follows this sequence:

```text
Developer pushes code to GitHub
             |
             v
       GitHub Actions
             |
             v
      Test and Lint Code
             |
             v
    Build Docker Image
             |
             v
     Push to Docker Hub
             |
             v
      Deploy to Render
             |
             v
       Health Check
             |
       +-----+-----+
       |           |
     Success     Failure
       |           |
       v           v
 Promote Stable  Rollback
       |           |
       v           v
   Deployment   Verify Recovery
```

## 4. Implementation

### Step 1: Project Structure

Organized the project into separate experiment directories and maintained GitHub Actions workflows under `.github/workflows/`.

### Step 2: Docker Authentication

Configured Docker Hub credentials as GitHub repository secrets:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

### Step 3: GitHub Secrets

Configured the Render deployment hook as:

- `RENDER_DEPLOY_HOOK`

These secrets allow GitHub Actions to authenticate and trigger deployments securely.

### Step 4: Automated Testing

The `test` job:

- Checks out the repository.
- Sets up Python 3.11.
- Installs dependencies.
- Runs Flake8 for linting.
- Runs Pytest for automated testing.

### Step 5: Docker Build and Push

The `build-and-push` job:

- Configures Docker Buildx.
- Authenticates with Docker Hub.
- Builds the Flask application image.
- Pushes two tags:
  - Git commit SHA
  - `latest`

### Step 6: Automated Deployment

The `deploy` job triggers the Render deployment hook and passes the newly published, version-specific Docker image.

### Step 7: Application Health Check

The `health-check` job:

- Waits for deployment.
- Sends HTTP requests to the deployed application.
- Checks for HTTP status 200.
- Verifies the expected application response.

### Step 8: Stable Image Promotion

After a successful health check, the `promote-stable` job:

- Pulls the current version-specific image.
- Tags it as `stable`.
- Pushes the stable tag to Docker Hub.

This maintains a known-good image for rollback.

### Step 9: Automated Rollback

If the health check fails, the `rollback` job:

- Triggers a Render deployment using the `stable` Docker image.
- Waits for recovery.
- Performs another health check.
- Confirms whether rollback was successful.

## 5. Failure Simulation and Rollback Testing

An intentional deployment failure was simulated to test the rollback mechanism.

### Failure scenario

The health-check job was made to fail deliberately.

### Observed results

- Testing completed successfully.
- Docker image build and push completed successfully.
- Render deployment was triggered.
- Health check failed as expected.
- Stable promotion was skipped.
- Rollback job executed successfully.
- The previous stable image was redeployed.
- Rollback health verification returned HTTP 200.

The application returned:

```json
{
  "environment": "development",
  "message": "Hello from a containerized Flask app!"
}
```

After completing the simulation, the temporary failure condition was removed and the healthy application was restored.

## 6. Screenshots

The following screenshots document the implementation:

| No. | Screenshot |
|---|---|
| 01 | Project Structure |
| 02 | Docker Authentication |
| 03 | GitHub Secrets |
| 04 | Full CI/CD Test Job |
| 05 | Docker Publish Workflow |
| 06 | GitHub Actions Success |
| 07 | Docker Hub Published Image |
| 08 | Render Service Configuration |
| 09 | Render Deployment Success |
| 10 | Live Application Response |
| 11 | Render Deploy Hook |
| 12 | Automated Render Deployment |
| 13 | Automated Health Check |
| 14 | Version-Specific Deployment |
| 15 | Stable Docker Tag |

All screenshots are available in the `screenshots/` directory.

## 7. Result

Successfully implemented an end-to-end CI/CD pipeline using GitHub Actions, Docker Hub and Render.

The pipeline automatically tests, builds, publishes and deploys the Flask application. Application health verification, stable image promotion and automated rollback were also tested successfully.

## 8. Conclusion

This experiment demonstrated how CI/CD automation reduces manual deployment effort and improves application reliability. It also demonstrated how versioned Docker images and automated rollback can help recover from unsuccessful deployments.
# Experiment 9: Docker Deployment and Rollback

## Aim

To simulate a faulty Docker application release, detect the failure
using application responses and container logs, roll back to a
previously working image, and permanently correct the source code using
`git revert`.

## Objectives

-   Build and run versioned Docker images of a Flask application.
-   Simulate a faulty application release.
-   Detect the failure using an HTTP response and Docker logs.
-   Restore service by running the previous known-good image.
-   Revert the faulty source-code commit using Git.
-   Build and verify a corrected image.

## Tools and Technologies

-   Docker Desktop
-   Docker CLI
-   Python and Flask
-   Git and GitHub
-   PowerShell
-   Flask application running on port `5000`

## Image Versions Used

  -----------------------------------------------------------------------
  Image tag                           Purpose
  ----------------------------------- -----------------------------------
  `nuxudhbi/flask-demo:1.0`           Known-good release used for initial
                                      deployment and rollback

  `nuxudhbi/flask-demo:2.0`           Deliberately faulty release used to
                                      simulate an incident

  `nuxudhbi/flask-demo:2.1`           Corrected release deployed after
                                      the Git revert

  `nuxudhbi/flask-demo:latest`        Tagged to the same corrected image
                                      as version `2.1`
  -----------------------------------------------------------------------

## Procedure

### 1. Run the known-good release

Start the version `1.0` container:

``` powershell
docker run -d -p 5000:5000 --name web --restart unless-stopped nuxudhbi/flask-demo:1.0
```

Test the application:

``` powershell
curl.exe http://localhost:5000
```

The application returned a successful response:

``` json
{"environment":"development","message":"Hello from a containerized Flask app!"}
```

### 2. Introduce a faulty release

A deliberate runtime error was added inside the Flask route in
`04_Docker_Containerization/app.py`:

``` python
raise RuntimeError("V2 crashes!")
```

Build the faulty image:

``` powershell
docker build -t nuxudhbi/flask-demo:2.0 .\04_Docker_Containerization
```

Stop and remove the previous container, then run version `2.0`:

``` powershell
docker stop web
docker rm web
docker run -d -p 5000:5000 --name web nuxudhbi/flask-demo:2.0
```

### 3. Detect the failure

Send a request to the application:

``` powershell
curl.exe http://localhost:5000
```

The request returned **HTTP 500**. Inspect the container logs:

``` powershell
docker logs web --tail 20
```

The logs showed the exception:

``` text
RuntimeError: V2 crashes!
```

The container process remained running because the error occurred while
handling the HTTP request. The failure was identified through the HTTP
500 response and the traceback in the logs.

### 4. Perform an immediate container rollback

Stop and remove the faulty container:

``` powershell
docker stop web
docker rm web
```

Run the previous known-good image:

``` powershell
docker run -d -p 5000:5000 --name web --restart unless-stopped nuxudhbi/flask-demo:1.0
```

Verify that the application is responding again:

``` powershell
curl.exe http://localhost:5000
```

The successful JSON response confirmed that the previous release
restored service.

### 5. Permanently correct the source code using Git

The faulty change was committed for the rollback exercise:

``` text
dc01168 feat: introduce faulty v2 release for rollback simulation
```

Revert that commit:

``` powershell
git revert dc01168 --no-edit
```

The revert created the following commit:

``` text
12da325 Revert "feat: introduce faulty v2 release for rollback simulation"
```

This removed the deliberate `RuntimeError` from the source code while
preserving the Git history.

### 6. Build and deploy the corrected release

Build the corrected image and apply both tags:

``` powershell
docker build -t nuxudhbi/flask-demo:2.1 -t nuxudhbi/flask-demo:latest ./04_Docker_Containerization
```

Stop and remove the previous container, then deploy version `2.1`:

``` powershell
docker stop web
docker rm web
docker run -d -p 5000:5000 --name web nuxudhbi/flask-demo:2.1
```

Verify the application:

``` powershell
curl.exe http://localhost:5000
```

The application returned the expected successful JSON response. The
`2.1` and `latest` tags referred to the same image ID.

## Result

The faulty version `2.0` was detected through an HTTP 500 response and
Docker logs. The application was restored by running the known-good
`1.0` image. The faulty source-code change was then reverted using Git,
and the corrected application was built and deployed as version `2.1`.

**Experiment 9 was completed successfully.**

## Incident Metrics

-   **Detection evidence:** HTTP 500 response and the
    `RuntimeError: V2 crashes!` traceback in container logs.
-   **Rollback evidence:** The known-good `1.0` image returned a
    successful response after redeployment.
-   **Permanent correction:** Git revert commit `12da325`.
-   **MTTD (Mean Time to Detect):** Not calculated because the exact
    faulty deployment and detection timestamps were not recorded.
-   **MTTR (Mean Time to Recover):** Not calculated because the exact
    incident start and service-restoration timestamps were not recorded.

## Screenshots

Save the experiment screenshots in the `screenshots/` directory using
the following filenames:

1.  `01-known-good-v1.png` --- Initial successful response from version
    1.0.
2.  `02-faulty-v2-build.png` --- Build of the faulty version 2.0 image.
3.  `03-failure-response.png` --- HTTP 500 response from the faulty
    application.
4.  `04-failure-logs.png` --- Docker logs showing the runtime exception.
5.  `05-rollback-v1.png` --- Successful response after rollback to
    version 1.0.
6.  `06-git-revert.png` --- Git revert operation and commit.
7.  `07-build-fixed-v2-1.png` --- Successful build of the corrected
    version 2.1.
8.  `08-final-v2-1.png` --- Successful response from the corrected
    version 2.1.

## Repository Structure

``` text
09_Docker_Deployment_Rollback/
├── README.md
├── incident_report.md
└── screenshots/
    ├── 01-known-good-v1.png
    ├── 02-faulty-v2-build.png
    ├── 03-failure-response.png
    ├── 04-failure-logs.png
    ├── 05-rollback-v1.png
    ├── 06-git-revert.png
    ├── 07-build-fixed-v2-1.png
    └── 08-final-v2-1.png
```

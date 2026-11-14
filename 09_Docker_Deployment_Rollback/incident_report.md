# Incident Report — Experiment 9: Docker Deployment Rollback

## 1. Incident details

| Field | Entry |
|---|---|
| Experiment | 9 — Perform a Rollback Simulation by Reverting a Containerized Deployment |
| Application | Containerized Flask application |
| Affected endpoint | `GET /` |
| Faulty release | `nuxudhbi/flask-demo:2.0` |
| Last known-good release | `nuxudhbi/flask-demo:1.0` |
| Corrected release | `nuxudhbi/flask-demo:2.1` |
| Container name | `web` |
| Incident date | 14 November 2026 |
| Final status | Service restored and corrected v2.1 deployment verified |

## 2. Incident timeline

| Event | Time / evidence |
|---|---|
| Faulty v2.0 image deployed | Exact time not recorded |
| Failure detected | 14 November 2026, 17:21:01 UTC — Flask error log records the failed `GET /` request |
| Container-level rollback to v1.0 | Completed; exact time not recorded |
| Corrected v2.1 image built and deployed | Completed; exact time not recorded |
| Final verification | `curl.exe http://localhost:5000` returned the expected healthy JSON response |

**Timing note:** The evidence captures the failure log time but not the exact faulty deployment time or rollback completion time. Therefore, numerical MTTD and MTTR values cannot be calculated reliably from the available records. Do not use the sample times in the lab manual as if they were actual measurements.

## 3. Detection method

The faulty release was detected by sending a request to the Flask endpoint:

```powershell
curl.exe http://localhost:5000
```

The endpoint returned **HTTP 500 Internal Server Error**. The application logs were then inspected:

```powershell
docker logs web --tail 20
```

The logs showed the traceback and the following root-cause message:

```text
File "/app/app.py", line 9, in home
    raise RuntimeError("V2 crashes!")
RuntimeError: V2 crashes!
```

The container was still shown as `Up`. This is because the exception occurred during request handling and did not terminate the Flask server process. Thus, checking container status alone was not sufficient to detect the application-level failure.

## 4. Root cause

A deliberate faulty statement was added inside the Flask `home()` route in `04_Docker_Containerization/app.py`:

```python
raise RuntimeError("V2 crashes!")
```

When a client requested `/`, Flask raised the exception and returned an HTTP 500 response.

## 5. Remediation

### Immediate container-level rollback

The faulty v2.0 container was stopped and removed. The known-good v1.0 image was started again:

```powershell
docker stop web
docker rm web
docker run -d -p 5000:5000 --name web --restart unless-stopped nuxudhbi/flask-demo:1.0
```

The endpoint returned the expected healthy response:

```json
{"environment":"development","message":"Hello from a containerized Flask app!"}
```

This restored the service using the previously built image; no image rebuild was required for the rollback.

### Permanent code-level correction

The faulty change was committed for the simulation:

```text
dc01168 feat: introduce faulty v2 release for rollback simulation
```

The change was reversed using Git's history-safe revert operation:

```powershell
git revert dc01168 --no-edit
```

The resulting corrective commit was:

```text
12da325 Revert "feat: introduce faulty v2 release for rollback simulation"
```

The corrected application was rebuilt with both `2.1` and `latest` tags:

```powershell
docker build -t nuxudhbi/flask-demo:2.1 -t nuxudhbi/flask-demo:latest ./04_Docker_Containerization
```

Both tags were confirmed to point to the same image ID. The corrected v2.1 container was then started and verified:

```powershell
docker stop web
docker rm web
docker run -d -p 5000:5000 --name web nuxudhbi/flask-demo:2.1
curl.exe http://localhost:5000
```

The final request returned:

```json
{"environment":"development","message":"Hello from a containerized Flask app!"}
```

## 6. Reliability metrics

- **MTTD (Mean Time To Detect):** The elapsed time between deploying the faulty release and detecting the failure. Not calculated because the exact v2.0 deployment time was not recorded.
- **MTTR (Mean Time To Recover):** The elapsed time from detection of the incident until service restoration. Not calculated because the exact rollback completion time was not recorded.

For a future measured run:

- `MTTD = failure detection time − faulty release deployment time`
- `MTTR = service restoration time − failure detection time`

## 7. Lessons learned

1. Keeping versioned Docker images makes rollback possible without rebuilding the previous release.
2. A container can remain running while its application endpoint returns HTTP errors.
3. Endpoint checks and application logs should be used together to detect failures.
4. `git revert` creates a new corrective commit and preserves shared Git history.
5. A version-specific tag such as `2.1` identifies a release, while `latest` is a movable tag that can point to the same image as the newest release.

## 8. Conclusion

The faulty v2.0 release was detected through an HTTP 500 response and the traceback in the Docker logs. The application was immediately restored using the known-good v1.0 image. The faulty source change was then reversed using `git revert`, and the corrected v2.1 image was deployed and verified successfully. The rollback and permanent correction were completed; MTTD and MTTR were left uncalculated because the required timestamps were not captured.

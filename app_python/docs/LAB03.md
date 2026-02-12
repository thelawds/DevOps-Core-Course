# Testing

#### Framework Selection:
I've selected **pytest** framework mainly because I have experience working with it - it is very simple, concise, but still rich enough with features.

#### Test structure

There is a directory structure of the `tests/` directory:

```
app_python/
├── tests/
│   ├── __init__.py              # Makes tests a Python package
│   ├── conftest.py              # Shared pytest fixtures
│   ├── test_app.py              # Main application tests
│   └── test_error_handlers.py   # Error handling tests
```

1. `conftest.py` - Contains shared fixtures
2. `test_app.py` - Contains main application tests
3. `test_error_handlers.py` - Contains error handling test cases

#### Running tests locally:
1. Install requirements with `pip install -r requirements.txt`
2. Run tests with `pytest -v`

#### Terminal output with tests:
```
alecsey@alecsey-B450-AORUS-ELITE:~/Documents/DevOps-Core-Course/app_python$ pytest -v
===================================== test session starts ======================================
platform linux -- Python 3.10.12, pytest-8.3.4, pluggy-1.6.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/alecsey/Documents/DevOps-Core-Course/app_python
plugins: cov-5.0.0, mock-3.14.0
collected 22 items                                                                             

tests/test_app.py::TestMainEndpoint::test_service_info_structure PASSED                  [  4%]
tests/test_app.py::TestMainEndpoint::test_service_info_with_mocked_system PASSED         [  9%]
tests/test_app.py::TestMainEndpoint::test_request_info_in_response PASSED                [ 13%]
tests/test_app.py::TestMainEndpoint::test_uptime_calculation PASSED                      [ 18%]
tests/test_app.py::TestMainEndpoint::test_uptime_human_formatting PASSED                 [ 22%]
tests/test_app.py::TestHealthEndpoint::test_health_check_structure PASSED                [ 27%]
tests/test_app.py::TestHealthEndpoint::test_health_check_iso_timestamp PASSED            [ 31%]
tests/test_app.py::TestHealthEndpoint::test_health_check_consistency PASSED              [ 36%]
tests/test_app.py::TestSystemInfo::test_system_info_linux PASSED                         [ 40%]
tests/test_app.py::TestSystemInfo::test_system_info_windows PASSED                       [ 45%]
tests/test_app.py::TestSystemInfo::test_system_info_macos PASSED                         [ 50%]
tests/test_app.py::TestUptimeFunction::test_get_uptime_seconds PASSED                    [ 54%]
tests/test_app.py::TestUptimeFunction::test_uptime_monotonic PASSED                      [ 59%]
tests/test_app.py::test_json_content_type PASSED                                         [ 63%]
tests/test_error_handlers.py::TestErrorHandlers::test_404_not_found PASSED               [ 68%]
tests/test_error_handlers.py::TestErrorHandlers::test_405_method_not_allowed PASSED      [ 72%]
tests/test_error_handlers.py::TestErrorHandlers::test_405_on_health_endpoint PASSED      [ 77%]
tests/test_error_handlers.py::TestErrorHandlers::test_multiple_invalid_methods[POST] PASSED [ 81%]
tests/test_error_handlers.py::TestErrorHandlers::test_multiple_invalid_methods[PUT] PASSED [ 86%]
tests/test_error_handlers.py::TestErrorHandlers::test_multiple_invalid_methods[DELETE] PASSED [ 90%]
tests/test_error_handlers.py::TestErrorHandlers::test_multiple_invalid_methods[PATCH] PASSED [ 95%]
tests/test_error_handlers.py::TestErrorHandlers::test_error_response_structure PASSED    [100%]

====================================== 22 passed in 1.27s ======================================
```

# GitHub Actions CI Workflow


#### Workflow Trigger Strategy

1. workflow_dispatch - we need to be able to run workflow manually
2. pull_request - checking code quality and correctness on each pull request
3. push to master - checking code quality and building application image on creating a new version

#### GitHub Actions Marketplace Selections
1. actions/checkout - checking out on our branch
2. actions/setup-python - python setup
3. docker/setup-buildx-action - docker buildx
4. docker/login-action - login to dockerhub
5. docker/build-push-action and docker/metadata-action to add metadata and push image to my docker account
6. aquasecurity/trivy-action - sequrity


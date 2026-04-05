terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = ">= 3.0.2"
    }
  }
}

provider "docker" {
  host = "unix:///Users/adi/.docker/run/docker.sock"
}

resource "docker_image" "api_framework" {
  name         = "tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim"
  keep_locally = true
}

resource "docker_container" "stable" {
  name  = "stable_llm"
  # Use the name string directly to avoid the SHA formatting error
  image = "tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim"
  command = ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
  
  env = ["NODE_ENV=STABLE_PROD"]

  volumes {
    host_path      = abspath(path.module)
    container_path = "/app"
  }
  must_run = true
  ports {
    internal = 80
    external = 4040
  }
}

resource "docker_container" "candidate" {
  name  = "candidate_llm"
  image = "tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim"
  command = ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
  
  env = ["NODE_ENV=CANDIDATE_TEST"]

  volumes {
    host_path      = abspath(path.module)
    container_path = "/app"
  }
  must_run = true
  ports {
    internal = 80
    external = 4041
  }
}
# Terraformer
This is our DevOps project demo

Terraformer: Shadow-Model LLM Evaluator
This project implements a Shadow-Model Evaluation Framework using Terraform and Docker. It allows for side-by-side parity checks between a "Stable" production model and a "Candidate" test model.

System Architecture
Infrastructure as Code: Managed via Terraform for immutable deployments.

Containerization: Dual FastAPI nodes (Stable & Candidate) running in Docker.

Model Routing: A centralized judge.py script that handles request distribution and latency tracking.

 **Prerequisites**
Docker Desktop: Required to host the API containers.

Terraform: For infrastructure orchestration.

Ollama: The local inference engine for LLMs.

Python 3.9+: For the evaluator and judge scripts.

Setup & Deployment
Initialize & Apply Infrastructure:

Bash
terraform init
terraform apply -auto-approve
Inject Dependencies:
Since the containers start from a slim image, run these to enable communication with the LLM:

Bash
docker exec -u 0 stable_llm pip install requests
docker exec -u 0 candidate_llm pip install requests
docker restart stable_llm candidate_llm
Run Evaluation:

Bash
python judge.py
 Features
Parity Checking: Compares outputs from two different LLM nodes simultaneously.

Latency Measurement: Tracks response times for performance benchmarking.

Environment Isolation: Uses Docker volumes to map local code into isolated runtime environments.

Node Identity: Each response is tagged with STABLE_PROD or CANDIDATE_TEST for auditability.

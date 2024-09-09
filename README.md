# automata-devops-assignment

# Project Title

## Overview

This project involves developing and deploying an ERC20 smart contract indexer application on an AWS EC2 instance that integrates with Prometheus for metrics collection and Grafana for visualization. The application tracks USDT transactions and other relevant data. To verify if certain step is fulfill, you can refer to screenshots in ```/contract-indexer/screenshots```.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Setup](#setup)
- [Deployment](#deployment)
- [Usage](#usage)
- [Metrics](#metrics)
- [Alerting](#alerting)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Features

- Indexer application to track USDT transactions and approvals.
- Prometheus for collecting metrics.
- Grafana for visualizing metrics and creating dashboards.
- Alerts for significant token transfers.

## Setup

### Prerequisites

- Docker
- Prometheus
- Grafana Cloud account
- Terraform

### Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    ```
    
2. **Install Terraform:**

    Follow the instructions [here](https://www.terraform.io/downloads.html) to install Terraform.

3. **Initialize Terraform & Apply Terraform Plan:**

    Change the configurations in '/contract-indexer/terraform_setup/main.tf' to match your AWS details.
    Run the following command in the root of your Terraform directory:

    ```sh
    terraform init
    terraform apply
    ```

    This will provision an EC2 instance, set up the necessary networking, and install Docker. To ssh into your EC2 instance, follow [this](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connect-linux-inst-ssh.html) guide
    
4. **Verify Deployment:**

    After the Terraform plan is applied, verify that the EC2 instance is running and that Docker is installed.
    
5. **Download Prometheus**

    To download Prometheus into your EC2 instance, run the following commands:
   
    ```sh
    wget https://github.com/prometheus/prometheus/releases/download/v2.36.0/prometheus-2.36.0.linux-amd64.tar.gz
    tar xvf prometheus-2.36.0.linux-amd64.tar.gz
    cd prometheus-2.36.0.linux-amd64
    ```
    
7. **Configure prometheus.yml and run Prometheus:**

    You should first create a free account on [Grafana Cloud](https://grafana.com/products/cloud/) and request for your own authentication details.
    Then fill in the 'remote-write' section and replace the two 'targets' parameter with indexer and node-exporter container IP respectively, using the following commands:
   
    ```sh
    docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' my-indexer-container
    docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' node-exporter
    ```

    Run Prometheus detached mode:

    ```sh
    nohup ./prometheus --config.file=prometheus.yml > prometheus.log 2>&1 &
    ```

    You are now good to connect your data source on Grafana Cloud and establish dashboards!
   
## Usage

- **Access Prometheus:**
  
  Open your browser and go to `http://<EC2-PUBLIC-IP>:9090/targets?search=`.

  You can expect something like this:
  
  ![http://<EC2-PUBLIC-IP>:9090/targets?search=](/contract-indexer/screenshots/9090-targets.png)

- **Access all metrics on node-exporter:**
  
  Open your browser and go to `http://<EC2-PUBLIC-IP>:9100`.

  You can expect something like this:
  
  ![http://<EC2-PUBLIC-IP>:9100](/contract-indexer/screenshots/9100.png)

- **Access indexer output:**
  
  Open your browser and go to `http://<EC2-PUBLIC-IP>:9200`.

  You can expect something like this:
  
  ![http://<EC2-PUBLIC-IP>:9200](/contract-indexer/screenshots/9200.png)

- **Final Dashboard:**
  
  You should see something like this!

  ![final-dashboard](/contract-indexer/screenshots/grafana-dashboard-token_transferred_per_second.png)

## Metrics

- **`tx_per_second`**: Shows the rate of transactions per second.
- **`token_transferred_per_second`**: Shows the rate of tokens transferred per second.
- **`approvals_per_second`**: Shows the rate of approvals per second.
- **`approval_amount_metric`**: Shows the rate of tokens approved per second.

## Alerting

1. **Create an alert rule in Grafana Cloud:**

    Set up an alert to trigger when the rate of token transfers exceeds a threshold.

    - **Metric:** `token_transferred_per_second`
    - **Condition:** Is above a certain value (e.g., 100 tokens)

## Troubleshooting

- **Issue:** No data in Grafana dashboard.
  
  **Solution:** Verify that the indexer container is running and exposing metrics on port 9200.

- **Issue:** Prometheus target is down.
  
  **Solution:** Ensure that Prometheus can access the indexer container on the specified port.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

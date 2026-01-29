# Hush K8s Goat App

A lightweight demo application that generates authentication events by calling the HubSpot API in a loop. Used to demonstrate and validate [Hush](https://hush.security) NHI tracking capabilities.

## Overview

This app:
- Runs as a single pod in your Kubernetes cluster
- Attempts to authenticate to HubSpot API every N seconds
- Works with valid, invalid, or revoked credentials
- Generates authentication events that Hush can track

## Quick Start

### Prerequisites
- Kubernetes cluster
- Helm 3.x installed

### Installation

```bash
helm install hush-goat oci://ghcr.io/hushsecurity/hush-k8s-goat-app
```

## Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `credentials.hubspotApiKey` | HubSpot API key | (demo key) |
| `config.intervalSeconds` | Seconds between auth attempts | `30` |
| `config.logLevel` | Log level (DEBUG, INFO, WARNING, ERROR) | `INFO` |
| `image.repository` | Container image repository | `public.ecr.aws/z0t8l6o4/hush-k8s-goat-app` |
| `image.tag` | Container image tag | `main` |

### Example: Custom interval

```bash
helm install hush-goat oci://ghcr.io/hushsecurity/hush-k8s-goat-app \
  --set config.intervalSeconds=60
```
## Uninstallation

```bash
helm uninstall hush-goat
```
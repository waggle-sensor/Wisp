# waggle-sensor GitHub org index (public repos)

Scraped from [github.com/orgs/waggle-sensor/repositories](https://github.com/orgs/waggle-sensor/repositories?type=public) via the public GitHub API on **2026-07-17**.

**Scope:** public repositories only (private repos skipped). Forks and archived repos are included and marked.

## How to use this file

1. Find the repo by name or skim category summaries below.
2. Open the **URL** (clone / browse README / issues) when you need source or examples — do not invent APIs from the summary alone.
3. Prefer camp skill refs + [sage-docs-index.md](sage-docs-index.md) for conceptual/docs answers; use this index when you need **code**.
4. Sibling org catalog: [sagecontinuum-repos-index.md](sagecontinuum-repos-index.md) for [sagecontinuum](https://github.com/orgs/sagecontinuum) public repos.
5. High-signal repos:
   - SDK: [pywaggle](https://github.com/waggle-sensor/pywaggle)
   - `pluginctl` / `sesctl`: [edge-scheduler](https://github.com/waggle-sensor/edge-scheduler)
   - On-node services: [waggle-edge-stack](https://github.com/waggle-sensor/waggle-edge-stack)
   - MCP: [sage-mcp](https://github.com/waggle-sensor/sage-mcp)
   - Website/docs source: [sage-website](https://github.com/waggle-sensor/sage-website)

**Public repos indexed:** 220 (curated categories; GitHub API lists 256 public as of this scrape)

## Core platform — WES, Beehive, Beekeeper, nodes (82)

### app-init-shim _Go_

- **URL:** https://github.com/waggle-sensor/app-init-shim
- **Summary:** Provides basic app init container shim.
- **Pushed:** 2022-11-01

### app-meta-cache _Go_

- **URL:** https://github.com/waggle-sensor/app-meta-cache
- **Summary:** A Docker container for managing meta information of Waggle plugins
- **Pushed:** 2024-01-04

### attach-to-node-k3s _Go_

- **URL:** https://github.com/waggle-sensor/attach-to-node-k3s
- **Summary:** Tool for remotely debugging nodes.
- **Pushed:** 2025-05-07

### beehive-data-api _Go_

- **URL:** https://github.com/waggle-sensor/beehive-data-api
- **Summary:** Beehive Data API Service
- **Topics:** beehive
- **Pushed:** 2024-12-04

### beehive-data-exporter _Python_

- **URL:** https://github.com/waggle-sensor/beehive-data-exporter
- **Summary:** Tools for exporting data files from Beehive.
- **Topics:** beehive
- **Pushed:** 2023-10-04

### beehive-etl _Python_

- **URL:** https://github.com/waggle-sensor/beehive-etl
- **Summary:** Beehive ETL code and tools
- **Pushed:** 2020-06-16

### beehive-influxdb-backup _Shell_

- **URL:** https://github.com/waggle-sensor/beehive-influxdb-backup
- **Summary:** Tools for performing native backup of Beehive's InfluxDB server.
- **Topics:** beehive
- **Pushed:** 2022-12-16

### beehive-influxdb-loader _Python_

- **URL:** https://github.com/waggle-sensor/beehive-influxdb-loader
- **Summary:** Beehive InfluxDB Data Loader Service
- **Topics:** beehive
- **Pushed:** 2025-08-21

### beehive-nodes-service _Go_

- **URL:** https://github.com/waggle-sensor/beehive-nodes-service
- **Summary:** Service that updates beehive component about new nodes
- **Topics:** beehive, beekeeper
- **Pushed:** 2025-08-26

### beehive-upload-server _Shell_

- **URL:** https://github.com/waggle-sensor/beehive-upload-server
- **Summary:** ssh+rsync based upload server for training data.
- **Topics:** beehive
- **Pushed:** 2022-12-17

### beekeeper _Python_

- **URL:** https://github.com/waggle-sensor/beekeeper
- **Summary:** Management and administrative cloud services for Waggle.
- **Topics:** cloud, beekeeper
- **Pushed:** 2024-01-09

### beekeeper-key-tools _Shell_

- **URL:** https://github.com/waggle-sensor/beekeeper-key-tools
- **Summary:** Houses the tools to create the beekeeper certificate authority keys, node registration keys, etc.
- **Pushed:** 2023-02-10

### beekeeper-netman-connectivity _Go_

- **URL:** https://github.com/waggle-sensor/beekeeper-netman-connectivity
- **Summary:** NetworkManager Connectivity check service
- **Topics:** beekeeper
- **Pushed:** 2022-12-17

### blade-image _Shell_

- **URL:** https://github.com/waggle-sensor/blade-image
- **Summary:** Blade-Image
- **Topics:** node, blade
- **Pushed:** 2023-12-21

### core _Python_

- **URL:** https://github.com/waggle-sensor/core
- **Summary:** Core software shared by both the Node Controller (NC) and Edge Processor (EP)
- **Pushed:** 2019-09-11

### data-repository

- **URL:** https://github.com/waggle-sensor/data-repository
- **Summary:** Waggle Data Repository
- **Topics:** docs, beehive
- **Pushed:** 2022-06-01

### edge-code-repository

- **URL:** https://github.com/waggle-sensor/edge-code-repository
- **Summary:** Edge Code Repository
- **Topics:** docs, beehive
- **Pushed:** 2022-06-01

### edge-scheduler _Jupyter Notebook_

- **URL:** https://github.com/waggle-sensor/edge-scheduler
- **Summary:** Waggle Edge Scheduler
- **Topics:** docs, beehive
- **Pushed:** 2025-10-23

### edge-scheduler-monitor

- **URL:** https://github.com/waggle-sensor/edge-scheduler-monitor
- **Summary:** A backend service to monitor activities in cloud/edge schedulers.
- **Pushed:** 2022-09-12

### edgeprocessor

- **URL:** https://github.com/waggle-sensor/edgeprocessor
- **Summary:** Edge Processor
- **Pushed:** 2022-09-09

### file-forager _Jupyter Notebook_

- **URL:** https://github.com/waggle-sensor/file-forager
- **Summary:** Runs on Waggle node to sync locale files to the Beehive file storage. The plugin manages its state locally due to the inability to query Beehive for synced fil…
- **Pushed:** 2025-05-14

### gpu-stress-test _Python_

- **URL:** https://github.com/waggle-sensor/gpu-stress-test
- **Summary:** Small GPU / CUDA stress bundle as a Docker image
- **Pushed:** 2024-01-06

### grafana-agent-loader _Go_

- **URL:** https://github.com/waggle-sensor/grafana-agent-loader
- **Summary:** Prometheus metrics loader to InfluxDB
- **Pushed:** 2023-11-20

### honeycomb _Python_

- **URL:** https://github.com/waggle-sensor/honeycomb
- **Summary:** Modular Peripheral configuration manager
- **Topics:** docs, node
- **Pushed:** 2021-08-06

### jetson-exporter _Go_

- **URL:** https://github.com/waggle-sensor/jetson-exporter
- **Summary:** A metrics provider for Jeton GPU
- **Pushed:** 2024-07-09

### jobctl _Python_

- **URL:** https://github.com/waggle-sensor/jobctl
- **Summary:** A Python package for controlling job submission and management on Waggle edge nodes using sesctl.
- **Pushed:** 2026-03-19

### k3s-test

- **URL:** https://github.com/waggle-sensor/k3s-test
- **Summary:** Some scripts and things to help test k3s.
- **Pushed:** 2021-02-17

### lambda-triggers

- **URL:** https://github.com/waggle-sensor/lambda-triggers
- **Summary:** Lambda Triggers
- **Topics:** docs, beehive
- **Pushed:** 2022-06-01

### media-streamer _Shell_

- **URL:** https://github.com/waggle-sensor/media-streamer
- **Summary:** A ffmpeg based streaming server over HTTP
- **Pushed:** 2021-07-24

### minimal-k3s-vagrantbox

- **URL:** https://github.com/waggle-sensor/minimal-k3s-vagrantbox
- **Summary:** Minimal Vagrantbox for experimenting with k3s.
- **Pushed:** 2022-01-27

### node-health-reporter _Python_

- **URL:** https://github.com/waggle-sensor/node-health-reporter
- **Summary:** Cronjob for check and reporting node status.
- **Pushed:** 2025-05-21

### node-platforms _Shell_

- **URL:** https://github.com/waggle-sensor/node-platforms
- **Summary:** Instructions for bootstrapping a Waggle node
- **Pushed:** 2025-11-11

### nodecontroller

- **URL:** https://github.com/waggle-sensor/nodecontroller
- **Summary:** Node Controller
- **Topics:** docs, node, wildnode
- **Pushed:** 2022-09-09

### nvidia_toolchain

- **URL:** https://github.com/waggle-sensor/nvidia_toolchain
- **Summary:** Contains the NVidia ARM64 build toolchain archive for use in building kernel & CBoot
- **Topics:** node, wildsage
- **Pushed:** 2023-02-28

### perf-mon _Jinja_

- **URL:** https://github.com/waggle-sensor/perf-mon
- **Summary:** A performance monitoring toolset for applications and edge systems
- **Pushed:** 2024-08-12

### prometheus-cadvisor-proxy _Go_

- **URL:** https://github.com/waggle-sensor/prometheus-cadvisor-proxy
- **Summary:** Prometheus cadvisor proxy (for nodes)
- **Pushed:** 2024-01-29

### pywaggle _Python_

- **URL:** https://github.com/waggle-sensor/pywaggle
- **Summary:** Python SDK for integrating plugins with Waggle.
- **Topics:** audio, python, vision, waggle, waggle-edge-stack
- **Pushed:** 2025-10-23

### pywagglemsg _Python_

- **URL:** https://github.com/waggle-sensor/pywagglemsg
- **Summary:** Python module for handling Waggle messages.
- **Topics:** waggle-edge-stack
- **Pushed:** 2022-12-01

### sage-mcp _Python_

- **URL:** https://github.com/waggle-sensor/sage-mcp
- **Summary:** Sage MCP Server
- **Pushed:** 2026-07-07

### stressme _Python_

- **URL:** https://github.com/waggle-sensor/stressme
- **Summary:** A set of programs to stress a computing device on Linux, particularly on Nvidia Jetson
- **Pushed:** 2024-07-31

### virtual-waggle _Python_

- **URL:** https://github.com/waggle-sensor/virtual-waggle
- **Summary:** Virtual Waggle is a set of software tools to help build and test code for the edge.
- **Pushed:** 2021-05-10

### waggle-beehive-v2 _Python_

- **URL:** https://github.com/waggle-sensor/waggle-beehive-v2
- **Summary:** Data and processing cloud services for Waggle.
- **Topics:** cloud, beehive
- **Pushed:** 2023-04-27

### waggle-bk-registration _Python_

- **URL:** https://github.com/waggle-sensor/waggle-bk-registration
- **Summary:** Services that run on end-points to handle the registration process with the beekeeper
- **Topics:** node, deb, beekeeper, wildnode
- **Pushed:** 2025-02-27

### waggle-bk-reverse-tunnel _Shell_

- **URL:** https://github.com/waggle-sensor/waggle-bk-reverse-tunnel
- **Summary:** Creates reverse ssh tunnel to beekeeper
- **Topics:** node, deb, blade, beekeeper, wildnode
- **Pushed:** 2022-06-08

### waggle-blade

- **URL:** https://github.com/waggle-sensor/waggle-blade
- **Summary:** Waggle Blades are standard, commercially available blade servers with x86-64 CPUS and NVIDIA GPUs for AI@Edge compute jobs.
- **Topics:** docs, node, blade
- **Pushed:** 2022-09-16

### waggle-common-tools _Python_

- **URL:** https://github.com/waggle-sensor/waggle-common-tools
- **Summary:** Common tools for Sage OS administration and operations.
- **Topics:** node, deb, blade, wildnode
- **Pushed:** 2023-10-11

### waggle-deb-builder _Shell_

- **URL:** https://github.com/waggle-sensor/waggle-deb-builder
- **Summary:** Container for building repo deb packages.
- **Topics:** deb
- **Pushed:** 2022-12-17

### waggle-edge-stack _Shell_

- **URL:** https://github.com/waggle-sensor/waggle-edge-stack
- **Summary:** The Waggle Edge Stack provides the core services which support running AI@Edge.
- **Topics:** node, waggle-edge-stack
- **Pushed:** 2026-07-14

### waggle-firewall _Shell_

- **URL:** https://github.com/waggle-sensor/waggle-firewall
- **Summary:** Network firewall service
- **Topics:** node, deb, blade, wildnode
- **Pushed:** 2022-06-08

### waggle-internet-share _Shell_

- **URL:** https://github.com/waggle-sensor/waggle-internet-share
- **Summary:** Service to share internet over local 10.31.81.1/24 network
- **Topics:** node, deb, blade, wildnode
- **Pushed:** 2022-06-08

### waggle-node-hostname _Python_

- **URL:** https://github.com/waggle-sensor/waggle-node-hostname
- **Summary:** Service run on the nodes on first boot to set the hostname [DEPRECATED]
- **Topics:** node, deb, blade, wildnode
- **Pushed:** 2022-06-08

### waggle-nodeid _Python_

- **URL:** https://github.com/waggle-sensor/waggle-nodeid
- **Summary:** Early running service in nodes to create the unique node ID used by other services.
- **Topics:** node, deb, blade, wildnode
- **Pushed:** 2022-06-08

### waggle-nodes _Shell_

- **URL:** https://github.com/waggle-sensor/waggle-nodes
- **Summary:** All waggle-node instances are tracked here.
- **Pushed:** 2018-12-06

### waggle-powercycle _Shell_

- **URL:** https://github.com/waggle-sensor/waggle-powercycle
- **Summary:** Tools to gracefully shutdown / reboot a Wild Waggle Node
- **Topics:** node, deb, wildnode
- **Pushed:** 2023-01-06

### waggle-rpi-pxeboot _Shell_

- **URL:** https://github.com/waggle-sensor/waggle-rpi-pxeboot
- **Summary:** Build's a Debian package to allow NX Boards to PxeBoot an Rpi4 and configures a DHCP server
- **Topics:** raspberry-pi, node, deb, wildnode
- **Pushed:** 2023-01-31

### waggle-rpi-sd-flash _Shell_

- **URL:** https://github.com/waggle-sensor/waggle-rpi-sd-flash
- **Summary:** Instructions for Building an SD Card *.img for flashing the RPI to a PxE-bootable state
- **Topics:** raspberry-pi, docs, factory, wildnode
- **Pushed:** 2023-01-26

### waggle-stress _Dockerfile_

- **URL:** https://github.com/waggle-sensor/waggle-stress
- **Summary:** A Docker container with tools for stressing Waggle node
- **Pushed:** 2023-01-20

### waggle-upload-sync _Shell_

- **URL:** https://github.com/waggle-sensor/waggle-upload-sync
- **Summary:** Service to sync the data upload folder to an external drive
- **Topics:** node, deb, blade, wildnode
- **Pushed:** 2022-04-14

### waggle-wagman-watchdog _Shell_

- **URL:** https://github.com/waggle-sensor/waggle-wagman-watchdog
- **Summary:** Wild Node Wagman Watchdog Service
- **Topics:** node, deb, wildnode, wagman
- **Pushed:** 2022-06-08

### waggle-wan-tunnel _Python_

- **URL:** https://github.com/waggle-sensor/waggle-wan-tunnel
- **Summary:** Service which manages WAN tunnel through Beekeeper.
- **Topics:** node, deb, blade, wildnode
- **Pushed:** 2022-06-08

### waggle_image _Python_

- **URL:** https://github.com/waggle-sensor/waggle_image
- **Summary:** Scripts to create waggle disk images
- **Pushed:** 2019-10-21

### wagman _C++_

- **URL:** https://github.com/waggle-sensor/wagman
- **Summary:** The Waggle Manager (Wagman), a custom circuit board and control system for Wild Waggle Nodes
- **Topics:** docs, node, wildnode
- **Pushed:** 2022-06-17

### wes-audio-server _Dockerfile_

- **URL:** https://github.com/waggle-sensor/wes-audio-server
- **Summary:** PulseAudio based server to provide audio data over the local network.
- **Topics:** node
- **Pushed:** 2022-12-17

### wes-camera-provisioner _Python_

- **URL:** https://github.com/waggle-sensor/wes-camera-provisioner
- **Summary:** WES-Camera-Provisioner
- **Topics:** waggle-edge-stack
- **Pushed:** 2026-04-10

### wes-chirpstack-server _Dockerfile_

- **URL:** https://github.com/waggle-sensor/wes-chirpstack-server
- **Summary:** WES customized implementation of the chirpstack server
- **Topics:** lorawan, waggle-edge-stack
- **Pushed:** 2025-08-21

### wes-chirpstack-tracker _Python_

- **URL:** https://github.com/waggle-sensor/wes-chirpstack-tracker
- **Summary:** Tracks chirpstack records such as devices and keys
- **Topics:** lorawan, waggle-edge-stack
- **Pushed:** 2025-01-22

### wes-data-sharing-service _Python_

- **URL:** https://github.com/waggle-sensor/wes-data-sharing-service
- **Summary:** Node data sharing service
- **Topics:** waggle-edge-stack
- **Pushed:** 2023-01-09

### wes-device-labeler _Python_

- **URL:** https://github.com/waggle-sensor/wes-device-labeler
- **Summary:** WES service which scan devices and updates labels on host node.
- **Topics:** waggle-edge-stack
- **Pushed:** 2024-01-08

### wes-factory _Python_

- **URL:** https://github.com/waggle-sensor/wes-factory
- **Summary:** Specialized WES application to be run in the factory when configuring the Wild Sage Node
- **Topics:** factory, waggle-edge-stack, wildnode
- **Pushed:** 2023-08-25

### wes-gps-server _Dockerfile_

- **URL:** https://github.com/waggle-sensor/wes-gps-server
- **Summary:** GPS server to provide GPS data over kubernetes network
- **Topics:** waggle-edge-stack
- **Pushed:** 2022-12-17

### wes-lorawan-device-templates _fork, JavaScript_ _fork_

- **URL:** https://github.com/waggle-sensor/wes-lorawan-device-templates
- **Summary:** Device Template Repository for LoRaWAN devices
- **Pushed:** 2025-10-16
- **Note:** fork

### wes-metrics-agent _Python_

- **URL:** https://github.com/waggle-sensor/wes-metrics-agent
- **Summary:** Metrics agent which collects metrics across devices on WES.
- **Topics:** waggle-edge-stack
- **Pushed:** 2025-02-26

### wes-playback-server _Go_

- **URL:** https://github.com/waggle-sensor/wes-playback-server
- **Summary:** Mock-up of simple playback server. Serves static files over HTTP interface.
- **Topics:** waggle-edge-stack
- **Pushed:** 2022-12-17

### wes-sftp-server _Shell_

- **URL:** https://github.com/waggle-sensor/wes-sftp-server
- **Summary:** Prototype SFTP server isolated to a container.
- **Pushed:** 2023-05-05

### wes-updater

- **URL:** https://github.com/waggle-sensor/wes-updater
- **Summary:** WES service responsible for updating all the WES services on a node
- **Topics:** waggle-edge-stack
- **Pushed:** 2022-11-29

### wes-upload-agent _Shell_

- **URL:** https://github.com/waggle-sensor/wes-upload-agent
- **Summary:** Agent which runs on the nodes to move training data to beehive.
- **Topics:** waggle-edge-stack
- **Pushed:** 2024-04-16

### wglctl _Go_

- **URL:** https://github.com/waggle-sensor/wglctl
- **Summary:** Prototype of a cli for controlling waggle
- **Pushed:** 2025-02-27

### wild-waggle-node

- **URL:** https://github.com/waggle-sensor/wild-waggle-node
- **Summary:** Wild Waggle Nodes are weatherized for remote, outdoor deployment in remote and hard-to-reach locations.
- **Topics:** docs, node, wildnode
- **Pushed:** 2022-09-12

### wildnode-cboot _C_

- **URL:** https://github.com/waggle-sensor/wildnode-cboot
- **Summary:** Wild Waggle Node NVidia Jetson Xavier NX CBoot Source.
- **Topics:** node, wildnode
- **Pushed:** 2022-09-09

### wildnode-image _Shell_

- **URL:** https://github.com/waggle-sensor/wildnode-image
- **Summary:** Open source code to build the base Wild Waggle Node OS image
- **Topics:** node, wildnode
- **Pushed:** 2024-01-30

### wildnode-kernel-releases

- **URL:** https://github.com/waggle-sensor/wildnode-kernel-releases
- **Summary:** Public Releases for Wild Waggle Node NVidia / CTI L4T BSP Source
- **Topics:** node, wildnode
- **Pushed:** 2022-09-07

### wildnode-switch-config

- **URL:** https://github.com/waggle-sensor/wildnode-switch-config
- **Summary:** Contains configuration files and firmware used when provisioning the Wild Waggle Node Unifi network switch
- **Pushed:** 2022-09-13

## ECR, scheduling helpers & science rules (5)

### ecr-docker-registry-auth _Go_

- **URL:** https://github.com/waggle-sensor/ecr-docker-registry-auth
- **Summary:** Sage auth backend for Docker Registry v2
- **Pushed:** 2023-02-02

### ecr-jenkins _Dockerfile_

- **URL:** https://github.com/waggle-sensor/ecr-jenkins
- **Summary:** Jenkins with additional tools and plugins needed to support ECR CI pipeline.
- **Pushed:** 2023-02-02

### edge-plugins _Python_

- **URL:** https://github.com/waggle-sensor/edge-plugins
- **Summary:** Waggle edge node plugins for collecting and analyzing sensor data
- **Pushed:** 2023-02-07

### sage-ecr _Python_

- **URL:** https://github.com/waggle-sensor/sage-ecr
- **Summary:** SAGE Edge Code Repository
- **Pushed:** 2023-05-11

### sciencerule-checker _Jupyter Notebook_

- **URL:** https://github.com/waggle-sensor/sciencerule-checker
- **Summary:** Sciencerule Checker
- **Pushed:** 2022-12-17

## Plugin / edge app templates & hellos (8)

### cookiecutter-HuggingFace-DatasetLoadingScript _Python_

- **URL:** https://github.com/waggle-sensor/cookiecutter-HuggingFace-DatasetLoadingScript
- **Summary:** A cookie cutter template that generates a starting dataset loading script to use in HuggingFace
- **Pushed:** 2023-09-11

### cookiecutter-sage-app _Python_

- **URL:** https://github.com/waggle-sensor/cookiecutter-sage-app
- **Summary:** A cookiecutter template for starting a Sage app.
- **Pushed:** 2023-08-21

### ollama-hello-world-app _Python_

- **URL:** https://github.com/waggle-sensor/ollama-hello-world-app
- **Summary:** Hello world example to test Ollama inference and publish pipeline.
- **Pushed:** 2026-06-25

### plugin-file-uploader _Python_

- **URL:** https://github.com/waggle-sensor/plugin-file-uploader
- **Summary:** Edge App Template
- **Pushed:** 2025-04-18

### plugin-generic-template _Python_

- **URL:** https://github.com/waggle-sensor/plugin-generic-template
- **Summary:** plugin-generic-template
- **Pushed:** 2021-12-04

### plugin-hello-world _Dockerfile_

- **URL:** https://github.com/waggle-sensor/plugin-hello-world
- **Summary:** Tutorial Example: Publish Hello World
- **Pushed:** 2022-03-02

### plugin-helloworld-ml _Python_

- **URL:** https://github.com/waggle-sensor/plugin-helloworld-ml
- **Summary:** A template for applications running on Waggle nodes
- **Topics:** plugin, machine-learning
- **Pushed:** 2023-04-13

### Simple_Flower_Example _Jupyter Notebook_

- **URL:** https://github.com/waggle-sensor/Simple_Flower_Example
- **Summary:** Simple Flower Example
- **Pushed:** 2024-11-04

## Plugins & apps — vision, ML, PTZ, image search (42)

### ai-tools _Python_

- **URL:** https://github.com/waggle-sensor/ai-tools
- **Summary:** Collection of tools for exploring AI/ML problems.
- **Pushed:** 2021-10-21

### anomaly-detection _Jupyter Notebook_

- **URL:** https://github.com/waggle-sensor/anomaly-detection
- **Summary:** Some Jupyter Notebooks with encoding models for image anomaly detection
- **Pushed:** 2021-08-05

### app-image-viewer _Python_

- **URL:** https://github.com/waggle-sensor/app-image-viewer
- **Summary:** Simple example of using data and storage API to explore Sage data.
- **Pushed:** 2022-12-16

### Cloud-Optical-Flow _Python_

- **URL:** https://github.com/waggle-sensor/Cloud-Optical-Flow
- **Summary:** Using sky Imager Movies and Optical Flow to determine cloud speed.
- **Pushed:** 2021-08-06

### computer_vision _HTML_

- **URL:** https://github.com/waggle-sensor/computer_vision
- **Summary:** computer_vision
- **Pushed:** 2019-03-29

### HFSandbox _Python_

- **URL:** https://github.com/waggle-sensor/HFSandbox
- **Summary:** Repository for testing HF models on nodes
- **Pushed:** 2025-01-07

### imsearch_benchmaker _Python_

- **URL:** https://github.com/waggle-sensor/imsearch_benchmaker
- **Summary:** Image Search Benchmark Maker is a tool for creating image retrieval benchmarks.
- **Pushed:** 2026-02-27

### imsearch_benchmarks _Python_

- **URL:** https://github.com/waggle-sensor/imsearch_benchmarks
- **Summary:** A repository holding benchmarks created to be used on Sage Image Search
- **Pushed:** 2026-03-07

### imsearch_eval _Python_

- **URL:** https://github.com/waggle-sensor/imsearch_eval
- **Summary:** Abstract, extensible framework for benchmarking vector databases and models across different datasets for Sage Image Search.
- **Pushed:** 2026-04-09

### labelbox-tools _Python_

- **URL:** https://github.com/waggle-sensor/labelbox-tools
- **Summary:** This repo contains tools for managing projects and datasets on Labelbox.
- **Pushed:** 2022-05-09

### machinelearning _Jupyter Notebook_

- **URL:** https://github.com/waggle-sensor/machinelearning
- **Summary:** machinelearning
- **Pushed:** 2021-06-02

### ml-neon-snow _Python_

- **URL:** https://github.com/waggle-sensor/ml-neon-snow
- **Summary:** Tools related to NEON snow image data.
- **Pushed:** 2021-02-02

### plugin-anomaly-detector _Python_

- **URL:** https://github.com/waggle-sensor/plugin-anomaly-detector
- **Summary:** General Purpose Image Anomaly Detector
- **Pushed:** 2021-08-03

### plugin-cloud-cover _Python_

- **URL:** https://github.com/waggle-sensor/plugin-cloud-cover
- **Summary:** Clouds have been widely studied in a variety of fields. The shape and distribution of clouds are not only important in modeling climate and weather, but also toward understanding the interactions between aerosols and clouds in weather research, and also to develop environment…
- **Pushed:** 2025-12-22

### plugin-cloudcover _Python_

- **URL:** https://github.com/waggle-sensor/plugin-cloudcover
- **Summary:** A cloud coverage estimator using machine learning models
- **Pushed:** 2021-05-16

### plugin-irradiance _Python_

- **URL:** https://github.com/waggle-sensor/plugin-irradiance
- **Summary:** plugin-FCN-cloud
- **Pushed:** 2020-09-04

### plugin-motion-analysis _Python_

- **URL:** https://github.com/waggle-sensor/plugin-motion-analysis
- **Summary:** Water Segmentation Plugin
- **Pushed:** 2024-08-14

### plugin-motion-detector _Jupyter Notebook_

- **URL:** https://github.com/waggle-sensor/plugin-motion-detector
- **Summary:** Simple motion detector plugin.
- **Pushed:** 2022-12-17

### plugin-object-counter-yolov7 _Python_

- **URL:** https://github.com/waggle-sensor/plugin-object-counter-yolov7
- **Summary:** plugin-object-counter-yolov7
- **Pushed:** 2022-11-02

### plugin-objectcounter _Python_

- **URL:** https://github.com/waggle-sensor/plugin-objectcounter
- **Summary:** Car and pedestrian counter plugin
- **Pushed:** 2022-12-17

### plugin-pole-detector _Python_

- **URL:** https://github.com/waggle-sensor/plugin-pole-detector
- **Summary:** NEON Pole / Snow Rod Detection
- **Pushed:** 2021-08-06

### plugin-solar-controller _Python_

- **URL:** https://github.com/waggle-sensor/plugin-solar-controller
- **Summary:** Plugin for obtaining metrics from a solar charge controller
- **Pushed:** 2024-06-19

### plugin-solar-irradiance _Python_

- **URL:** https://github.com/waggle-sensor/plugin-solar-irradiance
- **Summary:** Background
- **Pushed:** 2022-11-21

### plugin-solarcloud _Python_

- **URL:** https://github.com/waggle-sensor/plugin-solarcloud
- **Summary:** Cloud Coverage Estimator
- **Pushed:** 2021-05-17

### plugin-surface-water-detection _Python_

- **URL:** https://github.com/waggle-sensor/plugin-surface-water-detection
- **Summary:** Author: Kazuto Nakashima,
- **Pushed:** 2024-08-15

### plugin-surfacewater _Python_

- **URL:** https://github.com/waggle-sensor/plugin-surfacewater
- **Summary:** plugin-surfacewater
- **Pushed:** 2023-08-30

### plugin-trafficcounter _Python_

- **URL:** https://github.com/waggle-sensor/plugin-trafficcounter
- **Summary:** Traffic Counter
- **Pushed:** 2025-03-24

### plugin-trafficstate _Python_

- **URL:** https://github.com/waggle-sensor/plugin-trafficstate
- **Summary:** Traffic state estimator
- **Pushed:** 2024-06-30

### plugin-vehicle-type-identifier _Python_

- **URL:** https://github.com/waggle-sensor/plugin-vehicle-type-identifier
- **Summary:** plugin-vehicle-detecter
- **Pushed:** 2023-08-31

### plugin-water-depth _Jupyter Notebook_

- **URL:** https://github.com/waggle-sensor/plugin-water-depth
- **Summary:** Water Depth
- **Pushed:** 2022-12-18

### plugin-water-morph _Jupyter Notebook_

- **URL:** https://github.com/waggle-sensor/plugin-water-morph
- **Summary:** plugin-water-level
- **Pushed:** 2022-04-18

### plugin-wildfire-smoke-detection _Jupyter Notebook_

- **URL:** https://github.com/waggle-sensor/plugin-wildfire-smoke-detection
- **Summary:** sage-smoke-detection
- **Pushed:** 2022-01-04

### ptz-app _Python_

- **URL:** https://github.com/waggle-sensor/ptz-app
- **Summary:** This is an application for sending images of specific objects autonomously using PTZ cameras.
- **Pushed:** 2026-03-04

### ptz-sampler _Python_

- **URL:** https://github.com/waggle-sensor/ptz-sampler
- **Summary:** This is a plugin for sampling images from a ptz camera
- **Pushed:** 2024-06-12

### ptzjepa _Python_

- **URL:** https://github.com/waggle-sensor/ptzjepa
- **Summary:** Pan Tilt Zoom Joint Embedding Predictive Architecture (PTZJEPA)
- **Pushed:** 2025-02-20

### sage-nrp-image-search _fork, Jupyter Notebook_ _fork_

- **URL:** https://github.com/waggle-sensor/sage-nrp-image-search
- **Summary:** Sage Image Search on NRP
- **Pushed:** 2026-07-15
- **Note:** fork

### sage-smoke-detection _fork, Jupyter Notebook_ _fork_

- **URL:** https://github.com/waggle-sensor/sage-smoke-detection
- **Summary:** sage-smoke-detection
- **Pushed:** 2022-04-06
- **Note:** fork

### sage-vectordb-example _Jupyter Notebook_

- **URL:** https://github.com/waggle-sensor/sage-vectordb-example
- **Summary:** Examples using Sage w/Weaviate
- **Pushed:** 2025-12-15

### solar-irradiance-estimation _Python_

- **URL:** https://github.com/waggle-sensor/solar-irradiance-estimation
- **Summary:** Training
- **Pushed:** 2021-03-31

### traffic-state _Jupyter Notebook_

- **URL:** https://github.com/waggle-sensor/traffic-state
- **Summary:** - Functions for YOLOv4 are in the foler `tool`.  
- **Pushed:** 2021-05-18

### visual_disorder_plugin _Python_

- **URL:** https://github.com/waggle-sensor/visual_disorder_plugin
- **Summary:** Visual disorder app. Originally written by @Samaah330 and archived in waggle-sensor repo.
- **Pushed:** 2025-03-24

### VL_Correctness

- **URL:** https://github.com/waggle-sensor/VL_Correctness
- **Summary:** VL_Correctness
- **Pushed:** 2024-09-12

## Plugins & apps — audio, weather, sensors, triggers (42)

### app_birdcall_detector

- **URL:** https://github.com/waggle-sensor/app_birdcall_detector
- **Summary:** BirdCalls
- **Pushed:** 2021-05-14

### application-profiling _Python_

- **URL:** https://github.com/waggle-sensor/application-profiling
- **Summary:** Waggle Application Profiler (WaAP)
- **Pushed:** 2022-07-28

### goes-data _Python_

- **URL:** https://github.com/waggle-sensor/goes-data
- **Summary:** Plugin for GOES 16
- **Pushed:** 2021-08-05

### KonzaBurn _Jupyter Notebook_

- **URL:** https://github.com/waggle-sensor/KonzaBurn
- **Summary:** Some jupyter notebooks for showing classification of wildfire using Llava on our Konza controlled burn images
- **Pushed:** 2025-01-07

### mobotix-setup _Shell_

- **URL:** https://github.com/waggle-sensor/mobotix-setup
- **Summary:** This repository has codes and config to setup the Mobotix M16 Thermal Camera.
- **Pushed:** 2025-01-27

### NEXRAD-reflectivity _Python_

- **URL:** https://github.com/waggle-sensor/NEXRAD-reflectivity
- **Summary:** This is a simple plugin that downloads NEXRAD files from Amazon S3 and extracts vertical profiles of base reflectivity above a selected latitude and longitude.
- **Pushed:** 2021-08-06

### phenocam_download_script _fork, Python_ _fork_

- **URL:** https://github.com/waggle-sensor/phenocam_download_script
- **Summary:** Script to download PhenoCam images
- **Pushed:** 2020-01-17
- **Note:** fork

### plugin-air-quality _Python_

- **URL:** https://github.com/waggle-sensor/plugin-air-quality
- **Summary:** Public repository `plugin-air-quality` (no GitHub description or README summary found).
- **Pushed:** 2022-11-17

### plugin-aqt _fork, Python_ _fork_

- **URL:** https://github.com/waggle-sensor/plugin-aqt
- **Summary:** Waggle Sensor Plug-In for the Vaisala AQT530 Series Air Quality Transmitter
- **Pushed:** 2023-12-05
- **Note:** fork

### plugin-audio-sampler _Python_

- **URL:** https://github.com/waggle-sensor/plugin-audio-sampler
- **Summary:** Simple plugin which creates and uploads short audio clips.
- **Pushed:** 2022-12-17

### plugin-base-images _Dockerfile_

- **URL:** https://github.com/waggle-sensor/plugin-base-images
- **Summary:** Dockerfiles and build processes for plugin base images
- **Pushed:** 2024-06-13

### plugin-bird-song-classifier _Python_

- **URL:** https://github.com/waggle-sensor/plugin-bird-song-classifier
- **Summary:** Bird song Classifier
- **Pushed:** 2021-09-08

### plugin-cl61-plot _Python_

- **URL:** https://github.com/waggle-sensor/plugin-cl61-plot
- **Summary:** Uploads files from a waggle node home folder to beehive.
- **Pushed:** 2025-05-08

### plugin-cmv-fftpc _Python_

- **URL:** https://github.com/waggle-sensor/plugin-cmv-fftpc
- **Summary:** The plugin uses the phase correlation/Optical flow method to compute cloud motion vectors from the Waggle sky camera images.
- **Pushed:** 2025-08-07

### plugin-controller _Go_

- **URL:** https://github.com/waggle-sensor/plugin-controller
- **Summary:** Plugin Controller
- **Pushed:** 2024-05-14

### plugin-hut-monitoring _C++_

- **URL:** https://github.com/waggle-sensor/plugin-hut-monitoring
- **Summary:** Hut monitoring plugin
- **Pushed:** 2024-02-02

### plugin-iio _Python_

- **URL:** https://github.com/waggle-sensor/plugin-iio
- **Summary:** Plugin which scans and publishes all detected Linux IIO parameters.
- **Topics:** node
- **Pushed:** 2023-01-18

### plugin-image-captioning _Python_

- **URL:** https://github.com/waggle-sensor/plugin-image-captioning
- **Summary:** A Waggle plugin captioning images using large language models
- **Pushed:** 2024-08-30

### plugin-imagesampler _Python_

- **URL:** https://github.com/waggle-sensor/plugin-imagesampler
- **Summary:** A simple plugin that samples images from a stream
- **Pushed:** 2025-01-22

### plugin-licor-7500ds _Python_

- **URL:** https://github.com/waggle-sensor/plugin-licor-7500ds
- **Summary:** uploads data as csv files
- **Pushed:** 2025-03-11

### plugin-licor-smartflux _Python_

- **URL:** https://github.com/waggle-sensor/plugin-licor-smartflux
- **Summary:** Data retrieval from Licor SmartFlux enabling real-time environmental data processing @Edge.
- **Pushed:** 2025-05-08

### plugin-metek-sonic3d-sampler _Python_

- **URL:** https://github.com/waggle-sensor/plugin-metek-sonic3d-sampler
- **Summary:** Plugin for METEK Sonic3D
- **Pushed:** 2025-02-10

### plugin-metek-sonic3d-tcp _Python_

- **URL:** https://github.com/waggle-sensor/plugin-metek-sonic3d-tcp
- **Summary:** Sampling Metek Data on TCP connection
- **Pushed:** 2024-07-26

### plugin-metsense _Python_

- **URL:** https://github.com/waggle-sensor/plugin-metsense
- **Summary:** Plugin which uses BME680 sensor to provide basic meteorological data.
- **Pushed:** 2021-06-03

### plugin-mobotix-move _Python_

- **URL:** https://github.com/waggle-sensor/plugin-mobotix-move
- **Summary:** Move a Mobotix camera to a specified preset location.
- **Pushed:** 2023-03-03

### plugin-mobotix-sampler _C++_

- **URL:** https://github.com/waggle-sensor/plugin-mobotix-sampler
- **Summary:** Plugin to sample the image and thermal data from the Mobotix camera
- **Pushed:** 2023-02-23

### plugin-mobotix-scan _C++_

- **URL:** https://github.com/waggle-sensor/plugin-mobotix-scan
- **Summary:** Testing object oriented code for thermal camera scanning
- **Pushed:** 2024-08-22

### plugin-radar-optical-flow _Jupyter Notebook_

- **URL:** https://github.com/waggle-sensor/plugin-radar-optical-flow
- **Summary:** The code in `radar_data_processing.ipynb` allows users to:
- **Pushed:** 2021-08-23

### plugin-raingauge _Python_

- **URL:** https://github.com/waggle-sensor/plugin-raingauge
- **Summary:** Plugin which reads rain gauge values
- **Topics:** raspberry-pi, node
- **Pushed:** 2022-12-17

### plugin-rideshare _fork, Python_ _fork_

- **URL:** https://github.com/waggle-sensor/plugin-rideshare
- **Summary:** Sage rideshare detection plugin for AI at the Edge
- **Pushed:** 2023-07-27
- **Note:** fork

### plugin-sdr-sampler _fork, Python_ _fork_

- **URL:** https://github.com/waggle-sensor/plugin-sdr-sampler
- **Summary:** SDR sampler to detect RF anomalies.
- **Pushed:** 2023-08-01
- **Note:** fork

### plugin-sonic3d-rmyong _Python_

- **URL:** https://github.com/waggle-sensor/plugin-sonic3d-rmyong
- **Summary:** RMYong Sonic 3D Anemometer Sampler
- **Pushed:** 2024-01-25

### plugin-test-pipeline _Python_

- **URL:** https://github.com/waggle-sensor/plugin-test-pipeline
- **Summary:** Plugin to help smoke test our data pipeline.
- **Pushed:** 2025-02-20

### plugin-test-subscribe _Python_

- **URL:** https://github.com/waggle-sensor/plugin-test-subscribe
- **Summary:** Internal plugin to help perform system testing of Waggle Edge Stack.
- **Pushed:** 2022-01-20

### plugin-videosampler _Python_

- **URL:** https://github.com/waggle-sensor/plugin-videosampler
- **Summary:** Video Sampler Plugin
- **Pushed:** 2022-12-17

### plugin-wxt536 _fork, Python_ _fork_

- **URL:** https://github.com/waggle-sensor/plugin-wxt536
- **Summary:** Waggle Sensor Plug-In for the Vaisala WXT536 Series weather transmitter
- **Pushed:** 2023-12-05
- **Note:** fork

### plugin-yamnet _fork, Python_ _fork_

- **URL:** https://github.com/waggle-sensor/plugin-yamnet
- **Summary:** SAGE plugin for YAMNet audio classification model
- **Pushed:** 2024-08-13
- **Note:** fork

### sensors _HTML_

- **URL:** https://github.com/waggle-sensor/sensors
- **Summary:** Sensors integrated into Waggle
- **Pushed:** 2019-04-25

### severe-weather-trigger-example _Python_

- **URL:** https://github.com/waggle-sensor/severe-weather-trigger-example
- **Summary:** Example of using National Weather Service API to trigger starting / stopping a job.
- **Pushed:** 2023-11-02

### sonic-3d-sampler _Python_

- **URL:** https://github.com/waggle-sensor/sonic-3d-sampler
- **Summary:** Public repository `sonic-3d-sampler` (no GitHub description or README summary found).
- **Pushed:** 2023-02-15

### waggle-sonic3d _fork, Python_ _fork_

- **URL:** https://github.com/waggle-sensor/waggle-sonic3d
- **Summary:** Waggle Sensor Plug-In for the METEK Sonic 3D anemometer
- **Pushed:** 2023-07-20
- **Note:** fork

### wildfire-trigger-example _Python_

- **URL:** https://github.com/waggle-sensor/wildfire-trigger-example
- **Summary:** Wildfire Detection Workflow Example
- **Pushed:** 2023-06-15

## LoRaWAN (5)

### chirpstack_api_wrapper _Python_

- **URL:** https://github.com/waggle-sensor/chirpstack_api_wrapper
- **Summary:** An abstraction layer over the chirpstack_api python library
- **Topics:** lorawan, chirpstack
- **Pushed:** 2025-05-30

### init-chirpstack-server _Python_

- **URL:** https://github.com/waggle-sensor/init-chirpstack-server
- **Summary:** docker image for init chirpstack server job
- **Topics:** lorawan, chirpstack
- **Pushed:** 2024-04-25

### Lorawan-Packet-Test _Jupyter Notebook_

- **URL:** https://github.com/waggle-sensor/Lorawan-Packet-Test
- **Summary:** This repo holds the assets we used to conduct a Lorawan Packet test on our rpi.lorawan compute
- **Pushed:** 2025-07-22

### Lorawan-test-device _C++_

- **URL:** https://github.com/waggle-sensor/Lorawan-test-device
- **Summary:** A device used to test Lorawan on WSN or rpi_lorawan WSN modules
- **Topics:** lorawan
- **Pushed:** 2025-05-29

### waggle-lorawan _Python_

- **URL:** https://github.com/waggle-sensor/waggle-lorawan
- **Summary:** Waggle LoRaWAN Usage Instructions
- **Pushed:** 2024-06-06

## Docs, websites, camps & notebooks (15)

### BCN-demos _Python_

- **URL:** https://github.com/waggle-sensor/BCN-demos
- **Summary:** Demo instructions
- **Pushed:** 2026-05-02

### community

- **URL:** https://github.com/waggle-sensor/community
- **Summary:** Repo dedicated to Waggle community discussions!
- **Pushed:** 2023-04-17

### documents

- **URL:** https://github.com/waggle-sensor/documents
- **Summary:** Papers, presentation material (PPT slides, PDF decks) and posters go here.
- **Pushed:** 2018-08-22

### jupyter-training-example _Jupyter Notebook_

- **URL:** https://github.com/waggle-sensor/jupyter-training-example
- **Summary:** Model Training Example on Jupyter
- **Pushed:** 2024-06-10

### publications _TeX_

- **URL:** https://github.com/waggle-sensor/publications
- **Summary:** Papers, posters and publications by the team go here.
- **Topics:** papers, posters, presentation-slides
- **Pushed:** 2021-09-03

### sage-science-notebooks _Jupyter Notebook_

- **URL:** https://github.com/waggle-sensor/sage-science-notebooks
- **Summary:** Collections of notebooks and tutorials using sage_data_client and beehive
- **Pushed:** 2025-12-19

### sage-website _HTML_

- **URL:** https://github.com/waggle-sensor/sage-website
- **Summary:** sagecontinuum.org (docs & tutorials)
- **Pushed:** 2026-07-16

### spring2025 _Python_

- **URL:** https://github.com/waggle-sensor/spring2025
- **Summary:** spring2025
- **Pushed:** 2025-05-01

### summer-camp-2026 _Python_

- **URL:** https://github.com/waggle-sensor/summer-camp-2026
- **Summary:** Workspace for Summer of AI 2026
- **Pushed:** 2026-07-17

### summer2022 _Jupyter Notebook_

- **URL:** https://github.com/waggle-sensor/summer2022
- **Summary:** Summer 2022 Interns Repo
- **Pushed:** 2023-07-28

### summer2023 _Jupyter Notebook_

- **URL:** https://github.com/waggle-sensor/summer2023
- **Summary:** Summer 2023 Student Repo
- **Pushed:** 2025-01-29

### summer2024 _Jupyter Notebook_

- **URL:** https://github.com/waggle-sensor/summer2024
- **Summary:** Getting Started
- **Pushed:** 2024-09-16

### summer2025 _Jupyter Notebook_

- **URL:** https://github.com/waggle-sensor/summer2025
- **Summary:** Summer Student Repository
- **Pushed:** 2025-10-06

### waggle-docs _HTML_

- **URL:** https://github.com/waggle-sensor/waggle-docs
- **Summary:** Waggle Documentation/Tutorial Website
- **Topics:** docs
- **Pushed:** 2023-05-24

### waggle-sensor.github.io

- **URL:** https://github.com/waggle-sensor/waggle-sensor.github.io
- **Summary:** Webpage
- **Pushed:** 2025-06-23

## Auth, VPN, storage, registry & ops tooling (19)

### ansible-pull-test

- **URL:** https://github.com/waggle-sensor/ansible-pull-test
- **Summary:** Public repository `ansible-pull-test` (no GitHub description or README summary found).
- **Pushed:** 2023-10-31

### django-address _fork, Python_ _fork_

- **URL:** https://github.com/waggle-sensor/django-address
- **Summary:** A Django address model and field. Addresses may be specified by address components or by performing an automatic Google Maps lookup.
- **Pushed:** 2024-03-19
- **Note:** fork

### hpwren-mirror _Python_

- **URL:** https://github.com/waggle-sensor/hpwren-mirror
- **Summary:** hpwren-mirror
- **Pushed:** 2020-01-27

### node-influxdb-loader _Python_

- **URL:** https://github.com/waggle-sensor/node-influxdb-loader
- **Summary:** Public repository `node-influxdb-loader` (no GitHub description or README summary found).
- **Topics:** waggle-edge-stack
- **Pushed:** 2025-04-09

### padm-pdu _Python_

- **URL:** https://github.com/waggle-sensor/padm-pdu
- **Summary:** Power Distribution Unit (PDU) Controller
- **Pushed:** 2025-11-03

### pandawn _Python_

- **URL:** https://github.com/waggle-sensor/pandawn
- **Summary:** Codes associated specifically with the PANDA-DAWN datasets
- **Pushed:** 2024-03-23

### portal-notice

- **URL:** https://github.com/waggle-sensor/portal-notice
- **Summary:** Adds banner to Sage portal
- **Pushed:** 2025-09-06

### sage-storage-loader _Go_

- **URL:** https://github.com/waggle-sensor/sage-storage-loader
- **Summary:** Load files from filesystem into SAGE object store
- **Pushed:** 2026-06-18

### sage-vpn-user-tools _Shell_

- **URL:** https://github.com/waggle-sensor/sage-vpn-user-tools
- **Summary:** User facing tools for Sage VPN.
- **Pushed:** 2026-06-09

### sheets2json _Go_

- **URL:** https://github.com/waggle-sensor/sheets2json
- **Summary:** JSON API to serve google sheets table
- **Pushed:** 2022-01-14

### unifi_switch_client _Python_

- **URL:** https://github.com/waggle-sensor/unifi_switch_client
- **Summary:** Python Client for Unifi EdgeSwitch 8 150W
- **Pushed:** 2023-09-26

### update-rabbitmq-users-from-beekeeper _Python_

- **URL:** https://github.com/waggle-sensor/update-rabbitmq-users-from-beekeeper
- **Summary:** Job to update RabbitMQ users from a Beekeeper.
- **Topics:** beehive, beekeeper
- **Pushed:** 2025-08-26

### update-upload-server-users-from-beekeeper _Python_

- **URL:** https://github.com/waggle-sensor/update-upload-server-users-from-beekeeper
- **Summary:** Job to update an upload server's users from a Beekeeper.
- **Topics:** beehive, beekeeper
- **Pushed:** 2022-12-16

### waggle-auth-app _Python_

- **URL:** https://github.com/waggle-sensor/waggle-auth-app
- **Summary:** Prototype space of Waggle auth app. Intend to merge work with sage-auth.
- **Pushed:** 2026-03-01

### waggle-network-watchdog _Python_

- **URL:** https://github.com/waggle-sensor/waggle-network-watchdog
- **Summary:** Waggle Network Watchdog
- **Topics:** node, deb, wildnode
- **Pushed:** 2025-06-05

### waggle-pki-tools _Shell_

- **URL:** https://github.com/waggle-sensor/waggle-pki-tools
- **Summary:** Toolchain for building TLS and SSH PKIs.
- **Pushed:** 2025-10-27

### waggle-sanity-check _Shell_

- **URL:** https://github.com/waggle-sensor/waggle-sanity-check
- **Summary:** Waggle Sanity Check
- **Topics:** node, deb, wildnode
- **Pushed:** 2023-10-30

### zabbix-configs _Shell_

- **URL:** https://github.com/waggle-sensor/zabbix-configs
- **Summary:** Public repository `zabbix-configs` (no GitHub description or README summary found).
- **Pushed:** 2022-10-25

### zabbix-server-pgsql _Dockerfile_

- **URL:** https://github.com/waggle-sensor/zabbix-server-pgsql
- **Summary:** Customized Zabbix server image which provides additional tools.
- **Pushed:** 2022-12-16

## Org meta (1)

### .github

- **URL:** https://github.com/waggle-sensor/.github
- **Summary:** Repo for shared workflows and Github actions
- **Pushed:** 2025-08-19

## Other repositories (1)

### HPWREN_Experiments _Jupyter Notebook_

- **URL:** https://github.com/waggle-sensor/HPWREN_Experiments
- **Summary:** Some jupyter notebooks for showing classification of wildfire using Llava on HPWREN images
- **Pushed:** 2025-01-07

## Refresh

```bash
# Paginate — org has 100+ public repos
page=1
while true; do
  code=$(curl -sS -o "/tmp/waggle-repos-page-$page.json" -w "%{http_code}" \
    "https://api.github.com/orgs/waggle-sensor/repos?type=public&per_page=100&page=$page&sort=full_name" \
    -H "Accept: application/vnd.github+json" -H "User-Agent: sage-camp-index")
  [ "$code" = "200" ] || break
  n=$(python3 -c "import json; print(len(json.load(open('/tmp/waggle-repos-page-$page.json'))))")
  [ "$n" = "0" ] && break
  echo "page $page: $n repos"
  page=$((page+1))
done
```

`type=public` ensures private org repos are never listed. This file is a curated category index (220 repos); the API may list additional public repos — merge new names into categories when refreshing.


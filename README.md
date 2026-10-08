# AeroPulse India — Bharat AirShield™ Environmental Intelligence Platform (AWS Dummy)

[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
[![Status: Production](https://img.shields.io/badge/Status-Operational-brightgreen.svg)]()
[![AirShield: v2.4](https://img.shields.io/badge/AirShield-Suite%20v2.4-blue.svg)]()

> **AeroPulse India** is an enterprise-grade National Environmental Command Center and real-time air telemetry intelligence platform. Engineered with the **Bharat AirShield™** suite for the Bharat Builds Initiative, it delivers predictive exposure analytics, biomass smoke dispersion mapping, institutional safety protocols, and low-exposure navigation across India's monitored urban hubs.

---

## 🚀 Key Modules (Bharat AirShield™ Suite)

### 1. 🧬 Personal Pollution Exposure Twin & Exposure Budget
- **Micro-Environment Telemetry**: Dynamic intake calculations across AC Metro, Open Two-Wheelers/Autos, Office environments, and outdoor sports.
- **Biometric Particulate Dosage**: Real-time calculation of daily inhaled PM2.5 ($\mu\text{g}$) calibrated against the **WHO Safe Daily Standard (15 $\mu\text{g}/\text{m}^3$)**.
- Dynamic risk tier badges (*Minimal*, *Moderate*, *High*, *Hazardous Overload*).

### 2. 🏫 Smart School Air Guardian
- **District-Level Institutional Safety**: Automated protocol generator for school districts across Delhi-NCR, Bengaluru, Mumbai, and Lucknow.
- **Dynamic Action Directives**: Automated toggles for Morning Assemblies (Outdoor vs Indoor Auditorium), Sports/P.E., and Classroom Ventilation.
- **1-Click Official Notice Generator**: Formats and copies a formal institutional safety circular directly to the clipboard.

### 3. 🔥 Stubble Burning / Biomass Smoke Attribution
- **Satellite Thermal Anomaly Clusters**: Visualizes active fire clusters across the Punjab-Haryana agricultural corridor.
- **Dynamic Dispersion Plume**: Renders North-West to South-East atmospheric transport plumes entering the Indo-Gangetic Plain and Delhi-NCR.
- **Attribution Matrix**: Source decomposition: **38.4% Stubble Burning**, **28.6% Vehicular**, **18.2% Industrial**, and **14.8% Road Dust**.

### 4. 🏠 Indoor Air Quality & Infiltration Estimator
- **Enclosure Penetration Engine**: Estimates indoor PM2.5 levels based on structural sealing and filtration status (HEPA True Purifiers vs Non-Filtered).
- **Ventilation Window Optimizer**: Recommends safe natural air exchange windows (e.g., 1:30 PM – 3:30 PM) during minimum ground temperature inversions.

### 5. 🗺️ Clean-Air / Low-Exposure Google Maps Route Navigation
- **Dual Corridor Comparison**:
  - **Route A (Fastest Ring Road)**: 28 mins, Avg AQI **148 $\mu\text{g}/\text{m}^3$** (*Severe Exposure*).
  - **Route B (Clean Air Corridor / Ridge Green Belt)**: 34 mins (+6 mins), Avg AQI **74 $\mu\text{g}/\text{m}^3$** (**45% Cleaner Air**).
- Interactive polyline layers with real-time exposure difference badges.

---

## 🛠️ Tech Stack & Architecture

- **Frontend**: Vanilla HTML5, CSS3 Glassmorphism UI, Responsive Viewports (Dark / Light Cyberpunk Modes).
- **Mapping & GIS**: Leaflet.js with Google Maps Hybrid/Road Tiles, GeoJSON boundary layers, custom canvas particle animations.
- **Telemetry & Models**: Weighted Least Squares (WLS) Linear Algebra model, real-time NAQI multi-pollutant index calculations.
- **Planned AWS Cloud Architecture**:
  - **AWS IoT Core**: High-frequency sensor telemetry ingestion.
  - **Amazon SageMaker**: Continuous multi-variate air dispersion & plume forecasting.
  - **AWS Lambda & DynamoDB**: Serverless API routing and persistent station logs.
  - **Amazon Bedrock**: Automated institutional circular generation & environmental policy advice.

---

## 💻 Quick Start

Simply open `index.html` in any modern web browser:

```bash
# Clone the repository
git clone https://github.com/Adithya-2007/AWS-Dummy.git
cd AWS-Dummy

# Launch locally
start index.html
```

Or run with Python's local server:
```bash
python -m http.server 8080
```
Navigate to `http://localhost:8080` in your browser.

---

## 📄 License
This project is licensed under the MIT License.

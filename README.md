# Project Vulcan: Hybrid Cloud-Edge Digital Twin Orchestrator

### 🔬 Project Overview
[cite_start]Project Vulcan is an end-to-end engineering solution designed to deploy **State-of-the-Art (SOTA) 12B-parameter Diffusion Transformers (Flux.1)** on resource-constrained consumer hardware[cite: 22, 55]. [cite_start]By architecting a hybrid pipeline, we successfully bypassed the **24GB VRAM barrier** of the NVIDIA RTX 4050 (6GB VRAM)[cite: 24, 34].



### 🏗️ Technical Architecture
The system is built on three core pillars of optimization:
1.  [cite_start]**Decoupled Learning (Cloud):** Fine-tuned identity-specific weights (**LoRA**) on Kaggle using Tesla T4 GPUs to handle the high-memory requirements (40GB+) of the training phase[cite: 26, 104].
2.  [cite_start]**Quantization Engineering (Edge):** Implemented **4-bit GGUF (Q4_K_S) quantization**, reducing the model's memory footprint from **23.8GB to 6.8GB**—a **71.4% reduction** in overhead[cite: 176, 178].
3.  [cite_start]**Cross-OS Orchestration Bridge:** A Python-based **WebSocket bridge** (WSL2-to-Windows) that allows for a Linux-native development workflow while accessing bare-metal GPU performance on the host Windows OS[cite: 27, 106].



### 📊 Performance Benchmarks
| Metric | Baseline (FP16) | Optimized (GGUF Q4) | Change |
| :--- | :--- | :--- | :--- |
| **Model Size** | 23.8 GB | 6.8 GB | [cite_start]**-71.4%** [cite: 177, 178] |
| **VRAM Required** | >24 GB | <6 GB | [cite_start]**Hardware Viable** [cite: 23, 105] |
| **Training VRAM** | >40 GB | 16 GB (Cloud) | [cite_start]**Cost Optimized** [cite: 83, 104] |

### 🛠️ Tech Stack
* [cite_start]**Model:** Flux.1-Dev (12B Parameters) [cite: 70, 133]
* [cite_start]**Optimization:** GGUF 4-bit Quantization [cite: 174]
* [cite_start]**Fine-Tuning:** LoRA (Low-Rank Adaptation) [cite: 26, 151]
* [cite_start]**Infrastructure:** WSL2 (Mirrored Mode), ComfyUI API, WebSocket Client [cite: 27, 142]

### 📦 Setup & Asset Management
Due to repository hygiene and file size limitations, large binary weights are excluded from Git. 

#### 1. Host Asset Placement (Windows)
Ensure the following files are present in your ComfyUI directory:
* `models/unet/flux1-dev-Q4_K_S.gguf`
* `models/loras/caitlyn_lifestyle_v1.safetensors`

#### 2. Linux Orchestration (WSL2)
```bash
# Enable Mirrored Networking in .wslconfig for localhost access
# Install dependencies
pip install -r requirements.txt
# Run the Director
python core/director.py
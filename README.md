# 🌿 AyurvedaRAG: Personalized Treatment Intelligence

**Transforming Ancient Wisdom into Data-Driven Health Insights.**

AyurvedaRAG is a state-of-the-art **Retrieval-Augmented Generation (RAG)** system designed to provide personalized Ayurvedic health plans. By bridging the gap between millennium-old Ayurvedic principles and modern AI, this project offers deep insights into condition management through a structured, intelligence-driven approach.

---

## ✨ Key Features

### 🧠 Personalized Treatment Intelligence
- **Condition-Specific Analysis:** Supports targeted Ayurvedic insights for conditions like **Diabetes (Madhumeha)**, **Acidity (Amlapitta)**, **Thyroid (Galaganda)**, and **Anxiety (Chittodvega)**.
- **Custom Condition Support:** Beyond presets, users can enter any health concern, and the system will leverage RAG to provide the most relevant Ayurvedic advice possible.
- **Expert-Backed Logic:** Generates comprehensive plans including herbal recommendations, dietary guidelines, yoga practices, and lifestyle adjustments.
- **Dosha Identification:** Automatically maps health conditions to the primary Doshas (**Vata, Pitta, Kapha**) to ensure constitutional balance.

### 🔍 Advanced RAG Architecture
- **Multi-Collection Retrieval:** Uses **Qdrant** as an ultra-fast vector database to retrieve highly relevant knowledge from multiple specialized collections (Herbs, Yoga, Diet, Lifestyle).
- **Intelligent Contextualization:** Context-aware retrieval ensures that users receive advice tailored specifically to their symptoms and doshic imbalances.

### 📊 Progress Tracking & Evolution
- **Weekly Progress Logs:** Users can track their journey by logging energy levels, digestion quality, sleep, and symptom improvements.
- **Dynamic Progress Reports:** The system analyzes logs over time to generate evolving progress reports, helping users see the impact of their Ayurvedic routine.

### 📄 Premium PDF Reports
- **Professional Exports:** Generate beautifully styled, branded PDF reports of treatment plans for offline access or sharing with practitioners.
- **Rich Content:** Reports include detailed herbal dosages, step-by-step yoga instructions, and critical safety precautions.

### ⚡ Automated Workflows
- **Asynchronous Processing:** Powered by **Inngest**, ensuring long-running tasks like plan generation and progress analysis happen seamlessly in the background without blocking the UI.
- **Knowledge Base Seeding:** Automated tools to populate and update the vector database with the latest Ayurvedic research and classical texts.

---

## 🛠️ Technology Stack

- **Frontend:** [Streamlit](https://streamlit.io/) — A premium, responsive dashboard for health management.
- **Orchestration:** [FastAPI](https://fastapi.tiangolo.com/) — High-performance backend routing.
- **Vector Database:** [Qdrant](https://qdrant.tech/) — For high-dimensional semantic search and retrieval.
- **Workflow Engine:** [Inngest](https://www.inngest.com/) — Event-driven automation and background job management.
- **AI/LLM:** [LlamaIndex](https://www.llamaindex.ai/) & [OpenAI](https://openai.com/) — Advanced RAG orchestration and natural language generation.
- **Reporting:** [fpdf2](https://py-pdf.github.io/fpdf2/) — For server-side, premium PDF generation.

---

## 🛡️ Disclaimer
*This application is for educational and wellness guidance purposes only. AyurvedaRAG is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or a qualified Ayurvedic practitioner with any questions regarding a medical condition.*

---

<p align="center">
  Built with ❤️ for a Healthier World.
</p>

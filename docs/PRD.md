# Lune: Specification v1.0

## Document: Product Requirements Document (PRD) - Core Persona & Interaction

## 1.1 The problem Statement

  **Current Limitations:** The current landscape of language acquisition software relies on rigid, rule-based interactions. These systems fail to teach the "art of communication" specifically how to dynamically adjust tone, vocabulary, and rhetorical structure based on the audience and environmental context.

  **The Friction Point:** Existing conversational agents suffer from static formality. Even when prompted to adopt a relaxed persona, their output remains highly unnatural. This robotic interaction paradigm induces cognitive stress in the suer, raising the affective filter and halting natural language acquisition.

  **The LUNE Solution:** Enter Lune: an autonomous, multimodal conversational agent designed to eliminate learning friction. By utilizing real-time context and focusing on the user's specific technical interests, Lune passively coaches the user in advanced communication frameworks without the stress of a traditional academic environment. The core thesis: Fluency is achieved through low-stress, highly contextual engagement.

## 1.2 Target Audience

  **Primary Demographic:** Individuals who possess a foundational understanding of English (CEFR A2-C1) but require targeted improvement in oral fluency, rhetorical structure, and spontaneous communication.

  **Dynamic Scalability:** The system is intentionally language-level agnostic. By utilizing a Contextual Routing Engine, Lune dynamically scales its pedagogical complexity based on the user's demographic and chosen subject matter:

  **Beginner/Pediatric Level:** When prompted with accessible media (e.g., animation), the system utilizes high-frequency vocabulary and simplified syntactic structures.

  **Academic/Professional Level:** When discussing advanced domains (e.g., AI Research, Mechatronics), the system employs domain-specific lexicons, formal rhetorical frameworks, and sophisticated grammatical feedback.

## 1.3 Functional Requirements (FRs)

  **FR-01: Multimodal Visual Interface (Visemes):** The system must generate and stream real-time 3D facial animations (blendshapes/visemes) synchronized with the audio output to establish visual rapport with the user.

  **FR-02: End-of-Turn Pedagogical Audit:** The agent must employ a non-interruptive correction model. It will engage in natural, friendly dialogue (incorporating humour and relaxed conversational flow) and append a structured grammatical/rhetorical audit only at the conclusion of its conversational turn.

  **FR-03: Agentic Context Retrieval (MCP):** The system must integrate with external APIs via the Model Context Protocol to autonomously retrieve live news and trending topics relevant to the user’s specified interests (e.g., AI Research, Mechatronics).

  **FR-04: Persistent State & Memory (RAG):** The architecture must include a vector database to summarise, store, and retrieve historical conversation data, ensuring continuity across multiple sessions.

  **FR-05: Dynamic Formality & Sentiment Routing:** The system must run a lightweight sentiment analysis on the user's input to dynamically adjust its pedagogical tone (formal vs. informal) and match the user's age and baseline proficiency level.

## 1.4 Non-Functional Requirements (NFRs)

  **NFR-01: Ultra-Low Latency Inference:** The end-to-end architecture (Speech-to-Text -> LLM generation -> Text-to-Speech -> Viseme rendering) must achieve a glass-to-glass latency of under 500ms to preserve organic conversational flow and prevent affective filter spikes.

  **NFR-02: Hardware Agnosticism & Tiered Deplyoment:** The primary inference engine will be deployed via a cloud-hosted infrastructure to leverage maximum compute. Subsequently, the architecture must support aggressive weight compression (e.g., 4-bit NF4 quantization) for localized deployment on resource-constrained edge devices (mobile hardware and sub-8GB VRAM GPUs).

  **NFR-03: Asymmetric Memory Retention ( Semantic over Episodic):** The Retrieval Augmented Generation (RAG) vector database must heavily weight "Semantic Memory" (core user attributes, career goals, proficiency constraints) over "Episodic Memory" (historical chronological chat logs) to ensure optimal context-window efficiency and long-term pedagogical alignment


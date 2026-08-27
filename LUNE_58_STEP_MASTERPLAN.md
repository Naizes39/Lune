# LUNE — Pełna Mapa Budowy (od `uv init` do robota z osobowością)

**Zasada:** każdy krok dokłada się do istniejącego kodu. Żaden nie wymaga przebudowy poprzednich. Kroki oznaczone 🔬 to research-first — czytasz dokumentację/papers zanim napiszesz kod, bo gotowego rozwiązania nie ma.

---

## FAZA 1 — Fundamenty danych i struktury
- [x]  1. `uv init` — instalacja: fastapi, uvicorn, google-genai, openai, pydantic, motor (async MongoDB) lub aiosqlite, redis
- [x]  2. Globalne schematy Pydantic (`utils/schemas.py`) — od razu z: `UserMemory` (wagi zainteresowań), `requires_confirmation: bool` na narzędziach, `session.status` (active/paused/ended)
- [x]  3. Trwała baza danych (`utils/database.py`) — `save_chat_turn()`, `load_chat_history()` + tabela `user_memory` + pole statusu sesji

## FAZA 2 — System Skills & MCP
- [x]  4. Narzędzia lokalne (`skills/local_tools.py`) — try/except na każdej funkcji, flaga `requires_confirmation` przy rejestracji
- [x]  5. Narzędzie sieciowe (`skills/web_search.py`) — async, thread pool (posłuży też jako źródło "aktualnych wydarzeń na świecie")
- [x]  6. Semantic prompt cache (`utils/cache.py`) — Redis, hash MD5 promptu, TTL 10 min
- [ ]  7. Auto-generator manifestów MCP (`utils/mcp_formatter.py`)
- [x]  8. Rejestr `SKILLS_REGISTRY` (`skills/__init__.py`)

## FAZA 3 — RAG (wiedza długoterminowa)
- [ ]  9. Chunking i ingest dokumentów (`utils/rag_ingest.py`)
- [ ]  10. Wyszukiwanie semantyczne/BM25 (`skills/rag_search.py`) + rejestracja w `SKILLS_REGISTRY`

## FAZA 4 — Workerzy (lokalne modele 8B)
- [ ]  11. Manifesty tekstowe agentów (`manifests/*.md`)
- [ ]  12. `agents/worker_base.py` — połączenie z Ollamą, instrukcja "bądź robotem, wyciągaj fakty, zero uprzejmości"
- [ ]  13. `AGENT_REGISTRY` (`agents/__init__.py`)

## FAZA 5 — Orkiestracja hybrydowa (Gemini Pro)
- [ ]  14. `utils/client_routing.py` — klient google-genai (Gemini) + klient openai (Ollama/vLLM)
- [ ]  15. Routing intencji (`orchestrator.py -> route_task`) — structured output `{selected_worker, worker_instruction}`, filtrowany przez uprawnienia usera
- [ ]  16. Synteza odpowiedzi + persona (`orchestrator.py -> synthesize_response`) — dopisać pole `emotional_tone` w structured output

## FAZA 6 — System przepływu stanu
- [ ]  17. `utils/graph_engine.py` — klasa `StateGraph`, pętla plan→wykonaj→oceń, `max_loops=10`, węzeł `awaiting_confirmation`
- [ ]  18. Telemetria (`utils/telemetry.py`) — dekorator `@trace_agent`

## FAZA 7 — Serwer FastAPI
- [x]  19. `main.py` — endpoint `/agent/chat`: ładuje historię + `user_memory` + uprawnienia (cache), odpala `StateGraph`, zapisuje i zwraca odpowiedź


## FAZA 8 — Integracja interfejsu
- [ ]  20. Streaming SSE (Server-Sent Events) w `main.py`
- [ ]  21. Frontend czatu (React/Vue/HTML+JS) podpięty pod SSE

## FAZA 9 — Pamięć długoterminowa
- [ ]  22. `memory_summarizer_node` — worker w `AGENT_REGISTRY` odpala się na starcie sesji, zwraca do `user_memory`
- [ ]  23. Wstrzykiwanie pamięci do promptu Supervisora na starcie sesji

## FAZA 10 — Personalizacja (zainteresowania)
- [ ]  24. Silnik zainteresowań z wagą liczbową (wzmianka = +waga, decay flag)

## FAZA 11 — Głos i awatar (wariant ekranowy)
- [ ]  25. TTS z timestampami visemes
- [ ]  26. Mapper visemes → klatki animacji
- [ ]  27. Renderer awatara podpięty pod SSE

## FAZA 12 — Percepcja wizualna (emocje z twarzy)
- [ ]  28. Kanał wideo z kamery → wnioskowanie emocji

## FAZA 13 — Własny mózg (optymalizacja enterprise)
- [ ]  29. Evals + LLM-as-a-Judge (`evals.py`)
- [ ]  30. Trening QLoRA (`training/`) na własnym datasecie
- [ ]  31. Serwer vLLM z multi-LoRA pool
- [ ]  32. Hot-swap: Ollama -> vLLM

## FAZA 14 — RL na preferencjach (wymaga realnych danych)
- [ ]  33. Zbieranie par preferencji
- [ ]  34. DPO fine-tuning workera

## FAZA 15 — Monetyzacja ról
- [ ]  35. Tabela `user_entitlements`
- [ ]  36. Webhook płatności (Stripe)
- [ ]  37. Cache uprawnień (Redis)
- [ ]  38. Cron dzienny
- [ ]  39. Filtr ról w routingu
- [ ]  40. UI zakupu/aktywacji ról

## FAZA 16 — Naturalna rozmowa (research-first, turn-taking)
- [ ]  41. 🔬 Research: VAD (voice activity detection)
- [ ]  42. 🔬 Research: spekulatywne generowanie odpowiedzi
- [ ]  43. Implementacja: strumień audio + VAD
- [ ]  44. Integracja z TTS/SSE

## FAZA 17 — Ciągłość między urządzeniami
- [ ]  45. Pełna obsługa `session.status = paused`
- [ ]  46. Apka mobilna
- [ ]  47. Logika startowa dla `paused` sesji

## FAZA 18 — Fizyczny robot: mózg wysokopoziomowy → kontroler niskopoziomowy
- [ ]  48. Schemat komendy wysokopoziomowej
- [ ]  49. `execute_robot_action()` w `SKILLS_REGISTRY`
- [ ]  50. 🔬 Research: Isaac Sim/Isaac Lab
- [ ]  51. Trening kontrolera RL w symulacji
- [ ]  52. Sim-to-real transfer na fizycznego robota
- [ ]  53. `requires_confirmation=True` dla akcji fizycznych

## FAZA 19 — Role fizyczne robota
- [ ]  54. Rozszerzenie `user_entitlements` o role fizyczne w `SKILLS_REGISTRY`

## FAZA 20 — Wyraz fizyczny zamiast ekranu
- [ ]  55. Visemes/emocja → sterowanie serwomechanizmami twarzy i postawy robota

## FAZA 21 — Percepcja i ekspresja głosowa
- [ ]  56. Wykrywanie tonu/akcentu usera
- [ ]  57. Ekspresja emocjonalna Lune
- [ ]  58. Sprzężenie zwrotne głośności/tempa

## FAZA 22 — Offensive Security & Red Teaming (The Bulletproof Protocol)
- [ ]  59. 🔬 Research: OWASP Top 10 dla AI (Prompt Injection, Data Poisoning).
- [ ]  60. Symulacja ataków DDoS i SQL Injection na własne API (FastAPI) + łatanie luk (Rate Limiting).
- [ ]  61. Reverse Engineering: Analiza złośliwych payloadów w pamięci podręcznej i izolacja środowiska (Sandboxing workerów).
- [ ]  62. Kryptografia: Szyfrowanie bazy danych SQLite (SQLCipher) i bezpieczny transfer WebRTC (DTLS/SRTP).

## FAZA 23 — Hardware Architecture & Multi-GPU Scale (The Foundry)
- [ ]  63. Architektura klastra: Skonfigurowanie lokalnego serwera (Linux Bare-metal) pod 2x RTX 3090.
- [ ]  64. Programowanie CUDA: Podstawy alokacji pamięci na GPU (VRAM management) i optymalizacja operacji tensorowych.
- [ ]  65. Rozproszony trening (Distributed Training): Uruchomienie vLLM/Unsloth na wielu GPU jednocześnie (Data/Tensor Parallelism).

## FAZA 24 — B2B Capital Generation (The Freelance Bridge)
- [ ]  66. Paczkowanie (Packaging): Zamiana modułów Lune w "White-label SaaS", który można sprzedać zewnętrznej firmie.
- [ ]  67. Skalowalność Enterprise: Wdrożenie systemu kolejek (Celery/RabbitMQ) do obsługi 1000+ równoległych użytkowników.
- [ ]  68. Infrastruktura chmurowa (Przejściowa): Postawienie całości na AWS/GCP zanim kupisz własny sprzęt.

## FAZA 25 — The Polymath Synthesis (Medical & Physics Frontier)
- [ ]  69. 🔬 Research: Przetwarzanie zbiorów danych medycznych (Genomika, obrazowanie medyczne) przez modele multimodalne.
- [ ]  70. Symulacja Fizyczna: Zastosowanie praw fizyki (Kinematyka odwrotna) do precyzyjnego sterowania robotem w przestrzeni 3D.
- [ ]  71. The Universal Prodigy Milestone: Pełna integracja zmysłów (Vision, Audio, Logic, Physics) sterowana przez pojedynczy system operacyjny.

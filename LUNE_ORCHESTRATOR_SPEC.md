# LUNE ORCHESTRATOR: SYSTEM SPECIFICATION & PRD
**Status:** Inicjalizacja projektu (Faza 1: Silnik Backendowy)
**Architekt:** Karol Stefaniak

---

## 1. DEFINICJA SYSTEMU (CO BUDUJEMY?)
Lune Orchestrator to asynchroniczny, autonomiczny silnik (backend) do zarządzania wieloma agentami sztucznej inteligencji. 
Nie budujesz tu "chatbota". Budujesz **system operacyjny dla agentów LLM**. 
System przyjmuje cel od użytkownika, rozbija go na pod-zadania, wyznacza odpowiednich Agentów do ich wykonania, pozwala im używać narzędzi fizycznych (pisanie po dysku, szukanie w sieci) i samodzielnie koryguje ich błędy, chroniąc system przed nieskończonymi pętlami.

## 2. WYMAGANIA FUNKCJONALNE (CORE FEATURES)

### Filar 1: Warstwa Ingestii i Pamięci (Memory System)
*   **Krótkoterminowa (Short-Term Context):** System musi potrafić przechowywać historię konwersacji (State) dla bieżącego zadania. Kontekst musi być przycinany (Pruning), by nie przekroczyć limitu tokenów (Context Window).
*   **Długoterminowa (Long-Term Memory):** Szkielet do podpięcia w przyszłości bazy wektorowej (np. ChromaDB, Qdrant). Agent musi móc zapisać "fakt", a inny agent z innej sesji musi móc go odczytać.

### Filar 2: Router Decyzyjny (Cognitive Router)
*   **Wybór Narzędzi (Tool Calling):** Router analizuje wejście i decyduje, co trzeba zrobić. Zwraca absolutnie **tylko ustrukturyzowany JSON** (walidowany przez Pydantic), który mówi np.: `{"action": "write_file", "path": "test.txt", "content": "hello"}`. Brak bezpośredniego rzucania surowego tekstu do użytkownika, gdy w tle działa proces.
*   **Delegacja:** Jeśli zadanie jest za trudne dla jednego Agenta, Router musi umieć powołać Pod-Agenta (Sub-agent) ze specjalizacją (np. Agent-Programista powołuje Agenta-Krytyka).

### Filar 3: Warstwa Egzekucji (Actuator Sandbox)
*   **Separacja Zależności:** Agenty LLM (Filar 2) NIE MAJĄ dostępu do Twojego dysku. One tylko generują żądanie JSON. Warstwa Egzekucji to Twój kod w Pythonie, który odbiera ten JSON, upewnia się, że komenda jest bezpieczna (np. zablokowanie komendy `rm -rf /`), a następnie fizycznie wykonuje operację systemową.
*   **Rejestr Skutków:** Po wykonaniu akcji (np. udane zapisanie pliku), warstwa zwraca wynik (Success/Fail) do Pamięci.

### Filar 4: Ujemne Sprzężenie Zwrotne i Zabezpieczenia (Cybernetics & Runaway Guard)
*   **Refleksja:** Jeśli Warstwa Egzekucji napotka błąd (np. Agent podał złą ścieżkę do pliku i wywaliło błąd 404), błąd wraca do Agenta z poleceniem "Znalazłem błąd: [Treść Błędu]. Napraw to."
*   **Runaway Guard (Circuit Breaker):** Musisz zaimplementować twardy licznik (np. `max_retries = 3`). Jeśli Agent spróbuje poprawić błąd 3 razy i nadal mu się nie udaje, system PRZERYWA pętlę i rzuca krytyczny błąd (zwraca kontrolę człowiekowi). 

## 3. STOS TECHNOLOGICZNY (MVP TECH STACK)
1. **Język:** Python 3.11+
2. **Typowanie:** Pydantic (Ścisła walidacja wszystkiego, co wchodzi i wychodzi z modelu LLM).
3. **Asynchroniczność:** `asyncio` (każde wywołanie sieciowe do OpenAI/Anthropic musi być bezwzględnie asynchroniczne - `await`).
4. **API:** FastAPI (Szkielet pod przyszłą komunikację z React/Next.js z warstwy Frontendowej).
5. **Narzędzia LLM:** Możesz pisać surowe zapytania HTTP (używając `httpx`) lub użyć minimalnych bibliotek oficjalnych (np. `openai` SDK). **Zabrania się używania ciężkich frameworków ukrywających logikę (jak Langchain), budujesz silnik na First Principles.**

## 4. DEFINICJA UKOŃCZENIA (ACCEPTANCE CRITERIA DLA WERSJI 0.1)
Twój kod będzie uznany za "Gotowy MVP", kiedy:
1. Uruchomisz skrypt (lub serwer FastAPI).
2. Wyślesz do systemu polecenie: *"Sprawdź, co jest w pliku X, i na tej podstawie stwórz plik Y z podsumowaniem"*.
3. System (Orkiestrator) sam użyje narzędzia czytającego plik X.
4. Zrozumie zawartość (Pamięć).
5. Użyje narzędzia piszącego, by stworzyć plik Y.
6. Zwróci informację "Zadanie zakończone sukcesem".
7. *Opcjonalnie (Test Oporu):* Jeśli poprosisz go o przeczytanie pliku, który nie istnieje, system nie zawiesi się, tylko zauważy błąd i powie: "Ten plik nie istnieje".

---
**Wskazówka Architekta:** 
Nie próbuj pisać wszystkiego naraz. Zacznij od napisania klasy `Agent` i jednego prymitywnego narzędzia `Tool` (np. prostego kalkulatora dodającego liczby), by połączyć je w pętlę i udowodnić, że LLM potrafi zwrócić JSON decydujący o użyciu narzędzia. Dopiero gdy to zadziała, wpinaj zapis na dysk i skomplikowaną walidację.

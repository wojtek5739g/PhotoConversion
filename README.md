# Zarządzanie kolekcją zdjęć

## Zespół

- Wojciech Grunwald
- Dominika Młynarska
- Mikalai Stelmakh
- Bartosz Pomiankiewicz

## Opis projektu

Projekt ma za zadanie ułatwienie zarządzania personalną kolekcją zdjęć. Głównym problemem, na którym skupia się nasze rozwiązanie jest zapewnienie spójności metadanych obrazów podczas konwersji między różnymi programami do ich przechowywania. Naszym celem jest odciążenie użytkownika systemu, uwalniając go od konieczności dbania o poprawny zapis metadanych podczas przenoszenia zdjęć z jednego narzędzia do drugiego. Użytkownik powinien mieć możliwość wyboru obrazów do przesłania, a także ich lokalizacji źródłowej i docelowej; nie powinien natomiast martwić się o nieoczekiwaną utratę informacji. 

### Wymagania

Program musi być łatwo rozwijalny:

- łatwe dodanie wsparcia nowego narzędzia do zarządzania zdjęciami,

- łatwa zmiana formy kanonicznej, w której przechowywane są dane (np. dodanie nowych metadanych lub skasowanie przestarzałych).

Musi być wsparcie dla przynajmniej dwóch różnych narzędzi do zarządzania zdjęciami, czyli pobieranie z nich i konwersja do formy kanonicznej oraz w drugą stronę - konwersja z formy kanonicznej do takiej, którą obsługuje odbiorca.

Metadane zdjęć, które zostały przetworzone muszą być przechowywane w bazie danych w zdefiniowanej przez nas postaci kanonicznej. 

### Uwagi

- Program nie musi służyć do przeglądania zdjęć,

- trzeba być czujnym na języki różnej narodowości (np. format daty lub czasu może zależeć od języku systemu operacyjnego),

- możliwość edycji metadanych nie jest potrzebna, ważniejsza jest rozszerzalność o nowe narzędzia.

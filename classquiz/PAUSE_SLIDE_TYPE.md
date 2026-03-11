# Technische documentatie: PAUSE vraagtype

## Overzicht

Dit document beschrijft de toevoeging van het `PAUSE` vraagtype aan het ClassQuiz-platform. Het PAUSE-type is een wacht-slide waarop spelers niets hoeven te doen: zij wachten totdat de host/quizmaster beslist door te gaan naar de volgende vraag. Er kunnen geen punten worden verdiend op een PAUSE-slide.

---

## Gedachtegang

### Wat is het PAUSE-type?

In een quizsessie is het soms wenselijk om een tussenstop in te lassen — om iets uit te leggen, een foto te tonen, of simpelweg een moment rust te geven. Het bestaande `SLIDE`-type deed al iets vergelijkbaars, maar dat stuurt HTML-content naar de host/admin en toont niets aan de spelers. Het `PAUSE`-type is anders:

- **Spelers** ontvangen de slide wél, met een titel en een optionele afbeelding.
- **De host** bepaalt wanneer verder wordt gegaan (door de volgende vraag in te stellen via Socket.IO `set_question_number`).
- **Geen antwoordmogelijkheid**: spelers kunnen niets insturen en verdienen dus geen punten.
- **Geen timer-druk**: de tijdslimiet in het model is technisch aanwezig maar heeft geen effect op het spelverloop.

### Waarom een nieuw type en geen uitbreiding van SLIDE?

Het bestaande `SLIDE`-type stuurt HTML-tekst naar de admin en niets naar de speleers. Dat is bedoeld voor rich-text presentaties beheerd door de host. Het `PAUSE`-type heeft een fundamenteel andere UX-bedoeling: iedereen in de kamer ziet hetzelfde scherm (titel + optionele foto), en niemand kan iets doen. Een apart enum-waarde houdt de logica netjes gescheiden en maakt het onderscheid expliciet op zowel back-end als front-end niveau.

---

## Gewijzigde bestanden

### 1. `classquiz/db/models.py`

#### `QuizQuestionType` enum

```python
class QuizQuestionType(str, Enum):
    ABCD = "ABCD"
    RANGE = "RANGE"
    VOTING = "VOTING"
    SLIDE = "SLIDE"
    TEXT = "TEXT"
    ORDER = "ORDER"
    CHECK = "CHECK"
    PAUSE = "PAUSE"   # nieuw
```

De nieuwe waarde `PAUSE = "PAUSE"` is toegevoegd. Omdat `QuizQuestionType` erft van `str` én `Enum`, kan de string-waarde `"PAUSE"` direct worden opgeslagen in de PostgreSQL JSON-kolom en worden gedeserialiseerd via Pydantic.

#### `QuizQuestion.answers` veld

```python
# vóór
answers: list[ABCDQuizAnswer] | RangeQuizAnswer | list[TextQuizAnswer] | list[VotingQuizAnswer] | str

# na
answers: list[ABCDQuizAnswer] | RangeQuizAnswer | list[TextQuizAnswer] | list[VotingQuizAnswer] | str | None = None
```

Het veld accepteert nu ook `None`, met `None` als standaardwaarde. Dit is nodig omdat een PAUSE-vraag conceptueel geen antwoorden heeft. Voor alle andere typen (ABCD, RANGE, enz.) blijft het gedrag ongewijzigd — de validator controleert dat `None` alleen geldig is bij type PAUSE.

#### `QuizQuestion.answers` validator

```python
@validator("answers")
def answers_not_none_if_abcd_type(cls, v, values):
    if values.get("type") == QuizQuestionType.PAUSE:
        return v  # PAUSE type allows None answers; no answer input from players
    if v is None:
        raise ValueError("Answers cannot be None for this question type")
    # ... bestaande checks voor ABCD, RANGE, VOTING, TEXT, ORDER, SLIDE, CHECK ...
```

Er zijn twee wijzigingen:
1. Een vroege `return v` voor PAUSE, vóór alle andere checks. Dit voorkomt dat de validator crasht wanneer `v` `None` is.
2. Een expliciete foutmelding als `v` `None` is voor een niet-PAUSE-type.

### 2. `classquiz/socket_server/__init__.py`

#### `set_question_number` event handler

```python
if game_data.questions[int(float(data))].type == QuizQuestionType.PAUSE:
    await sio.emit(
        "set_question_number",
        {
            "question_index": int(float(data)),
            "question": {
                "question": temp_return["question"],
                "image": temp_return.get("image"),
                "type": "PAUSE",
                "time": temp_return["time"],
                "answers": None,
                "hide_results": False,
            },
        },
        room=game_pin,
    )
    return
```

**Verschil met SLIDE**:

| | SLIDE | PAUSE |
|---|---|---|
| Ontvangers van `set_question_number` | Alleen admin (`room=sid`) | Alle spelers én admin (`room=game_pin`) |
| Meegestuurde data | Alleen `question_index` | `question_index` + vraagobject (titel, afbeelding) |
| Bedoeling | Host showt HTML-presentatie via eigen scherm | Iedereen ziet dezelfde wacht-slide |

De emit gaat naar `game_pin` (de volledige kamer, inclusief de host) zodat elke client de juiste UI kan renderen. De functie keert daarna onmiddellijk terug (`return`) en slaat de generieke `ReturnQuestion`-instantiatie over.

#### `submit_answer` event handler

```python
elif game_data.questions[int(float(data.question_index))].type == QuizQuestionType.PAUSE:
    return  # PAUSE type has no answers; players cannot submit anything
```

Wanneer een speler toch een `submit_answer`-evenement stuurt voor een PAUSE-vraag (in theorie niet mogelijk vanuit een correcte front-end, maar als vangnet), keert de handler onmiddellijk terug zonder punten toe te kennen of iets op te slaan. Dit staat vóór de `else: raise NotImplementedError`-tak, zodat er geen onverwachte serverfout optreedt.

---

## Wat de front-end moet doen

De back-end stuurt het volgende object via het `set_question_number` Socket.IO-evenement voor een PAUSE-vraag:

```json
{
  "question_index": 3,
  "question": {
    "question": "Tijd voor een pauze!",
    "image": "uuid-van-afbeelding-of-null",
    "type": "PAUSE",
    "time": "0",
    "answers": null,
    "hide_results": false
  }
}
```

De front-end herkent `type === "PAUSE"` en toont:
- De **titel** (`question.question`) prominent in beeld.
- De **afbeelding** (`question.image`) als die niet `null` is.
- **Geen antwoordknoppen**, **geen score-feedback**, **geen timer**.
- Een wacht-indicator ("Wacht op de host…" of vergelijkbaar).

De host/admin heeft een "Volgende vraag"-knop om door te gaan, die het `set_question_number`-evenement naar de server stuurt.

---

## Databankmigratie

Er is **geen databankmigratie nodig**. De vraagtypen worden opgeslagen als JSON in de kolom `questions` van de `quiz`-tabel (Ormar `JSON`-veld). Omdat er een nieuwe enum-waarde wordt toegevoegd aan een string-enum (geen aparte enum in PostgreSQL), is er geen schemawijziging. Bestaande quiz-records worden niet aangetast.

---

## Validatieregels samengevat

| Veld | Vereiste | Opmerking |
|---|---|---|
| `question` (titel) | **Verplicht** | Niet leeg, gesanitiseerd via Bleach |
| `image` | Optioneel (`null` toegestaan) | Moet een geldig storage-UUID zijn als aanwezig |
| `answers` | Altijd `null` | Back-end weigert antwoorden op te slaan voor dit type |
| `time` | Aanwezig maar niet functioneel | Wordt niet gebruikt voor scoring |
| `type` | `"PAUSE"` | Vaste waarde |

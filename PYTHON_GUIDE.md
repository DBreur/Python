# Python String Basisfunctionaliteiten

Dit document bevat een overzicht van de belangrijkste string-operaties in Python, inclusief string-indexing, escape-sequences en f-strings.

## 1. String Indexing & Slicing
Python strings kunnen worden uitgelezen met behulp van indexen (posities). Indexering begint bij `0`. Negatieve indexen tellen vanaf het einde terug.

```python
course = "Python"

print(len(course))   # Output: 6  (Geeft de lengte van de string)
print(course[0])     # Output: P  (Eerste karakter)
print(course[-1])    # Output: n  (Laatste karakter)
print(course[0:3])   # Output: Pyt (Karakters van index 0 tot 3, exclusief 3)
print(course[0:])    # Output: Python (Vanaf index 0 tot het einde)
print(course[:3])    # Output: Pyt (Vanaf het begin tot index 3)
print(course[:])     # Output: Python (Kopie van de volledige string)
```

## 2. Escape Sequences
Een escape sequence is een combinatie van een backslash (\) met een letter of teken. Het verandert de betekenis van dat teken. Het maakt van een code-teken gewone tekst (zoals \"), of het maakt van gewone letters juist een speciale actie (zoals \n voor een nieuwe regel).

```python
print("Python \"Programming") # Output als het zonder backslash zou zijn: SyntaxError: unterminated string literal (Geeft een error)

print("Python \"Programming") # Output met backslash: Python "Programming
print("Python \'Programming") # Output: Python 'Programming
print("Python \\Programming") # Output: Python \Programming
print("Python \nProgramming") # Output: 
# Python 
# Programming
```

# 3. String Formatting
String formatting is het dynamisch invullen van tekst. In plaats van tekst en variabelen aan elkaar te lijmen met +, gebruik je een f-string. Je zet een f voor je tekst en plaatst je variabelen of berekeningen simpelweg tussen {}. Python berekent en vult de waardes vervolgens automatisch voor je in.

```python
first = "Dion"
last = "Breur"
full = first + " " + last
print(full)
# Output: Dion Breur

first = "Dion"
last = "Breur"
full = f"{first} {last}"
print(full)
# Output: Dion Breur

first = "Dion"
last = "Breur"
full = f"{len(first)} {last}"
print(full)
# Output: 4 Breur

first = "Dion"
last = "Breur"
full = f"{len(first)} {2+2}"
print(full)
# Output: 4 4
```

# 4. String Methods
String methods zijn de ingebouwde functies van Python waarmee je tekst kunt manipuleren. Je roept ze aan door een punt achter je variabele te zetten (zoals tekst.upper()). Onthoud dat ze de originele variabele nooit aanpassen, maar altijd een schone, nieuwe versie van de tekst teruggeven.

```python
course = "Python Programming"
print(course.upper()) # Output: PYTHON PROGRAMMING
print(course.lower())  # Output: python programming

course = "python programming"
print(course.title())  # Output: Python Programming
print(course.capitilize()) # Output: Python programming

course = "  python   programming   "
print(course.strip())  # Output: python   programming
# Ook nog .lstrip en .rstrip voor alleen links en alleen rechts

course = "python programming"
print(course.find("pro"))  # Output: 7 (vind index, oftewel de plaats in de string)
print(course.find("Pro")) # Output: -1 (Betekent niet gevonden, want we hebben geen hoofdletter p, het programma is namelijk hoofdletter gevoelig)

print(course.replace("p", "j"))  # Output: jython jrogramming

print("pro" in course)  # Output: True
print("jro" in course)  # Output: False
print("jro" not in course)  # Output: True
```

# 5. Numbers
In Python werk je voornamelijk met drie verschillende soorten getallen: integers (gehele getallen), floats (kommagetallen) en complex (complexe getallen). Python herkent automatisch welk type getal je gebruikt, dus je hoeft dit niet handmatig te definiëren.

```python
x = 10      # Dit is een int (geheel getal)
y = 3.14    # Dit is een float (kommagetal, let op de punt!)
z = 3 + 5j  # Dit is een complex getal (met een imaginair deel 'j')

# Standaard berekeningen
print(10 + 3)   # Output: 13  (Optellen)
print(10 - 3)   # Output: 7   (Aftrekken)
print(10 * 3)   # Output: 30  (Vermenigvuldigen)
print(10 / 3)   # Output: 3.3333333333333335 (Delen - geeft altijd een float)

# Speciale operatoren
print(10 // 3)  # Output: 3   (Floor division: rondt af naar beneden op een heel getal)
print(10 % 3)   # Output: 1   (Modulo: geeft de restwaarde die overblijft na deling)
print(10 ** 3)  # Output: 1000 (Exponent/Macht: 10 tot de macht 3)

x = 10
x += 3          # Dit is hetzelfde als: x = x + 3
print(x)        # Output: 13

y = 10
y *= 2          # Dit is hetzelfde als: y = y * 2
print(y)        # Output: 20

print(round(2.6))   # Output: 3    (Rondt het getal af naar het dichtstbijzijnde hele getal)
print(round(2.4))   # Output: 2    (Rondt af naar beneden)
print(abs(-15))     # Output: 15   (Absolute waarde: maakt van een negatief getal een positief getal)
```
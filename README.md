# Grammar Generator

## Description

In this evidence, we **implement a Python script that is designed to validate sentences** according to a **Context-Free Grammar (CFG)** build for this specific language.
The system checks whether an input sentence matches the structure and rules of the specified language.

## Context

The language that we are using is a **basic Japanese-like made up language**.
It models simple sentences involving subjects, objects, verbs, and optional particles, reflecting common sentence patterns found in beginner-level Japanese sections of the learning platform "Duolingo".

### Language Characteristics

#### Word Order and Syntax

The language modeled for this project is inspired by basic Japanese sentence structure, which typically follows a **Subject-Object-Verb word order**.
This means that in a normal sentence, the subject appears first, followed by the object, and finally the verb.

Some examples would be:
- You watch TV = Anata wa terebi o mimasu
- I eat rice = Watashi wa gohan o tabemasu
- I listen to rock = Watashi wa rokku o kikimasu

Still there is the possibility to include conjunctions as **"to"**, which means "and", to combine multiple subjects or objects.

Also, an optional particle **"ka"** can be added at the end of a sentence to transform a statement into a yes or no question.

Following the previous examples, the sentence "Anata wa terebi o mimasu" can be transformed into a question if we use the "ka" particle at the end: "Anata wa terebi o mimasu ka" = "Do you watch TV?".

#### Particles and Sentence Roles

You may have noticed that there are particles that are always included in our sentences, these are:

-   **"wa"** marks the topic or subject of the sentence.
-   **"o"** marks the direct object.    

Without these particles, identifying the role of nouns in the sentence would be more ambiguous. In this model, particles are required immediately after the respective subject or object.

#### Optional Elements

-   The **object** is optional, allowing sentences to be composed of just a subject and a verb.  
-   The **ka** particle at the end of a sentence is optional, depending on whether the sentence is a statement or a question.

#### Sentence Components

The grammar that we are going to implemet uses the following components:

-  **Pronouns**: "watashi", "anata", "kimi", "boku"
-  **Nouns**: "eiga", "terebi", "hon", "manga", "gohan", "sushi", "rokku", "poppu"
-  **Verbs**: "mimasu", "kikimasu", "tabemasu", "yomimasu"
-  **Conjunction**: "to"
-  **Particles**: "wa", "o"
-  **Question Marker**: "ka"

## Models

In this section we are going to construct both the grammar of the language and the LL(1) parser that we'll be using to make a syntax analysis of our sentences.

### 1.- Generating the Grammar

The language is defined by the following context-free grammar, which follows all previous rules:

    S → Subject partWa (Object partO | ε) Verb
    
    Subject → Subject Conjunction Pronoun | Pronoun
    
    Object → Object Conjunction Noun | Noun
    
    Pronoun → watashi | anata | kimi | boku
    Noun → eiga | terebi | hon | manga | gohan | sushi | rokku | poppu
    Verb → mimasu | kikimasu | tabemasu | yomimasu
    
    Conjunction → to
    partWa → wa
    partO → o

### 2. Ambiguity Removal

The original grammar had ambiguity issues in the structure of **Object**, as it could be either a valid item of S or an empty value, leading to multiple parse trees for the same sentence. We’ve fixed this by separating it, into **Obj**.

#### Original Grammar
	
	S → Subject partWa (Object partO | ε) Verb
	Object → Object Conjunction Noun | Noun
    
#### Corrected Grammar

	S → Subject partWa Obj Verb
	Obj → Object partO | ε
	Object → Object Conjunction Noun | Noun

### 3. Left Recursion Elimination

Left recursion occurs when a non-terminal symbol on the left-hand side of a production rule refers to itself directly or indirectly.

In the original grammar, the rule `Subject → Subject Conjunction Pronoun` introduced left recursion. To remove this, we’ve split the production into two parts: `Subject` and `Subject'`, also with `Object` and `Object'`.

#### Original Left Recursive Rules:
	Subject → Subject Conjunction Pronoun | Pronoun
	Object → Object Conjunction Noun | Noun

#### Removed Left Recursion:
	Subject → Pronoun Subject'
	Subject' → Conjunction Pronoun Subject' | ε
	
	Obj → Object partO | ε
	
	Object → Noun Object'
	Object' → Conjunction Noun Object' | ε


### 4. Syntactic Tree Examples

To better illustrate the changes in the grammar, here are two syntactic trees:

#### Example 1: "watashi wa terebi o mimasu"

	S
		Subject
			Pronoun (watashi)
			Subject' (ε)
		partWa (wa)
		Obj
			Object
				Noun (terebi)
				Object' (ε)
			partO (o)
		Verb (mimasu)

#### Example 2: "boku wa hon to manga o yomimasu"

	S
		Subject
			Pronoun (boku)
			Subject' (ε)
		partWa (wa)
		Obj
			Object
				Noun (hon)
				Object'
					Conjunction (to)
					Noun (manga)
					Object' (ε)
			partO (o)
		Verb (yomimasu)

In these examples, in this example we can go right trough the algorithm without different paths for a single sentence, and also all of our recursions are right sided as in this example you can see that every downgrade on identation level is at the end of the respective block.

## CFG - Corrected

    S → Subject partWa Obj Verb
    
    Subject → Pronoun Subject'
    Subject' → Conjunction Pronoun Subject' | ε
	
	Obj → Object partO | ε
    Object → Noun Object'
    Object' → Conjunction Noun Object' | ε
    
    Pronoun → watashi | anata | kimi | boku
    Noun → eiga | terebi | hon | manga | gohan | sushi | rokku | poppu
    Verb → mimasu | kikimasu | tabemasu | yomimasu
    
    Conjunction → to
    partWa → wa
    partO → o

## Test

### Implementation

We implemented a series of tests using the `test_sentence` function, which splits the input into tokens and attempts to parse them using the defined CFG and a Chart Parser.  
If a sentence is correctly parsed, it is accepted and shows it's tree; otherwise, it is rejected.

	test_sentence("watashi wa eiga o tabemasu")
	test_sentence("boku wa hon o tabemasu")
	test_sentence("kimi wa gohan o tabemasu")
	test_sentence("anata wa manga o yomimasu")
	test_sentence("watashi wa terebi o mimasu")
	test_sentence("watashi wa sushi o tabemasu")
	test_sentence("boku wa manga o yomimasu")
	test_sentence("anata wa rokku o kikimasu")
	test_sentence("kimi wa poppu o kikimasu")
	test_sentence("watashi to anata wa gohan o tabemasu")
	test_sentence("boku to kimi wa eiga o mimasu")
	test_sentence("watashi wa terebi o mimasu")
	test_sentence("boku wa hon o yomimasu")
	test_sentence("anata wa sushi o tabemasu")
	test_sentence("kimi wa manga o yomimasu")
	test_sentence("watashi to boku wa poppu o kikimasu")
	test_sentence("anata to kimi wa rokku o kikimasu")
	test_sentence("watashi wa hon o omimasu")
	test_sentence("boku wa gohan o tabemasu")
	test_sentence("anata wa poppu o kikimasu")

### Pushdown Automata Example

Let's illustrate how the parser (simulating a **pushdown automaton** behavior) processes an **accepted sentence**:

Example sentence: **"watashi wa terebi o mimasu"**

1.  Push `S`
2.  Expand `S → Subject partWa Obj Verb`
3.  Expand `Subject → Pronoun Subject'`
4.  Match `Pronoun → watashi`
5.  Match `partWa → wa`
6.  Expand `Obj → Object partO`
7.  Expand `Object → Noun Object'`
8.  Match `Noun → terebi`
9.  `Object' → ε` (no conjunction after terebi)
10.  Match `partO → o`
11.  Match `Verb → mimasu`
12.  Stack empty → **Accepted**

## Analysis

### 1. Chomsky Hierarchy Level Before Grammar Refinement

**Before removing ambiguity and left recursion**, the grammar was a bit more unefficient, mainly because:

-   It allows recursion.
-   It has ambiguity (different trees possible for the same string).
-   The left recursion (`Subject → Subject Conjunction Pronoun`) makes it **unsuitable** for simple parsing.

-   **Classification**:  
    **Level:** Context-Free Grammar (Type 2)

### 2. Chomsky Hierarchy Level After Grammar Refinement

**After removing ambiguity and left recursion**, the grammar remains a **Context-Free Grammar (CFG)** but more efficient and also ready to implement with LL(1) parsers. Now the grammar:

-   It is **non-ambiguous** (only one way to parse any sentence).
-   It is now **right-recursive**, making it **compatible with LL(1)** parsers.
    
-   **Classification**:  
    **Level:** Context-Free Grammar (Type 2)

## References
- Duolingo, Inc. (2025). Duolingo (6.27.4) App. https://play.google.com/store/apps/details?id=com.duolingo&hl=es_MX.
from nltk import CFG
from nltk.parse import ChartParser

# Modified Grammar for NLTK
grammar = CFG.fromstring("""
    S -> Subject partWa Obj Verb
    Subject -> Pronoun SubjectPrime
    SubjectPrime -> Conjunction Pronoun SubjectPrime | Empty
    Obj -> Object partO | Empty
    Object -> Noun ObjectPrime
    ObjectPrime -> Conjunction Noun ObjectPrime | Empty
    Empty ->
    Pronoun -> 'watashi' | 'anata' | 'kimi' | 'boku'
    Noun -> 'eiga' | 'terebi' | 'hon' | 'manga' | 'gohan' | 'sushi' | 'rokku' | 'poppu'
    Verb -> 'mimasu' | 'kikimasu' | 'tabemasu' | 'yomimasu'
    Conjunction -> 'to'
    partWa -> 'wa'
    partO -> 'o'
""")

# Create a parser to work with the grammar
parser = ChartParser(grammar)


# Tester Function
def test_sentence(sentence):
    sentence_tokens = sentence.split()
    try:
        parse_trees = list(parser.parse(sentence_tokens))
        if parse_trees:
            print(f"Valid sentence: {sentence}")
            for tree in parse_trees:
                tree.pretty_print()  # Display the syntactic tree
        else:
            print(f"Invalid sentence: {sentence}")
    except Exception as e:
        print(f"Error parsing the sentence: {sentence}")
        print(e)


# Test cases
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

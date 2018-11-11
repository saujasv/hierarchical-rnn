from nltk.parse.generate import generate
from nltk import CFG

def transform(tokens):
    """
        Function that transforms a sentence into the IDENT sentence and
        the QUEST sentence.

        Args:
            tokens: list of words
        
        Returns:
            tuple (ident, quest)
    """

    index = int(tokens[0])
    words = tokens[1:]
    ident = ' '.join(words)
    quest = ' '.join([words[index]] + words[:index] + words[index + 1:])
    return ident, quest


def generate_pairs(grammar_string, n=10):
    """
        Given a grammar as a string, generate declarative sentences, transform them
        into questions, and return a list of (declarative senctence, question) pairs.

        Args:
            grammar_string: string that specifies a CFG that can be parsed by NLTK
            n: integer number of sentences to be generated
        
        Returns:
            list of tuples
    """

    grammar = CFG.fromstring(grammar_string)
    sentence_pairs = list()
    for sentence in generate(grammar, n=n):
        sentence_pairs.append(transform(sentence))
    return sentence_pairs

class NoAgreementLanguage:
    """
        Class of methods to generate sentence-question pairs in the 
        no-agreement language.
    """

    def __init__(self):
        self.grammar_folder = 'no_agreement_grammars/'

    def no_rc(self, n=10):
        """
            Returns a list of sentences without any relative clauses.
        """
        grammar_file = open(self.grammar_folder + 'no_rc', 'r')
        return generate_pairs(grammar_file.read(), n=n)
    
    def rc_on_subject(self, n=10):
        """
            Returns a list of sentences with a relative clause in the 
            subject position.
        """
        grammar_file = open(self.grammar_folder + 'rc_on_subject', 'r')
        return generate_pairs(grammar_file.read(), n=n)
    
    def rc_on_object(self, n=10):
        """
            Returns a list of sentences with a relative clause in the 
            object position.
        """
        grammar_file = open(self.grammar_folder + 'rc_on_object', 'r')
        return generate_pairs(grammar_file.read(), n=n)

if __name__ == '__main__':
    # no_agreement = NoAgreementLanguage()
    # i = 0
    # for pair in no_agreement.rc_on_object(1000):
    #     if i % 50 == 0:
    #         print(pair)
    #     i += 1
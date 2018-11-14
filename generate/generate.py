from nltk.parse.generate import generate
from nltk import CFG

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class LanguageError(Error):
    """
        Error raised when the grammar doesn't support the
        requirement.
    """

    def __init__(self, message):
        self.message = message

class Language:
    """
        Class of methods to generate sentence-question pairs in the 
        specified language.
    """

    VERB = {'transitive': '/trans', 'intransitive': '/intrans'}
    RC = {'none': '/no_rc',
            'subject': '/rc_on_subject', 
            'object': '/rc_on_object'}
    PP = {'none': '/no_pp', 
            'subject': '/pp_on_subject', 
            'object': '/pp_on_object'}

    def __init__(self):
        self.grammar_folder = None
    
    @staticmethod
    def transform(tokens, ident):
        """
            Function that produces the input-output pair for a sentence. If the
            ident flag is True, then the output pair is the identical sentence,
            otherwise the output is the question.

            Args:
                tokens: list of words
                ident: boolean indicating whether output is identical sentence or 
                question
            
            Returns:
                tuple (ident, quest, main_auxiliary)
        """

        index = int(tokens[0])
        words = tokens[1:]
        main_aux = words[index]
        if ident:
            ident_input = ' '.join(words)
            words.append('IDENT')
            ident_output = ' '.join(words)
            return ident_input, ident_output, main_aux
        else:
            quest_words = [words[index]] + words[:index] + words[index + 1:]
            words.append('IDENT')
            quest_words.append('QUEST')
            ident = ' '.join(words)
            quest = ' '.join(quest_words)
            return ident, quest, main_aux
    
    def generate(self, n=10, verb='intransitive', rc='none', 
                        pp='none', ident=False):
        """
            Generate input-output pairs with the main auxiliary in the given 
            language. Arguments specify whether the verb should be transitive 
            or intransitive, the position of the relative clause, and the 
            position of the prepositional phrase.

            Args:
                n: integer number of pairs to be generated
                verb: 'transitive' or 'intransitive', type of verb
                rc: 'none', 'subject', or 'object', position of relative clause
                pp: 'none', 'subject', or 'object', position of prepositional
                    phrase
                ident: boolean indicating whether output is identical sentence 
                    or question
            
            Return:
                list of tuples (input, output, main_aux)
        """
        if rc != 'none' and rc == pp:
            raise LanguageError('language does not allow relative clause\
             and prepositional phrase on the same noun phrase')

        if verb == 'intransitive' and (rc == 'object' or pp == 'object'):
            raise LanguageError('intransitive verbs do not take an object')
        
        try:
            grammar_path = self.grammar_folder + Language.VERB[verb] +\
         Language.RC[rc] + Language.PP[pp]
        except KeyError:
            raise LanguageError('enter valid values for verb type, relative\
            clause position, and preposition position')

        grammar_file = open(grammar_path, 'r')
        grammar = CFG.fromstring(grammar_file.read())

        sentences = list()
        for sentence in generate(grammar, n=n):
            sentences.append(Language.transform(sentence, ident))
        return sentences

class NoAgreementLanguage(Language):
    """
        Class of methods to generate sentence-question pairs in the 
        no-agreement language.
    """

    def __init__(self):
        super().__init__()
        self.grammar_folder = 'no_agreement_grammars/'

class AgreementLanguage(Language):
    """
        Class of methods to generate sentence-question pairs in the 
        agreement language.
    """

    def __init__(self):
        super().__init__()
        self.grammar_folder = 'agreement_grammars_test/'

if __name__ == '__main__':
<<<<<<< HEAD
    no_agreement = NoAgreementLanguage()
    i = 0
    for pair in no_agreement.rc_on_object(1000):
        if i % 50 == 0:
            print(pair)
        i += 1
=======
    no_agreement = AgreementLanguage()
    i = 0
    for triple in no_agreement.generate(n=1000, verb='transitive', rc='object', pp='subject'):
        if i % 30 == 0:
            print(triple)
        i += 1
        # print(triple)
>>>>>>> 0fe6930300da50875c448811377501f34f1c4cf2

from nltk.parse.generate import generate as generate_from_cfg
from nltk import CFG
from random import sample, randint, shuffle

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
            'object': '/rc_on_object',
            'both': '/rc_on_both'}
    PP = {'none': '/no_pp', 
            'subject': '/pp_on_subject', 
            'object': '/pp_on_object',
            'both': '/pp_on_both'}

    def __init__(self):
        self.grammar_folder = None
        self.vocabulary = None
    
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
            words.append('.')
            words.append('IDENT')
            ident_input = ' '.join(words)
            ident_output = ' '.join(words)
            return ident_input, ident_output, main_aux
        else:
            quest_words = [words[index]] + words[:index] + words[index + 1:]
            words.append('.')
            words.append('QUEST')
            quest_words.append('?')
            quest_words.append('QUEST')
            ident = ' '.join(words)
            quest = ' '.join(quest_words)
            return ident, quest, main_aux
    
    def get_grammar_string(self, verb='intransitive', rc='none', pp='none'):
        """
            Get the grammar rules from the file as a string, and add the
            randomly chosen terminals.

            Args:
                verb: 'transitive' or 'intransitive', type of verb
                rc: 'none', 'subject', or 'object', position of relative clause
                pp: 'none', 'subject', or 'object', position of prepositional
                    phrase

            Return:
                string specifying grammar that can be parsed by the NLTK CFG 
                    module
        """

        if rc != 'none' and rc == pp:
            raise LanguageError('language does not allow relative clause\
             and prepositional phrase on the same noun phrase')

        if verb == 'intransitive' and (rc == 'object' or pp == 'object'):
            raise LanguageError('intransitive verbs do not take an object')
        
        if (rc == 'both' and pp != 'none') or (rc != 'none' and pp == 'both'):
            raise LanguageError('language does not allow relative clause\
             and prepositional phrase on the same noun phrase')

        try:
            grammar_path = self.grammar_folder + Language.VERB[verb] +\
         Language.RC[rc] + Language.PP[pp]
        except KeyError:
            raise LanguageError('enter valid values for verb type, relative\
            clause position, and preposition position')

        grammar_file = open(grammar_path, 'r')
        grammar = grammar_file.read() + self.sample_vocabulary()

        return grammar

    def generate(self, n=10, verb='intransitive', rc='none', 
                        pp='none', ident=False):
        """
            Generate input-output pairs with the main auxiliary in the given 
            language. Arguments specify whether the verb should be transitive 
            or intransitive, the position of the relative clause, and the 
            position of the prepositional phrase.
            The vocabulary used in this function is a random sample (class-wise)
            if the entire vocabulary to allow for generating sentences in a 
            reasonable amount of time.

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

        grammar = CFG.fromstring(self.get_grammar_string(verb, rc, pp))

        sentences = list()
        for sentence in generate_from_cfg(grammar, n=n):
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
        self.vocabulary = {
            'Rel': ['who' ,'that'],
            'Det': ['the' ,'some' ,'my' ,'your' ,'our' ,'her'],
            'N': ['cat' ,'cats' ,'dog' ,'dogs' ,'bird' ,'birds' ,'yak' ,'yaks' ,
                    'unicorn' ,'unicorns', 'rabbit', 'rabbits', 'seal', 'seals',
                    'elephant', 'elephants', 'monkey', 'monkeys'],
            'V_trans': ['admire' ,'entertain' ,'impress' ,'irritate' ,'call', 'confuse'],
            'V_intrans': ['laugh' ,'smile' ,'giggle' ,'sleep' ,'live' ,'read'],
            'P': ['around' ,'near' ,'with' ,'upon' ,'by' ,'behind' ,'above' ,'below'],
            'Aux': ['can' ,'will' ,'could' ,'would']
        }
    
    def sample_vocabulary(self):
        aux = list(sample(self.vocabulary['Aux'], 2))
        shuffle(aux)
        vocab = "\n"
        vocab += 'Rel -> ' + "'" + "' | '".join(self.vocabulary['Rel']) + "'\n"
        vocab += 'Det -> ' + "'" + "' | '".join(sample(self.vocabulary['Det'], 2)) + "'\n"
        vocab += 'N -> ' + "'" + "' | '".join(sample(self.vocabulary['N'], 3)) + "'\n"
        vocab += 'V_trans -> ' + "'" + "' | '".join(sample(self.vocabulary['V_trans'], 2)) + "'\n"
        vocab += 'V_intrans -> ' + "'" + "' | '".join(sample(self.vocabulary['V_intrans'], 2)) + "'\n"
        vocab += 'P -> ' + "'" + "' | '".join(sample(self.vocabulary['P'], 2)) + "'\n"
        vocab += 'Aux -> ' + "'" + "' | '".join(aux) + "'"
        return vocab

class AgreementLanguage(Language):
    """
        Class of methods to generate sentence-question pairs in the 
        agreement language.
    """

    def __init__(self):
        super().__init__()
        self.grammar_folder = 'agreement_grammars/'
        self.vocabulary = {
            'N_SG': ['cat', 'dog', 'bird', 'yak', 'unicorn', 'rabbit', 
                        'seal', 'elephant', 'monkey'],
            'N_PL': ['cats', 'dogs', 'birds', 'yaks', 'unicorns', 'rabbits', 
                        'seals', 'elephants', 'monkeys'],
            'V_intrans': ['laugh', 'smile', 'giggle', 'sleep', 'live', 'read'],
            'V_trans': ['admire', 'entertain', 'impress', 'irritate', 'call', 'confuse'],
            'Aux_SG': ['does', 'doesnt'],
            'Aux_PL': ['do', 'dont'],
            'P': ['around', 'near', 'with', 'upon', 'by', 'behind', 'above', 'below'],
            'Rel': ['who', 'that'],
            'Det': ['the', 'some', 'my', 'your', 'our', 'her']
        }
    
    def sample_vocabulary(self):
        aux_sg = list(self.vocabulary['Aux_SG'])
        aux_pl = list(self.vocabulary['Aux_PL'])
        # print(aux_sg, aux_pl)
        shuffle(aux_sg)
        shuffle(aux_pl)
        # print(aux_sg, aux_pl)
        vocab = "\n"
        vocab += 'N_SG -> ' + "'" + "' | '".join(sample(self.vocabulary['N_SG'], 3)) + "'\n"
        vocab += 'N_PL -> ' + "'" + "' | '".join(sample(self.vocabulary['N_PL'], 3)) + "'\n"
        vocab += 'V_intrans -> ' + "'" + "' | '".join(sample(self.vocabulary['V_intrans'], 2)) + "'\n"
        vocab += 'V_trans -> ' + "'" + "' | '".join(sample(self.vocabulary['V_trans'], 2)) + "'\n"
        vocab += 'Aux_SG -> ' + "'" + "' | '".join(aux_sg) + "'\n"
        vocab += 'Aux_PL -> ' + "'" + "' | '".join(aux_pl) + "'\n"
        vocab += 'P -> ' + "'" + "' | '".join(sample(self.vocabulary['P'], 2)) + "'\n"
        vocab += 'Rel -> ' + "'" + "' | '".join(self.vocabulary['Rel']) + "'\n"
        vocab += 'Det -> ' + "'" + "' | '".join(sample(self.vocabulary['Det'], 2)) + "'"
        # print(vocab)
        return vocab

'''
Stats from McCoy et. al.
No Agreement:
    Intransitive:
        No modifiers                    1440    1440
        PP on subject                   14400   14400
        RC on subject                   14400   0
    Transitive:
        No modifiers                    4800    4800
        PP on subject                   4800    4800
        PP on object                    4800    4800
        RC on subject                   4800    0
        RC on object                    4800    4800
        PP on subject, PP on object     4800    4800
        PP on subject, RC on object     4800    4800
        RC on subject, PP on object     4800    0
        RC on subject, RC on object     4800    0

 Agreement:
    Intransitive:
        No modifiers                    700     700
        PP on subject                   14400   14400
        RC on subject                   14400   0
    Transitive:
        No modifiers                    4800    4800
        PP on subject                   4800    4800
        PP on object                    4800    4800
        RC on subject                   4800    0
        RC on object                    4800    4800
        PP on subject, PP on object     4800    4800
        PP on subject, RC on object     4800    4800
        RC on subject, PP on object     4800    0
        RC on subject, RC on object     4800    0
'''

def bad_gen_sentence(sentence):
    main_aux = sentence[int(sentence[0]) + 1]
    count = 0
    for w in sentence:
        if w == main_aux:
            count += 1
    if count > 1:
        return True
    else:
        return False

def generate_data(agreement=False):
    """
        Generate the data from grammars, and store it in ./data
        The data can be partitioned into test and train and used
        to train models after this.
        Statistics are similar to McCoy et. al. and specified in
        the tuples.

        NOTE: All sentences may not be unique. Choose unique
        sentences before partitioning.

        Args: 
            agreement: boolean specifying whether agreement language
            should be used
    """

    # Translate from feature number to feature name to call
    # Language.get_grammar_string
    v = ['intransitive', 'transitive']
    rc = ['none', 'subject', 'object', 'both']
    pp = ['none', 'subject', 'object', 'both']

    # Statistics:
    #     Each index of the tuple corresponds to a feature
    #     verb: kind of verb as index of the verb array above
    #     rc: position of relative clause as index of rc array above
    #     pp: position of prepositonal phrase as index of pp array above
    #     tr_i: Number of IDENT inputs in training set
    #     tr_q: Number of QUEST inputs in training set
    #     ts_i: Number of IDENT inputs in test set
    #     ts/g_q: Number of QUEST inputs in test or generalisation set,
    #                 depending on whether samples for this combination
    #                 of features were presented in training

    no_agreement_stats = [
    #   verb    rc      pp  tr_i      tr_q    ts_i  ts_q g_q
        (0,     0,      0,  1440,     1440,   440,  440, 0),
        (0,     0,      1,  14400,    14400,  440,  440, 0),
        (0,     1,      0,  14400,    0,      880,  0,   2500),
        (1,     0,      0,  4800,     4800,   440,  440, 0),
        (1,     0,      1,  4800,     4800,   440,  440, 0),
        (1,     0,      2,  4800,     4800,   440,  440, 0),
        (1,     1,      0,  4800,     0,      880,  0,   2500),
        (1,     2,      0,  4800,     4800,   440,  440, 0),
        (1,     0,      3,  4800,     4800,   440,  440, 0),
        (1,     2,      1,  4800,     4800,   440,  440, 0),
        (1,     1,      2,  4800,     0,      880,  0,   2500),
        (1,     3,      0,  4800,     0,      880,  0,   2500)
    ]

    agreement_stats = [
    #   verb    rc      pp  tr_i      tr_q    ts_i  ts_q g_q
        (0,     0,      0,  700,      700,    440,  440, 0),
        (0,     0,      1,  14400,    14400,  440,  440, 0),
        (0,     1,      0,  14400,    0,      880,  0,   2500),
        (1,     0,      0,  4800,     4800,   440,  440, 0),
        (1,     0,      1,  4800,     4800,   440,  440, 0),
        (1,     0,      2,  4800,     4800,   440,  440, 0),
        (1,     1,      0,  4800,     0,      880,  0,   2500),
        (1,     2,      0,  4800,     4800,   440,  440, 0),
        (1,     0,      3,  4800,     4800,   440,  440, 0),
        (1,     2,      1,  4800,     4800,   440,  440, 0),
        (1,     1,      2,  4800,     0,      880,  0,   2500),
        (1,     3,      0,  4800,     0,      880,  0,   2500)
    ]
    
    # Choose language
    if agreement:
        stats = agreement_stats
        lang = AgreementLanguage()
        prefix = 'agreement'
    else:
        stats = no_agreement_stats
        lang = NoAgreementLanguage()
        prefix = 'no_agreement'
    
    sentences = dict()
    for features in stats:
        sentences[features] = {'ident': set(), 'quest': set()}

    # Generate sentences for each combination of features
    for features in stats:
        ident_count = 0
        quest_count = 0
        ident_target = features[3] + features[5]
        quest_target = features[4] + features[6] + features[7]
        # ident_file = open('data/' + prefix + '/' +\
        #                             v[features[0]] +\
        #                             '_rc-' + rc[features[1]] +\
        #                             '_pp-' + pp[features[2]] +\
        #                             '_ident.txt', 'w')
        # quest_file = open('data/' + prefix + '/' +\
        #                             v[features[0]] +\
        #                             '_rc-' + rc[features[1]] +\
        #                             '_pp-' + pp[features[2]] +\
        #                             '_quest.txt', 'w')
        while ident_count < ident_target or quest_count < quest_target:
            grammar = CFG.fromstring(lang.get_grammar_string(
                                        verb=v[features[0]], 
                                        rc=rc[features[1]], 
                                        pp=pp[features[2]]))
            
            # Force change in vocabulary after 50 sentences
            to_vocab_change = 50
            for sentence in generate_from_cfg(grammar):
                # Sample randomly from generated sentences
                lottery = randint(1, 1000)
                if ident_count <= ident_target and 1 <= lottery <= 10:
                    # inp, out, main = Language.transform(sentence, ident=True)
                    # ident_file.write(out + '\t' + inp + '\t' + main + '\n')
                    sentences[features]['ident'].add(Language.transform(sentence, ident=True))
                    ident_count += 1
                    to_vocab_change -= 1
                elif quest_count <= quest_target and 990 <= lottery <= 1000:
                    if (features[1] == 1 or features[1] == 3) and bad_gen_sentence(sentence):
                        continue
                    # inp, out, main = Language.transform(sentence, ident=False)
                    # quest_file.write(out + '\t' + inp + '\t' + main + '\n')
                    sentences[features]['quest'].add(Language.transform(sentence, ident=False))
                    quest_count += 1
                    to_vocab_change -= 1
                if to_vocab_change == 0:
                    break
        # ident_file.close()
        # quest_file.close()

        # ident_file = open('data/' + prefix + '/' +\
        #                             v[features[0]] +\
        #                             '_rc-' + rc[features[1]] +\
        #                             '_pp-' + pp[features[2]] +\
        #                             '_ident.txt', 'r')
        # quest_file = open('data/' + prefix + '/' +\
        #                             v[features[0]] +\
        #                             '_rc-' + rc[features[1]] +\
        #                             '_pp-' + pp[features[2]] +\
        #                             '_quest.txt', 'r')
        # train_file = open('data/' + prefix + '/train.txt', 'a')
        # test_file = open('data/' + prefix + '/test.txt', 'a')
        # generalisation_file = open('data/' + prefix + '/generalisation.txt', 'a')
        # ident_lines = [l for l in ident_file.readlines() if len(l) >= 5]
        # quest_lines = [l for l in quest_file.readlines() if len(l) >= 5]
        # shuffle(ident_lines)
        # shuffle(quest_lines)
        # train_lines = ident_lines[:features[3]] + quest_lines[:features[4]]
        # test_lines = ident_lines[features[3]+1:features[3]+features[5]] +\
        #                 quest_lines[features[4]+1:features[4]+features[6]]
        # gen_lines = quest_lines[features[4]+features[6]+1:features[4]+features[6]+features[7]]
        # shuffle(train_lines)
        # shuffle(test_lines)
        # shuffle(gen_lines)
        # for l in train_lines:
        #     train_file.write('\t'.join(l.split('\t')[:2]) + '\n')
        # for l in test_lines:
        #     test_file.write('\t'.join(l.split('\t')[:2]) + '\n')
        # for l in gen_lines:
        #     generalisation_file.write('\t'.join(l.split('\t')[:2]) + '\n')
        # train_file.close()
        # test_file.close()
        # generalisation_file.close()
        print(prefix, v[features[0]], 'rc =', rc[features[1]], 'pp =', pp[features[2]], 'done')
    
    train_file = open('data/' + prefix + '/train.txt', 'w')
    test_file = open('data/' + prefix + '/test.txt', 'w')
    generalisation_file = open('data/' + prefix + '/generalisation.txt', 'w')
    train_lines = list()
    test_lines = list()
    gen_lines = list()
    for features in stats:
        ident_lines = list(sentences[features]['ident'])
        quest_lines = list(sentences[features]['quest'])
        shuffle(ident_lines)
        shuffle(quest_lines)
        train_lines.extend(ident_lines[:features[3]] + quest_lines[:features[4]])
        test_lines.extend(ident_lines[features[3]+1:features[3]+features[5]] +\
                            quest_lines[features[4]+1:features[4]+features[6]])
        gen_lines.extend(quest_lines[features[4]+features[6]+1:features[4]+\
                            features[6]+features[7]])
    train_lines = list(set(train_lines))
    test_lines = list(set(test_lines))
    gen_lines = list(set(gen_lines))
    for l in train_lines:
        train_file.write('\t'.join(l[:2]) + '\n')
    for l in test_lines:
        test_file.write('\t'.join(l[:2]) + '\n')
    for l in gen_lines:
        generalisation_file.write('\t'.join(l[:2]) + '\n')
    train_file.close()
    test_file.close()
    generalisation_file.close()


if __name__ == '__main__':
    # Generate sentences for no-agreement language
    generate_data(agreement=False)

    # Generate sentences for agreement language
    generate_data(agreement=True)

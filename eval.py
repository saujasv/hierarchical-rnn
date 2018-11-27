'''
    Functions for determining if predicted sentence is correct during 
    evaluation.
'''

def full_sentence_word_match(prediction, expected):
    '''
        Check if every word matches.

        Args:
            prediciton: list of words
            expected: list of words
        Return:
            boolean
    '''
    if len(prediction) != len(expected):
        return False

    for i in range(len(prediction)):
        if prediction[i] != expected[i]:
            return False
    return True

def full_sentence_pos_match(prediction, expected, agreement=False):
    '''
        Check if POS of every word matches.

        Args:
            prediciton: list of words
            expected: list of words
            agreement: boolean, whether agreement language is used
        Return:
            boolean
    '''
    no_agreement_inverse_pos = {'who': 'Rel', 'that': 'Rel', 'the': 'Det', 'some': 'Det', 
                                'my': 'Det', 'your': 'Det', 'our': 'Det', 'her': 'Det', 
                                'cat': 'N', 'cats': 'N', 'dog': 'N', 'dogs': 'N', 
                                'bird': 'N', 'birds': 'N','yak': 'N', 'yaks': 'N', 
                                'unicorn': 'N', 'unicorns': 'N', 'rabbit': 'N', 'rabbits': 'N', 
                                'seal': 'N', 'seals': 'N', 'elephant': 'N', 'elephants': 'N', 
                                'monkey': 'N', 'monkeys': 'N', 'admire':'V_trans', 
                                'entertain': 'V_trans', 'impress': 'V_trans', 'irritate': 'V_trans', 
                                'call': 'V_trans', 'confuse': 'V_trans', 'laugh': 'V_intrans', 
                                'smile': 'V_intrans', 'giggle': 'V_intrans', 'sleep': 'V_intrans', 
                                'live': 'V_intrans', 'read': 'V_intrans', 'around': 'P', 'near': 'P', 
                                'with': 'P', 'upon': 'P', 'by': 'P', 'behind': 'P', 'above': 'P', 
                                'below': 'P', 'can': 'Aux', 'will': 'Aux', 'could': 'Aux', 
                                'would': 'Aux'}
    agreement_inverse_pos = {'cat': 'N_SG', 'dog': 'N_SG', 'bird': 'N_SG', 'yak': 'N_SG', 
                                'unicorn': 'N_SG', 'rabbit': 'N_SG', 'seal': 'N_SG', 'elephant': 'N_SG', 
                                'monkey': 'N_SG', 'cats': 'N_PL', 'dogs': 'N_PL', 'birds': 'N_PL', 
                                'yaks': 'N_PL', 'unicorns': 'N_PL', 'rabbits': 'N_PL', 'seals': 'N_PL',
                                'elephants': 'N_PL', 'monkeys': 'N_PL', 'laugh': 'V_intrans', 
                                'smile': 'V_intrans', 'giggle': 'V_intrans', 'sleep': 'V_intrans', 
                                'live': 'V_intrans', 'read': 'V_intrans', 'admire': 'V_trans', 
                                'entertain': 'V_trans', 'impress': 'V_trans', 'irritate': 'V_trans', 
                                'call': 'V_trans', 'confuse': 'V_trans','does': 'Aux_SG', 
                                'doesnt': 'Aux_SG', 'do': 'Aux_PL', 'dont': 'Aux_PL', 'around': 'P', 
                                'near': 'P', 'with': 'P', 'upon': 'P', 'by': 'P', 'behind': 'P', 
                                'above': 'P', 'below': 'P', 'who': 'Rel', 'that': 'Rel', 'the': 'Det', 
                                'some': 'Det', 'my': 'Det', 'your': 'Det', 'our': 'Det', 'her': 'Det'}
    
    if agreement:
        inverse_pos = agreement_inverse_pos
    else:
        inverse_pos = no_agreement_inverse_pos

    if len(prediction) != len(expected):
        return False

    for i in range(len(prediction)):
        if inverse_pos[prediction[i]] != inverse_pos[expected[i]]:
            return False
    return True

def auxiliary_match(predction, expected):
    '''
        Check if auxiliary matches for generalization set.

        Args:
            prediciton: list of words
            expected: list of words
        Return:
            boolean
    '''
    if prediction[0] == expected[0]:
        return True

    return False
from PythonHelperTools.vqaTools.vqa import VQA
from PythonEvaluationTools.vqaEvaluation.vqaEval import VQAEval
import ujson
import os
import pdb


def condensed_question_types():
    question_types_file = os.path.join(
        os.path.dirname(__file__),
        'QuestionTypes/mscoco_question_types.txt')

    with open(question_types_file, 'r') as file:
        question_types = file.read().splitlines()
        
    ques_map = dict()
    for ques_type in question_types:
        if ques_type.startswith('is') or ques_type.startswith('are') \
           or ques_type.startswith('was'):
            ques_map[ques_type] = 'is/are/was'
            
        elif ques_type.startswith('what kind') or ques_type.startswith('what type') \
           or ques_type.startswith('what animal'):
            ques_map[ques_type] = 'what kind/type/animal'
            
        elif ques_type.startswith('how many'):
            ques_map[ques_type] = 'how many'

        # elif ques_type.startswith('what color') \
        #      or ques_type.startswith('what is the color of the'):
        elif 'color' in ques_type:
            ques_map[ques_type] = 'what color'
            
        elif ques_type.startswith('can') or ques_type.startswith('could') \
             or ques_type.startswith('does') or ques_type.startswith('has') \
             or ques_type.startswith('do'):
            ques_map[ques_type] = 'can/could/does/do/has'

        elif ques_type.startswith('where'):
            ques_map[ques_type] = 'where'
            
        elif ques_type.startswith('why') or ques_type.startswith('how'):
            ques_map[ques_type] = 'why/how'

        elif ques_type.startswith('what is the man') \
             or ques_type.startswith('what is the woman') \
             or ques_type.startswith('what is the person'):
            ques_map[ques_type] = 'what is the man/woman/person'

        elif ques_type.startswith('what is on') \
             or ques_type.startswith('what is in'):
            ques_map[ques_type] = 'what is in/on'

        elif ques_type.startswith('which') or ques_type.startswith('who'):
            ques_map[ques_type] = 'which/who'

        elif ques_type.startswith('what does') or ques_type.startswith('what number') \
             or ques_type.startswith('what name') or ques_type.startswith('what is the name'):
            ques_map[ques_type] = 'what does/number/name'

        elif ques_type.startswith('what room') or ques_type.startswith('what sport'):
            ques_map[ques_type] = 'what room/sport'

        elif ques_type.startswith('what time'):
            ques_map[ques_type] = 'what time'

        elif ques_type.startswith('what brand'):
            ques_map[ques_type] = 'what brand'

        elif ques_type.startswith('what is') or ques_type.startswith('what are'):
            ques_map[ques_type] = 'what is/are'

        else:
            ques_map[ques_type] = 'none of the above'

    ques_map['none of the above'] = 'none of the above'

    return ques_map       
            

def analyze(
        anno_json,
        ques_json,
        results_json,
        output_dir,
        prefix = 'eval_val_'):
    
    file_types   = [
        'accuracy', 
        'evalQA', 
        'evalQuesType', 
        'evalAnsType',
    ] 
    
    filenames = dict()
    filenames['results'] = results_json
    for file_type in file_types:
        file_path = os.path.join(
            output_dir,
            prefix + file_type + '.json')
        filenames[file_type] = file_path

    vqa = VQA(anno_json, ques_json)

    vqa_results = vqa.loadRes(results_json, ques_json)

    with open(results_json,'r') as file:
        anno_data = ujson.load(file)

    ques_ids = [anno_data['question_id'] for anno_data in anno_data]
    print len(ques_ids)

    vqaEval = VQAEval(vqa, vqa_results, n=2)
    vqaEval.evaluate(ques_ids, condensed_question_types())

    # print accuracies
    print "\n"
    print "Overall Accuracy is: %.02f\n" %(vqaEval.accuracy['overall'])
    print "Per Question Type Accuracy is the following:"
    for quesType in vqaEval.accuracy['perQuestionType']:
	print "%s : %.02f" %(quesType, vqaEval.accuracy['perQuestionType'][quesType])
    print "\n"
    print "Per Answer Type Accuracy is the following:"
    for ansType in vqaEval.accuracy['perAnswerType']:
        print "%s : %.02f" %(ansType, vqaEval.accuracy['perAnswerType'][ansType])
    print "\n"
    
    # save evaluation results to ./Results folder
    with open(filenames['accuracy'],'w') as file:
        ujson.dump(vqaEval.accuracy, file, indent=4, sort_keys=True)

    with open(filenames['evalQA'],'w') as file:
        ujson.dump(vqaEval.evalQA, file, indent=4, sort_keys=True)

    with open(filenames['evalQuesType'],'w') as file:
        ujson.dump(vqaEval.evalQuesType, file, indent=4, sort_keys=True)
        
    with open(filenames['evalAnsType'],'w') as file:
        ujson.dump(vqaEval.evalAnsType, file, indent=4, sort_keys=True)

    

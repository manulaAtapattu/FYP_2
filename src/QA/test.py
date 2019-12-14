from src.QA.bert import QA


# model = QA('model')
#
# doc = "Good Morning Everyone. How is everyone today? The financial report will be submitted in December. The progress report will be submitted in september. Goodbye everyone"
# doc = "Good Morning Everyone. I do not know the date."
# q = 'When will the progress report be submitted?'
#
# answer = model.predict(doc,q)
#
# print(answer['answer'])
# print(answer.keys())


def main(q, context):
    # model = QA('../src/QA/model')
    model = QA('model')   #local testing
    answer = model.predict(context, q)
    print('answer : ', answer)
    return answer


if __name__ == '__main__':
    main("What is the cost of construction project?",
         "It is going to take a long time to complete. Moving on, let's talk about the hiring of John. He is a well talented employee with lot of experience.")

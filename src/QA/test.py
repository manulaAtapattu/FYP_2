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
    model = QA('../src/QA/model')
    # model = QA('model')
    answer = model.predict(context,q)
    return answer
# if __name__ == '__main__':
#     main()
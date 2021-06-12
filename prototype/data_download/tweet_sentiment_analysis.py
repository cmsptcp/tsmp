import sparknlp

sparknlp.start()
from sparknlp.pretrained import PretrainedPipeline
pipeline = PretrainedPipeline('analyze_sentiment_ml', 'en')
result1 = pipeline.annotate('I love sweet home when I am abroad.')
result2 = pipeline.annotate('Harry Potter is a great movie')

print(result1)
print(result2)
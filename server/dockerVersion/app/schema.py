import graphene
from api import predict_module
import sys
import time


class Query(graphene.ObjectType):
    placeholder = graphene.String()

    def resolve_placeholder(self, info):
        return "This is a placeholder query, use the mutation instead"


class EmotionRecognitionResult(graphene.ObjectType):
    emotions = graphene.List(graphene.String)


class TranscriptionSentence(graphene.InputObjectType):
    bg = graphene.String()
    ed = graphene.String()
    onebest = graphene.String()
    speaker = graphene.String()


class RecognizeEmotion(graphene.Mutation):
    class Arguments:
        # geo = GeoInput(required=True)
        audioURL = graphene.String(required=True)
        # transcription_list = graphene.List(graphene.Field(TranscriptionSentence))
        transcription_list = graphene.String(required=True)

    Output = EmotionRecognitionResult

    def mutate(self, info, audioURL, transcription_list):
        # print('category_list', category_list, file=sys.stderr)
        result = predict_module(audioURL, transcription_list)
        print('EmotionRecognitionResult', result, file=sys.stderr)

        # time.sleep(5) # used for test server timeout config
        return EmotionRecognitionResult(emotions=result)


class Mutation(graphene.ObjectType):
    recognizeEmotion = RecognizeEmotion.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

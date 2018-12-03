import graphene
import sys
from api import predict_module
from emotion import Emotion

class Query(graphene.ObjectType):
    placeholder = graphene.String()

    def resolve_placeholder(self, info):
        return "This is a placeholder query, use the mutation instead"


class EmotionRecognitionResult(graphene.ObjectType):
    # emotions = graphene.List(graphene.String)
    emotions = graphene.List(Emotion)


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

        print('emotion recognization is performed on {}'.format(audioURL), file=sys.stderr)
        return EmotionRecognitionResult(emotions=result)


class Mutation(graphene.ObjectType):
    recognizeEmotion = RecognizeEmotion.Field()


graphqlSchema = graphene.Schema(query=Query, mutation=Mutation)

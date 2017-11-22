import graphene


class Emotion(graphene.ObjectType):
    begin = graphene.String()
    end = graphene.String()
    # prob = graphene.String()
    prob = graphene.List(graphene.Float)
    tag = graphene.String()


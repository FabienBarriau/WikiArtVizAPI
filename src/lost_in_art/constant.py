from enum import Enum, auto

class Metric(Enum, str):
    COLOR = 'color-encoding'
    CONTENT = 'encoding'

class MongoDBCollection(Enum, str):
    ART = "paintings"
    DISTANCE = "distance"
    CATEGORY = "categories"


class ArtProperty(Enum, str):
    TITLE = "title"
    ARTIST = "artistName"
    GALLERIES = "galleries"
    STYLES = "styles"
    DESCRIPTION = "description"
    IMAGE_LINK = "image"
    WIDTH = "width"
    HEIGHT = "height"


class FilterableArtProperty(Enum, str):
    ARTIST = "artistName"
    GALLERIES = "galleries"
    STYLES = "styles"

from marshmallow import Schema, fields


class PaintingSchema(Schema):
    paintingsId = fields.String()
    image = fields.URL()
    x = fields.Float()
    y = fields.Float()
    width = fields.Float()
    height = fields.Float()


class BoundingBoxSchema(Schema):
    x_max = fields.Float()
    x_min = fields.Float()
    y_max = fields.Float()
    y_min = fields.Float()


class PaintingsPositionSchema(Schema):
    data = fields.List(fields.Nested(PaintingSchema))
    bounding_box = fields.Nested(BoundingBoxSchema)


class PaintingDetailSchema(Schema):
    title = fields.String()
    artistName = fields.String()
    image = fields.URL()
    description = fields.String()
    galleries = fields.List(fields.String)
    styles = fields.List(fields.String)


class PaintingsDetailsSchema(Schema):
    data = fields.List(fields.Nested(PaintingDetailSchema))
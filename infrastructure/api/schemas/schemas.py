from marshmallow import fields, Schema

from infrastructure.api.schemas.custom_fields import CustomStringField


class LanguageSchema(Schema):
    id = fields.UUID()
    name = fields.String()
    code = fields.String()


class VendorSchema(Schema):
    id = fields.UUID()
    name = fields.String()
    description = fields.String()
    url = CustomStringField()
    language = fields.Nested('LanguageSchema')


class CategorySchema(Schema):
    id = fields.UUID()
    name = fields.String()
    url = CustomStringField()
    vendor = fields.Nested('VendorSchema')


class AuthorSchema(Schema):
    name = fields.String()


class AggregateRatingSchema(Schema):
    rating_count = fields.Integer()
    rating_value = fields.Float()


class IngredientSchema(Schema):
    id = fields.UUID()
    text = fields.String()


class RecipeSchema(Schema):
    id = fields.UUID()
    name = fields.String()
    description = fields.String()
    author = fields.Nested('AuthorSchema')
    prep_time = fields.TimeDelta()
    cook_time = fields.TimeDelta()
    total_time = fields.TimeDelta()
    date_published = fields.DateTime()
    url = CustomStringField()
    category = fields.Nested('CategorySchema')
    vendor = fields.Nested('VendorSchema')
    language = fields.Nested('LanguageSchema')
    aggregate_rating = fields.Nested('AggregateRatingSchema')
    image = CustomStringField()
    ingredients = fields.List(fields.Nested('IngredientSchema'))


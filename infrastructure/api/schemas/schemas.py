from __future__ import annotations

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


class MatchSchema(Schema):
    """User is not part of the schema, because a match is only requested over a user"""
    id = fields.UUID()
    timestamp = fields.Time()
    is_seen_by_user = fields.Boolean()
    is_active = fields.Boolean()
    recipe = fields.Nested('RecipeSchema')


class UserSchema(Schema):
    id = fields.UUID()
    name = fields.String()
    first_name = fields.String()
    email = fields.Email()
    languages = fields.List(fields.Nested('LanguageSchema'))


vendor_schema = VendorSchema()
vendor_list_schema = VendorSchema(many=True)
category_schema = CategorySchema()
category_list_schema = CategorySchema(many=True)
recipe_schema = RecipeSchema()
recipe_list_schema = RecipeSchema(many=True)
match_schema = MatchSchema()
match_list_schema = MatchSchema(many=True)
user_schema = UserSchema()
user_list_schema = UserSchema(many=True)

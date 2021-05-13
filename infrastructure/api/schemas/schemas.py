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


class CategoryLikeSchema(Schema):
    id = fields.UUID()
    category = fields.Nested('CategorySchema')
    views = fields.Integer()
    matches = fields.Integer()


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


class UserSchema(Schema):
    id = fields.UUID()
    name = fields.String()
    first_name = fields.String()
    email = fields.Email()
    is_confirmed = fields.Boolean()
    date_last_login = fields.DateTime()
    languages = fields.List(fields.Nested('LanguageSchema'))


class MatchResponseSchema(Schema):
    """User is not part of the schema, because a match is only requested over a user"""
    id = fields.UUID()
    timestamp = fields.DateTime()
    is_seen_by_user = fields.Boolean()
    is_active = fields.Boolean()
    recipe = fields.Nested('RecipeSchema')


class MatchRequestSchema(Schema):
    id = fields.UUID()
    timestamp = fields.DateTime()
    is_seen_by_user = fields.Boolean()
    is_active = fields.Boolean()
    user_id = fields.String()
    recipe_id = fields.String()

from pydantic import BaseModel, ValidationError
from pydantic.error_wrappers import ErrorWrapper


class IValidationError(ValidationError):
    def __init__(
        self, msg: type[ValidationError], loc: tuple[str], model: type[BaseModel]
    ) -> None:
        super().__init__(errors=[ErrorWrapper(Exception(msg), loc=loc)], model=model)


# raise ValidationError(
#     [ErrorWrapper(Exception('provider_name is not matched'), loc=("slug", 'pooo'))],
#     model=schemas.CreateLinkModel,
# )

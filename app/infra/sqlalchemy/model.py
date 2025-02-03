from abc import abstractmethod
from typing import Any
from typing import Callable
from typing import Generic
from typing import Self
from typing import Type
from typing import TypeVar

from core.models.model import Model
from sqlalchemy.orm import DeclarativeBase

ModelType = TypeVar("ModelType", bound="Model")


class SaModel(DeclarativeBase, Generic[ModelType]):
    model_class: Type[ModelType]

    @classmethod
    @abstractmethod
    def _from_model_custom_converters(
        cls,
    ) -> dict[str, Callable[["SaModel", Any], None]]:
        """
        key: The field name of the domain model

        Example:
            >>> def _from_model_custom_converters(cls) -> dict[str, Callable[["SaModel", Any], None]]:
            ...     def f(sa_model: SaModel, money: Money) -> None:
            ...         setattr(sa_model, "budget_amount", money.amount)
            ...         setattr(sa_model, "budget_currency", money.currency)
            ...
            ...     def g(sa_model: SaModel, value: str) -> str:
            ...         setattr(sa_model, "some_field", value)
            ...
            ...     return {"buget": f, "_some_private_field": g}

        """
        return {}

    @abstractmethod
    def _to_model_custom_converters(self) -> dict[str, Callable[[], Any]]:
        """
        key: The field name of the domain model

        Example:
            >>> def _to_model_custom_converters(self) -> dict[str, Callable[[], Money]]:
            ...     def f() -> Money:
            ...         amount: Decimal = self.budget.amount
            ...         currency: Currency = self.budget.currency
            ...         return Money(amount, currency)
            ...
            ...     def g() -> str:
            ...         return self.some_field
            ...
            ...     return {"buget": f, "_some_private_field": g}

        """
        return {}

    @classmethod
    @abstractmethod
    def from_model(cls, model: ModelType) -> Self:
        converters: dict[str, Callable] = cls._from_model_custom_converters()
        sa_model = cls()

        # Construct public fields
        for field_name in model.model_fields:
            value = getattr(model, field_name)
            # Apply custom converters first if any
            if field_name in converters:
                converters[field_name](sa_model, value)
            else:
                setattr(sa_model, field_name, value)

        # Construct private fields
        for field_name_with_underscore in model.__private_attributes__:
            field_name = field_name_with_underscore[1:]
            value = getattr(model, field_name_with_underscore)
            # Apply custom converters first if any
            if field_name_with_underscore in converters:
                converters[field_name_with_underscore](sa_model, value)
            elif isinstance(value, list):  # Must be a list of Models
                sa_attr = getattr(cls, field_name, None)
                if (
                    sa_attr is not None
                    and hasattr(sa_attr, "property")
                    and hasattr(sa_attr.property, "mapper")
                ):
                    nested_sa = sa_attr.property.mapper.class_
                    nested = [nested_sa.from_model(item) for item in value]
                    setattr(sa_model, field_name, nested)
            else:
                setattr(sa_model, field_name, value)

        return sa_model

    def to_model(self) -> ModelType:
        converters: dict[str, Callable] = self._to_model_custom_converters()
        model_dict: dict[str, Any] = {}

        # Construct public fields first
        for field_name in self.__class__.model_class.model_fields:
            if field_name in converters:
                model_dict[field_name] = converters[field_name]()
            else:
                value = getattr(self, field_name, None)
                model_dict[field_name] = value

        # Instantiate a model with public fields
        model = self.__class__.model_class(**model_dict)

        # Populate private fields
        private_fields = self.__class__.model_class.__private_attributes__
        for field_name_with_underscore in private_fields:
            sa_field_name = field_name_with_underscore[1:]
            value = getattr(self, sa_field_name, None)
            if field_name_with_underscore in converters:
                setattr(
                    model,
                    field_name_with_underscore,
                    converters[field_name_with_underscore](),
                )
            elif isinstance(value, list) and value:
                setattr(
                    model,
                    field_name_with_underscore,
                    [item.to_model() for item in value],
                )

        return model

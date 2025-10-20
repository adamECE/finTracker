from enum import Enum

# Set of categories
class ExpenseCategories(Enum):
    GROCERIES       = "Groceries",
    RESTARUANT      = "Restaurants",
    VEHICLE         = "Vehicle",
    TRAVEL          = "Travel",
    ENTERTAINMENT   = "Entertainment",
    SHOPPING        = "Shopping",
    PENDING         = "Pending" # Default status before a categorization is made

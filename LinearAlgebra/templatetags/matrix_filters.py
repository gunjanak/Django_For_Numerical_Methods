from django import template

register = template.Library()


# @register.filter(name='get_matrix_value')
# def get_matrix_value(matrix_values, tuple_key):
#     """Get the value from matrix_values dictionary using the tuple key."""
#     # Convert string to tuple (e.g., '1,2' -> (1, 2))
#     key_tuple = tuple(map(int, tuple_key.split(',')))
#     print("****************")
#     print(tuple_key)
#     print(key_tuple)  # Now printing the tuple (row, col)
    
#     return matrix_values.get(key_tuple, None)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, '')
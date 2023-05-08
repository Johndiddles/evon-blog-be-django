def convertErrorToArray(error): 
    error_array = []
    for field_name in error.keys():
        print(field_name)
        error_array.append(field_name)

    return error_array
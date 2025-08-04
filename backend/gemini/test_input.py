from parse_user_input import parse_product_description, extract_json_from_response

test_input="siyah pileli medium kadın etek"

raw_response = parse_product_description(test_input)
clean_data = extract_json_from_response(raw_response)
print(clean_data)

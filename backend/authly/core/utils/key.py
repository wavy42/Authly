"""
Generates keys based on a provided format string with embedded regular\
        expression patterns using the exrex library.

Args:
    key_format (str): A string containing the desired format for the keys.\
        The format string should include placeholders
    with the syntax '%%[regular expression pattern]%%', where the regular\
            expression pattern specifies the format of the
    random characters to be generated.

Returns:
    tuple: A tuple containing the randomly generated key and the formatted\
        key that follows the specified format based
    on the embedded regular expression patterns.

Example Usage:
    Input: "%%^[a-zA-Z]{3,}#[0-9]{4}$%%"
    Output: ("abc#1234", "abc#1234")

    Input: "Perma-%%^[a-zA-Z]{2,3}#[0-9]{3,4}$%%"
    Output: ("Perma-xyz#5678", "Perma-xyz#5678")

    Input: "Key: %%^[a-zA-Z0-9_]{5,8}%%"
    Output: ("Key: abCdE_12", "Key: abCdE_12")

    Input: "%%^[a-zA-Z]{2,4}_[0-9]{3,5}%%_Code"
    Output: ("xy_7890_Code", "xy_7890_Code")

The regular expression syntax used in the `key_format` string follows\
    standard conventions. The placeholder syntax
'%%[regular expression pattern]%%' allows for the specification of desired\
    patterns for the random characters to be
generated. For example, the pattern '%%^[a-zA-Z]{3,}#[0-9]{4}$%%' denotes\
    a string that starts with at least 3 or more
letters, followed by '#', and ending with exactly 4 digits. The `exrex`\
    library interprets these regular expression
patterns and generates random strings that match the specified patterns,\
    ensuring that the generated keys adhere to
the defined format.
"""
import re
import exrex


async def generate_keys_with_format(key_format, num_keys=1):
    pattern = r"%%(.*?)%%"
    matches = re.findall(pattern, key_format)
    generated_keys = []
    for _ in range(num_keys):
        current_key = key_format
        for match in matches:
            placeholder = "%%" + match + "%%"
            generated_value = exrex.getone(match)
            current_key = current_key.replace(placeholder, generated_value, 1)
        generated_keys.append(current_key)
    return generated_keys


if __name__ == "__main__":
    # Define the key format string
    key_format_string = "%%^[a-zA-Z]{5,20}-[0-9]{3,5}%%_Code"

    # Generate and print a key with the specified format
    generated_key = generate_keys_with_format(key_format_string)
    print(generated_key)

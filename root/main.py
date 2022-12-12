import lexer
import settings

def main() -> None:
    input_file = input("File name: \n> ") # "test/webpage.hbml"

    # generate html tags
    tags = lexer.Lexer(open(input_file, 'r').read()).make_tags()

    if settings.DEBUG:
        print("Writing HTML output to file...")

    # overwrite html file
    with open(input_file.replace('.hbml', '.html'), 'w') as file:
        file.write(concatenate_tag_list(tags))
        file.close()

    print(f"Wrote HTML output to {input_file.replace('.hbml', '.html')}")

def concatenate_tag_list(list: []) -> str:
    """
    Concatenates a list of tag objects into a string
    """
    if settings.DEBUG:
        print("Concatenating tags...")

    output = ""

    # add to output
    for t in list:
        output += t.generate_html()

    return output

if __name__ == '__main__':
    main()
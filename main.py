import tag, tag_generator

def main():
    input_file = "test/webpage.hbml"

    tags = tag_generator.TagGenerator('shell', open(input_file, 'r').read()).make_tags()

    with open(input_file.replace('.hbml', '.html'), 'w') as f:
        f.write(concatenate_tag_list(tags))
        f.close()

def concatenate_tag_list(list: []) -> str:
    output = ""

    for t in list:
        output += t.generate_html()

    return output

if __name__ == '__main__':
    main()
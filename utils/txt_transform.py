output_path = "data/output"

def transform_txt_for_table_latex_row(input_file: str, output_file: str):
    with open(input_file, "r", encoding="utf-8") as infile:
        for line in infile:
            line = line.strip()
            line = line[1:-1]  # remove parentheses
            if line and not line.startswith("#"):
                source, param = line.split(",")
                source = source[1:-1] # remove quotes
                source = source.replace("_", " ") # replace underscores with spaces
                with open(output_file, "a", encoding="utf-8") as outfile:
                    outfile.write(f"{source} & {param} \\\\ \n")
                    outfile.write("\\hline\n")


transform_txt_for_table_latex_row(f"{output_path}/authorities.txt", f"{output_path}/authorities_latex.txt")

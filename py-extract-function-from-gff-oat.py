import pandas as pd
import re
import argparse

# Function to parse GO annotations
def parse_go_annotations(go_string):
    go_annotations = []
    go_terms = go_string.split('%2B')
    for term in go_terms:
        go_id, category, description = term.split('^')
        go_annotations.append({'GO_ID': go_id, 'Category': category, 'Description': description})
    return go_annotations

# Main parsing function
def parse_gff(input_file, output_file):
    gene_data = []

    with open(input_file, 'r') as f:
        for line in f:
            if line.startswith('#') or line.strip() == '':
                continue
            fields = line.strip().split('\t')
            if fields[2] == 'gene':
                attr_field = fields[8]

                gene_id = re.search(r'ID=([^;]+)', attr_field).group(1)
                alias_match = re.search(r'Alias=([^;]+)', attr_field)
                gene_alias = alias_match.group(1) if alias_match else 'NA'

                note_match = re.search(r'Note=([^;]+)', attr_field)
                gene_note = note_match.group(1) if note_match else 'NA'

                pfam_match = re.search(r'Pfam=([^;]+)', attr_field)
                gene_pfam = pfam_match.group(1) if pfam_match else 'NA'

                uniref_match = re.search(r'Uniref90_id=([^;]+)', attr_field)
                gene_uniref = uniref_match.group(1) if uniref_match else 'NA'

                go_match = re.search(r'UniProt_GO=([^;]+)', attr_field)
                gene_go = parse_go_annotations(go_match.group(1)) if go_match else []

                gene_data.append({
                    'Gene_ID': gene_id,
                    'Alias': gene_alias,
                    'Function': gene_note,
                    'Pfam': gene_pfam,
                    'Uniref90_ID': gene_uniref,
                    'GO_annotations': gene_go
                })

    gene_df = pd.json_normalize(gene_data, 'GO_annotations', ['Gene_ID', 'Alias', 'Function', 'Pfam', 'Uniref90_ID'])
    cols = ['Gene_ID', 'Alias', 'Function', 'Uniref90_ID', 'GO_ID', 'Category', 'Description', 'Pfam']
    gene_df = gene_df[cols]

    gene_df.to_csv(output_file, index=False)
    print(f"Data successfully saved to {output_file}")

# Command-line interface
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract gene information from GFF file.')
    parser.add_argument('input_file', help='Path to the input GFF file')
    parser.add_argument('output_file', help='Path to the output CSV file')
    args = parser.parse_args()

    parse_gff(args.input_file, args.output_file)

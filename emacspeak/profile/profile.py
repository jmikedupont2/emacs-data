import click
import json

@click.command()
@click.argument('infile', type=click.File('r'))
def main(infile):
    for line in infile:
        parts = line.split("]")
        for part in parts:
            parts = part.split("[")
            if len(parts)>1:
                parts =parts[1].split(" ")
            print(json.dumps(parts))
            #print(emacs.eval(part))
    
if __name__ == "__main__":
    main()

